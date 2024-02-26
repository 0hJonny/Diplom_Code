-- Установка параметров сеанса
SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

-- Удаление базы данных и роли, если они уже существуют
DROP DATABASE IF EXISTS articles;
DROP ROLE IF EXISTS articles_maker;
DROP DATABASE IF EXISTS users;
DROP ROLE IF EXISTS user_profiler;

-- Создание роли и базы данных
CREATE ROLE articles_maker
    LOGIN PASSWORD 'articlespassword'
    CREATEDB CREATEROLE
    VALID UNTIL 'infinity';

CREATE ROLE user_profiler
    LOGIN PASSWORD 'userprofilepassword'
    CREATEDB CREATEROLE
    VALID UNTIL 'infinity';

GRANT articles_maker TO postgres;

GRANT user_profiler TO postgres;

CREATE DATABASE articles
    WITH OWNER = articles_maker
    ENCODING = 'UTF8'
    CONNECTION LIMIT = -1;

CREATE DATABASE users
    WITH OWNER = user_profiler
    ENCODING = 'UTF8'
    CONNECTION LIMIT = -1;

-- Создание расширений PostgreSQL
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS pgcrypto;
-- CREATE EXTENSION IF NOT EXISTS pg_cron;
CREATE EXTENSION IF NOT EXISTS postgres_fdw;
-- CREATE EXTENSION IF NOT EXISTS tablefunc WITH SCHEMA indicators;
CREATE EXTENSION IF NOT EXISTS rum;

-- Назначение привилегий доступа
GRANT pg_monitor TO articles_maker;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO articles_maker;
GRANT ALL PRIVILEGES ON SCHEMA public TO articles_maker;
-- GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA cron TO articles_maker;
-- GRANT ALL PRIVILEGES ON SCHEMA cron TO articles_maker;

-- Назначение привилегий доступа
GRANT pg_monitor TO user_profiler;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO user_profiler;
GRANT ALL PRIVILEGES ON SCHEMA public TO user_profiler;
-- GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA cron TO user_profiler;
-- GRANT ALL PRIVILEGES ON SCHEMA cron TO user_profiler;

-- Подключение к базе данных "articles"
\c articles;

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS rum;

-- Инициализация таблиц в articles


-- Создание таблицы themes
CREATE TABLE IF NOT EXISTS themes (
    theme_id BIGSERIAL PRIMARY KEY,
    theme_name VARCHAR(255) UNIQUE NOT NULL
);

-- Заполняем таблицу themes

INSERT INTO themes (theme_name) VALUES 
	('tech'), 
	('crypto'), 
	('privacy'), 
	('security') ON CONFLICT DO NOTHING;;

-- Создание таблицы articles
CREATE TABLE IF NOT EXISTS articles (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(255) NOT NULL,
    publication_date DATE,
    author VARCHAR(255) NOT NULL,
    theme_id INTEGER,
    source_link VARCHAR(255) UNIQUE NOT NULL,
    image_link VARCHAR(255),
    body TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT now(),
    FOREIGN KEY (theme_id) REFERENCES themes(theme_id) ON DELETE CASCADE
);

-- Создание индекса
CREATE INDEX IF NOT EXISTS idx_source_link ON articles (source_link);

-- Создание таблицы tags
CREATE TABLE IF NOT EXISTS tags (
    tag_id BIGSERIAL PRIMARY KEY,
    tag_name VARCHAR(255) UNIQUE NOT NULL
);

-- Создание таблицы article_tags
CREATE TABLE IF NOT EXISTS article_tags (
    article_id uuid,
    tag_id INTEGER,
    FOREIGN KEY (article_id) REFERENCES articles(id) ON DELETE CASCADE,
    FOREIGN KEY (tag_id) REFERENCES tags(tag_id) ON DELETE CASCADE,
    PRIMARY KEY (article_id, tag_id)
);

-- Создание таблицы annotations
CREATE TABLE IF NOT EXISTS annotations (
    annotation_id BIGSERIAL PRIMARY KEY,
    article_id uuid UNIQUE,
    annotation TEXT NOT NULL,
    FOREIGN KEY (article_id) REFERENCES articles(id) ON DELETE CASCADE
);

-- Создание триггера для удаления связанных статей при удалении тега
CREATE OR REPLACE FUNCTION delete_articles_on_tag_delete()
RETURNS TRIGGER AS $$
BEGIN
    DELETE FROM articles
    WHERE id IN (
        SELECT article_id
        FROM article_tags
        WHERE tag_id = OLD.tag_id
    );
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER delete_articles_trigger
AFTER DELETE ON tags
FOR EACH ROW
EXECUTE FUNCTION delete_articles_on_tag_delete();

