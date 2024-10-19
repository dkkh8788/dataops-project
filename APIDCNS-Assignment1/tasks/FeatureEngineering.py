import pandas as pd
from scipy.stats import pearsonr
import logging
from matplotlib import pyplot as plt
import io
import base64
from scipy.stats import pearsonr
import os


# Configure standard Python logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Get the current script's directory
script_dir = os.path.dirname(__file__)
csv_file_path = os.path.join(script_dir, '../data/encoded_v1.csv')

# Import the data
normalized_df = pd.read_csv(csv_file_path)

# Removing Duration_Since_Last_charge as it is redundent

featured_df = normalized_df.drop(columns=['Duration_Since_Last_Charge'])
logger.info(featured_df.dtypes)

###############################################Export DF to CSV###################################################
op_csv_file_path = os.path.join(script_dir, '../data/feature_engineered_v1.csv')
featured_df.to_csv(op_csv_file_path, index=False)
