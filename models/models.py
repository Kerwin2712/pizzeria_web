# Importa los módulos necesarios de SQLAlchemy
from sqlalchemy import create_engine, Column, Integer, String, Text, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

# Define la base declarativa para tus modelos.
# Todos tus modelos de base de datos heredarán de esta clase.
Base = declarative_base()

# --- Modelos de la Aplicación ---

class Cliente(Base):
    """
    Modelo para almacenar la información de los clientes.
    """
    __tablename__ = 'clientes' # Nombre de la tabla en la base de datos

    id = Column(Integer, primary_key=True, autoincrement=True) # Identificador único del cliente
    nombre = Column(String(100), nullable=False) # Nombre completo del cliente
    email = Column(String(120), unique=True, nullable=False) # Correo electrónico, debe ser único
    telefono = Column(String(20), nullable=True) # Número de teléfono del cliente
    direccion = Column(Text, nullable=False) # Dirección completa para el delivery
    fecha_registro = Column(DateTime, default=datetime.now) # Fecha y hora de registro del cliente

    # Relación uno a muchos con Pedido (un cliente puede tener muchos pedidos)
    pedidos = relationship("Pedido", back_populates="cliente")

    def __repr__(self):
        return f"<Cliente(id={self.id}, nombre='{self.nombre}', email='{self.email}')>"

class CategoriaMenu(Base):
    """
    Modelo para categorizar los ítems del menú (ej: Pizzas, Bebidas, Postres).
    Esto permite una mejor organización del menú.
    """
    __tablename__ = 'categorias_menu'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(50), unique=True, nullable=False) # Nombre de la categoría (ej: "Pizzas Clásicas")
    descripcion = Column(Text, nullable=True) # Descripción opcional de la categoría

    # Relación uno a muchos con ItemMenu
    items_menu = relationship("ItemMenu", back_populates="categoria")

    def __repr__(self):
        return f"<CategoriaMenu(id={self.id}, nombre='{self.nombre}')>"

class ItemMenu(Base):
    """
    Modelo para los ítems individuales del menú (pizzas, bebidas, etc.).
    """
    __tablename__ = 'items_menu'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False) # Nombre del ítem (ej: "Pizza Pepperoni")
    descripcion = Column(Text, nullable=True) # Descripción del ítem
    precio = Column(Float, nullable=False) # Precio del ítem
    imagen_url = Column(String(255), nullable=True) # URL de la imagen del ítem (opcional)
    disponible = Column(Boolean, default=True) # Indica si el ítem está disponible actualmente

    # Clave foránea para la categoría a la que pertenece este ítem
    categoria_id = Column(Integer, ForeignKey('categorias_menu.id'), nullable=False)
    categoria = relationship("CategoriaMenu", back_populates="items_menu")

    def __repr__(self):
        return f"<ItemMenu(id={self.id}, nombre='{self.nombre}', precio={self.precio})>"

class Pedido(Base):
    """
    Modelo para almacenar los pedidos realizados por los clientes.
    """
    __tablename__ = 'pedidos'

    id = Column(Integer, primary_key=True, autoincrement=True)
    # Clave foránea al cliente que realizó el pedido
    cliente_id = Column(Integer, ForeignKey('clientes.id'), nullable=False)
    fecha_hora = Column(DateTime, default=datetime.now) # Fecha y hora en que se realizó el pedido
    total = Column(Float, nullable=False) # Precio total del pedido
    estado = Column(String(50), default="Pendiente", nullable=False) # Estado del pedido (ej: "Pendiente", "En preparación", "En camino", "Entregado", "Cancelado")
    direccion_delivery = Column(Text, nullable=False) # Dirección final de entrega para este pedido

    # Relación muchos a uno con Cliente
    cliente = relationship("Cliente", back_populates="pedidos")
    # Relación uno a muchos con DetallePedido
    detalles = relationship("DetallePedido", back_populates="pedido")
    # Relación uno a uno con RegistroFinanciero (un pedido puede tener un registro de ingreso)
    registro_financiero = relationship("RegistroFinanciero", back_populates="pedido", uselist=False)


    def __repr__(self):
        return f"<Pedido(id={self.id}, cliente_id={self.cliente_id}, total={self.total}, estado='{self.estado}')>"

