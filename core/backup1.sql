--
-- Script de inserción de datos para las tablas de menú (categorias_menu e items_menu).
--
-- Este script asume que la estructura de la base de datos (tablas, secuencias, constraints)
-- ya existe y solo inserta/actualiza los datos del menú.
--

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

-- Desactivar temporalmente los triggers y restricciones de clave foránea
-- para permitir TRUNCATE de tablas con dependencias.
ALTER TABLE public.items_menu DISABLE TRIGGER ALL;
ALTER TABLE public.detalles_pedido DISABLE TRIGGER ALL; -- Si 'detalles_pedido' depende de 'items_menu'
ALTER TABLE public.registros_financieros DISABLE TRIGGER ALL; -- Si 'registros_financieros' depende de 'pedidos' que a su vez puede depender de 'detalles_pedido'

-- Limpiar tablas de menú y reiniciar secuencias
-- RESTART IDENTITY reinicia la secuencia asociada a la columna ID.
-- CASCADE también truncará tablas que dependen de estas.
TRUNCATE TABLE public.detalles_pedido RESTART IDENTITY CASCADE; -- Primero detalles_pedido si tiene FK a items_menu
TRUNCATE TABLE public.items_menu RESTART IDENTITY CASCADE;
TRUNCATE TABLE public.categorias_menu RESTART IDENTITY CASCADE;

--
-- Data for Name: categorias_menu; Type: TABLE DATA; Schema: public; Owner: pizzeria_user
--

COPY public.categorias_menu (id, nombre, descripcion) FROM stdin;
1	PIZZAS INDIVIDUALES	Pizzas de tamaño individual.
2	PIZZAS FAMILIARES	Pizzas de tamaño familiar.
3	PIZZAS 1/2 QUESO	Pizzas con doble queso.
4	PIZZAS XL	Pizzas extra grandes.
5	CALZONE	Calzones rellenos.
6	BEBIDAS	Bebidas refrescantes.
7	ADICIONALES	Ingredientes adicionales para tu pizza.
8	ENVASES	Cargos por envases.
\.


--
-- Data for Name: items_menu; Type: TABLE DATA; Schema: public; Owner: pizzeria_user
--

