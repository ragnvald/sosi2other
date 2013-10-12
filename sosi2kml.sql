---
--- Create user sosi
---
--- create database sosi_repository with user sosi
---
--- Run the below script within pgadmin with the sosi user



--
-- sosiQL database dump
--

SET client_encoding = 'LATIN1';
SET standard_conforming_strings = off;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET escape_string_warning = off;

--
-- Name: sosi_repository; Type: DATABASE; Schema: -; Owner: -
--



--
-- TOC entry 277 (class 2612 OID 16386)
-- Name: plpgsql; Type: PROCEDURAL LANGUAGE; Schema: -; Owner: sosi
--

CREATE PROCEDURAL LANGUAGE plpgsql;


ALTER PROCEDURAL LANGUAGE plpgsql OWNER TO sosi;

SET search_path = public, pg_catalog;

--
-- TOC entry 1297 (class 1259 OID 17317)
-- Dependencies: 4
-- Name: id_seq; Type: SEQUENCE; Schema: public; Owner: sosi
--

CREATE SEQUENCE id_seq
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.id_seq OWNER TO sosi;

--
-- TOC entry 1681 (class 0 OID 0)
-- Dependencies: 1297
-- Name: id_seq; Type: SEQUENCE SET; Schema: public; Owner: sosi
--

SELECT pg_catalog.setval('id_seq', 848678, true);


SET default_tablespace = '';

SET default_with_oids = false;

--
-- TOC entry 1282 (class 1259 OID 17225)
-- Dependencies: 4
-- Name: tbl_fil; Type: TABLE; Schema: public; Owner: sosi; Tablespace: 
--

CREATE TABLE tbl_fil (
    id integer NOT NULL,
    filnavn character varying(512) NOT NULL
);


ALTER TABLE public.tbl_fil OWNER TO sosi;

SET default_with_oids = true;

--
-- TOC entry 1283 (class 1259 OID 17227)
-- Dependencies: 4
-- Name: tbl_koordinat; Type: TABLE; Schema: public; Owner: sosi; Tablespace: 
--

CREATE TABLE tbl_koordinat (
    id integer NOT NULL,
    y numeric(20,2),
    x numeric(20,2),
    z numeric(20,2)
);


ALTER TABLE public.tbl_koordinat OWNER TO sosi;

--
-- TOC entry 1284 (class 1259 OID 17229)
-- Dependencies: 4 1283
-- Name: tbl_koordinat_id_seq; Type: SEQUENCE; Schema: public; Owner: sosi
--

CREATE SEQUENCE tbl_koordinat_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.tbl_koordinat_id_seq OWNER TO sosi;

--
-- TOC entry 1684 (class 0 OID 0)
-- Dependencies: 1284
-- Name: tbl_koordinat_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: sosi
--

ALTER SEQUENCE tbl_koordinat_id_seq OWNED BY tbl_koordinat.id;


--
-- TOC entry 1685 (class 0 OID 0)
-- Dependencies: 1284
-- Name: tbl_koordinat_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sosi
--

SELECT pg_catalog.setval('tbl_koordinat_id_seq', 1, false);


SET default_with_oids = false;

--
-- TOC entry 1285 (class 1259 OID 17231)
-- Dependencies: 4
-- Name: tbl_rel_fil_sniv1; Type: TABLE; Schema: public; Owner: sosi; Tablespace: 
--

CREATE TABLE tbl_rel_fil_sniv1 (
    ref_fil integer NOT NULL,
    ref_sniv1 integer NOT NULL,
    rekkefolge integer NOT NULL
);


ALTER TABLE public.tbl_rel_fil_sniv1 OWNER TO sosi;

SET default_with_oids = true;

--
-- TOC entry 1286 (class 1259 OID 17233)
-- Dependencies: 4
-- Name: tbl_rel_geoobj_koordinat; Type: TABLE; Schema: public; Owner: sosi; Tablespace: 
--

