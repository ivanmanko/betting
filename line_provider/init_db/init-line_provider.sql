-- Проверка существования пользователя
DO
$$
BEGIN
    IF NOT EXISTS (
        SELECT FROM pg_catalog.pg_roles
        WHERE rolname = 'line_provider_user') THEN
        CREATE USER line_provider_user WITH PASSWORD 'line_provider_password';
    END IF;
END
$$;

-- Проверка существования базы данных
DO
$$
BEGIN
    IF NOT EXISTS (
        SELECT datname FROM pg_catalog.pg_database
        WHERE datname = 'line_provider_db') THEN
        CREATE DATABASE line_provider_db;
    END IF;
END
$$;

-- Предоставление прав пользователю на базу данных
GRANT ALL PRIVILEGES ON DATABASE line_provider_db TO line_provider_user;
