# Opis skryptu Docker Compose

Poniższy plik `docker-compose.yml` definiuje konfigurację dwóch usług: **Elasticsearch** oraz **Kibana**, które razem tworzą stos Elastic. Skrypt umożliwia łatwe uruchomienie lokalnego środowiska analitycznego z dodatkowymi wtyczkami.

## Wersja
`version: '3.8'` – Określa wersję specyfikacji Compose, zapewniając kompatybilność z najnowszymi funkcjami Dockera.

## Usługi

### 1. Elasticsearch
Elasticsearch to rozproszony silnik wyszukiwania i analizy danych.

- **Obraz**: `docker.elastic.co/elasticsearch/elasticsearch:8.15.3`
- **Nazwa kontenera**: `elasticsearch`
- **Zmienne środowiskowe**:
  - `discovery.type=single-node` – Tryb pracy jako pojedynczy węzeł.
  - `xpack.security.enabled=false` – Wyłączenie uwierzytelnienia dla uproszczenia.
  - `bootstrap.memory_lock=true` – Blokowanie pamięci dla zwiększenia wydajności.
  - `ES_JAVA_OPTS=-Xms1g -Xmx1g` – Ustawienie limitów pamięci dla maszyny wirtualnej Javy.
- **Ograniczenia pamięci** (`ulimits`):
  - `memlock`:
    - `soft`: -1 (brak limitu miękkiego).
    - `hard`: -1 (brak limitu twardego).
- **Porty**:
  - `9200:9200` – Port REST API.
  - `9300:9300` – Port transportowy używany do komunikacji między węzłami.
- **Woluminy**:
  - `es_data:/usr/share/elasticsearch/data` – Trwałe przechowywanie danych Elasticsearch.
- **Polecenia startowe**:
  - Instalacja wtyczek:
    - `com.github.chytreg/elasticsearch-analysis-morfologik/2.3.1`
    - `analysis-stempel`
    - `elasticsearch-learning-to-rank` (wskazana wersja `1.5.10` dla Elasticsearch `8.15.3`).
  - Uruchomienie kontenera z wykorzystaniem narzędzia Tini.

---

### 2. Kibana
Kibana to interfejs wizualizacji danych dla Elasticsearch.

- **Obraz**: `docker.elastic.co/kibana/kibana:8.15.3`
- **Nazwa kontenera**: `kibana`
- **Zmienne środowiskowe**:
  - `ELASTICSEARCH_HOSTS=http://elasticsearch:9200` – Adres węzła Elasticsearch.
- **Porty**:
  - `5601:5601` – Port dla interfejsu Kibany.
- **Zależności**:
  - Kibana zależy od uruchomienia Elasticsearch (określone w `depends_on`).

---

## Woluminy
- **es_data**: Wolumin lokalny używany do przechowywania danych Elasticsearch, zapewniający trwałość między restartami.

## Uwagi
- Możesz dostosować wersję obrazów (np. Elasticsearch lub Kibana) do swoich wymagań.
- Uwierzytelnienie w Elasticsearch zostało wyłączone dla uproszczenia (`xpack.security.enabled=false`), co może być niewskazane w środowisku produkcyjnym.
- Dodano dodatkowe wtyczki do Elasticsearch, m.in. `analysis-morfologik`, `analysis-stempel`, oraz `learning-to-rank`, co zwiększa jego funkcjonalność.

### Jak uruchomić?
Aby uruchomić środowisko:
1. Zapisz plik jako `docker-compose.yml`.
2. Wykonaj polecenie:
   ```bash
   docker-compose up


Uzyskaj dostęp do:
Elasticsearch: http://localhost:9200
Kibana: http://localhost:5601