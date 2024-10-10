# Importing the required python Libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import preprocessing
import matplotlib.pyplot as plt
import logging
from sklearn.preprocessing import LabelEncoder


# Configure standard logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load the dataset
df = pd.read_csv('../data/binned_v1.csv')
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
df.to_csv('../data/encoded_v1.csv', index=False)