CREATE TABLE tbl_rel_geoobj_koordinat (
    ref_geoobj integer NOT NULL,
    ref_koordinat integer NOT NULL,
    rekkefnr integer,
    kp integer,
    kvalitet character varying(24)
);


ALTER TABLE public.tbl_rel_geoobj_koordinat OWNER TO sosi;

SET default_with_oids = false;

--
-- TOC entry 1287 (class 1259 OID 17235)
-- Dependencies: 4
-- Name: tbl_rel_sniv1_sniv2; Type: TABLE; Schema: public; Owner: sosi; Tablespace: 
--

CREATE TABLE tbl_rel_sniv1_sniv2 (
    ref_sniv1 integer NOT NULL,
    ref_sniv2 integer NOT NULL
);


ALTER TABLE public.tbl_rel_sniv1_sniv2 OWNER TO sosi;

--
-- TOC entry 1288 (class 1259 OID 17237)
-- Dependencies: 4
-- Name: tbl_rel_sniv2_sniv3; Type: TABLE; Schema: public; Owner: sosi; Tablespace: 
--

CREATE TABLE tbl_rel_sniv2_sniv3 (
    ref_sniv2 integer NOT NULL,
    ref_sniv3 integer NOT NULL
);


ALTER TABLE public.tbl_rel_sniv2_sniv3 OWNER TO sosi;

SET default_with_oids = true;

--
-- TOC entry 1289 (class 1259 OID 17239)
-- Dependencies: 4
-- Name: tbl_sniv1; Type: TABLE; Schema: public; Owner: sosi; Tablespace: 
--

CREATE TABLE tbl_sniv1 (
    id integer NOT NULL,
    main character varying(512) NOT NULL,
    content character varying(1024)
);


ALTER TABLE public.tbl_sniv1 OWNER TO sosi;

--
-- TOC entry 1691 (class 0 OID 0)
-- Dependencies: 1289
-- Name: COLUMN tbl_sniv1.main; Type: COMMENT; Schema: public; Owner: sosi
--

COMMENT ON COLUMN tbl_sniv1.main IS 'SOSI nivå 1 beskrivelse';


--
-- TOC entry 1290 (class 1259 OID 17241)
-- Dependencies: 4 1289
-- Name: tbl_sniv1_id_seq; Type: SEQUENCE; Schema: public; Owner: sosi
--

CREATE SEQUENCE tbl_sniv1_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.tbl_sniv1_id_seq OWNER TO sosi;

--
-- TOC entry 1693 (class 0 OID 0)
-- Dependencies: 1290
-- Name: tbl_sniv1_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: sosi
--

ALTER SEQUENCE tbl_sniv1_id_seq OWNED BY tbl_sniv1.id;


--
-- TOC entry 1694 (class 0 OID 0)
-- Dependencies: 1290
-- Name: tbl_sniv1_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sosi
--

SELECT pg_catalog.setval('tbl_sniv1_id_seq', 1, false);


--
-- TOC entry 1291 (class 1259 OID 17243)
-- Dependencies: 4
-- Name: tbl_sniv2; Type: TABLE; Schema: public; Owner: sosi; Tablespace: 
--

CREATE TABLE tbl_sniv2 (
    id integer NOT NULL,
    main character varying(512),
    content character varying(1024)
);


ALTER TABLE public.tbl_sniv2 OWNER TO sosi;

--
-- TOC entry 1292 (class 1259 OID 17245)
-- Dependencies: 1291 4
-- Name: tbl_sniv2_id_seq; Type: SEQUENCE; Schema: public; Owner: sosi
--

CREATE SEQUENCE tbl_sniv2_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.tbl_sniv2_id_seq OWNER TO sosi;

--
-- TOC entry 1697 (class 0 OID 0)
-- Dependencies: 1292
-- Name: tbl_sniv2_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: sosi
--

ALTER SEQUENCE tbl_sniv2_id_seq OWNED BY tbl_sniv2.id;


--
-- TOC entry 1698 (class 0 OID 0)
-- Dependencies: 1292
-- Name: tbl_sniv2_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sosi
--

