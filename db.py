"""Funciones de acceso a MySQL.

Separar la base de datos de la interfaz hace que el proyecto sea más fácil
de explicar: app.py se preocupa de la pantalla y este archivo del SQL.
"""

import os

import mysql.connector
from dotenv import load_dotenv


# Carga las variables de conexión escritas en el archivo .env.
load_dotenv()


def conectar():
    """Abre y devuelve una conexión a la base de datos MySQL."""
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "reservas_laboratorio"),
    )


def consultar(sql, parametros=()):
    """Ejecuta un SELECT y entrega una lista de diccionarios."""
    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)
    try:
        cursor.execute(sql, parametros)
        return cursor.fetchall()
    finally:
        cursor.close()
        conexion.close()


def obtener_alumnos():
    """Obtiene los alumnos que aparecerán en el selector."""
    return consultar("SELECT id, nombre, curso FROM alumnos ORDER BY nombre")


def obtener_computadores():
    """Solo muestra computadores disponibles para realizar reservas."""
    return consultar(
        "SELECT id, codigo FROM computadores "
        "WHERE estado = 'DISPONIBLE' ORDER BY codigo"
    )


def obtener_bloques():
    """Obtiene los bloques y convierte las horas a texto."""
    return consultar(
        "SELECT id, nombre, "
        "TIME_FORMAT(hora_inicio, '%H:%i') AS inicio, "
        "TIME_FORMAT(hora_fin, '%H:%i') AS fin "
        "FROM bloques ORDER BY hora_inicio"
    )


def obtener_reservas():
    """Consulta que une las tablas para mostrar información entendible."""
    return consultar(
        """
        SELECT r.id, r.alumno_id, r.computador_id, r.bloque_id,
               r.fecha, a.nombre AS alumno, a.curso,
               c.codigo AS computador, b.nombre AS bloque
        FROM reservas r
        INNER JOIN alumnos a ON a.id = r.alumno_id
        INNER JOIN computadores c ON c.id = r.computador_id
        INNER JOIN bloques b ON b.id = r.bloque_id
        WHERE r.estado = 'ACTIVA'
        ORDER BY r.fecha, b.hora_inicio
        """
    )


def realizar_reserva(alumno_id, computador_id, bloque_id, fecha):
    """Llama al procedimiento que valida y registra una reserva."""
    conexion = conectar()
    cursor = conexion.cursor()
    try:
        # CALL permite ejecutar la lógica almacenada dentro de MySQL.
        cursor.execute(
            "CALL realizar_reserva(%s, %s, %s, %s)",
            (alumno_id, computador_id, bloque_id, fecha),
        )
        conexion.commit()
    except Exception:
        # Si ocurre un error, se deshacen los cambios incompletos.
        conexion.rollback()
        raise
    finally:
        cursor.close()
        conexion.close()


def actualizar_reserva(reserva_id, alumno_id, computador_id, bloque_id, fecha):
    """Actualiza una reserva usando SQL directo (sin procedimiento)."""
    conexion = conectar()
    cursor = conexion.cursor()
    try:
        # Se comprueba que otro registro no tenga el mismo equipo, fecha y bloque.
        cursor.execute(
            """
            SELECT COUNT(*)
            FROM reservas
            WHERE computador_id = %s
              AND bloque_id = %s
              AND fecha = %s
              AND estado = 'ACTIVA'
              AND id <> %s
            """,
            (computador_id, bloque_id, fecha, reserva_id),
        )
        cantidad = cursor.fetchone()[0]

        if cantidad > 0:
            raise ValueError("El computador ya está reservado en ese bloque")

        cursor.execute(
            """
            UPDATE reservas
            SET alumno_id = %s,
                computador_id = %s,
                bloque_id = %s,
                fecha = %s
            WHERE id = %s
            """,
            (alumno_id, computador_id, bloque_id, fecha, reserva_id),
        )
        conexion.commit()
    except Exception:
        conexion.rollback()
        raise
    finally:
        cursor.close()
        conexion.close()


def eliminar_reserva(reserva_id):
    """Elimina definitivamente una reserva usando SQL directo."""
    conexion = conectar()
    cursor = conexion.cursor()
    try:
        cursor.execute("DELETE FROM reservas WHERE id = %s", (reserva_id,))
        conexion.commit()
    except Exception:
        conexion.rollback()
        raise
    finally:
        cursor.close()
        conexion.close()
