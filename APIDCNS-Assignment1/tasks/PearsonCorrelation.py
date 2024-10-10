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
logger.info("Dataset loaded for Pearson correlation.")

# Convert dataframe into series
list1 = normalized_df['Battery_Level']
list2 = normalized_df['Duration_Since_Last_Charge']


# Apply the pearsonr()
corr, _ = pearsonr(list1, list2)
print('Pearson correlation: %.3f' % corr)

# Scatter plot
plt.scatter(list1, list2)
plt.title("Correlation")
plt.ylabel('Battery_Level')
plt.xlabel('Duration_Since_Last_Charge')

# Save the plot to a buffer
buf = io.BytesIO()
plt.savefig(buf, format='png')
buf.seek(0)

# Encode the image in base64 and log it
img_base64 = base64.b64encode(buf.read()).decode('utf-8')

# Save the plot as a file
plt.savefig("../output/scatter_plot.png")
logger.info("Scatter plot saved as 'scatter_plot.png'")

# Close the buffer
buf.close()
