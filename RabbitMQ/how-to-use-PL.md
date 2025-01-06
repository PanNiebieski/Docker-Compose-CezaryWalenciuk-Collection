# Opis skryptu Docker Compose

Poniższy plik `docker-compose.yml` definiuje konfigurację usługi RabbitMQ z włączonym interfejsem zarządzania.

## Usługi

### RabbitMQ
RabbitMQ to broker wiadomości obsługujący różne protokoły komunikacji, takie jak AMQP.

- **Obraz**: `rabbitmq:4-management`
  - Wersja obrazu zawiera wbudowany plugin zarządzania.
- **Nazwa kontenera**: `rabbitmq`
- **Porty**:
  - `5672:5672` – Port do obsługi protokołu AMQP.
  - `15672:15672` – Port interfejsu zarządzania RabbitMQ.
- **Zmienne środowiskowe**:
  - `RABBITMQ_DEFAULT_USER: admin` – Domyślna nazwa użytkownika.
  - `RABBITMQ_DEFAULT_PASS: admin` – Domyślne hasło użytkownika.
  - `RABBITMQ_DEFAULT_VHOST: my_vhost` – Domyślny wirtualny host.
- **Woluminy**:
  - `rabbitmq_data:/var/lib/rabbitmq` – Persistent storage do przechowywania danych RabbitMQ.
  - `rabbitmq_logs:/var/log/rabbitmq` – Wolumin przechowujący logi RabbitMQ.

---

## Woluminy
- **rabbitmq_data**: Wolumin przechowujący trwałe dane RabbitMQ.
- **rabbitmq_logs**: Wolumin przechowujący logi serwera RabbitMQ.

---

## Uwagi
- Skrypt definiuje domyślnego użytkownika i hasło. W środowisku produkcyjnym zaleca się zmodyfikowanie tych wartości na bardziej bezpieczne.
- Ustawiony wirtualny host `my_vhost` pozwala na organizację wymiany wiadomości w odseparowanym środowisku.
- Włączenie interfejsu zarządzania ułatwia monitorowanie i konfigurację RabbitMQ za pomocą przeglądarki.

---

## Jak uruchomić?
1. Zapisz plik jako `docker-compose.yml`.
2. Uruchom polecenie:
   ```bash
   docker-compose up


Uzyskaj dostęp do:
RabbitMQ (AMQP): http://localhost:5672
Panel zarządzania RabbitMQ: http://localhost:15672
Domyślne dane logowania:
Login: admin
Hasło: admin