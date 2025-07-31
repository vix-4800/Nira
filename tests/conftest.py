import sys
import warnings
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# Silence deprecation warnings emitted by the PyPDF2 package at import time.
warnings.filterwarnings(
    "ignore",
    message="PyPDF2 is deprecated.*",
    category=DeprecationWarning,
    module=r".*PyPDF2.*",
)
