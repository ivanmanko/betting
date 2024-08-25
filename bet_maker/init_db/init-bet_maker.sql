-- Проверка существования пользователя
DO
$$
BEGIN
    IF NOT EXISTS (
        SELECT FROM pg_catalog.pg_roles
        WHERE rolname = 'bet_maker_user') THEN
        CREATE USER bet_maker_user WITH PASSWORD 'bet_maker_password';
    END IF;
END
$$;

-- Проверка существования базы данных
DO
$$
BEGIN
    IF NOT EXISTS (
        SELECT datname FROM pg_catalog.pg_database
        WHERE datname = 'bet_maker_db') THEN
        CREATE DATABASE bet_maker_db;
    END IF;
END
$$;

-- Предоставление прав пользователю на базу данных
GRANT ALL PRIVILEGES ON DATABASE bet_maker_db TO bet_maker_user;