COPY public.items_menu (id, nombre, descripcion, precio, imagen_url, disponible, categoria_id) FROM stdin;
1	Pizza Sapore (Ind.)	Salsa, mozzarella, tocineta, champiñones y cebolla caramelizada	3.60	https://placehold.co/300x200/343a40/FFFFFF?text=Pizza+Sapore	t	1
2	Pizza Sapore (Fam.)	Salsa, mozzarella, tocineta, champiñones y cebolla caramelizada	10.90	https://placehold.co/300x200/343a40/FFFFFF?text=Pizza+Sapore	t	2
3	Pizza Sapore (1/2 Q.)	Salsa, mozzarella, tocineta, champiñones y cebolla caramelizada	13.10	https://placehold.co/300x200/343a40/FFFFFF?text=Pizza+Sapore	t	3
4	Pizza Sapore (XL)	Salsa, mozzarella, tocineta, champiñones y cebolla caramelizada	27.75	https://placehold.co/300x200/343a40/FFFFFF?text=Pizza+Sapore	t	4
5	Pizza Toscana (Ind.)	Salsa, mozzarella, Pepperoni, champiñones, tocineta y maíz	4.20	https://placehold.co/300x200/343a40/FFFFFF?text=Pizza+Toscana	t	1
6	Pizza Toscana (Fam.)	Salsa, mozzarella, Pepperoni, champiñones, tocineta y maíz	12.30	https://placehold.co/300x200/343a40/FFFFFF?text=Pizza+Toscana	t	2
7	Pizza Toscana (1/2 Q.)	Salsa, mozzarella, Pepperoni, champiñones, tocineta y maíz	14.45	https://placehold.co/300x200/343a40/FFFFFF?text=Pizza+Toscana	t	3
8	Pizza Toscana (XL)	Salsa, mozzarella, Pepperoni, champiñones, tocineta y maíz	30.75	https://placehold.co/300x200/343a40/FFFFFF?text=Pizza+Toscana	t	4
9	Pizza Mareale (Ind.)	Salsa, mozzarella, salami, tocineta y aceitunas negras	4.90	https://placehold.co/300x200/343a40/FFFFFF?text=Pizza+Mareale	t	1
10	Pizza Mareale (Fam.)	Salsa, mozzarella, salami, tocineta y aceitunas negras	13.60	https://placehold.co/300x200/343a40/FFFFFF?text=Pizza+Mareale	t	2
11	Pizza Mareale (1/2 Q.)	Salsa, mozzarella, salami, tocineta y aceitunas negras	15.75	https://placehold.co/300x200/343a40/FFFFFF?text=Pizza+Mareale	t	3
12	Pizza Mareale (XL)	Salsa, mozzarella, salami, tocineta y aceitunas negras	34.00	https://placehold.co/300x200/343a40/FFFFFF?text=Pizza+Mareale	t	4
13	Pizza Hongo y morrón (Ind.)	Salsa, mozzarella, champiñones y pimentón	3.30	https://placehold.co/300x200/343a40/FFFFFF?text=Pizza+Hongo	t	1
14	Pizza Hongo y morrón (Fam.)	Salsa, mozzarella, champiñones y pimentón	9.55	https://placehold.co/300x200/343a40/FFFFFF?text=Pizza+Hongo	t	2
15	Pizza Hongo y morrón (1/2 Q.)	Salsa, mozzarella, champiñones y pimentón	11.70	https://placehold.co/300x200/343a40/FFFFFF?text=Pizza+Hongo	t	3
16	Pizza Hongo y morrón (XL)	Salsa, mozzarella, champiñones y pimentón	23.87	https://placehold.co/300x200/343a40/FFFFFF?text=Pizza+Hongo	t	4
17	Pizza Funghi Pancetta (Ind.)	Salsa, mozzarella, pimentón, cebolla, champiñones, tocineta y orégano	3.70	https://placehold.co/300x200/343a40/FFFFFF?text=Pizza+Funghi	t	1
18	Pizza Funghi Pancetta (Fam.)	Salsa, mozzarella, pimentón, cebolla, champiñones, tocineta y orégano	11.00	https://placehold.co/300x200/343a40/FFFFFF?text=Pizza+Funghi	t	2
19	Pizza Funghi Pancetta (1/2 Q.)	Salsa, mozzarella, pimentón, cebolla, champiñones, tocineta y orégano	13.15	https://placehold.co/300x200/343a40/FFFFFF?text=Pizza+Funghi	t	3
20	Pizza Funghi Pancetta (XL)	Salsa, mozzarella, pimentón, cebolla, champiñones, tocineta y orégano	27.50	https://placehold.co/300x200/343a40/FFFFFF?text=Pizza+Funghi	t	4
21	Pizza Brutale (Ind.)	Salsa, mozzarella, tomates en cuadrito, champiñones, jamón, pepperoni, tocineta y orégano	5.00	https://placehold.co/300x200/343a40/FFFFFF?text=Pizza+Brutale	t	1
22	Pizza Brutale (Fam.)	Salsa, mozzarella, tomates en cuadrito, champiñones, jamón, pepperoni, tocineta y orégano	13.20	https://placehold.co/300x200/343a40/FFFFFF?text=Pizza+Brutale	t	2
23	Pizza Brutale (1/2 Q.)	Salsa, mozzarella, tomates en cuadrito, champiñones, jamón, pepperoni, tocineta y orégano	15.35	https://placehold.co/300x200/343a40/FFFFFF?text=Pizza+Brutale	t	3
24	Pizza Brutale (XL)	Salsa, mozzarella, tomates en cuadrito, champiñones, jamón, pepperoni, tocineta y orégano	33.00	https://placehold.co/300x200/343a40/FFFFFF?text=Pizza+Brutale	t	4
25	Pizza Vegetariana (Ind.)	Salsa, mozzarella, pimentón, cebolla, champiñones, maíz y orégano	3.40	https://placehold.co/300x200/343a40/FFFFFF?text=Pizza+Vegetariana	t	1
26	Pizza Vegetariana (Fam.)	Salsa, mozzarella, pimentón, cebolla, champiñones, maíz y orégano	10.30	https://placehold.co/300x200/343a40/FFFFFF?text=Pizza+Vegetariana	t	2
27	Pizza Vegetariana (1/2 Q.)	Salsa, mozzarella, pimentón, cebolla, champiñones, maíz y orégano	12.45	https://placehold.co/300x200/343a40/FFFFFF?text=Pizza+Vegetariana	t	3
28	Pizza Vegetariana (XL)	Salsa, mozzarella, pimentón, cebolla, champiñones, maíz y orégano	25.75	https://placehold.co/300x200/343a40/FFFFFF?text=Pizza+Vegetariana	t	4
29	Pizza Margarita (Ind.)	Salsa, mozzarella y orégano	2.20	https://placehold.co/300x200/343a40/FFFFFF?text=Pizza+Margarita	t	1
30	Pizza Margarita (Fam.)	Salsa, mozzarella y orégano	7.20	https://placehold.co/300x200/343a40/FFFFFF?text=Pizza+Margarita	t	2
31	Pizza Margarita (1/2 Q.)	Salsa, mozzarella y orégano	9.35	https://placehold.co/300x200/343a40/FFFFFF?text=Pizza+Margarita	t	3
32	Pizza Margarita (XL)	Salsa, mozzarella y orégano	16.70	https://placehold.co/300x200/343a40/FFFFFF?text=Pizza+Margarita	t	4
33	Pizza Tradicional (Ind.)	Salsa, mozzarella, jamón	2.55	https://placehold.co/300x200/343a40/FFFFFF?text=Pizza+Tradicional	t	1
34	Pizza Tradicional (Fam.)	Salsa, mozzarella, jamón	8.15	https://placehold.co/300x200/343a40/FFFFFF?text=Pizza+Tradicional	t	2
35	Pizza Tradicional (1/2 Q.)	Salsa, mozzarella, jamón	10.30	https://placehold.co/300x200/343a40/FFFFFF?text=Pizza+Tradicional	t	3
36	Pizza Tradicional (XL)	Salsa, mozzarella, jamón	19.60	https://placehold.co/300x200/343a40/FFFFFF?text=Pizza+Tradicional	t	4
37	Pizza Tocineta (Ind.)	Salsa, mozzarella, tocineta	2.95	https://placehold.co/300x200/343a40/FFFFFF?text=Pizza+Tocineta	t	1
38	Pizza Tocineta (Fam.)	Salsa, mozzarella, tocineta	8.80	https://placehold.co/300x200/343a40/FFFFFF?text=Pizza+Tocineta	t	2
39	Pizza Tocineta (1/2 Q.)	Salsa, mozzarella, tocineta	10.95	https://placehold.co/300x200/343a40/FFFFFF?text=Pizza+Tocineta	t	3
40	Pizza Tocineta (XL)	Salsa, mozzarella, tocineta	22.00	https://placehold.co/300x200/343a40/FFFFFF?text=Pizza+Tocineta	t	4
41	Pizza Champiñón (Ind.)	Salsa, mozzarella, champiñones y orégano	2.70	https://placehold.co/300x200/343a40/FFFFFF?text=Pizza+Champinon	t	1
42	Pizza Champiñón (Fam.)	Salsa, mozzarella, champiñones y orégano	8.20	https://placehold.co/300x200/343a40/FFFFFF?text=Pizza+Champinon	t	2
43	Pizza Champiñón (1/2 Q.)	Salsa, mozzarella, champiñones y orégano	10.35	https://placehold.co/300x200/343a40/FFFFFF?text=Pizza+Champinon	t	3
44	Pizza Champiñón (XL)	Salsa, mozzarella, champiñones y orégano	20.50	https://placehold.co/300x200/343a40/FFFFFF?text=Pizza+Champinon	t	4
45	Pizza Salami (Ind.)	Salsa, mozzarella, salami	3.70	https://placehold.co/300x200/343a40/FFFFFF?text=Pizza+Salami	t	1
46	Pizza Salami (Fam.)	Salsa, mozzarella, salami	9.40	https://placehold.co/300x200/343a40/FFFFFF?text=Pizza+Salami	t	2
47	Pizza Salami (1/2 Q.)	Salsa, mozzarella, salami	11.55	https://placehold.co/300x200/343a40/FFFFFF?text=Pizza+Salami	t	3
48	Pizza Salami (XL)	Salsa, mozzarella, salami	23.50	https://placehold.co/300x200/343a40/FFFFFF?text=Pizza+Salami	t	4
49	Pizza Napolitana (Ind.)	Salsa, mozzarella, anchoas y orégano	2.70	https://placehold.co/300x200/343a40/FFFFFF?text=Pizza+Napolitana	t	1
50	Pizza Napolitana (Fam.)	Salsa, mozzarella, anchoas y orégano	8.20	https://placehold.co/300x200/343a40/FFFFFF?text=Pizza+Napolitana	t	2
51	Pizza Napolitana (1/2 Q.)	Salsa, mozzarella, anchoas y orégano	10.35	https://placehold.co/300x200/343a40/FFFFFF?text=Pizza+Napolitana	t	3
52	Pizza Napolitana (XL)	Salsa, mozzarella, anchoas y orégano	20.50	https://placehold.co/300x200/343a40/FFFFFF?text=Pizza+Napolitana	t	4
53	Pizza Pepperoni (Ind.)	Salsa, mozzarella y pepperoni	2.80	https://placehold.co/300x200/343a40/FFFFFF?text=Pizza+Pepperoni	t	1
54	Pizza Pepperoni (Fam.)	Salsa, mozzarella y pepperoni	8.40	https://placehold.co/300x200/343a40/FFFFFF?text=Pizza+Pepperoni	t	2
55	Pizza Pepperoni (1/2 Q.)	Salsa, mozzarella y pepperoni	10.55	https://placehold.co/300x200/343a40/FFFFFF?text=Pizza+Pepperoni	t	3
56	Pizza Pepperoni (XL)	Salsa, mozzarella y pepperoni	21.00	https://placehold.co/300x200/343a40/FFFFFF?text=Pizza+Pepperoni	t	4
57	Pizza Hawaiana (Ind.)	Salsa, mozzarella, piña, jamón o tocineta	3.20	https://placehold.co/300x200/343a40/FFFFFF?text=Pizza+Hawaiana	t	1
58	Pizza Hawaiana (Fam.)	Salsa, mozzarella, piña, jamón o tocineta	9.30	https://placehold.co/300x200/343a40/FFFFFF?text=Pizza+Hawaiana	t	2
59	Pizza Hawaiana (1/2 Q.)	Salsa, mozzarella, piña, jamón o tocineta	11.50	https://placehold.co/300x200/343a40/FFFFFF?text=Pizza+Hawaiana	t	3
60	Pizza Hawaiana (XL)	Salsa, mozzarella, piña, jamón o tocineta	23.25	https://placehold.co/300x200/343a40/FFFFFF?text=Pizza+Hawaiana	t	4
61	Calzone	Salsa, mozzarella, jamón, tocineta, pimentón, cebolla y champiñones	5.00	https://placehold.co/300x200/343a40/FFFFFF?text=Calzone	t	5
62	Refresco de botella 0.35 lts	\N	1.20	\N	t	6
63	Refresco 1.5 lts	\N	3.70	\N	t	6
64	Refresco 2 lts	\N	4.25	\N	t	6
65	Nestea	\N	1.25	\N	t	6
66	Chukery	\N	1.25	\N	t	6
67	Agua mineral	\N	1.25	\N	t	6
68	Postre	\N	2.30	\N	t	6
69	Queso (Adicional Ind.)	\N	0.70	\N	t	7
70	Vegetales (Adicional Ind.)	\N	0.70	\N	t	7
71	Maíz (Adicional Ind.)	\N	0.70	\N	t	7
72	Champiñones (Adicional Ind.)	\N	0.70	\N	t	7
73	Piña (Adicional Ind.)	\N	0.70	\N	t	7
74	Cebolla caramelizada (Adicional Ind.)	\N	0.70	\N	t	7
75	Aceitunas negras (Adicional Ind.)	\N	0.70	\N	t	7
76	Anchoas (Adicional Ind.)	\N	0.70	\N	t	7
77	Jamón (Adicional Ind.)	\N	1.00	\N	t	7
78	Tocineta (Adicional Ind.)	\N	1.00	\N	t	7
79	Pepperoni (Adicional Ind.)	\N	1.00	\N	t	7
80	Salami (Adicional Ind.)	\N	1.00	\N	t	7
81	Pecorino (Adicional Ind.)	\N	0.60	\N	t	7
82	Salsa (Adicional Ind.)	\N	0.60	\N	t	7
83	Queso (Adicional Fam.)	\N	3.00	\N	t	7
84	Vegetales (Adicional Fam.)	\N	3.00	\N	t	7
85	Maíz (Adicional Fam.)	\N	3.00	\N	t	7
86	Champiñones (Adicional Fam.)	\N	3.00	\N	t	7
87	Piña (Adicional Fam.)	\N	3.00	\N	t	7
88	Cebolla caramelizada (Adicional Fam.)	\N	3.00	\N	t	7
89	Aceitunas negras (Adicional Fam.)	\N	3.00	\N	t	7
90	Anchoas (Adicional Fam.)	\N	3.00	\N	t	7
91	Jamón (Adicional Fam.)	\N	5.00	\N	t	7
92	Tocineta (Adicional Fam.)	\N	5.00	\N	t	7
93	Pepperoni (Adicional Fam.)	\N	5.00	\N	t	7
94	Salami (Adicional Fam.)	\N	5.00	\N	t	7
95	Pecorino (Adicional Fam.)	\N	3.00	\N	t	7
96	Salsa (Adicional Fam.)	\N	3.00	\N	t	7
97	Queso (Adicional XL)	\N	7.50	\N	t	7
98	Vegetales (Adicional XL)	\N	7.50	\N	t	7
99	Maíz (Adicional XL)	\N	7.50	\N	t	7
100	Champiñones (Adicional XL)	\N	7.50	\N	t	7
101	Piña (Adicional XL)	\N	7.50	\N	t	7
102	Cebolla caramelizada (Adicional XL)	\N	7.50	\N	t	7
103	Aceitunas negras (Adicional XL)	\N	7.50	\N	t	7
104	Anchoas (Adicional XL)	\N	7.50	\N	t	7
105	Jamón (Adicional XL)	\N	10.00	\N	t	7
106	Tocineta (Adicional XL)	\N	10.00	\N	t	7
107	Pepperoni (Adicional XL)	\N	10.00	\N	t	7
108	Salami (Adicional XL)	\N	10.00	\N	t	7
109	Pecorino (Adicional XL)	\N	7.50	\N	t	7
110	Salsa (Adicional XL)	\N	7.50	\N	t	7
111	Caja familiar	\N	1.40	\N	t	8
112	Caja individual	\N	0.80	\N	t	8
113	Platos de anime	\N	0.20	\N	t	8
\.


