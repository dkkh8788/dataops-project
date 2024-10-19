# Importing the required python Libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import preprocessing
import matplotlib.pyplot as plt
import logging
import os

# Configure standard logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Get the current script's directory
script_dir = os.path.dirname(__file__)
csv_file_path = os.path.join(script_dir, '../data/mobile_crash_data_csv.csv')

# Load the dataset
df = pd.read_csv(csv_file_path)
logger.info("Dataset loaded successfully.")

logger.info(f"DataFrame head:\n{df.head()}")


########################SUMMARY STATISTICS##########################################

#This will do find mean, meadian and Quantiles 
# providing central tendencies and dispersion

print("\nSummary Statistics:")
logger.info(f"\n{df.describe(include='all')}")

