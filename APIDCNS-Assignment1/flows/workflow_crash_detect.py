from prefect import flow, task, get_run_logger
import subprocess
import os

@task(log_prints=True)  # Ensures all prints are captured in logs
def run_task(script_name):
    logger = get_run_logger()
    
    # Define the full path to the script based on the project structure
    script_path = os.path.join(os.path.dirname(__file__), '../tasks', script_name)
    
    try:
        # Run the external Python script using its full path
        result = subprocess.run(['python', script_path], capture_output=True, text=True)
        
        # Log both stdout and stderr
        if result.returncode == 0:
            logger.info(f"Successfully executed {script_name}:\n{result.stdout}")  # Log standard output
        else:
            logger.error(f"Error in {script_name}: {result.stderr}")  # Log standard error

        # Always print both stdout and stderr, regardless of success or failure
        print(result.stdout)
        print(result.stderr)

    except Exception as e:
        logger.error(f"Failed to execute {script_name}: {str(e)}")

    return 0

@flow
def main_flow():
    # Run tasks sequentially and capture the results
   data1 = run_task("../tasks/BasicStats.py")
   data2 = run_task("../tasks/DataPreProcess.py", wait_for=[data1])
   data3 = run_task("../tasks/Normalization.py", wait_for=[data2]) 
   data4 = run_task("../tasks/Binning.py", wait_for=[data3])  
   data5 = run_task("../tasks/Encoder.py", wait_for=[data4]) 
   data6 = run_task("../tasks/HeatMap.py", wait_for=[data5]) 
   data7 = run_task("../tasks/PearsonCorrelation.py", wait_for=[data5]) 
   data8 = run_task("../tasks/FeatureEngineering.py", wait_for=[data5])
   data9 = run_task("../tasks/FeatureImportanceMLAlgorithms.py", wait_for=[data6]) 
   data10 = run_task("../tasks/UnivariateAnalysis.py", wait_for=[data5])

# To run locally
if __name__ == "__main__":
    main_flow.serve(name="system-crash-ds-workflow",
                      tags=["system crash datascience project workflow"],
                      parameters={},
                      interval=120)
