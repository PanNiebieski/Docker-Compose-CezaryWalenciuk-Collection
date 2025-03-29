# FROM mcr.microsoft.com/dotnet/sdk:6.0 as core
# FROM adoptopenjdk/openjdk8:jdk8u292-b10

# RUN curl -L https://archive.apache.org/dist/spark/spark-3.1.2/spark-3.1.2-bin-hadoop3.2.tgz \
#   | tar -xzC /usr/local

# # If you donwload the Apache Spark files separately, just add them
# #ADD spark-3.1.2-bin-hadoop3.2.tgz /usr/local

# RUN curl -L https://github.com/dotnet/spark/releases/download/v2.0.0/Microsoft.Spark.Worker.netcoreapp3.1.linux-x64-2.0.0.tar.gz \
#   | tar -xzC /usr/local

# # If you donwload the Microsoft.Spark files separately, just add them
# #ADD Microsoft.Spark.Worker.netcoreapp3.1.linux-x64-2.0.0.tar.gz /usr/local

# COPY --from=core /usr/share/dotnet /usr/share/dotnet
# CMD "ln -s /usr/share/dotnet/dotnet"

# ENV \
#     # Enable detection of running in a container
#     DOTNET_RUNNING_IN_CONTAINER=true \
#     # Set the invariant mode since icu_libs isn't included
#     DOTNET_SYSTEM_GLOBALIZATION_INVARIANT=true \
#     # Set worker location to where it's downloaded to
#     DOTNET_WORKER_DIR=/usr/local/Microsoft.Spark.Worker-2.0.0

# ENV SPARK_HOME=/usr/local/spark-3.1.2-bin-hadoop3.2/
# ENV PATH=:${PATH}:${SPARK_HOME}/bin:/usr/share/dotnet

# # Quiet down some Spark logging
# RUN echo 'log4j.rootCategory=WARN, console\n\
# log4j.appender.console=org.apache.log4j.ConsoleAppender\n\
# log4j.appender.console.target=System.err\n\
# log4j.appender.console.layout=org.apache.log4j.PatternLayout\n\
# log4j.appender.console.layout.ConversionPattern=%d{yy/MM/dd HH:mm:ss} %p %c{1}: %m%n\n'\
# > $SPARK_HOME/conf/log4j.properties

# RUN chmod 777 $DOTNET_WORKER_DIR/*

# Stage 1: Build or fetch dotnet runtime files
FROM mcr.microsoft.com/dotnet/sdk:9.0 AS core
# (Optional: Build your application here if desired)

# Stage 2: Base image with Java (required by Spark)
FROM adoptopenjdk/openjdk8:jdk8u292-b10

# Install Apache Spark
RUN curl -L https://archive.apache.org/dist/spark/spark-3.1.2/spark-3.1.2-bin-hadoop3.2.tgz \
    | tar -xzC /usr/local

# Install Microsoft Spark Worker
RUN curl -L https://github.com/dotnet/spark/releases/download/v2.0.0/Microsoft.Spark.Worker.netcoreapp3.1.linux-x64-2.0.0.tar.gz \
    | tar -xzC /usr/local

# Copy the dotnet runtime from the core stage
COPY --from=core /usr/share/dotnet /usr/share/dotnet

# Create a symlink so that the "dotnet" command is on the PATH
RUN ln -s /usr/share/dotnet/dotnet /usr/local/bin/dotnet

# Set environment variables for .NET for Apache Spark
ENV DOTNET_RUNNING_IN_CONTAINER=true \
    DOTNET_SYSTEM_GLOBALIZATION_INVARIANT=true \
    DOTNET_WORKER_DIR=/usr/local/Microsoft.Spark.Worker-2.0.0 \
    SPARK_HOME=/usr/local/spark-3.1.2-bin-hadoop3.2

# Fix the PATH so Spark’s bin directory and dotnet are available
ENV PATH=${PATH}:${SPARK_HOME}/bin:/usr/local/bin

# Quiet down Spark logging
RUN echo 'log4j.rootCategory=WARN, console\n\
log4j.appender.console=org.apache.log4j.ConsoleAppender\n\
log4j.appender.console.target=System.err\n\
log4j.appender.console.layout=org.apache.log4j.PatternLayout\n\
log4j.appender.console.layout.ConversionPattern=%d{yy/MM/dd HH:mm:ss} %p %c{1}: %m%n\n' \
> $SPARK_HOME/conf/log4j.properties

# Ensure Microsoft Spark Worker binaries are executable
RUN chmod 777 $DOTNET_WORKER_DIR/*

# Copy your application files into the image.
# (Make sure that your build produces a Linux DLL, not a Windows .exe)
COPY MySparkApp/bin/Debug/net9.0/ /opt/spark_app
WORKDIR /opt/spark_app

# Option A: Rely on the fixed PATH (preferred)
CMD ["spark-submit", \
     "--class", "org.apache.spark.deploy.dotnet.DotnetRunner", \
     "--master", "local", \
     "/opt/spark_app/microsoft-spark-3-2_2.12-2.1.1.jar", \
     "dotnet", "/opt/spark_app/MySparkApp.dll", "input.txt"]

# Option B: Use the absolute path to spark-submit
# CMD ["/usr/local/spark-3.1.2-bin-hadoop3.2/bin/spark-submit", \
#      "--class", "org.apache.spark.deploy.dotnet.DotnetRunner", \
#      "--master", "local", \
#      "/opt/spark_app/microsoft-spark-3-1_2.12-2.0.0.jar", \
#      "dotnet", "/opt/spark_app/MySparkApp.dll", "input.txt"]
