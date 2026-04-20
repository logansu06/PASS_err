import csv
import json
import logging
import os
from datetime import datetime
from typing import List, Dict, Any

import numpy as np


def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def setup_logger(log_path: str) -> logging.Logger:
    """Create a logger that writes to both stdout and a log file."""
    logger = logging.getLogger("pass_err")
    logger.setLevel(logging.INFO)
    logger.handlers = []
    fmt = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    fh = logging.FileHandler(log_path, mode="w", encoding="utf-8")
    fh.setFormatter(fmt)
    sh = logging.StreamHandler()
    sh.setFormatter(fmt)
    logger.addHandler(fh)
    logger.addHandler(sh)
    return logger


def save_json(path: str, data: Dict[str, Any]) -> None:
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def save_csv(path: str, fieldnames: List[str], rows: List[Dict[str, Any]]) -> None:
    ensure_dir(os.path.dirname(path))
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def save_npz(path: str, **arrays: Any) -> None:
    ensure_dir(os.path.dirname(path))
    np.savez(path, **arrays)


def now_ts() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def detect_reorder(deltas: np.ndarray) -> bool:
    """Return True if any neighboring positions are not strictly increasing."""
    diffs = np.diff(deltas)
    return np.any(diffs <= 0)


def version_info() -> Dict[str, str]:
    import numpy
    import scipy
    import matplotlib

    return {
        "numpy": numpy.__version__,
        "scipy": scipy.__version__,
        "matplotlib": matplotlib.__version__,
    }

