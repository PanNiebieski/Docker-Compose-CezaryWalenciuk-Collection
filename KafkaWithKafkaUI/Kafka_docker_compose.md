# Konfiguracja `docker-compose.yml` dla klastra Kafka z Zookeeper i Kafka UI

## **Opis usług**

### **1. Zookeeper**
- **Funkcja**: Zarządza metadanymi klastru Kafka i koordynuje pracę brokerów.
- **Obraz**: `bitnami/zookeeper:3.9.1`
- **Tymczasowy system plików**:
  - Montowany na `/zktmp`, aby dane tymczasowe przetrwały restart kontenera.
- **Porty**:
  - `2181:2181` - Port używany do komunikacji między Kafka a Zookeeperem.
- **Zmienne środowiskowe**:
  - `ALLOW_ANONYMOUS_LOGIN: 'yes'` - Zezwala na logowanie bez uwierzytelnienia.

---

### **2. Kafka Brokers**
#### **Broker 1 (`kafka1`)**
- **Funkcja**: Pierwszy broker w klastrze Kafka.
- **Obraz**: `bitnami/kafka:3.7.0`
- **Zależności**: Uruchamia się po Zookeeperze (`depends_on`).
- **Zmienne środowiskowe**:
  - `KAFKA_BROKER_ID: 1` - Identyfikator brokera.
  - `KAFKA_CFG_ZOOKEEPER_CONNECT: zookeeper:2181` - Adres Zookeepera.
  - `KAFKA_CFG_LISTENERS` i `KAFKA_CFG_ADVERTISED_LISTENERS`:
    - **INTERNAL**: Do komunikacji między brokerami.
    - **EXTERNAL**: Do komunikacji z aplikacjami klienckimi.
  - `KAFKA_CFG_LISTENER_SECURITY_PROTOCOL_MAP: INTERNAL:PLAINTEXT,EXTERNAL:PLAINTEXT` - Mapowanie protokołów.
  - `KAFKA_CFG_AUTO_CREATE_TOPICS_ENABLE: 'true'` - Automatyczne tworzenie tematów.
  - `ALLOW_PLAINTEXT_LISTENER: 'yes'` - Zezwala na komunikację bez szyfrowania.
- **Porty**:
  - `9092:9092` - Port wewnętrzny brokera.
  - `29092:29092` - Port zewnętrzny dla lokalnego dostępu.
- **Wolumeny**:
  - `kafka_data1` - Wolumen do przechowywania danych brokera.

#### **Broker 2 (`kafka2`) i Broker 3 (`kafka3`)**
- **Podobna konfiguracja** jak dla `kafka1`, ale:
  - **Identyfikator brokera**: `2` i `3`.
  - **Porty**:
    - `9093:9093` i `29093:29093` dla `kafka2`.
    - `9094:9094` i `29094:29094` dla `kafka3`.
  - **Wolumeny**:
    - `kafka_data2` dla `kafka2`.
    - `kafka_data3` dla `kafka3`.

---

### **3. Kafka UI**
- **Funkcja**: Interfejs webowy do monitorowania i zarządzania klastrem Kafka.
- **Obraz**: `provectuslabs/kafka-ui:latest`
- **Zależności**: Uruchamia się po wszystkich brokerach (`depends_on`).
- **Porty**:
  - `1111:8080` - Dostępne na porcie `1111` na hoście.
- **Zmienne środowiskowe**:
  - `KAFKA_CLUSTERS_0_NAME: local` - Nazwa klastra.
  - `KAFKA_CLUSTERS_0_BOOTSTRAPSERVERS: kafka1:9092,kafka2:9093,kafka3:9094` - Adresy brokerów.
  - `KAFKA_CLUSTERS_0_ZOOKEEPER: zookeeper:2181` - Adres Zookeepera.

---

## **Wolumeny**
- **`kafka_data1`, `kafka_data2`, `kafka_data3`**:
  - Każdy broker ma osobny wolumen przechowujący jego dane.
  - Dzięki temu dane są trwałe, nawet po restarcie kontenera.

---

## **Jak to działa**
1. **Zookeeper**:
   - Uruchamia się jako pierwszy i koordynuje pracę brokerów.
2. **Kafka Brokers**:
   - Trzy brokery komunikują się z Zookeeperem i między sobą.
   - Każdy broker obsługuje inne porty, co pozwala na równoległą pracę w klastrze.
3. **Kafka UI**:
   - Dostępny przez przeglądarkę pod adresem `http://localhost:1111`.
   - Umożliwia monitorowanie i zarządzanie klastrem w prosty sposób.

---

## **Uwagi**
- Zmienne środowiskowe w konfiguracji pozwalają na dużą elastyczność i dostosowanie klastra do różnych potrzeb.
- Porty **INTERNAL** są używane wewnętrznie przez brokerów, natomiast porty **EXTERNAL** są wystawiane na zewnątrz, aby aplikacje mogły łączyć się z Kafką.
