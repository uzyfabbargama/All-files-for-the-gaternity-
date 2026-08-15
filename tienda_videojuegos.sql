--
-- PostgreSQL database dump
--

\restrict cLIGEQ65An2F2hdmj5NDI7lNY5puqONc06oHvj0RgJfwFpNGbQL1U4zWjQy3TB0

-- Dumped from database version 16.10 (Ubuntu 16.10-0ubuntu0.24.04.1)
-- Dumped by pg_dump version 16.10 (Ubuntu 16.10-0ubuntu0.24.04.1)

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
-- Name: estudio; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.estudio (
    id_estudio bigint NOT NULL,
    nombre_estudio character varying(128) NOT NULL
);


ALTER TABLE public.estudio OWNER TO postgres;

--
-- Name: género; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."género" (
    "id_género" bigint NOT NULL,
    "nombre_género" character varying(128) NOT NULL
);


ALTER TABLE public."género" OWNER TO postgres;

--
-- Name: juego_género; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."juego_género" (
    id_juego integer NOT NULL,
    "id_género" integer NOT NULL
);


ALTER TABLE public."juego_género" OWNER TO postgres;

--
-- Name: juego_os; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.juego_os (
    id_juego integer NOT NULL,
    id_os integer NOT NULL
);


ALTER TABLE public.juego_os OWNER TO postgres;

--
-- Name: juegos; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.juegos (
    id_juego bigint NOT NULL,
    titulo_juego character varying(100) NOT NULL,
    "fecha_creación" date,
    costo numeric(10,2),
    "versión" character varying(20),
    nivel_popularidad character varying(50),
    id_estudio integer
);


ALTER TABLE public.juegos OWNER TO postgres;

--
-- Name: os_compatible; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.os_compatible (
    id_os bigint NOT NULL,
    nombre_os character varying(50) NOT NULL
);


ALTER TABLE public.os_compatible OWNER TO postgres;

--
-- Name: requisitos; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.requisitos (
    id_requisito integer NOT NULL,
    id_juego integer NOT NULL,
    tipo_requisito character varying(20) NOT NULL,
    componente character varying(50) NOT NULL,
    "descripción" character varying(512) NOT NULL
);


ALTER TABLE public.requisitos OWNER TO postgres;

--
-- Name: requisitos_id_requisito_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.requisitos_id_requisito_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.requisitos_id_requisito_seq OWNER TO postgres;

--
-- Name: requisitos_id_requisito_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.requisitos_id_requisito_seq OWNED BY public.requisitos.id_requisito;


--
-- Name: vista_juegos_por_genero; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW public.vista_juegos_por_genero AS
 SELECT j.titulo_juego,
    g."nombre_género"
   FROM ((public.juegos j
     JOIN public."juego_género" jg ON ((j.id_juego = jg.id_juego)))
     JOIN public."género" g ON ((jg."id_género" = g."id_género")));


ALTER VIEW public.vista_juegos_por_genero OWNER TO postgres;

--
-- Name: requisitos id_requisito; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.requisitos ALTER COLUMN id_requisito SET DEFAULT nextval('public.requisitos_id_requisito_seq'::regclass);


--
-- Data for Name: estudio; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.estudio (id_estudio, nombre_estudio) FROM stdin;
1	Mojang Studios
2	Rockstar Games
3	CD Projekt Red
4	FromSoftware
5	Nintendo EAD
6	Santa Monica Studio
7	Larian Studios
8	ConcernedApe
9	Supergiant Games
10	Valve Corporation
11	Square Enix
12	Activision/Infinity Ward
\.


--
-- Data for Name: género; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."género" ("id_género", "nombre_género") FROM stdin;
1	Sandbox
2	Supervivenvia
3	Acción
4	Aventura
5	Mundo Abierto
6	RPG
7	ARPG
8	Táctico por turnos
9	Simulación
10	Roguelike
11	Puzzle
12	Plataformas
13	JRPG
14	Battle Royal
15	FPS
16	Táctico
\.


--
-- Data for Name: juego_género; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."juego_género" (id_juego, "id_género") FROM stdin;
1	1
1	2
2	3
2	5
3	6
3	4
3	5
4	3
4	5
4	4
5	7
5	4
6	4
6	6
7	3
7	4
8	6
8	3
8	5
9	6
9	8
10	9
10	4
11	10
11	7
12	11
12	12
13	13
14	14
14	15
15	15
15	16
\.


