import torch
from torch import nn
from torch.utils.data import DataLoader, TensorDataset

from .dataset import load_split
from .features import FEATURE_VERSION
from .labels import CLASS_NAMES
from .model import GestureLSTM


def train_model(config, *, epochs=30):
    torch.manual_seed(42)

    train_x, train_y, _ = load_split(config, "train")
    val_x, val_y, _ = load_split(config, "validation")

    train_data = TensorDataset(
        torch.from_numpy(train_x), torch.from_numpy(train_y)
    )
    train_loader = DataLoader(train_data, batch_size=16, shuffle=True)
    val_features = torch.from_numpy(val_x)
    val_targets = torch.from_numpy(val_y)

    model_settings = {
        "feature_dim": config.feature_dim,
        "hidden_size": config.hidden_size,
        "num_layers": config.num_layers,
        "num_classes": config.num_classes,
    }
    model = GestureLSTM(**model_settings)
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

    best_val_loss = float("inf")
    checkpoint_path = config.checkpoint_path
    checkpoint_path.parent.mkdir(parents=True, exist_ok=True)

    for epoch in range(1, epochs + 1):
        model.train()
        train_loss_sum = 0.0

        for features, labels in train_loader:
            optimizer.zero_grad()
            logits = model(features)
            loss = criterion(logits, labels)
            loss.backward()
            optimizer.step()
            train_loss_sum += loss.item() * labels.size(0)

        train_loss = train_loss_sum / len(train_data)

        model.eval()
        with torch.inference_mode():
            val_logits = model(val_features)
            val_loss = criterion(val_logits, val_targets).item()
            val_predictions = val_logits.argmax(dim=1)
            val_accuracy = (val_predictions == val_targets).float().mean().item()

        print(
            f"Epoch {epoch}/{epochs} | train_loss={train_loss:.4f} | "
            f"val_loss={val_loss:.4f} | val_accuracy={val_accuracy:.1%}"
        )

        if val_loss < best_val_loss:
            best_val_loss = val_loss
            torch.save(
                {
                    "model_state_dict": model.state_dict(),
                    "model_settings": model_settings,
                    "class_names": list(CLASS_NAMES),
                    "feature_version": FEATURE_VERSION,
                    "sequence_length": config.sequence_length,
                    "sample_rate_hz": config.sample_rate_hz,
                    "mirror": config.mirror,
                    "epoch": epoch,
                    "val_loss": val_loss,
                    "val_accuracy": val_accuracy,
                },
                checkpoint_path,
            )
            print(f"Saved best checkpoint to {checkpoint_path}")