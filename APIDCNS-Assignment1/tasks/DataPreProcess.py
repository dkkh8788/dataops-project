# Importing the required python Libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import preprocessing
import matplotlib.pyplot as plt
import logging


# Configure standard logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load the dataset
df = pd.read_csv('../data/mobile_crash_data_csv.csv')
logger.info("Dataset loaded successfully.")
logger.info(f"DataFrame head:\n{df.head()}")


################################################CONFORMITY CLEANUP##########################################

# Find records greater than 100 in 'Battery Level' which is beyond conformity
outliers = df[df['Battery_Level'] > 100]
logger.info("\nRecords greater than 100:")
logger.info(outliers['Battery_Level'])

# Remove records greater than 100
cleaned_data = df[df['Battery_Level'] <= 100]

outliers = cleaned_data[cleaned_data['Battery_Level'] > 100]
logger.info("\nRecords greater than 100:")
logger.info(outliers['Battery_Level'])

################################################REMOVE OUTLIER##########################################

# Identify outliers in all numeric coloumns
new_df = cleaned_data.copy()
numeric_cols = cleaned_data.select_dtypes(include=np.number).columns
non_binary_non_discrete_numerical_columns = [col for col in numeric_cols if cleaned_data[col].nunique() > 10]

logger.info(f"cleaned_data summary")
logger.info(f"=======================================================================")
logger.info(cleaned_data.describe())
for col in non_binary_non_discrete_numerical_columns:
    Q1 = cleaned_data[col].quantile(0.25)
    Q3 = cleaned_data[col].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    logger.info(f"\n{col}, Outliers Range[lb, ub] => [{lower_bound},  {upper_bound}] ")
    logger.info(f"=====================================================================")
    filtered_df = cleaned_data[(cleaned_data[col] < lower_bound) | (cleaned_data[col] > upper_bound)]
    if not filtered_df.empty:
        logger.info(filtered_df.head(4))
        logger.info(f"\n")
    # removing outliers in this coloumn
    temp_df = cleaned_data[(cleaned_data[col] >= lower_bound) & (cleaned_data[col] <= upper_bound)]
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
# plt.show()
plt.savefig('../output/boxplot-with-outlier-removed.png')

cleaned_data = new_df

###############################################IMPUTE missing values###################################################

# Missing values
logger.info("\nMissing Values Before Imputation:")
logger.info(cleaned_data.isnull().sum())

cleaned_data['CPU_Usage']=cleaned_data['CPU_Usage'].fillna(cleaned_data['CPU_Usage'].mean())

cleaned_data['Memory_Usage']=cleaned_data['Memory_Usage'].fillna(cleaned_data['Memory_Usage'].median())

cleaned_data['Temperature']=cleaned_data['Temperature'].ffill()
cleaned_data['Session_Time']=cleaned_data['Session_Time'].fillna(cleaned_data['Session_Time'].median())


logger.info("\nMissing Values after imputation:")
logger.info(cleaned_data.isnull().sum())

## round to 2 decimal digit
cleaned_data = cleaned_data.round(2)
logger.info(cleaned_data)


###############################################Export DF to CSV###################################################
cleaned_data.to_csv('../data/pre-processed_data_v1.csv', index=False)