SELECT pg_catalog.setval('tbl_sniv2_id_seq', 1, false);


--
-- TOC entry 1293 (class 1259 OID 17247)
-- Dependencies: 4
-- Name: tbl_sniv3; Type: TABLE; Schema: public; Owner: sosi; Tablespace: 
--

CREATE TABLE tbl_sniv3 (
    id integer NOT NULL,
    main character varying(512),
    content character varying(1024)
);


ALTER TABLE public.tbl_sniv3 OWNER TO sosi;

--
-- TOC entry 1294 (class 1259 OID 17249)
-- Dependencies: 1293 4
-- Name: tbl_sniv3_id_seq; Type: SEQUENCE; Schema: public; Owner: sosi
--

CREATE SEQUENCE tbl_sniv3_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.tbl_sniv3_id_seq OWNER TO sosi;

--
-- TOC entry 1701 (class 0 OID 0)
-- Dependencies: 1294
-- Name: tbl_sniv3_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: sosi
--

ALTER SEQUENCE tbl_sniv3_id_seq OWNED BY tbl_sniv3.id;


--
-- TOC entry 1702 (class 0 OID 0)
-- Dependencies: 1294
-- Name: tbl_sniv3_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sosi
--

SELECT pg_catalog.setval('tbl_sniv3_id_seq', 1, false);


SET default_with_oids = false;

--
-- TOC entry 1295 (class 1259 OID 17251)
-- Dependencies: 4
-- Name: tbl_type_geoobj; Type: TABLE; Schema: public; Owner: sosi; Tablespace: 
--

CREATE TABLE tbl_type_geoobj (
    id integer NOT NULL,
    navn character varying(256) NOT NULL
);


ALTER TABLE public.tbl_type_geoobj OWNER TO sosi;

--
-- TOC entry 1296 (class 1259 OID 17253)
-- Dependencies: 4
-- Name: tbl_utmkoder; Type: TABLE; Schema: public; Owner: sosi; Tablespace: 
--

CREATE TABLE tbl_utmkoder (
    id integer NOT NULL,
    sosi_kode character varying(5) NOT NULL,
    utmsone character varying(5) NOT NULL
);


ALTER TABLE public.tbl_utmkoder OWNER TO sosi;

--
-- TOC entry 1628 (class 2604 OID 17255)
-- Dependencies: 1284 1283
-- Name: id; Type: DEFAULT; Schema: public; Owner: sosi
--

ALTER TABLE tbl_koordinat ALTER COLUMN id SET DEFAULT nextval('tbl_koordinat_id_seq'::regclass);


--
-- TOC entry 1629 (class 2604 OID 17256)
-- Dependencies: 1290 1289
-- Name: id; Type: DEFAULT; Schema: public; Owner: sosi
--

ALTER TABLE tbl_sniv1 ALTER COLUMN id SET DEFAULT nextval('tbl_sniv1_id_seq'::regclass);


--
-- TOC entry 1630 (class 2604 OID 17257)
-- Dependencies: 1292 1291
-- Name: id; Type: DEFAULT; Schema: public; Owner: sosi
--

ALTER TABLE tbl_sniv2 ALTER COLUMN id SET DEFAULT nextval('tbl_sniv2_id_seq'::regclass);


--
-- TOC entry 1631 (class 2604 OID 17258)
-- Dependencies: 1294 1293
-- Name: id; Type: DEFAULT; Schema: public; Owner: sosi
--

ALTER TABLE tbl_sniv3 ALTER COLUMN id SET DEFAULT nextval('tbl_sniv3_id_seq'::regclass);


--
-- TOC entry 1665 (class 0 OID 17225)
-- Dependencies: 1282
-- Data for Name: tbl_fil; Type: TABLE DATA; Schema: public; Owner: sosi
--



--
-- TOC entry 1666 (class 0 OID 17227)
-- Dependencies: 1283
-- Data for Name: tbl_koordinat; Type: TABLE DATA; Schema: public; Owner: sosi
--