--
-- Data for Name: juego_os; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.juego_os (id_juego, id_os) FROM stdin;
1	1
1	2
1	3
1	9
1	8
2	1
2	4
2	5
2	6
2	7
3	1
3	4
3	5
3	6
3	7
3	8
4	1
4	5
4	7
5	1
5	4
5	5
5	6
5	7
6	8
6	10
7	5
7	1
8	1
8	4
8	5
8	6
8	7
9	1
9	2
9	4
9	6
10	1
10	2
10	3
10	8
10	9
11	1
11	2
11	8
11	4
11	5
11	6
11	7
12	1
12	2
12	3
12	11
12	12
13	4
14	1
14	4
14	5
14	6
14	7
15	1
15	3
\.


--
-- Data for Name: juegos; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.juegos (id_juego, titulo_juego, "fecha_creación", costo, "versión", nivel_popularidad, id_estudio) FROM stdin;
1	Minecraft	2011-11-18	39856.71	1.20+	Muy Alto (fama mundial)	1
2	Grand Theft Auto V	2013-09-17	39856.71	Online	Muy Alto (Ventas)	2
3	The Witcher 3: Wild Hunt	2015-05-19	53146.71	Juego Base + Exp.	Alto (Crítica y Fans)	3
4	Red Dead Redemption 2	2018-10-26	79726.71	Juego Base + Online	Alto (Crítica y Ventas)	2
5	Elden Ring	2022-01-25	79726.71	1.10+	Muy Alto (Juego del Año)	4
6	The Legend of Zelda: Breath of the Wild	2017-03-03	79726.71	Juego Base + DLC	Alto (Crítica)	5
7	God of War	2018-04-20	66436.71	1.0.1+	Alto (Crítica y Fans)	6
8	Cyberpunk 2077	2020-12-10	79726.71	2.1+	Alto (Popularidad Recup.)	3
9	Baldur's Gate 3	2023-08-03	79726.71	4.0+	Muy Alto (Juego del Año)	7
10	Stardew Valley	2016-02-26	19856.71	1.6+	Alto (Indie Aclamado)	8
11	Hades	2020-09-17	33146.71	1.0+	Alto (Indie Aclamado)	9
12	Portal 2	2011-04-19	13286.71	N/A	Alto (Clásico Puzzles)	10
13	Final Fantasy VII Rebirth	2024-02-29	86376.71	1.0+	Alto (JRPG Reciente)	11
14	Call of Duty: Warzone	2020-03-10	0.00	Constante	Muy Alto (Battle Royale)	12
15	Counter-Strike 2	2023-09-27	0.00	Constante	Muy Alto (eSports)	10
\.


--
-- Data for Name: os_compatible; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.os_compatible (id_os, nombre_os) FROM stdin;
1	Windows
2	macOS
3	Linux
4	PlayStation 5
5	PlayStation 4
6	Xbox Series X/S
7	Xbox One
8	Nintendo Switch
9	Móvil (Android/iOS)
10	Wii U
11	PlayStation 3
12	Xbox 360
\.


--
-- Data for Name: requisitos; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.requisitos (id_requisito, id_juego, tipo_requisito, componente, "descripción") FROM stdin;
1	1	Mínimo	RAM	4 GB
2	1	Mínimo	Almacenamiento	1 GB
3	1	Mínimo	Procesador	Intel Core i3-3210 / AMD A8-7600
4	2	Mínimo	RAM	8 GB
5	2	Mínimo	Almacenamiento	72 GB
6	2	Mínimo	Procesador	Intel Core 2 Quad Q6600 / AMD Phenom 9850
7	3	Mínimo	RAM	8 GB
8	3	Mínimo	Almacenamiento	50 GB
9	3	Mínimo	Procesador	Intel Core i5-2500K / AMD Phenom II X4 940
10	4	Mínimo	RAM	8 GB
11	4	Mínimo	Almacenamiento	150 GB
12	4	Mínimo	Procesador	Intel Core i5-2500K / AMD FX-6300
13	5	Mínimo	RAM	12 GB
14	5	Mínimo	Almacenamiento	60 GB
15	5	Mínimo	Procesador	Intel Core i5-8400 / AMD Ryzen 3 3300X
16	7	Mínimo	RAM	8 GB
17	7	Mínimo	Almacenamiento	70 GB
18	7	Mínimo	Procesador	Intel Core i5-2500k / AMD Ryzen 3 1200
19	8	Mínimo	RAM	12 GB
20	8	Mínimo	Almacenamiento	70 GB (SSD)
21	8	Mínimo	Procesador	Intel Core i7-6700 / AMD Ryzen 5 1600
22	9	Mínimo	RAM	8 GB
23	9	Mínimo	Almacenamiento	150 GB (SSD)
24	9	Mínimo	Procesador	Intel i7 4790K / AMD Ryzen 5 1500X
25	10	Mínimo	RAM	2 GB
26	10	Mínimo	Almacenamiento	1 GB
27	10	Mínimo	Procesador	2 GHz
28	11	Mínimo	RAM	4 GB
29	11	Mínimo	Almacenamiento	15 GB
30	11	Mínimo	Procesador	Dual Core 3.0 GHz+
31	12	Mínimo	RAM	2 GB
32	12	Mínimo	Almacenamiento	8 GB
33	12	Mínimo	Procesador	Dual Core a 3.0 GHz
34	14	Mínimo	RAM	8 GB
35	14	Mínimo	Almacenamiento	175 GB
36	14	Mínimo	Procesador	Intel Core i3-6100 / AMD Ryzen 3 1200
37	15	Mínimo	RAM	8 GB
38	15	Mínimo	Almacenamiento	85 GB
39	15	Mínimo	Procesador	4 núcleos
\.