--
-- Restablecer las secuencias de IDs para futuras inserciones automáticas.
-- Asegúrate de que el valor sea el ID más alto existente en la tabla después de tu COPY.
--
SELECT pg_catalog.setval('public.categorias_menu_id_seq', 8, true);
SELECT pg_catalog.setval('public.items_menu_id_seq', 113, true);

--
-- Reactivar triggers y restricciones de clave foránea
--
ALTER TABLE public.items_menu ENABLE TRIGGER ALL;
ALTER TABLE public.detalles_pedido ENABLE TRIGGER ALL; -- Reactivar si se deshabilitó
ALTER TABLE public.registros_financieros ENABLE TRIGGER ALL; -- Reactivar si se deshabilitó


-- Desactivar temporalmente los triggers y restricciones de clave foránea
-- para permitir TRUNCATE de tablas con dependencias.
-- (Este bloque ya no es necesario aquí si se maneja al principio y no hay otras tablas a truncar)

--
-- Comandos de CREATE/ALTER de la estructura original (eliminados de este script de inserción)
--
-- Los siguientes comandos han sido removidos ya que asumen que la base de datos
-- se está creando desde cero, lo que causaba los errores de "ya existe".
--
-- Name: administradores; Type: TABLE; ...
-- Name: administradores_id_seq; Type: SEQUENCE; ...
-- Name: categorias_menu; Type: TABLE; ...
-- Name: categorias_menu_id_seq; Type: SEQUENCE; ...
-- Name: clientes; Type: TABLE; ...
-- Name: clientes_id_seq; Type: SEQUENCE; ...
-- Name: detalles_pedido; Type: TABLE; ...
-- Name: detalles_pedido_id_seq; Type: SEQUENCE; ...
-- Name: informacion_pizzeria; Type: TABLE; ...
-- Name: informacion_pizzeria_id_seq; Type: SEQUENCE; ...
-- Name: items_menu; Type: TABLE; ...
-- Name: items_menu_id_seq; Type: SEQUENCE; ...
-- Name: pedidos; Type: TABLE; ...
-- Name: pedidos_id_seq; Type: SEQUENCE; ...
-- Name: registros_financieros; Type: TABLE; ...
-- Name: registros_financieros_id_seq; Type: SEQUENCE; ...
-- DEFAULTs para columnas ID (removidos)
-- CONSTRAINTs (removidos)
-- Foreign-key constraints (removidos)
-- ACL (removido)

-- Los comandos de COPY para administradores, clientes, pedidos, informacion_pizzeria,
-- y registros_financieros también se han eliminado ya que este script se centra
-- en el menú y esos datos no deberían ser sobrescritos en una actualización de menú.
-- Si necesitas actualizarlos, considera scripts específicos para esos datos.


-- PostgreSQL database dump complete
--