--
-- TOC entry 1667 (class 0 OID 17231)
-- Dependencies: 1285
-- Data for Name: tbl_rel_fil_sniv1; Type: TABLE DATA; Schema: public; Owner: sosi
--



--
-- TOC entry 1668 (class 0 OID 17233)
-- Dependencies: 1286
-- Data for Name: tbl_rel_geoobj_koordinat; Type: TABLE DATA; Schema: public; Owner: sosi
--



--
-- TOC entry 1669 (class 0 OID 17235)
-- Dependencies: 1287
-- Data for Name: tbl_rel_sniv1_sniv2; Type: TABLE DATA; Schema: public; Owner: sosi
--



--
-- TOC entry 1670 (class 0 OID 17237)
-- Dependencies: 1288
-- Data for Name: tbl_rel_sniv2_sniv3; Type: TABLE DATA; Schema: public; Owner: sosi
--



--
-- TOC entry 1671 (class 0 OID 17239)
-- Dependencies: 1289
-- Data for Name: tbl_sniv1; Type: TABLE DATA; Schema: public; Owner: sosi
--



--
-- TOC entry 1672 (class 0 OID 17243)
-- Dependencies: 1291
-- Data for Name: tbl_sniv2; Type: TABLE DATA; Schema: public; Owner: sosi
--



--
-- TOC entry 1673 (class 0 OID 17247)
-- Dependencies: 1293
-- Data for Name: tbl_sniv3; Type: TABLE DATA; Schema: public; Owner: sosi
--



--
-- TOC entry 1674 (class 0 OID 17251)
-- Dependencies: 1295
-- Data for Name: tbl_type_geoobj; Type: TABLE DATA; Schema: public; Owner: sosi
--

INSERT INTO tbl_type_geoobj (id, navn) VALUES (1, 'PUNKT');
INSERT INTO tbl_type_geoobj (id, navn) VALUES (2, 'KURVE');
INSERT INTO tbl_type_geoobj (id, navn) VALUES (3, 'FLATE');
INSERT INTO tbl_type_geoobj (id, navn) VALUES (4, 'LINJE');


--
-- TOC entry 1675 (class 0 OID 17253)
-- Dependencies: 1296
-- Data for Name: tbl_utmkoder; Type: TABLE DATA; Schema: public; Owner: sosi
--

INSERT INTO tbl_utmkoder (id, sosi_kode, utmsone) VALUES (1, '22', '32');
INSERT INTO tbl_utmkoder (id, sosi_kode, utmsone) VALUES (2, '23', '33');


--
-- TOC entry 1633 (class 2606 OID 17260)
-- Dependencies: 1282 1282
-- Name: tbl_fil_pkey; Type: CONSTRAINT; Schema: public; Owner: sosi; Tablespace: 
--

ALTER TABLE ONLY tbl_fil
    ADD CONSTRAINT tbl_fil_pkey PRIMARY KEY (id);


--
-- TOC entry 1636 (class 2606 OID 17262)
-- Dependencies: 1283 1283
-- Name: tbl_knutepunkt_pkey; Type: CONSTRAINT; Schema: public; Owner: sosi; Tablespace: 
--

ALTER TABLE ONLY tbl_koordinat
    ADD CONSTRAINT tbl_knutepunkt_pkey PRIMARY KEY (id);


--
-- TOC entry 1638 (class 2606 OID 17264)
-- Dependencies: 1285 1285 1285
-- Name: tbl_rel_fil_sniv1_pkey; Type: CONSTRAINT; Schema: public; Owner: sosi; Tablespace: 
--

ALTER TABLE ONLY tbl_rel_fil_sniv1
    ADD CONSTRAINT tbl_rel_fil_sniv1_pkey PRIMARY KEY (ref_fil, ref_sniv1);


--
-- TOC entry 1640 (class 2606 OID 17266)
-- Dependencies: 1286 1286 1286
-- Name: tbl_rel_geoobj_koordinat_pkey; Type: CONSTRAINT; Schema: public; Owner: sosi; Tablespace: 
--

