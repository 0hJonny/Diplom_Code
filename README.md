# Запуск проекта с использованием Docker Compose

Этот проект использует Docker Compose для развертывания проекта

## Инструкции по запуску

1. **Настройка переменных окружения**

   Файл `.env` в корневой директории `docker` содержит необходимые переменные окружения, пример:

   ```dotenv
   # PostgresSQL
   IMAGE_POSTGRES=postgres:16
   DATASOURCE_HOST=postgres
   DATASOURCE_PORT=5432
   DATASOURCE_DB=postgres
   DATASOURCE_USER=postgres
   DATASOURCE_PASSWORD=postgresdb

   # PgAdmin
   PGADMIN_DEFAULT_EMAIL=pguser@example.com
   PGADMIN_DEFAULT_PASSWORD=pgpassword

   # MinIO
   MINIO_USER=root
   MINIO_PASSWORD=miniopassword
   ```

2. **Запуск через start.sh**

   Используйте скрипт `start.sh`, чтобы запустить проект:

   ```bash
   ./start.sh
   ```

3. **Проверка запуска**

   После успешного выполнения скрипта, сервисы должны быть доступны по следующим адресам:

   - PostgreSQL: `postgresql://postgres:postgresdb@localhost:5432/postgres`
   - PgAdmin: [http://localhost:5050](http://localhost:5050)
   - MinIO: [http://localhost:9000](http://localhost:9000)

   Используйте учетные данные, указанные в `.env` файле, для входа в PgAdmin и MinIO.

4. **Добавить запись авторизации для Parser**
    
    - Пример записи "Server/Parser/.env" -> данные для авторизации на сервере
    - Стоит добавить эти данные в postgres в таблицу users, и "user_verify" установить "true"
    - По этим данным создается token авторизации.