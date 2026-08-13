# Sistema de Reserva de Computadores

Aplicación CRUD desarrollada con **Python**, **Flet** y **MySQL** para administrar
las reservas de computadores de un laboratorio escolar.

Este proyecto fue creado para el módulo de **Administración de Bases de Datos**
de 4° Medio de la especialidad de Programación.

## Objetivo

El sistema evita que un mismo computador sea reservado por dos estudiantes en
la misma fecha y bloque horario. Además, permite consultar, modificar y eliminar
las reservas registradas.

## Funciones principales

- Agregar una reserva.
- Mostrar las reservas activas.
- Actualizar los datos de una reserva.
- Eliminar una reserva.
- Seleccionar la fecha desde un calendario.
- Impedir reservas duplicadas mediante un procedimiento almacenado.
- Adaptar la interfaz al tamaño de la ventana.

## Operaciones CRUD

| Operación | Acción | Implementación |
|---|---|---|
| Create | Agregar una reserva | Procedimiento `realizar_reserva` |
| Read | Mostrar reservas | Consulta `SELECT` con `INNER JOIN` |
| Update | Modificar una reserva | Sentencia `UPDATE` desde Python |
| Delete | Eliminar una reserva | Sentencia `DELETE` desde Python |

El proyecto utiliza **un solo procedimiento almacenado**, empleado al agregar
una reserva para comprobar que el computador esté disponible.

## Tecnologías utilizadas

- Python 3.11 o superior.
- Flet para la interfaz gráfica.
- MySQL 8 para almacenar y administrar los datos.
- DBeaver para ejecutar el script SQL y revisar la base de datos.
- MySQL Connector/Python para conectar Python con MySQL.
- python-dotenv para leer la configuración local.

## Estructura del proyecto

```text
proyecto_reservas_flet/
├── app.py
├── db.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── GUION_PRESENTACION.md
└── sql/
    └── base_datos.sql
```

### Archivos principales

- `app.py`: contiene la interfaz y los eventos de Flet.
- `db.py`: contiene la conexión y las operaciones con MySQL.
- `sql/base_datos.sql`: crea las tablas, datos iniciales y procedimiento.
- `.env.example`: muestra las variables necesarias para la conexión.
- `requirements.txt`: contiene las dependencias de Python.

## Requisitos previos

Antes de instalar el proyecto se necesita:

1. Python 3.11 o superior.
2. MySQL Server 8 o superior.
3. DBeaver.
4. GitHub Desktop, solamente si se desea publicar o actualizar el repositorio.

## Instalación en Windows

### 1. Descargar el proyecto

Desde GitHub se puede utilizar **Code → Download ZIP** y descomprimir el archivo.

También se puede clonar mediante GitHub Desktop:

1. Abrir GitHub Desktop.
2. Seleccionar **File → Clone repository**.
3. Elegir el repositorio.
4. Presionar **Clone**.

### 2. Abrir PowerShell en la carpeta

Ejemplo:

```powershell
cd "C:\Users\nombreususario_\Desktop\proyecto_reservas_flet"
```

### 3. Crear el entorno virtual

```powershell
python -m venv .venv
```

### 4. Activar el entorno virtual

```powershell
.\.venv\Scripts\Activate.ps1
```

Si PowerShell bloquea la activación:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

### 5. Instalar las dependencias

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Configuración de MySQL

### 1. Crear la base de datos

1. Abrir DBeaver.
2. Conectarse a MySQL.
3. Abrir `sql/base_datos.sql`.
4. Ejecutar el archivo completo.
5. Actualizar la conexión.
6. Comprobar que aparezca `reservas_laboratorio`.

El script crea las tablas:

- `alumnos`
- `computadores`
- `bloques`
- `reservas`

También crea el procedimiento almacenado `realizar_reserva`.

### 2. Configurar las credenciales

Crear una copia del archivo `.env.example`:

```powershell
Copy-Item .env.example .env
```

Abrirlo:

```powershell
notepad .env
```

Completar la configuración:

```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=CLAVE_DE_MYSQL
DB_NAME=reservas_laboratorio
```

Se debe reemplazar `CLAVE_DE_MYSQL` por la contraseña real.

> **Importante:** el archivo `.env` contiene información privada y no debe
> subirse a GitHub.

## Ejecutar la aplicación

Con el entorno virtual activado:

```powershell
python app.py
```

Para detenerla desde la terminal:

```text
Ctrl + C
```

## Demostración del proyecto

Para comprobar el funcionamiento:

1. Seleccionar un alumno.
2. Seleccionar un computador.
3. Seleccionar un bloque.
4. Elegir la fecha desde el calendario.
5. Presionar **Agregar reserva**.
6. Editar la reserva con el botón del lápiz.
7. Eliminarla con el botón rojo.
8. Intentar registrar dos veces el mismo computador, fecha y bloque.

La segunda reserva debe ser rechazada con el mensaje:

```text
El computador ya está reservado en ese bloque
```

## Modelo de datos

- Un alumno puede tener varias reservas.
- Un computador puede tener varias reservas en diferentes fechas o bloques.
- Cada reserva pertenece a un alumno, un computador y un bloque.
- Las claves foráneas evitan referencias a registros inexistentes.

## Seguridad

El repositorio debe incluir un archivo `.gitignore` con, al menos:

```gitignore
.env
.venv/
venv/
__pycache__/
*.py[cod]
.vscode/
.idea/
```

Antes de publicar, se debe comprobar que `.env` no aparezca en GitHub Desktop.

## Errores frecuentes

### Flet no está instalado

```powershell
python -m pip install -r requirements.txt
```

### No se encuentra `mysql.connector`

```powershell
python -m pip install mysql-connector-python
```

### Error de conexión con MySQL

Revisar:

- Que MySQL Server esté iniciado.
- El usuario y la contraseña escritos en `.env`.
- Que el puerto sea `3306`.
- Que exista la base de datos `reservas_laboratorio`.

## Autor

**Curso:** 4° Medio - Especialidad de Programación  
**Módulo:** Administración de Bases de Datos  
**Establecimiento:** Liceo Manuel Montt  

## Licencia

Proyecto educativo desarrollado con fines académicos.