ALTER TABLE ONLY tbl_rel_geoobj_koordinat
    ADD CONSTRAINT tbl_rel_geoobj_koordinat_pkey PRIMARY KEY (ref_geoobj, ref_koordinat);


--
-- TOC entry 1644 (class 2606 OID 17268)
-- Dependencies: 1288 1288 1288
-- Name: tbl_rel_sniv2_sniv3_pkey; Type: CONSTRAINT; Schema: public; Owner: sosi; Tablespace: 
--

ALTER TABLE ONLY tbl_rel_sniv2_sniv3
    ADD CONSTRAINT tbl_rel_sniv2_sniv3_pkey PRIMARY KEY (ref_sniv2, ref_sniv3);


--
-- TOC entry 1647 (class 2606 OID 17270)
-- Dependencies: 1289 1289
-- Name: tbl_sl1_pkey; Type: CONSTRAINT; Schema: public; Owner: sosi; Tablespace: 
--

ALTER TABLE ONLY tbl_sniv1
    ADD CONSTRAINT tbl_sl1_pkey PRIMARY KEY (id);


--
-- TOC entry 1642 (class 2606 OID 17272)
-- Dependencies: 1287 1287 1287
-- Name: tbl_sniv1_sniv2_pkey; Type: CONSTRAINT; Schema: public; Owner: sosi; Tablespace: 
--

ALTER TABLE ONLY tbl_rel_sniv1_sniv2
    ADD CONSTRAINT tbl_sniv1_sniv2_pkey PRIMARY KEY (ref_sniv1, ref_sniv2);


--
-- TOC entry 1650 (class 2606 OID 17274)
-- Dependencies: 1291 1291
-- Name: tbl_sniv2_pkey; Type: CONSTRAINT; Schema: public; Owner: sosi; Tablespace: 
--

ALTER TABLE ONLY tbl_sniv2
    ADD CONSTRAINT tbl_sniv2_pkey PRIMARY KEY (id);


--
-- TOC entry 1653 (class 2606 OID 17276)
-- Dependencies: 1293 1293
-- Name: tbl_sniv3_pkey; Type: CONSTRAINT; Schema: public; Owner: sosi; Tablespace: 
--

ALTER TABLE ONLY tbl_sniv3
    ADD CONSTRAINT tbl_sniv3_pkey PRIMARY KEY (id);


--
-- TOC entry 1655 (class 2606 OID 17278)
-- Dependencies: 1295 1295
-- Name: tbl_type_geoobj_pkey; Type: CONSTRAINT; Schema: public; Owner: sosi; Tablespace: 
--

ALTER TABLE ONLY tbl_type_geoobj
    ADD CONSTRAINT tbl_type_geoobj_pkey PRIMARY KEY (id);


--
-- TOC entry 1657 (class 2606 OID 17280)
-- Dependencies: 1296 1296
-- Name: tbl_utmkoder_pkey; Type: CONSTRAINT; Schema: public; Owner: sosi; Tablespace: 
--

ALTER TABLE ONLY tbl_utmkoder
    ADD CONSTRAINT tbl_utmkoder_pkey PRIMARY KEY (id);


--
-- TOC entry 1634 (class 1259 OID 512079)
-- Dependencies: 1283 1283 1283
-- Name: ind_koord_id_x_y; Type: INDEX; Schema: public; Owner: sosi; Tablespace: 
--

CREATE INDEX ind_koord_id_x_y ON tbl_koordinat USING btree (id, x, y);


--
-- TOC entry 1645 (class 1259 OID 512076)
-- Dependencies: 1289 1289
-- Name: ind_sniv1_id_main; Type: INDEX; Schema: public; Owner: sosi; Tablespace: 
--

CREATE UNIQUE INDEX ind_sniv1_id_main ON tbl_sniv1 USING btree (id, main);


--
-- TOC entry 1648 (class 1259 OID 512075)
-- Dependencies: 1291 1291
-- Name: ind_sniv2_id_main; Type: INDEX; Schema: public; Owner: sosi; Tablespace: 
--

