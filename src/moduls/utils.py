import os
from pathlib import Path

import logging
from moduls.config import ModelConfig


def concat_path(p1, p2) -> str:
    return str(Path(".") / p1 / p2)


def get_latest_weights_file_path(config: ModelConfig) -> str:
    model_folder = config.model_folder
    model_basename = config.model_filename
    # Check all files in the model folder
    model_files = Path(model_folder).glob(f"*.pt")
    # Sort by epoch number (ascending order)
    model_files = sorted(model_files, key=lambda x: int(x.stem.split("_")[-1]))
    if len(model_files) == 0:
        return None
    # Get the last one
    model_filename = model_files[-1]
    return str(model_filename)


def get_weights_file_path(config: ModelConfig, epoch: str) -> str:
    model_folder = config.model_folder
    model_filename = config.model_filename.format(epoch)
    return str(Path(".") / model_folder / model_filename)

def delete_previous_models(config, current_epoch):
    model_folder = Path(config.model_folder)
    for file in model_folder.iterdir():
        if file.is_file() and not file.name.endswith(f"{current_epoch}.pt"):
            file.unlink()
