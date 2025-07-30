import warnings

# Silence deprecation warnings emitted by the PyPDF2 package at import time.
warnings.filterwarnings(
    "ignore",
    message="PyPDF2 is deprecated.*",
    category=DeprecationWarning,
    module=r".*PyPDF2.*",
)