CREATE UNIQUE INDEX ind_sniv2_id_main ON tbl_sniv2 USING btree (id, main);


--
-- TOC entry 1651 (class 1259 OID 512077)
-- Dependencies: 1293 1293
-- Name: ind_sniv3_id_main; Type: INDEX; Schema: public; Owner: sosi; Tablespace: 
--

CREATE INDEX ind_sniv3_id_main ON tbl_sniv3 USING btree (id, main);


--
-- TOC entry 1658 (class 2606 OID 17281)
-- Dependencies: 1646 1289 1285
-- Name: Ref_-02; Type: FK CONSTRAINT; Schema: public; Owner: sosi
--

ALTER TABLE ONLY tbl_rel_fil_sniv1
    ADD CONSTRAINT "Ref_-02" FOREIGN KEY (ref_sniv1) REFERENCES tbl_sniv1(id);


--
-- TOC entry 1661 (class 2606 OID 17286)
-- Dependencies: 1287 1646 1289
-- Name: Ref_-03; Type: FK CONSTRAINT; Schema: public; Owner: sosi
--

ALTER TABLE ONLY tbl_rel_sniv1_sniv2
    ADD CONSTRAINT "Ref_-03" FOREIGN KEY (ref_sniv1) REFERENCES tbl_sniv1(id);


--
-- TOC entry 1663 (class 2606 OID 17291)
-- Dependencies: 1288 1293 1652
-- Name: Ref_00; Type: FK CONSTRAINT; Schema: public; Owner: sosi
--

ALTER TABLE ONLY tbl_rel_sniv2_sniv3
    ADD CONSTRAINT "Ref_00" FOREIGN KEY (ref_sniv3) REFERENCES tbl_sniv3(id);


--
-- TOC entry 1664 (class 2606 OID 17296)
-- Dependencies: 1288 1649 1291
-- Name: Ref_01; Type: FK CONSTRAINT; Schema: public; Owner: sosi
--

ALTER TABLE ONLY tbl_rel_sniv2_sniv3
    ADD CONSTRAINT "Ref_01" FOREIGN KEY (ref_sniv2) REFERENCES tbl_sniv2(id);


--
-- TOC entry 1659 (class 2606 OID 17301)
-- Dependencies: 1286 1635 1283
-- Name: Ref_03; Type: FK CONSTRAINT; Schema: public; Owner: sosi
--

ALTER TABLE ONLY tbl_rel_geoobj_koordinat
    ADD CONSTRAINT "Ref_03" FOREIGN KEY (ref_koordinat) REFERENCES tbl_koordinat(id);


--
-- TOC entry 1660 (class 2606 OID 17306)
-- Dependencies: 1289 1286 1646
-- Name: Ref_04; Type: FK CONSTRAINT; Schema: public; Owner: sosi
--

ALTER TABLE ONLY tbl_rel_geoobj_koordinat
    ADD CONSTRAINT "Ref_04" FOREIGN KEY (ref_geoobj) REFERENCES tbl_sniv1(id);


--
-- TOC entry 1662 (class 2606 OID 17311)
-- Dependencies: 1287 1649 1291
-- Name: test; Type: FK CONSTRAINT; Schema: public; Owner: sosi
--

ALTER TABLE ONLY tbl_rel_sniv1_sniv2
    ADD CONSTRAINT test FOREIGN KEY (ref_sniv2) REFERENCES tbl_sniv2(id);


--
-- TOC entry 1680 (class 0 OID 0)
-- Dependencies: 4
-- Name: public; Type: ACL; Schema: -; Owner: sosi
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM sosi;
GRANT ALL ON SCHEMA public TO sosi;


--
-- TOC entry 1682 (class 0 OID 0)
-- Dependencies: 1282
-- Name: tbl_fil; Type: ACL; Schema: public; Owner: sosi
--

REVOKE ALL ON TABLE tbl_fil FROM PUBLIC;
REVOKE ALL ON TABLE tbl_fil FROM sosi;
GRANT ALL ON TABLE tbl_fil TO sosi;
GRANT ALL ON TABLE tbl_fil TO PUBLIC;


