-- backup.sql - Script para crear las tablas de la base de datos de la pizzería en PostgreSQL

-- Eliminar tablas si ya existen (útil para recrear el esquema)
DROP TABLE IF EXISTS registros_financieros CASCADE;
DROP TABLE IF EXISTS detalles_pedido CASCADE;
DROP TABLE IF EXISTS pedidos CASCADE;
DROP TABLE IF EXISTS items_menu CASCADE;
DROP TABLE IF EXISTS categorias_menu CASCADE;
DROP TABLE IF EXISTS clientes CASCADE;
DROP TABLE IF EXISTS informacion_pizzeria CASCADE;
DROP TABLE IF EXISTS administradores CASCADE;


-- Tabla: administradores
-- Almacena la información de los usuarios administradores.
CREATE TABLE administradores (
    id SERIAL PRIMARY KEY,
    usuario VARCHAR(50) NOT NULL UNIQUE,
    contrasena_hash VARCHAR(255) NOT NULL,
    email VARCHAR(120) UNIQUE,
    super_admin BOOLEAN DEFAULT FALSE
);

-- Tabla: categorias_menu
-- Almacena las categorías de los ítems del menú (ej: Pizzas, Bebidas, Postres).
CREATE TABLE categorias_menu (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL UNIQUE,
    descripcion TEXT
);

-- Tabla: clientes
-- Almacena la información de los clientes de la pizzería.
CREATE TABLE clientes (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE,
    telefono VARCHAR(20),
    direccion TEXT NOT NULL,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla: informacion_pizzeria
-- Almacena la información general de la pizzería (dirección, contacto, etc.).
-- Se espera que solo haya una fila en esta tabla.
CREATE TABLE informacion_pizzeria (
    id SERIAL PRIMARY KEY,
    nombre_pizzeria VARCHAR(100) NOT NULL,
    direccion TEXT NOT NULL,
    telefono VARCHAR(20) NOT NULL,
    email_contacto VARCHAR(120),
    horario_atencion TEXT,
    red_social_facebook VARCHAR(255),
    red_social_instagram VARCHAR(255)
);

-- Tabla: items_menu
-- Almacena los ítems individuales que se ofrecen en el menú de la pizzería.
CREATE TABLE items_menu (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    precio REAL NOT NULL, -- Usamos REAL para números con decimales, como precios.
    imagen_url VARCHAR(255),
    disponible BOOLEAN DEFAULT TRUE,
    categoria_id INTEGER NOT NULL,
    FOREIGN KEY (categoria_id) REFERENCES categorias_menu(id)
);

-- Tabla: pedidos
-- Almacena los pedidos realizados por los clientes.
CREATE TABLE pedidos (
    id SERIAL PRIMARY KEY,
    cliente_id INTEGER NOT NULL,
    fecha_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total REAL NOT NULL, -- Total del pedido.
    estado VARCHAR(50) NOT NULL DEFAULT 'Pendiente', -- Ej: 'Pendiente', 'En preparación', 'En camino', 'Entregado', 'Cancelado'
    direccion_delivery TEXT NOT NULL,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id)
);

-- Tabla: detalles_pedido
-- Almacena los ítems específicos incluidos en cada pedido (relación muchos a muchos).
CREATE TABLE detalles_pedido (
    id SERIAL PRIMARY KEY,
    pedido_id INTEGER NOT NULL,
    item_menu_id INTEGER NOT NULL,
    cantidad INTEGER NOT NULL,
    precio_unitario REAL NOT NULL, -- Precio del ítem en el momento de la compra para historial.
    FOREIGN KEY (pedido_id) REFERENCES pedidos(id),
    FOREIGN KEY (item_menu_id) REFERENCES items_menu(id)
);

-- Tabla: registros_financieros
-- Almacena los ingresos y gastos de la pizzería.
CREATE TABLE registros_financieros (
    id SERIAL PRIMARY KEY,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    monto REAL NOT NULL,
    tipo VARCHAR(20) NOT NULL, -- Ej: 'Ingreso', 'Gasto'
    descripcion TEXT,
    pedido_id INTEGER, -- Clave foránea opcional a pedidos (si el registro es por un pedido)
    FOREIGN KEY (pedido_id) REFERENCES pedidos(id)
);
