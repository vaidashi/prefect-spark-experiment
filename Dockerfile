# Default image doesn't have jdk installed, so we need to install it from alternative
FROM python:3.8-bullseye

# Install Java
RUN apt-get update && apt-get install -y openjdk-11-jdk

# Set environment variables
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV PYSPARK_PYTHON=python3
ENV PYSPARK_DRIVER_PYTHON=python3

COPY . . 

# Install PySpark and Prefect
# RUN pip install pyspark prefect python-dontenv Requests
RUN pip install -r requirements.txt

# Set the command to run the script
CMD ["spark-submit", "--driver-memory", "4g", "--executor-memory", "4g", "--conf", "spark.driver.maxResultSize=4g", "--master", "local[*]", "/prefect_run.py"]
