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


################################################SUMMARY STATISTICS##########################################

#This will do find mean and Quantiles finding central tendencies and dispersion
print("\nSummary Statistics:")
logger.info(df.describe(include='all'))
logger.info(f"\n{df.describe(include='all')}")

################################################HISTOGRAM ANALYSIS##########################################

# Print Histograms for all numerical data (visualize data)
numeric_columns = df.select_dtypes(include='number').columns.tolist()
non_binary_non_discrete_numerical_columns = [col for col in numeric_columns if df[col].nunique() > 10]

fig, axes = plt.subplots(nrows=len(non_binary_non_discrete_numerical_columns), ncols=1, figsize=(10, 30))
# Iterate over numeric columns and create histograms
for i, column in enumerate(non_binary_non_discrete_numerical_columns):
    df[column].hist(ax=axes[i], bins=30, color='blue', alpha=0.7)
    axes[i].set_title(f"Histogram of {column}")
    axes[i].set_xlabel(column)
    axes[i].set_ylabel('Frequency')

# Adjust spacing between subplots
plt.tight_layout()

# Show the plot
# plt.show()

plt.savefig('../output/histogram.png')

###############################################BOX PLOT###################################################

# Box Plot of numeric coloumns
import pandas as pd
import matplotlib.pyplot as plt

# Get numeric columns
numeric_columns = df.select_dtypes(include='number').columns.tolist()
non_binary_non_discrete_numerical_columns = [col for col in numeric_columns if df[col].nunique() > 10]
new_df = df[non_binary_non_discrete_numerical_columns]
fig, ax = plt.subplots(figsize=(12, 8))
# Create box plots
new_df.boxplot(ax=ax)
plt.title("Box Plots for Numeric/Continuous features")
plt.ylabel('Values')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('../output/boxplot-with-outlier.png')
# plt.show()

###############################################MISSING VALUES###################################################

# Checking for missing values
logger.info("Missing Values:")
logger.info(f"\n{df.isnull().sum()}")

# Data type information
logger.info("Data Types:")
logger.info(f"\n{df.dtypes}")

############################### OUTPUT Data SET###################################################
