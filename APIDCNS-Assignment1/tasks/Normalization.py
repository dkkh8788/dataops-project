# Importing the required python Libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import preprocessing
import matplotlib.pyplot as plt
import logging
from sklearn.preprocessing import LabelEncoder
import os


# Configure standard logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Get the current script's directory
script_dir = os.path.dirname(__file__)
csv_file_path = os.path.join(script_dir, '../data/pre-processed_data_v1.csv')

# Load the dataset
df = pd.read_csv(csv_file_path)
logger.info("Dataset loaded successfully.")
logger.info(f"DataFrame head:\n{df.head()}")


# Normalize Numerical Data
# copy the data
df_min_max_scaled = df.copy()

# Loop through each numerical column
for column in df_min_max_scaled.select_dtypes(include=['int64', 'float64']).columns:
    min_val = df_min_max_scaled[column].min()
    max_val = df_min_max_scaled[column].max()
    df_min_max_scaled[column] = (df_min_max_scaled[column] - min_val) / (max_val - min_val)

# Display the normalized DataFrame
logger.info("\nNormalized DataFrame:")
logger.info(df_min_max_scaled)

###############################################Export DF to CSV###################################################
csv_file_path_output = os.path.join(script_dir, '../data/normalized_v1.csv')
df_min_max_scaled.to_csv(csv_file_path_output, index=False)