# Użyj oficjalnego obrazu Jupyter, który zawiera JupyterLab 3+
FROM jupyter/base-notebook:python-3.11.6
# Etykiety metadanych dla łatwiejszego śledzenia i zarządzania
LABEL maintainer="c@gmail.com" \
      version="1.0" \
      description="Obraz Jupyter Notebook z rozszerzeniami ułatwiającymi debugowanie, kontrolę wersji i formatowanie kodu."
# Zainstaluj OpenJDK
USER root
RUN apt-get update && apt-get install -y openjdk-11-jdk && \
    rm -rf /var/lib/apt/lists/*
# Ustaw zmienną środowiskową JAVA_HOME
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
USER ${NB_UID}
# Przełącz na użytkownika root, aby zainstalować pakiety systemowe
USER root
# Zainstaluj pakiety systemowe (np. narzędzia do kompilacji, git) i wyczyść po instalacji
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      build-essential \
      git && \
    rm -rf /var/lib/apt/lists/*
# Przełącz z powrotem na użytkownika notebooka
USER ${NB_UID}
# Zaktualizuj pip i zainstaluj dodatkowe pakiety Python oraz rozszerzenia JupyterLab
RUN pip install --upgrade pip && \
    pip install --no-cache-dir \
      ipykernel>=6.0 \
      ipdb \
      debugpy \
      jupyterlab-git \
      nbdime \
      jupyterlab-lsp \
      jupyterlab-code-formatter \
      autopep8
# Zainstaluj wymagane pakiety Python
RUN pip install --no-cache-dir \
    pyspark \
    psycopg2-binary \
    pandas
# Upewnij się, że JupyterLab jest włączony
ENV JUPYTER_ENABLE_LAB=yes
# Ustaw katalog roboczy
WORKDIR /home/jovyan/work
# Odsłoń domyślny port Jupyter
EXPOSE 8888
# Sprawdzenie stanu, aby zweryfikować, czy serwer Jupyter jest aktywny
HEALTHCHECK --interval=30s --timeout=10s CMD curl --fail http://localhost:8888/api || exit 1
# Uruchom Jupyter Notebook (domyślnie JupyterLab)
CMD ["start-notebook.sh"]