--
-- Name: requisitos_id_requisito_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.requisitos_id_requisito_seq', 1, false);


--
-- Name: estudio estudio_nombre_estudio_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.estudio
    ADD CONSTRAINT estudio_nombre_estudio_key UNIQUE (nombre_estudio);


--
-- Name: estudio estudio_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.estudio
    ADD CONSTRAINT estudio_pkey PRIMARY KEY (id_estudio);


--
-- Name: género género_nombre_género_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."género"
    ADD CONSTRAINT "género_nombre_género_key" UNIQUE ("nombre_género");


--
-- Name: género género_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."género"
    ADD CONSTRAINT "género_pkey" PRIMARY KEY ("id_género");


--
-- Name: juegos juegos_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.juegos
    ADD CONSTRAINT juegos_pkey PRIMARY KEY (id_juego);


--
-- Name: os_compatible os_compatible_nombre_os_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.os_compatible
    ADD CONSTRAINT os_compatible_nombre_os_key UNIQUE (nombre_os);


--
-- Name: os_compatible os_compatible_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.os_compatible
    ADD CONSTRAINT os_compatible_pkey PRIMARY KEY (id_os);


--
-- Name: juego_género pk_juego_género; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."juego_género"
    ADD CONSTRAINT "pk_juego_género" PRIMARY KEY (id_juego, "id_género");


--
-- Name: juego_os pk_juego_os; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.juego_os
    ADD CONSTRAINT pk_juego_os PRIMARY KEY (id_juego, id_os);


--
-- Name: requisitos requisitos_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.requisitos
    ADD CONSTRAINT requisitos_pkey PRIMARY KEY (id_requisito);


--
-- Name: juegos fk_estudio; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.juegos
    ADD CONSTRAINT fk_estudio FOREIGN KEY (id_estudio) REFERENCES public.estudio(id_estudio);


--
-- Name: juego_género fk_jg_género; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."juego_género"
    ADD CONSTRAINT "fk_jg_género" FOREIGN KEY ("id_género") REFERENCES public."género"("id_género") ON DELETE CASCADE;


--
-- Name: juego_género fk_jg_juego; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."juego_género"
    ADD CONSTRAINT fk_jg_juego FOREIGN KEY (id_juego) REFERENCES public.juegos(id_juego) ON DELETE CASCADE;


--
-- Name: juego_os fk_jo_juego; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.juego_os
    ADD CONSTRAINT fk_jo_juego FOREIGN KEY (id_juego) REFERENCES public.juegos(id_juego) ON DELETE CASCADE;


--
-- Name: juego_os fk_jo_os; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.juego_os
    ADD CONSTRAINT fk_jo_os FOREIGN KEY (id_os) REFERENCES public.os_compatible(id_os) ON DELETE CASCADE;


--
-- Name: requisitos fk_requisito_juego; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.requisitos
    ADD CONSTRAINT fk_requisito_juego FOREIGN KEY (id_juego) REFERENCES public.juegos(id_juego) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

\unrestrict cLIGEQ65An2F2hdmj5NDI7lNY5puqONc06oHvj0RgJfwFpNGbQL1U4zWjQy3TB0

