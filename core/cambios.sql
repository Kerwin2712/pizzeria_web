-- cambios.sql - Script para añadir campos de pago y WhatsApp a la información de la pizzería y pedidos

-- Añadir columnas para los datos de Pago Móvil en la tabla informacion_pizzeria
ALTER TABLE informacion_pizzeria
ADD COLUMN pago_movil_banco VARCHAR(100),
ADD COLUMN pago_movil_telefono VARCHAR(20),
ADD COLUMN pago_movil_cedula VARCHAR(20),
ADD COLUMN pago_movil_cuenta VARCHAR(50),
ADD COLUMN pago_movil_beneficiario VARCHAR(100);

-- Añadir columnas para el número de WhatsApp y el link del chat en la tabla informacion_pizzeria
ALTER TABLE informacion_pizzeria
ADD COLUMN whatsapp_numero VARCHAR(20),
ADD COLUMN whatsapp_chat_link TEXT;

-- Añadir columna para el método de pago en la tabla pedidos
ALTER TABLE pedidos
ADD COLUMN metodo_pago VARCHAR(50);
