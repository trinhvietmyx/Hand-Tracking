param([int[]]$Slides = @())
$ErrorActionPreference = 'Stop'
$taskSource = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot 'qa/cai_thien_2026-11-08/Bao_Cao_Tien_Do_candidate.pptx'))
$taskPdf = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot 'qa/cai_thien_2026-11-08/Bao_Cao_Tien_Do.pdf'))
$taskRender = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot 'qa/cai_thien_2026-11-08/previews'))
if (-not (Test-Path -LiteralPath $taskRender)) { New-Item -ItemType Directory -Path $taskRender | Out-Null }
$taskExisting = @(Get-Process POWERPNT -ErrorAction SilentlyContinue)
$taskApp = $null
$taskDeck = $null
try {
    $taskApp = New-Object -ComObject PowerPoint.Application
    $taskApp.DisplayAlerts = 1
    $taskDeck = $taskApp.Presentations.Open($taskSource, -1, 0, 0)
    $taskItems = @()
    for ($taskI=1; $taskI -le $taskDeck.Slides.Count; $taskI++) {
        $taskSlide = $taskDeck.Slides.Item($taskI)
        if (($Slides.Count -eq 0) -or ($taskI -in $Slides)) {
            $taskSlide.Export((Join-Path $taskRender ('slide-{0:d2}.png' -f $taskI)), 'PNG', 1600, 900)
        }
        for ($taskJ=1; $taskJ -le $taskSlide.Shapes.Count; $taskJ++) {
            $taskShape = $taskSlide.Shapes.Item($taskJ)
            if ($taskShape.HasTextFrame -eq -1 -and $taskShape.TextFrame2.HasText -eq -1) {
                $taskRange = $taskShape.TextFrame2.TextRange
                $taskOver = $taskRange.BoundHeight - $taskShape.Height
                if ($taskOver -gt 2) {
                    $taskItems += [pscustomobject]@{kind='text_overflow';slide=$taskI;shape=$taskShape.Name;overflow_pt=[math]::Round($taskOver,2);text=$taskRange.Text}
                }
                $taskOverWidth = $taskRange.BoundWidth - $taskShape.Width
                if ($taskOverWidth -gt 2) {
                    $taskItems += [pscustomobject]@{kind='text_width_overflow';slide=$taskI;shape=$taskShape.Name;overflow_pt=[math]::Round($taskOverWidth,2);text=$taskRange.Text}
                }
            }
            if ($taskShape.Type -eq 16) {
                $taskItems += [pscustomobject]@{kind='media';slide=$taskI;media_type=$taskShape.MediaType;duration_ms=$taskShape.MediaFormat.Length}
            }
            if ($taskShape.HasChart -eq -1) {
                $taskItems += [pscustomobject]@{kind='native_chart';slide=$taskI}
            }
            if ($taskShape.HasTable -eq -1) {
                $taskItems += [pscustomobject]@{kind='native_table';slide=$taskI;rows=$taskShape.Table.Rows.Count;cols=$taskShape.Table.Columns.Count}
                for ($taskR=1; $taskR -le $taskShape.Table.Rows.Count; $taskR++) {
                    for ($taskC=1; $taskC -le $taskShape.Table.Columns.Count; $taskC++) {
                        $taskCell = $taskShape.Table.Cell($taskR,$taskC).Shape
                        $taskOver = $taskCell.TextFrame2.TextRange.BoundHeight - $taskCell.Height
                        if ($taskOver -gt 2) {
                            $taskItems += [pscustomobject]@{kind='table_overflow';slide=$taskI;row=$taskR;col=$taskC;overflow_pt=[math]::Round($taskOver,2);text=$taskCell.TextFrame2.TextRange.Text}
                        }
                        $taskOverWidth = $taskCell.TextFrame2.TextRange.BoundWidth - $taskCell.Width
                        if ($taskOverWidth -gt 2) {
                            $taskItems += [pscustomobject]@{kind='table_width_overflow';slide=$taskI;row=$taskR;col=$taskC;overflow_pt=[math]::Round($taskOverWidth,2);text=$taskCell.TextFrame2.TextRange.Text}
                        }
                    }
                }
            }
        }
    }
    $taskDeck.SaveAs($taskPdf,32)
    $taskReport = [pscustomobject]@{slides=$taskDeck.Slides.Count;width_pt=$taskDeck.PageSetup.SlideWidth;height_pt=$taskDeck.PageSetup.SlideHeight;rendered=(Get-ChildItem -LiteralPath $taskRender -Filter '*.png').Count;pdf=$taskPdf;findings=$taskItems}
    $taskReport | ConvertTo-Json -Depth 7 | Set-Content -LiteralPath (Join-Path $PSScriptRoot 'qa/cai_thien_2026-11-08/powerpoint_checks.json') -Encoding utf8
    $taskReport | ConvertTo-Json -Depth 7 -Compress
}
finally {
    if ($null -ne $taskDeck) { $taskDeck.Close(); [void][Runtime.InteropServices.Marshal]::FinalReleaseComObject($taskDeck) }
    if ($null -ne $taskApp) { if ($taskExisting.Count -eq 0) {$taskApp.Quit()}; [void][Runtime.InteropServices.Marshal]::FinalReleaseComObject($taskApp) }
    [GC]::Collect()
    [GC]::WaitForPendingFinalizers()
}
