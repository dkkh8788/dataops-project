import pandas as pd
import logging
from matplotlib import pyplot as plt
import io
import base64
from scipy.stats import pearsonr
from tkinter import TRUE 
import seaborn as sns


# Configure standard Python logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Import the data
normalized_df = pd.read_csv("../data/normalized_v1.csv")
logger.info("Dataset loaded for Pearson correlation.")



# Correlation Matrix - Internally uses Pearson Correlation
cor = normalized_df.corr()

# Plotting Heatmap
plt.figure(figsize = (10,6))

sns.heatmap(
    cor,
    annot=True,              # Annotate cells with their values
    fmt=".2f",              # Format for annotation
    cmap='coolwarm',        # Color map
    cbar=True,              # Show color bar
    linewidths=.5,          # Lines between cells
    linecolor='black',       # Color of the lines
    square=False,            # Make cells square-shaped
    xticklabels=True,       # Show x-tick labels
    yticklabels=True        # Show y-tick labels
)

# Save the plot to a buffer
buf = io.BytesIO()
plt.savefig(buf, format='png')
buf.seek(0)

# Encode the image in base64 and log it
img_base64 = base64.b64encode(buf.read()).decode('utf-8')

# Save the plot as a file
plt.savefig("../output/heatmap.png")
logger.info("Heast Map is saved")

# Close the buffer
buf.close()