--
-- TOC entry 1683 (class 0 OID 0)
-- Dependencies: 1283
-- Name: tbl_koordinat; Type: ACL; Schema: public; Owner: sosi
--

REVOKE ALL ON TABLE tbl_koordinat FROM PUBLIC;
REVOKE ALL ON TABLE tbl_koordinat FROM sosi;
GRANT ALL ON TABLE tbl_koordinat TO sosi;
GRANT ALL ON TABLE tbl_koordinat TO PUBLIC;


--
-- TOC entry 1686 (class 0 OID 0)
-- Dependencies: 1284
-- Name: tbl_koordinat_id_seq; Type: ACL; Schema: public; Owner: sosi
--

REVOKE ALL ON SEQUENCE tbl_koordinat_id_seq FROM PUBLIC;
REVOKE ALL ON SEQUENCE tbl_koordinat_id_seq FROM sosi;
GRANT ALL ON SEQUENCE tbl_koordinat_id_seq TO sosi;
GRANT SELECT,UPDATE ON SEQUENCE tbl_koordinat_id_seq TO PUBLIC;


--
-- TOC entry 1687 (class 0 OID 0)
-- Dependencies: 1285
-- Name: tbl_rel_fil_sniv1; Type: ACL; Schema: public; Owner: sosi
--

REVOKE ALL ON TABLE tbl_rel_fil_sniv1 FROM PUBLIC;
REVOKE ALL ON TABLE tbl_rel_fil_sniv1 FROM sosi;
GRANT ALL ON TABLE tbl_rel_fil_sniv1 TO sosi;
GRANT ALL ON TABLE tbl_rel_fil_sniv1 TO PUBLIC;


--
-- TOC entry 1688 (class 0 OID 0)
-- Dependencies: 1286
-- Name: tbl_rel_geoobj_koordinat; Type: ACL; Schema: public; Owner: sosi
--

REVOKE ALL ON TABLE tbl_rel_geoobj_koordinat FROM PUBLIC;
REVOKE ALL ON TABLE tbl_rel_geoobj_koordinat FROM sosi;
GRANT ALL ON TABLE tbl_rel_geoobj_koordinat TO sosi;
GRANT ALL ON TABLE tbl_rel_geoobj_koordinat TO PUBLIC;


--
-- TOC entry 1689 (class 0 OID 0)
-- Dependencies: 1287
-- Name: tbl_rel_sniv1_sniv2; Type: ACL; Schema: public; Owner: sosi
--

REVOKE ALL ON TABLE tbl_rel_sniv1_sniv2 FROM PUBLIC;
REVOKE ALL ON TABLE tbl_rel_sniv1_sniv2 FROM sosi;
GRANT ALL ON TABLE tbl_rel_sniv1_sniv2 TO sosi;
GRANT ALL ON TABLE tbl_rel_sniv1_sniv2 TO PUBLIC;


--
-- TOC entry 1690 (class 0 OID 0)
-- Dependencies: 1288
-- Name: tbl_rel_sniv2_sniv3; Type: ACL; Schema: public; Owner: sosi
--

REVOKE ALL ON TABLE tbl_rel_sniv2_sniv3 FROM PUBLIC;
REVOKE ALL ON TABLE tbl_rel_sniv2_sniv3 FROM sosi;
GRANT ALL ON TABLE tbl_rel_sniv2_sniv3 TO sosi;
GRANT ALL ON TABLE tbl_rel_sniv2_sniv3 TO PUBLIC;


--
-- TOC entry 1692 (class 0 OID 0)
-- Dependencies: 1289
-- Name: tbl_sniv1; Type: ACL; Schema: public; Owner: sosi
--

REVOKE ALL ON TABLE tbl_sniv1 FROM PUBLIC;
REVOKE ALL ON TABLE tbl_sniv1 FROM sosi;
GRANT ALL ON TABLE tbl_sniv1 TO sosi;
GRANT ALL ON TABLE tbl_sniv1 TO PUBLIC;


