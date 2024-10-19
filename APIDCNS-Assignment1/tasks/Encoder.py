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
csv_file_path = os.path.join(script_dir, '../data/binned_v1.csv')

# Load the dataset
df = pd.read_csv(csv_file_path)
logger.info("Dataset loaded successfully.")
logger.info(f"DataFrame head:\n{df.head()}")


le = LabelEncoder()  
df['App_Usage_Level']=le.fit_transform(df['App_Usage_Level'])

df['Device_Model']=le.fit_transform(df['Device_Model'])

df['App_Name']=le.fit_transform(df['App_Name'])

df['Session_Time']=le.fit_transform(df['Session_Time'])

# Validate if now all attributes are numerical
logger.info("\nData Types:")
logger.info(df.dtypes)

logger.info(df)

###############################################Export DF to CSV###################################################
output_csv_file_path = os.path.join(script_dir, '../data/encoded_v1.csv')
df.to_csv(output_csv_file_path, index=False)