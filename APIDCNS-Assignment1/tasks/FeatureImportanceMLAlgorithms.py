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
featured_data = pd.read_csv("../data/feature_engineered_v1.csv")

# Removing Duration_Since_Last_charge as it is redundent

from sklearn.ensemble import RandomForestRegressor
# define the model
model = RandomForestRegressor()

X = featured_data.iloc[:,[0,1,2,3,4,5,6,7,8,9,10,11,12]] 
Y = featured_data.iloc[:,[13]]  

# fit the model
model.fit(X,Y)
# get importance
importance = model.feature_importances_
# summarize feature importance
for i,v in enumerate(importance):
	#print('Feature: %0d, Score: %.5f' % (i,v))
    print(f'Feature: {X.columns[i]}, Score: {v:.5f}')
# plot feature importance
plt.bar([x for x in range(len(importance))], importance)
plt.title("Feature Importance")
plt.ylabel('Importance towards Crash_Label')
plt.xlabel('Features')

# Save the plot to a buffer
buf = io.BytesIO()
plt.savefig(buf, format='png')
buf.seek(0)

# Encode the image in base64 and log it
img_base64 = base64.b64encode(buf.read()).decode('utf-8')

# Save the plot as a file
plt.savefig("../output/feature_importance.png")
logger.info("Scatter plot saved as 'feature_importancet.png'")

# Close the buffer
buf.close()



