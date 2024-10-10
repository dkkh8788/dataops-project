import pandas as pd
from scipy.stats import pearsonr
import logging
from matplotlib import pyplot as plt
import io
import base64
from scipy.stats import pearsonr


# Configure standard Python logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Import the data
normalized_df = pd.read_csv("../data/normalized_v1.csv")

# Removing Duration_Since_Last_charge as it is redundent

featured_df = normalized_df.drop(columns=['Duration_Since_Last_Charge'])
logger.info(featured_df.dtypes)

###############################################Export DF to CSV###################################################
featured_df.to_csv('../data/feature_engineered_v1.csv', index=False)