-- Подключение к базе данных "users"
\c users;
CREATE EXTENSION IF NOT EXISTS postgres_fdw;
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- Инициализация таблиц в users

CREATE TABLE IF NOT EXISTS users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE,
    password TEXT NOT NULL, -- Тип данных TEXT для хранения хэшированного пароля
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    birthdate DATE,
    avatar VARCHAR(255),
    confirmed BOOLEAN DEFAULT FALSE, -- Поле для отслеживания подтверждения учетной записи
    created_at TIMESTAMP DEFAULT now()
);

-- Функция для хэширования пароля при вставке новой записи
CREATE OR REPLACE FUNCTION hash_password()
	RETURNS TRIGGER AS $$
	BEGIN
		NEW.password := crypt(NEW.password, gen_salt('bf')); -- Хэширование пароля с использованием bcrypt
		RETURN NEW;
	END;
	$$ LANGUAGE plpgsql;

-- Триггер для автоматического хэширования пароля при вставке новой записи
CREATE TRIGGER hash_password_trigger
	BEFORE INSERT ON users
	FOR EACH ROW
	EXECUTE FUNCTION hash_password();

CREATE SERVER articles_server
	FOREIGN DATA WRAPPER postgres_fdw
	OPTIONS (dbname 'articles', host 'postgres', port '5432');

CREATE USER MAPPING FOR CURRENT_USER
	SERVER articles_server
	OPTIONS (user 'articles_maker', password 'articlespassword');

CREATE FOREIGN TABLE local_articles (
	id UUID,
	title TEXT
	)
	SERVER articles_server
	OPTIONS (table_name 'articles');

CREATE TABLE IF NOT EXISTS bookmarks (
    bookmark_id BIGSERIAL PRIMARY KEY,
    user_id INTEGER,
    article_id UUID,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
    -- FOREIGN KEY (article_id) REFERENCES local_articles(id) ON DELETE CASCADE
);


-- Создаем функцию, которая будет проверять существование записи с заданным article_id
CREATE OR REPLACE FUNCTION check_and_delete_invalid_bookmarks()
RETURNS TRIGGER AS $$
BEGIN
    -- Проверяем существование записи с заданным article_id
    IF NOT EXISTS (
        SELECT 1 FROM local_articles WHERE id = NEW.article_id
    ) THEN
        -- Если запись не существует, удаляем текущую запись из bookmarks
        DELETE FROM bookmarks WHERE bookmark_id = NEW.bookmark_id;
        RETURN NULL; -- Отменяем операцию вставки/обновления
    END IF;
    RETURN NEW; -- Пропускаем операцию вставки/обновления, если все в порядке
END;
$$ LANGUAGE plpgsql;

-- Создаем триггер, который будет вызывать функцию check_and_delete_invalid_bookmarks перед вставкой или обновлением записей в таблице bookmarks
CREATE TRIGGER check_and_delete_invalid_bookmarks_trigger
BEFORE INSERT OR UPDATE ON bookmarks
FOR EACH ROW
EXECUTE FUNCTION check_and_delete_invalid_bookmarks();

CREATE TABLE IF NOT EXISTS likes (
    like_id BIGSERIAL PRIMARY KEY,
    user_id INTEGER,
    article_id UUID,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- Триггер для таблицы "likes"
CREATE OR REPLACE FUNCTION check_and_delete_invalid_likes()
RETURNS TRIGGER AS $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM local_articles WHERE id = NEW.article_id
    ) THEN
        DELETE FROM likes WHERE like_id = NEW.like_id;
        RETURN NULL;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER check_and_delete_invalid_likes_trigger
BEFORE INSERT ON likes
FOR EACH ROW
EXECUTE FUNCTION check_and_delete_invalid_likes();

CREATE TABLE IF NOT EXISTS history (
    history_id BIGSERIAL PRIMARY KEY,
    user_id INTEGER,
    article_id UUID,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- Триггер для таблицы "history"
CREATE OR REPLACE FUNCTION check_and_delete_invalid_history()
RETURNS TRIGGER AS $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM local_articles WHERE id = NEW.article_id
    ) THEN
        DELETE FROM history WHERE history_id = NEW.history_id;
        RETURN NULL;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER check_and_delete_invalid_history_trigger
BEFORE INSERT ON history
FOR EACH ROW
EXECUTE FUNCTION check_and_delete_invalid_history();