--
-- TOC entry 1695 (class 0 OID 0)
-- Dependencies: 1290
-- Name: tbl_sniv1_id_seq; Type: ACL; Schema: public; Owner: sosi
--

REVOKE ALL ON SEQUENCE tbl_sniv1_id_seq FROM PUBLIC;
REVOKE ALL ON SEQUENCE tbl_sniv1_id_seq FROM sosi;
GRANT ALL ON SEQUENCE tbl_sniv1_id_seq TO sosi;
GRANT SELECT,UPDATE ON SEQUENCE tbl_sniv1_id_seq TO PUBLIC;


--
-- TOC entry 1696 (class 0 OID 0)
-- Dependencies: 1291
-- Name: tbl_sniv2; Type: ACL; Schema: public; Owner: sosi
--

REVOKE ALL ON TABLE tbl_sniv2 FROM PUBLIC;
REVOKE ALL ON TABLE tbl_sniv2 FROM sosi;
GRANT ALL ON TABLE tbl_sniv2 TO sosi;
GRANT ALL ON TABLE tbl_sniv2 TO PUBLIC;


--
-- TOC entry 1699 (class 0 OID 0)
-- Dependencies: 1292
-- Name: tbl_sniv2_id_seq; Type: ACL; Schema: public; Owner: sosi
--

REVOKE ALL ON SEQUENCE tbl_sniv2_id_seq FROM PUBLIC;
REVOKE ALL ON SEQUENCE tbl_sniv2_id_seq FROM sosi;
GRANT ALL ON SEQUENCE tbl_sniv2_id_seq TO sosi;
GRANT SELECT,UPDATE ON SEQUENCE tbl_sniv2_id_seq TO PUBLIC;


--
-- TOC entry 1700 (class 0 OID 0)
-- Dependencies: 1293
-- Name: tbl_sniv3; Type: ACL; Schema: public; Owner: sosi
--

REVOKE ALL ON TABLE tbl_sniv3 FROM PUBLIC;
REVOKE ALL ON TABLE tbl_sniv3 FROM sosi;
GRANT ALL ON TABLE tbl_sniv3 TO sosi;
GRANT ALL ON TABLE tbl_sniv3 TO PUBLIC;


--
-- TOC entry 1703 (class 0 OID 0)
-- Dependencies: 1294
-- Name: tbl_sniv3_id_seq; Type: ACL; Schema: public; Owner: sosi
--

REVOKE ALL ON SEQUENCE tbl_sniv3_id_seq FROM PUBLIC;
REVOKE ALL ON SEQUENCE tbl_sniv3_id_seq FROM sosi;
GRANT ALL ON SEQUENCE tbl_sniv3_id_seq TO sosi;
GRANT SELECT,UPDATE ON SEQUENCE tbl_sniv3_id_seq TO PUBLIC;


--
-- TOC entry 1704 (class 0 OID 0)
-- Dependencies: 1295
-- Name: tbl_type_geoobj; Type: ACL; Schema: public; Owner: sosi
--

REVOKE ALL ON TABLE tbl_type_geoobj FROM PUBLIC;
REVOKE ALL ON TABLE tbl_type_geoobj FROM sosi;
GRANT ALL ON TABLE tbl_type_geoobj TO sosi;
GRANT ALL ON TABLE tbl_type_geoobj TO PUBLIC;


--
-- TOC entry 1705 (class 0 OID 0)
-- Dependencies: 1296
-- Name: tbl_utmkoder; Type: ACL; Schema: public; Owner: sosi
--

REVOKE ALL ON TABLE tbl_utmkoder FROM PUBLIC;
REVOKE ALL ON TABLE tbl_utmkoder FROM sosi;
GRANT ALL ON TABLE tbl_utmkoder TO sosi;
GRANT ALL ON TABLE tbl_utmkoder TO PUBLIC;


-- Completed on 2008-06-09 15:08:10

--
-- sosiQL database dump complete
--

