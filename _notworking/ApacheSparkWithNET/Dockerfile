# Base image with Java 8 (required for Spark)
FROM openjdk:8-jdk-slim-buster

# Set environment variables
ENV SPARK_VERSION=3.2.0
ENV HADOOP_VERSION=3.2
ENV DOTNET_SDK_VERSION=6.0
ENV MICROSOFT_SPARK_VERSION=2.0.0

# Install required dependencies
RUN apt-get update && \
    apt-get install -y wget curl gnupg apt-transport-https software-properties-common python3 python3-pip && \
    # Install .NET SDK
    wget https://packages.microsoft.com/config/debian/10/packages-microsoft-prod.deb -O packages-microsoft-prod.deb && \
    dpkg -i packages-microsoft-prod.deb && \
    apt-get update && \
    apt-get install -y dotnet-sdk-${DOTNET_SDK_VERSION} && \
    # Cleanup to reduce image size
    rm -rf /var/lib/apt/lists/* && \
    apt-get clean

# Download and install Apache Spark
RUN wget https://archive.apache.org/dist/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz && \
    tar -xzf spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz && \
    mv spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION} /spark && \
    rm spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz

# Download and install Microsoft Spark
RUN dotnet tool install --global Microsoft.Spark.Worker --version ${MICROSOFT_SPARK_VERSION} && \
    wget https://github.com/dotnet/spark/releases/download/v${MICROSOFT_SPARK_VERSION}/Microsoft.Spark.Worker.netcoreapp3.1.linux-x64-${MICROSOFT_SPARK_VERSION}.tar.gz && \
    mkdir -p /dotnet/spark && \
    tar -xzf Microsoft.Spark.Worker.netcoreapp3.1.linux-x64-${MICROSOFT_SPARK_VERSION}.tar.gz -C /dotnet/spark && \
    rm Microsoft.Spark.Worker.netcoreapp3.1.linux-x64-${MICROSOFT_SPARK_VERSION}.tar.gz

# Set environment variables for Spark and .NET
ENV SPARK_HOME=/spark
ENV PATH=$PATH:$SPARK_HOME/bin:$SPARK_HOME/sbin
ENV DOTNET_WORKER_DIR=/dotnet/spark

# Create working directory for .NET apps
WORKDIR /app

# Copy necessary files (modify as needed for your specific requirements)
COPY jars/ /app/jars/

# Add Microsoft.Spark.jar to Spark jars directory
RUN cp /dotnet/spark/Microsoft.Spark.jar ${SPARK_HOME}/jars/

# Create a script to run the Spark master and workers
RUN echo '#!/bin/bash \n\
${SPARK_HOME}/sbin/start-master.sh \n\
${SPARK_HOME}/sbin/start-worker.sh spark://$(hostname):7077 \n\
tail -f ${SPARK_HOME}/logs/*' > /start-spark.sh && \
    chmod +x /start-spark.sh

# Default command
CMD ["/start-spark.sh"]

# Expose Spark ports
EXPOSE 4040 7077 8080 8081