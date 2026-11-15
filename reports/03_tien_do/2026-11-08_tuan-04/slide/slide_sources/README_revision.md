# Tạo lại bản cải thiện ngày 08/11/2026

Bản hiện tại gồm 16 slide, giữ chỉnh sửa bìa của người dùng, không có kế hoạch hoặc đầu ra theo tuần. Đọc sâu IPN HandS, đối chiếu với code đồ án và giữ kết quả thực nghiệm hiện có. Không tuyên bố đã tái lập LSTM gốc của tác giả.

## Đầu vào được bảo toàn

`qa/cai_thien_2026-11-08/revision_input.json` chỉ tới bản gốc 15 slide đã sao lưu tại `reports/99_luu_tru/truoc_cai_thien_2026-11-08/`. Không thay snapshot này bằng bản đầu ra 16 slide. Script kiểm tra giữ nguyên 14 part ảnh/video/chart/workbook và chín nội dung slide ngoài chân trang; các thay đổi chữ còn lại được ghi trong log bảo toàn.

## Các lệnh hiện hành

Chạy PowerShell tại `D:/Learn/Hutech/DACN/Hand-Tracking`. Cần Microsoft PowerPoint trên Windows.

```powershell
$taskRuntime = 'C:/Program Files/WindowsApps/OpenAI.CodexPrimaryRuntime.v26-1105-1297-0_26.1105.1297.0_x64__3k8sg7r9htsxt/dependencies'
$taskSource = 'reports/03_tien_do/2026-11-08_tuan-04/slide/slide_sources'
$taskWork = "$taskSource/qa/cai_thien_2026-11-08"
$taskInput = 'reports/99_luu_tru/truoc_cai_thien_2026-11-08/Bao_Cao_Tien_Do.pptx'
$taskSkill = 'D:/App/DataApp/CodexData/codex-skills/pptx'
$env:PYTHONUTF8 = '1'
& "$taskRuntime/node/bin/node.exe" "$taskSource/build_improved_sections.cjs"
& "$taskRuntime/python/python.exe" "$taskSkill/scripts/add_slide.py" $taskInput slide4.xml --after slide4.xml -o "$taskWork/structured_16.pptx"
& "$taskRuntime/python/python.exe" "$taskSource/improve_current_deck.py"
& "$taskRuntime/native/powershell/pwsh.exe" -NoProfile -File "$taskSource/render_improved_deck.ps1"
$env:PYTHONPATH = 'D:/App/DataApp/CodexData/Temp/progress-report-python-deps'
& "$taskRuntime/python/python.exe" "$taskSkill/scripts/office/validate.py" "$taskWork/Bao_Cao_Tien_Do_candidate.pptx" --original $taskInput -v
```

Xem PNG trong `qa/cai_thien_2026-11-08/previews/`, nhất là slide 4, 5, 9, 13–16. Sau khi kiểm tra hiển thị và đóng bản PowerPoint đích:

```powershell
& "$taskRuntime/python/python.exe" "$taskSource/finalize_improved_deck.py" --publish
& "$taskRuntime/python/python.exe" "$taskSource/verify_package.py"
```

Publish chỉ cho phép ghi đè đúng bản đầu vào đã lưu hoặc bản do pipeline này phát hành; nếu mã băm thay đổi do người dùng sửa, phải ghép chỉnh sửa mới trước. Không tự vượt kiểm tra này. Không cần chạy các script tạo cũ được liệt kê trong README.md.

## Phạm vi kiểm chứng

- IPN HandS: số Bảng 6 là mean/std của bài; khác dữ liệu/giao thức với đồ án, không xếp hạng trực tiếp.
- 44 = 42 tọa độ cục bộ + 2 tọa độ cổ tay. 30 mẫu ở 20 Hz tạo khoảng đầu–cuối 1,45 giây. Hidden size 64 là cấu hình cơ sở, chưa chứng minh tối ưu.
- Video là phát lại clip test; chưa có phép đo FPS/latency và kiểm thử điều khiển trực tiếp đầy đủ.
- PowerPoint COM kiểm tra mở/render và thời lượng media, chưa thay cho thao tác phát video trong Slide Show.
- PptxGenJS 4.0.1: bảng dùng `valign: 'middle'`; giữ đối tượng native, nguồn biểu đồ và ảnh/video thật.
- `trace_current_model.py` chỉ suy luận clip bằng Python `.venv` của đồ án; pipeline chỉnh slide không huấn luyện lại.
