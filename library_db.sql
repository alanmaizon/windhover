--
-- PostgreSQL database dump
--

-- Dumped from database version 16.3 (Debian 16.3-1.pgdg120+1)
-- Dumped by pg_dump version 16.4

-- Started on 2024-10-18 23:02:59

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

--
-- TOC entry 5 (class 2615 OID 2200)
-- Name: public; Type: SCHEMA; Schema: -; Owner: admin
--

-- *not* creating schema, since initdb creates it


ALTER SCHEMA public OWNER TO admin;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 215 (class 1259 OID 16405)
-- Name: books; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.books (
    bookid integer NOT NULL,
    title character varying(255) NOT NULL,
    author character varying(255) NOT NULL,
    genre character varying(100),
    publicationyear integer,
    imagepath character varying(255),
    available boolean DEFAULT true
);


ALTER TABLE public.books OWNER TO admin;

--
-- TOC entry 216 (class 1259 OID 16411)
-- Name: books_bookid_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.books_bookid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.books_bookid_seq OWNER TO admin;

--
-- TOC entry 3384 (class 0 OID 0)
-- Dependencies: 216
-- Name: books_bookid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.books_bookid_seq OWNED BY public.books.bookid;


--
-- TOC entry 217 (class 1259 OID 16412)
-- Name: borrowing; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.borrowing (
    borrowid integer NOT NULL,
    memberid integer NOT NULL,
    bookid integer NOT NULL,
    borrowdate date NOT NULL,
    returndate date,
    duedate date NOT NULL
);


ALTER TABLE public.borrowing OWNER TO admin;

--
-- TOC entry 218 (class 1259 OID 16415)
-- Name: borrowing_borrowid_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.borrowing_borrowid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.borrowing_borrowid_seq OWNER TO admin;

--
-- TOC entry 3385 (class 0 OID 0)
-- Dependencies: 218
-- Name: borrowing_borrowid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.borrowing_borrowid_seq OWNED BY public.borrowing.borrowid;


--
-- TOC entry 219 (class 1259 OID 16416)
-- Name: members; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.members (
    memberid integer NOT NULL,
    firstname character varying(100) NOT NULL,
    lastname character varying(100) NOT NULL,
    email character varying(100) NOT NULL,
    joindate date DEFAULT CURRENT_DATE,
    profilepicture character varying(100)
);


ALTER TABLE public.members OWNER TO admin;

--
-- TOC entry 220 (class 1259 OID 16420)
-- Name: members_memberid_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.members_memberid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.members_memberid_seq OWNER TO admin;

--
-- TOC entry 3386 (class 0 OID 0)
-- Dependencies: 220
-- Name: members_memberid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.members_memberid_seq OWNED BY public.members.memberid;


--
-- TOC entry 3217 (class 2604 OID 16421)
-- Name: books bookid; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.books ALTER COLUMN bookid SET DEFAULT nextval('public.books_bookid_seq'::regclass);


--
-- TOC entry 3219 (class 2604 OID 16422)
-- Name: borrowing borrowid; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.borrowing ALTER COLUMN borrowid SET DEFAULT nextval('public.borrowing_borrowid_seq'::regclass);


--
-- TOC entry 3220 (class 2604 OID 16423)
-- Name: members memberid; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.members ALTER COLUMN memberid SET DEFAULT nextval('public.members_memberid_seq'::regclass);


--
-- TOC entry 3387 (class 0 OID 0)
-- Dependencies: 216
-- Name: books_bookid_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.books_bookid_seq', 38, true);


--
-- TOC entry 3388 (class 0 OID 0)
-- Dependencies: 218
-- Name: borrowing_borrowid_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.borrowing_borrowid_seq', 22, true);


--
-- TOC entry 3389 (class 0 OID 0)
-- Dependencies: 220
-- Name: members_memberid_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.members_memberid_seq', 12, true);


--
-- TOC entry 3223 (class 2606 OID 16425)
-- Name: books books_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.books
    ADD CONSTRAINT books_pkey PRIMARY KEY (bookid);


--
-- TOC entry 3225 (class 2606 OID 16427)
-- Name: borrowing borrowing_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.borrowing
    ADD CONSTRAINT borrowing_pkey PRIMARY KEY (borrowid);


--
-- TOC entry 3227 (class 2606 OID 16429)
-- Name: members members_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.members
    ADD CONSTRAINT members_pkey PRIMARY KEY (memberid);


--
-- TOC entry 3228 (class 2606 OID 16430)
-- Name: borrowing borrowing_bookid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.borrowing
    ADD CONSTRAINT borrowing_bookid_fkey FOREIGN KEY (bookid) REFERENCES public.books(bookid);


--
-- TOC entry 3229 (class 2606 OID 16435)
-- Name: borrowing borrowing_memberid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.borrowing
    ADD CONSTRAINT borrowing_memberid_fkey FOREIGN KEY (memberid) REFERENCES public.members(memberid);


--
-- TOC entry 2049 (class 826 OID 16391)
-- Name: DEFAULT PRIVILEGES FOR SEQUENCES; Type: DEFAULT ACL; Schema: -; Owner: postgres
--

ALTER DEFAULT PRIVILEGES FOR ROLE postgres GRANT ALL ON SEQUENCES TO admin;


--
-- TOC entry 2051 (class 826 OID 16393)
-- Name: DEFAULT PRIVILEGES FOR TYPES; Type: DEFAULT ACL; Schema: -; Owner: postgres
--

ALTER DEFAULT PRIVILEGES FOR ROLE postgres GRANT ALL ON TYPES TO admin;


--
-- TOC entry 2050 (class 826 OID 16392)
-- Name: DEFAULT PRIVILEGES FOR FUNCTIONS; Type: DEFAULT ACL; Schema: -; Owner: postgres
--

ALTER DEFAULT PRIVILEGES FOR ROLE postgres GRANT ALL ON FUNCTIONS TO admin;


--
-- TOC entry 2048 (class 826 OID 16390)
-- Name: DEFAULT PRIVILEGES FOR TABLES; Type: DEFAULT ACL; Schema: -; Owner: postgres
--

ALTER DEFAULT PRIVILEGES FOR ROLE postgres GRANT ALL ON TABLES TO admin;


-- Completed on 2024-10-18 23:03:06

--
-- PostgreSQL database dump complete
--

