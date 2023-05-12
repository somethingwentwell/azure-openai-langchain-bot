--
-- PostgreSQL database dump
--

-- Dumped from database version 15.2
-- Dumped by pg_dump version 15.2

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: agent_log; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.agent_log (
    id integer NOT NULL,
    session_id character varying(255) NOT NULL,
    callback_type character varying(255) NOT NULL,
    log json NOT NULL
);


ALTER TABLE public.agent_log OWNER TO postgres;

--
-- Name: agent_log_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.agent_log_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.agent_log_id_seq OWNER TO postgres;

--
-- Name: agent_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.agent_log_id_seq OWNED BY public.agent_log.id;


--
-- Name: message_store; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.message_store (
    id integer NOT NULL,
    session_id text NOT NULL,
    message jsonb NOT NULL
);


ALTER TABLE public.message_store OWNER TO postgres;

--
-- Name: message_store_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.message_store_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.message_store_id_seq OWNER TO postgres;

--
-- Name: message_store_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.message_store_id_seq OWNED BY public.message_store.id;


--
-- Name: agent_log id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.agent_log ALTER COLUMN id SET DEFAULT nextval('public.agent_log_id_seq'::regclass);


--
-- Name: message_store id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.message_store ALTER COLUMN id SET DEFAULT nextval('public.message_store_id_seq'::regclass);


--
-- Name: agent_log agent_log_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.agent_log
    ADD CONSTRAINT agent_log_pkey PRIMARY KEY (id);


--
-- Name: message_store message_store_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.message_store
    ADD CONSTRAINT message_store_pkey PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--

