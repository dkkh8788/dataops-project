# Import necessary libraries
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, precision_score, recall_score, f1_score, confusion_matrix
import mlflow
import mlflow.sklearn
import psutil
import time
from mlflow.models import infer_signature

# Set the MLflow tracking URI to 'http'
mlflow.set_tracking_uri("http://localhost:5000")

# Function for data preprocessing
def preprocess_data(data):

    X = data.drop('Crash_Label', axis=1)
    y = data['Crash_Label']

    return X, y

# Function for training the model in Random Forest
def train_model_randomforest(X_train, y_train, max_depth=3, n_estimators=100):
    # Initialize the classifier
    clf = RandomForestClassifier(max_depth=max_depth, n_estimators=n_estimators, random_state=42)

    # Train the model
    clf.fit(X_train, y_train)
    #mlflow.sklearn.log_model(clf,'random_forest_model')
    return clf

# Function for training the model in Random Forest
def train_model_decisiontree(X_train, y_train):
    # Initialize the classifier
    clf = DecisionTreeClassifier(random_state=42)

    # Train the model
    clf.fit(X_train, y_train)
    #mlflow.sklearn.log_model(clf,'decision_tree_model')
    return clf

# Function to evaluate the model
def evaluate_model(model, X_test, y_test):
    # Make predictions
    y_pred = model.predict(X_test)

    # Evaluate accuracy
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Accuracy: {accuracy:.2f}")

    # Display classification report
    print("Classification Report:")
    print(classification_report(y_test, y_pred))

# Function to log model and system metrics to MLflow
def log_to_mlflow(modeltype, model, X_train, X_test, y_train, y_test):
    with mlflow.start_run():
        if modeltype == 'RandomForest':
            # Log hyper parameters using in Random Forest Algorithm
            mlflow.log_param("max_depth", model.max_depth)
            mlflow.log_param("n_estimators", model.n_estimators)

        # Log model metrics
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred, average='micro')
        recall = recall_score(y_test, y_pred, average='micro')
        f1 = f1_score(y_test, y_pred, average='micro')
        confusion = confusion_matrix(y_test, y_pred)
        
        mlflow.log_metric("accuracy", accuracy)
        mlflow.log_metric("precision", precision)
        mlflow.log_metric("recall", recall)
        mlflow.log_metric("f1-score", f1)
        
        # Log confusion matrix
        confusion_dict = {
            "true_positive": confusion[1][1],
            "false_positive": confusion[0][1],
            "true_negative": confusion[0][0],
            "false_negative": confusion[1][0]
        }
        mlflow.log_metrics(confusion_dict)

        # Log system metrics
        # Example: CPU and Memory Usage
        cpu_usage = psutil.cpu_percent(interval=1)
        memory_usage = psutil.virtual_memory().percent

        mlflow.log_metric("system_cpu_usage", cpu_usage)
        mlflow.log_metric("system_memory_usage", memory_usage)

        # Log execution time for training the model
        execution_time = {}  # Dictionary to store execution times for different stages
        # Example: Execution time for training the model
        start_time = time.time()
        if modeltype == 'RandomForest':
            model = train_model_randomforest(X_train, y_train)
        elif modeltype == 'DecisionTree':
            model = train_model_decisiontree(X_train, y_train)
        end_time = time.time()
        execution_time["system_model_training"] = end_time - start_time

        # Log execution time 
        mlflow.log_metrics(execution_time)

        # Evaluate model and log metrics
        evaluate_model(model, X_test, y_test)

        # Log model
        # Infer the model signature
        if modeltype == 'RandomForest':
            y_pred = model.predict(X_test)
            signature = infer_signature(X_test, y_pred)
            mlflow.sklearn.log_model(sk_model = model, artifact_path="sklearn-model", signature=signature,  registered_model_name = "crashData_RandomForestModel")
            
        elif modeltype == 'DecisionTree':
            y_pred = model.predict(X_test)
            signature = infer_signature(X_test, y_pred)
            mlflow.sklearn.log_model(sk_model = model, artifact_path="sklearn-model", signature=signature,  registered_model_name = "crashData_DecisionTreeModel")
            


# Main function
def main(modeltype):
    # Load the dataset
    print('Starting Load of Training Data')
    data = pd.read_csv("train.csv")  

    # Preprocess the data
    print('Starting Preprocess Data')
    X, y = preprocess_data(data)

    # Split the data into training and testing sets
    print('Starting Data Split between Train and Test Data')
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    if modeltype == 'RandomForest':
        # Train the model
        print('Starting Model Training for Random Forest')
        model = train_model_randomforest(X_train, y_train)

        # Evaluate and log to MLflow
        print('Starting MLflow Logging')
        log_to_mlflow(modeltype, model, X_train, X_test, y_train, y_test)
    elif modeltype == 'DecisionTree':
         # Train the model
        print('Starting Model Training for Decision Tree')
        model = train_model_decisiontree(X_train, y_train)

        # Evaluate and log to MLflow
        print('Starting MLflow Logging')
        log_to_mlflow(modeltype, model, X_train, X_test, y_train, y_test)

if __name__ == "__main__":
    main('RandomForest')
    main('DecisionTree')