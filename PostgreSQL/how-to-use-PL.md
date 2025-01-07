# Opis skryptu Docker Compose

Poniższy plik `docker-compose.yml` definiuje konfigurację usługi PostgreSQL, prostego systemu zarządzania bazą danych typu relacyjnego.

## Usługi

### PostgreSQL
PostgreSQL to otwartoźródłowy system zarządzania bazami danych.

- **Obraz**: `postgres:14-alpine`
  - Lekka wersja PostgreSQL oparta na Alpine Linux.
- **Porty**:
  - `5432:5432` – Port PostgreSQL otwarty na lokalnym hoście i dostępny z aplikacji lub narzędzi bazodanowych.
- **Woluminy**:
  - `~/apps/postgres:/var/lib/postgresql/data` – Mapowanie lokalnego folderu `~/apps/postgres` na folder wewnątrz kontenera, aby zapewnić trwałość danych.
- **Zmienne środowiskowe**:
  - `POSTGRES_PASSWORD`: Hasło administratora bazy danych (`#password123sdJwnwlk`).
  - `POSTGRES_USER`: Nazwa użytkownika bazy danych (`citizix_user`).
  - `POSTGRES_DB`: Domyślna nazwa bazy danych (`citizix_db`).

---

## Jak uruchomić?

1. Zapisz plik jako `docker-compose.yml`.
2. Upewnij się, że katalog `~/apps/postgres` istnieje. Jeśli nie, utwórz go:
   ```bash
   mkdir -p ~/apps/postgres


## Dane logowania do bazy

Host: localhost
Port: 5432
Użytkownik: citizix_user
Hasło: #password123sdJwnwlk
Domyślna baza danych: citizix_db

## Uwagi
Trwałość danych:
Dane są przechowywane w katalogu ~/apps/postgres na hoście, co zapewnia ich trwałość nawet po usunięciu kontenera.
Zmiana danych logowania:
Aby zmienić użytkownika, hasło lub nazwę bazy danych, edytuj odpowiednie zmienne środowiskowe w sekcji environment.

## Bezpieczeństwo:
W środowiskach produkcyjnych należy używać silniejszego hasła niż przykładowe.