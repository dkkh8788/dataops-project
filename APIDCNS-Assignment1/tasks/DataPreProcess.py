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

####################### MISSING VALUES#######################
# Checking for missing values
logger.info("Missing Values:")
logger.info(f"\n{df.isnull().sum()}")


#######################IMPUTE missing Numeric values#########################

# imputation using mean, median and forward-fill methods 

df['CPU_Usage']=df['CPU_Usage'].fillna(df['CPU_Usage'].mean())

df['Memory_Usage']=df['Memory_Usage'].fillna(df['Memory_Usage'].median())

df['Temperature']=df['Temperature'].ffill()
df['Session_Time']=df['Session_Time'].fillna(df['Session_Time'].median())


logger.info("\nMissing Values after imputation:")
logger.info(df.isnull().sum())

##################################CONFORMITY CLEANUP#################

# BatteryLevel in records is greater than 100, 
# Find records greater than 100 in 'Battery Level' which is beyond conformity
outliers = df[df['Battery_Level'] > 100]
logger.info("\nRecords greater than 100:")
logger.info(outliers['Battery_Level'])

# Remove records greater than 100
df = df[df['Battery_Level'] <= 100]

outliers = df[df['Battery_Level'] > 100]
logger.info("\nRecords greater than 100:")
logger.info(outliers['Battery_Level'])

############################ round to 2 decimal digit ############
df = df.round(2)
logger.info(df)

############################ Show DataTypes ############
# Print data types of each column
print("\nData Types:")
print(df.dtypes)

#################################REMOVE OUTLIER###########################

# Identify outliers in all numeric coloumns
new_df = df.copy()
numeric_cols = df.select_dtypes(include=np.number).columns
non_binary_non_discrete_numerical_columns = [col for col in numeric_cols if df[col].nunique() > 10]

logger.info(f"df summary")
logger.info(f"=======================================================================")
logger.info(df.describe())
for col in non_binary_non_discrete_numerical_columns:
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    logger.info(f"\n{col}, Outliers Range[lb, ub] => [{lower_bound},  {upper_bound}] ")
    logger.info(f"=====================================================================")
    filtered_df = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
    if not filtered_df.empty:
        logger.info(filtered_df.head(4))
        logger.info(f"\n")
    # removing outliers in this coloumn
    temp_df = df[(df[col] >= lower_bound) & (df[col] <= upper_bound)]
    new_df[col] = temp_df[col]

non_binary_non_discrete_numerical_columns = [col for col in numeric_cols if new_df[col].nunique() > 10]
non_binary_non_discrete_numerical_columns_df =  new_df[non_binary_non_discrete_numerical_columns]

fig, ax = plt.subplots(figsize=(12, 8))
# Create box plots
non_binary_non_discrete_numerical_columns_df.boxplot(ax=ax)
#new_df.boxplot(ax=ax)
plt.title("Box Plots After Outliers removed")
plt.ylabel('Values')
plt.xticks(rotation=45)
plt.tight_layout()
img_file_path = os.path.join(script_dir, '../output/boxplot-with-outlier-removed.png')
plt.savefig(img_file_path)

df = new_df


###############################################Export DF to CSV###################################################
output_csv_file_path = os.path.join(script_dir, '../data/pre-processed_data_v1.csv')
df.to_csv(output_csv_file_path, index=False)