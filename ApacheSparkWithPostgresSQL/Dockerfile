# Use the official Jupyter base image that includes JupyterLab 3+
FROM jupyter/base-notebook:latest

# Switch to root to install additional packages if needed
USER root
# (Optional) Install any system packages you might need
RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*

# Switch back to the notebook user
USER $NB_UID

# Install required Python packages for debugging
RUN pip install --no-cache-dir ipykernel>=6.0 ipdb debugpy

# Note: No need to install @jupyterlab/debugger as prebuilt extensions are used

# Set the working directory
WORKDIR /home/jovyan/work

# Start Jupyter Notebook (JupyterLab will be the default with JUPYTER_ENABLE_LAB)
CMD ["start-notebook.sh"]