class DetallePedido(Base):
    """
    Modelo para almacenar los ítems específicos incluidos en cada pedido.
    Una tabla intermedia para la relación muchos a muchos entre Pedido e ItemMenu.
    """
    __tablename__ = 'detalles_pedido'

    id = Column(Integer, primary_key=True, autoincrement=True)
    # Clave foránea al pedido al que pertenece este detalle
    pedido_id = Column(Integer, ForeignKey('pedidos.id'), nullable=False)
    # Clave foránea al ítem del menú que se incluyó en el pedido
    item_menu_id = Column(Integer, ForeignKey('items_menu.id'), nullable=False)
    cantidad = Column(Integer, nullable=False) # Cantidad de este ítem en el pedido
    precio_unitario = Column(Float, nullable=False) # Precio unitario del ítem al momento de la compra (para historial)

    # Relación muchos a uno con Pedido
    pedido = relationship("Pedido", back_populates="detalles")
    # Relación muchos a uno con ItemMenu
    item_menu = relationship("ItemMenu")

    def __repr__(self):
        return f"<DetallePedido(id={self.id}, pedido_id={self.pedido_id}, item_menu_id={self.item_menu_id}, cantidad={self.cantidad})>"

class InformacionPizzeria(Base):
    """
    Modelo para almacenar la información general de la pizzería que se mostrará en la web.
    Solo debería haber una fila en esta tabla.
    """
    __tablename__ = 'informacion_pizzeria'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre_pizzeria = Column(String(100), nullable=False)
    direccion = Column(Text, nullable=False)
    telefono = Column(String(20), nullable=False)
    email_contacto = Column(String(120), nullable=True)
    horario_atencion = Column(Text, nullable=True) # Ej: "Lunes a Viernes: 10 AM - 10 PM"
    red_social_facebook = Column(String(255), nullable=True) # URL de Facebook
    red_social_instagram = Column(String(255), nullable=True) # URL de Instagram
    # Puedes añadir más campos para otra información relevante (descripción, etc.)

    def __repr__(self):
        return f"<InformacionPizzeria(id={self.id}, nombre='{self.nombre_pizzeria}')>"

class Administrador(Base):
    """
    Modelo para los usuarios administradores que gestionarán la página.
    La contraseña se almacenará como un hash (se debe implementar hashing en la lógica de la aplicación).
    """
    __tablename__ = 'administradores'

    id = Column(Integer, primary_key=True, autoincrement=True)
    usuario = Column(String(50), unique=True, nullable=False) # Nombre de usuario del administrador
    contrasena_hash = Column(String(255), nullable=False) # Contraseña encriptada (hash)
    email = Column(String(120), unique=True, nullable=True) # Correo electrónico del administrador
    super_admin = Column(Boolean, default=False) # Indica si es un super administrador con todos los permisos

    def __repr__(self):
        return f"<Administrador(id={self.id}, usuario='{self.usuario}')>"

class RegistroFinanciero(Base):
    """
    Modelo para registrar ingresos y gastos de la pizzería.
    """
    __tablename__ = 'registros_financieros'

    id = Column(Integer, primary_key=True, autoincrement=True)
    fecha = Column(DateTime, default=datetime.now, nullable=False) # Fecha y hora del registro
    monto = Column(Float, nullable=False) # Monto de la transacción
    tipo = Column(String(20), nullable=False) # Tipo de transacción (ej: 'Ingreso', 'Gasto')
    descripcion = Column(Text, nullable=True) # Descripción del registro financiero
    # Clave foránea opcional a Pedido (si este ingreso proviene de un pedido)
    pedido_id = Column(Integer, ForeignKey('pedidos.id'), nullable=True)

    # Relación muchos a uno con Pedido (un registro financiero puede estar vinculado a un pedido)
    pedido = relationship("Pedido", back_populates="registro_financiero")

    def __repr__(self):
        return f"<RegistroFinanciero(id={self.id}, fecha='{self.fecha}', tipo='{self.tipo}', monto={self.monto})>"

# --- Configuración de la Base de Datos ---

# Función para configurar la conexión a la base de datos
def setup_database(db_url):
    """
    Configura la conexión a la base de datos y crea todas las tablas si no existen.
    :param db_url: URL de conexión a la base de datos (ej: "postgresql://user:password@host:port/dbname")
    """
    engine = create_engine(db_url)
    Base.metadata.create_all(engine) # Crea todas las tablas definidas en los modelos
    Session = sessionmaker(bind=engine)
    return Session, engine

# Ejemplo de uso (esto no se ejecutará si solo importas el archivo)
# if __name__ == "__main__":
#     # Reemplaza con tus credenciales de PostgreSQL
#     DATABASE_URL = "postgresql://tu_usuario:tu_contrasena@localhost:5432/tu_base_de_datos"
#     Session, engine = setup_database(DATABASE_URL)
#     print("Tablas de la base de datos creadas o verificadas.")
