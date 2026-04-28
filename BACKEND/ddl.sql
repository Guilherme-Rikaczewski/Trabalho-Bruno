-- TABELA DE USUÁRIOS
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(20) NOT NULL UNIQUE,
    email VARCHAR(256) NOT NULL UNIQUE,
    password TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- TABELA DE SALAS
CREATE TABLE rooms (
    id SERIAL PRIMARY KEY,
    room_name VARCHAR(100) NOT NULL,
    code CHAR(6) NOT NULL UNIQUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Index extra para consultas frequentes pelo código
CREATE INDEX idx_rooms_code ON rooms(code);

-- ENUM PARA ROLE
CREATE TYPE room_role AS ENUM ('master', 'player');


-- TABELA DE RELACIONAMENTO
CREATE TABLE room_users (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    room_id INTEGER REFERENCES rooms(id) ON DELETE CASCADE,
    role room_role NOT NULL,
    joined_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    last_access TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
);

-- Índices para performance
CREATE INDEX idx_room_users_room ON room_users(room_id);
CREATE INDEX idx_room_users_user ON room_users(user_id);
CREATE INDEX idx_room_users_last_access ON room_users(last_access);

-- Garantir apenas 1 master por sala
CREATE UNIQUE INDEX unique_master_per_room
ON room_users(room_id)
WHERE role = 'master';