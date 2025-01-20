-- Database: user_system

-- DROP DATABASE IF EXISTS user_system;

CREATE DATABASE user_system
    WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'Russian_Russia.1251'
    LC_CTYPE = 'Russian_Russia.1251'
    LOCALE_PROVIDER = 'libc'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1
    IS_TEMPLATE = False;

-- Table: public.users

-- DROP TABLE IF EXISTS public.users;

CREATE TABLE IF NOT EXISTS public.users
(
    id bigint NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 9223372036854775807 CACHE 1 ),
    login character varying(32) COLLATE pg_catalog."default" NOT NULL,
    email character varying(64) COLLATE pg_catalog."default",
    is_admin boolean NOT NULL DEFAULT false,
    CONSTRAINT users_pkey PRIMARY KEY (id),
    CONSTRAINT users_login_key UNIQUE (login)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.users
    OWNER to postgres;

-- Table: public.passwords

-- DROP TABLE IF EXISTS public.passwords;

CREATE TABLE IF NOT EXISTS public.passwords
(
    id bigint NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 9223372036854775807 CACHE 1 ),
    user_id bigint NOT NULL,
    password character varying(32) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT passwords_pkey PRIMARY KEY (id),
    CONSTRAINT passwords_user_id_fkey FOREIGN KEY (user_id)
        REFERENCES public.users (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.passwords
    OWNER to postgres;

INSERT INTO public.users VALUES(DEFAULT, 'admin', 'admin@example.com', true);

INSERT INTO public.passwords VALUES(DEFAULT, (SELECT public.users.id FROM public.users WHERE login='admin'), 'admin');

