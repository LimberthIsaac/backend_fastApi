from sqlalchemy import Column, Integer, String, Float, Time, Boolean, DECIMAL, Text, ForeignKey, TIMESTAMP, func
from sqlalchemy.orm import relationship
from database import Base

class Cliente(Base):
    __tablename__ = "clientes"

    id_cliente = Column(Integer, primary_key=True, index=True)
    nombres = Column(String(100), nullable=False)
    apellidos = Column(String(100), nullable=False)
    telefono = Column(String(20), nullable=False)
    correo = Column(String(100), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    reset_token = Column(String(255), nullable=True)
    token_expiry = Column(TIMESTAMP, nullable=True)
    fecha_registro = Column(TIMESTAMP, server_default=func.now())
    estado_cuenta = Column(String(20), default='Activo')
    calificacion_promedio = Column(DECIMAL(3, 2), default=5.00)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    vehiculos = relationship("Vehiculo", back_populates="cliente", cascade="all, delete-orphan")
    incidentes = relationship("Incidente", back_populates="cliente")


class Taller(Base):
    __tablename__ = "talleres"

    id_taller = Column(Integer, primary_key=True, index=True)
    razon_social = Column(String(150), nullable=False)
    nit = Column(String(30), unique=True, nullable=False)
    ubicacion_base_latitud = Column(Float, nullable=False)
    ubicacion_base_longitud = Column(Float, nullable=False)
    horario_apertura = Column(Time, nullable=False)
    horario_cierre = Column(Time, nullable=False)
    cuenta_bancaria = Column(String(50), nullable=True)
    calificacion_promedio = Column(DECIMAL(3, 2), default=5.00)
    estado_aprobacion = Column(String(20), default='Pendiente')
    correo = Column(String(100), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    reset_token = Column(String(255), nullable=True)
    token_expiry = Column(TIMESTAMP, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    tecnicos = relationship("Tecnico", back_populates="taller", cascade="all, delete-orphan")
    taller_servicios = relationship("TallerServicio", back_populates="taller", cascade="all, delete-orphan")
    asistencias = relationship("Asistencia", back_populates="taller")


class Servicio(Base):
    __tablename__ = "servicios"

    id_servicio = Column(Integer, primary_key=True, index=True)
    nombre_servicio = Column(String(100), nullable=False)
    descripcion = Column(Text, nullable=True)
    tarifa_base_estimada = Column(DECIMAL(10, 2), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    taller_servicios = relationship("TallerServicio", back_populates="servicio", cascade="all, delete-orphan")


class Vehiculo(Base):
    __tablename__ = "vehiculos"

    id_vehiculo = Column(Integer, primary_key=True, index=True)
    id_cliente = Column(Integer, ForeignKey('clientes.id_cliente', ondelete='CASCADE'), nullable=False)
    placa = Column(String(15), unique=True, nullable=False)
    marca = Column(String(50), nullable=False)
    modelo = Column(String(50), nullable=False)
    año = Column(Integer, nullable=False)
    color = Column(String(30), nullable=False)
    tipo_transmision = Column(String(20), nullable=False)
    tipo_combustible = Column(String(20), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    cliente = relationship("Cliente", back_populates="vehiculos")
    incidentes = relationship("Incidente", back_populates="vehiculo")


class Tecnico(Base):
    __tablename__ = "tecnicos"

    id_tecnico = Column(Integer, primary_key=True, index=True)
    id_taller = Column(Integer, ForeignKey('talleres.id_taller', ondelete='CASCADE'), nullable=False)
    nombres = Column(String(100), nullable=False)
    apellidos = Column(String(100), nullable=False)
    telefono_contacto = Column(String(20), nullable=False)
    especialidad = Column(String(50), nullable=True)
    en_turno = Column(Boolean, default=False)
    ubicacion_actual_latitud = Column(Float, nullable=True)
    ubicacion_actual_longitud = Column(Float, nullable=True)
    estado_operativo = Column(String(20), default='Disponible')
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    taller = relationship("Taller", back_populates="tecnicos")
    asistencias = relationship("Asistencia", back_populates="tecnico")


class TallerServicio(Base):
    __tablename__ = "taller_servicios"

    id_taller_servicio = Column(Integer, primary_key=True, index=True)
    id_taller = Column(Integer, ForeignKey('talleres.id_taller', ondelete='CASCADE'), nullable=False)
    id_servicio = Column(Integer, ForeignKey('servicios.id_servicio', ondelete='CASCADE'), nullable=False)
    precio_especifico_taller = Column(DECIMAL(10, 2), nullable=False)
    tiempo_estimado_minutos = Column(Integer, nullable=True)
    estado_disponible = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    taller = relationship("Taller", back_populates="taller_servicios")
    servicio = relationship("Servicio", back_populates="taller_servicios")


class Incidente(Base):
    __tablename__ = "incidentes"

    id_incidente = Column(Integer, primary_key=True, index=True)
    id_cliente = Column(Integer, ForeignKey('clientes.id_cliente'), nullable=False)
    id_vehiculo = Column(Integer, ForeignKey('vehiculos.id_vehiculo'), nullable=False)
    fecha_hora_reporte = Column(TIMESTAMP, server_default=func.now())
    ubicacion_latitud = Column(Float, nullable=False)
    ubicacion_longitud = Column(Float, nullable=False)
    tipo_problema = Column(String(50), nullable=False)
    descripcion_manual = Column(Text, nullable=True)
    nivel_prioridad = Column(String(15), nullable=True)
    estado_solicitud = Column(String(20), default='Pendiente')
    distancia_km_calculada = Column(DECIMAL(5, 2), nullable=True)
    motivo_cancelacion = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    cliente = relationship("Cliente", back_populates="incidentes")
    vehiculo = relationship("Vehiculo", back_populates="incidentes")
    evidencias = relationship("Evidencia", back_populates="incidente", cascade="all, delete-orphan")
    analisis_ia = relationship("AnalisisIA", back_populates="incidente", uselist=False, cascade="all, delete-orphan")
    asistencia = relationship("Asistencia", back_populates="incidente", uselist=False)


class Evidencia(Base):
    __tablename__ = "evidencias"

    id_evidencia = Column(Integer, primary_key=True, index=True)
    id_incidente = Column(Integer, ForeignKey('incidentes.id_incidente', ondelete='CASCADE'), nullable=False)
    tipo_recurso = Column(String(20), nullable=False)
    url_archivo = Column(String(255), nullable=False)
    fecha_subida = Column(TIMESTAMP, server_default=func.now())
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    incidente = relationship("Incidente", back_populates="evidencias")


class AnalisisIA(Base):
    __tablename__ = "analisis_ia"

    id_analisis = Column(Integer, primary_key=True, index=True)
    id_incidente = Column(Integer, ForeignKey('incidentes.id_incidente', ondelete='CASCADE'), nullable=False, unique=True)
    transcripcion_audio = Column(Text, nullable=True)
    clasificacion_sugerida = Column(String(50), nullable=True)
    resumen_estructurado = Column(Text, nullable=True)
    nivel_confianza_porcentaje = Column(Integer, nullable=True)
    requiere_revision_manual = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    incidente = relationship("Incidente", back_populates="analisis_ia")


class Asistencia(Base):
    __tablename__ = "asistencias"

    id_asistencia = Column(Integer, primary_key=True, index=True)
    id_incidente = Column(Integer, ForeignKey('incidentes.id_incidente'), nullable=False, unique=True)
    id_taller = Column(Integer, ForeignKey('talleres.id_taller'), nullable=False)
    id_tecnico = Column(Integer, ForeignKey('tecnicos.id_tecnico'), nullable=False)
    fecha_hora_asignacion = Column(TIMESTAMP, server_default=func.now())
    fecha_hora_llegada_tecnico = Column(TIMESTAMP, nullable=True)
    fecha_hora_finalizacion = Column(TIMESTAMP, nullable=True)
    observaciones_tecnico = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    incidente = relationship("Incidente", back_populates="asistencia")
    taller = relationship("Taller", back_populates="asistencias")
    tecnico = relationship("Tecnico", back_populates="asistencias")
    pago = relationship("Pago", back_populates="asistencia", uselist=False)


class Pago(Base):
    __tablename__ = "pagos"

    id_pago = Column(Integer, primary_key=True, index=True)
    id_asistencia = Column(Integer, ForeignKey('asistencias.id_asistencia'), nullable=False, unique=True)
    monto_subtotal = Column(DECIMAL(10, 2), nullable=False)
    monto_comision_plataforma = Column(DECIMAL(10, 2), nullable=False)
    monto_total_cliente = Column(DECIMAL(10, 2), nullable=False)
    metodo_pago = Column(String(30), nullable=False)
    estado_transaccion = Column(String(20), default='Pendiente')
    fecha_pago = Column(TIMESTAMP, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    asistencia = relationship("Asistencia", back_populates="pago")
