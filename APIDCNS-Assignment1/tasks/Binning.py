import pandas as pd
import numpy as np
import logging
import os

# Configure standard Python logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Get the current script's directory
script_dir = os.path.dirname(__file__)
csv_file_path = os.path.join(script_dir, '../data/normalized_v1.csv')

df = pd.read_csv(csv_file_path)
logger.info("Normalized Dataset loaded for binning.")

# Distance binning
min_value = df['Session_Time'].min()
max_value = df['Session_Time'].max()
logger.info(f"Min Session_Time: {min_value}, Max Session_Time: {max_value}")

# Bin size is 4
bins = np.linspace(min_value, max_value, 4)
logger.info(f"Bins: {bins}")

labels = ['Low', 'Medium', 'High'];

# We need to specify the bins and the labels.
df['Session_Time'] = pd.cut(df['Session_Time'], bins=bins, labels=labels, include_lowest=True)
logger.info(f"Distance Binning Results:\n{df['Session_Time']}")

###############################################Export DF to CSV###################################################
output_csv_file_path = os.path.join(script_dir, '../data/binned_v1.csv')

df.to_csv(output_csv_file_path, index=False)
