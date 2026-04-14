# This file makes the pages folder a Python package

# Import all page modules
from . import stock_analysis
from . import stock_prediction

# Only import capm_beta if the file exists (optional)
try:
    from . import capm_beta
except ImportError:
    pass

# List all modules that are available
__all__ = ['stock_analysis', 'stock_prediction']