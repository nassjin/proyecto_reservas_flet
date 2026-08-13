# Guía de instalación - Sistema de reserva de computadores

**Módulo:** Administración de Bases de Datos  
**Nivel:** 4° Medio - Especialidad de Programación  
**Tecnologías:** Python, Flet, MySQL y DBeaver  

---

## 1. Programas necesarios

Antes de instalar el proyecto, el computador debe tener:

- Python 3.11 o superior.
- MySQL Server 8 o superior.
- DBeaver.
- La carpeta `proyecto_reservas_flet` descomprimida en el escritorio.

## 2. Comprobar Python

Abrir **PowerShell** y ejecutar:

```powershell
python --version
```

Si Windows no reconoce el comando, probar:

```powershell
py --version
```

Debe aparecer una respuesta similar a:

```text
Python 3.11.9
```

## 3. Entrar en la carpeta del proyecto

```powershell
cd "C:\Users\carpetaususario\Desktop\proyecto_reservas_flet"
```

> Si la carpeta está guardada en otro lugar, se debe cambiar la ruta anterior.

## 4. Crear el entorno virtual

El entorno virtual mantiene las dependencias del proyecto separadas de otros
programas de Python.

```powershell
python -m venv .venv
```

Si se está utilizando el comando `py`:

```powershell
py -m venv .venv
```

## 5. Activar el entorno virtual

En PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Si PowerShell bloquea la activación, ejecutar:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Después, volver a activar:

```powershell
.\.venv\Scripts\Activate.ps1
```

Cuando el entorno se encuentre activo, la terminal mostrará algo parecido a:

```text
(.venv) PS C:\Users\nombreusurio_\Desktop\proyecto_reservas_flet>
```

### Alternativa para CMD

Si se utiliza el Símbolo del sistema en lugar de PowerShell:

```bat
.venv\Scripts\activate.bat
```

## 6. Instalar las dependencias

Actualizar el instalador de paquetes:

```powershell
python -m pip install --upgrade pip
```

Instalar las bibliotecas indicadas por el proyecto:

```powershell
python -m pip install -r requirements.txt
```

Esto instalará:

- `flet`: crea la interfaz gráfica.
- `mysql-connector-python`: conecta Python con MySQL.
- `python-dotenv`: lee la configuración desde el archivo `.env`.

## 7. Crear el archivo de configuración

Copiar `.env.example` con el nuevo nombre `.env`:

```powershell
Copy-Item .env.example .env
```

Abrir el archivo con el Bloc de notas:

```powershell
notepad .env
```

Escribir los datos de la conexión:

```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=CLAVE_DE_MYSQL
DB_NAME=reservas_laboratorio
```

Se debe reemplazar `CLAVE_DE_MYSQL` por la contraseña real del usuario `root`.

> El archivo `.env` contiene una contraseña y no debe publicarse ni compartirse.

## 8. Crear la base de datos desde DBeaver

1. Abrir DBeaver.
2. Conectarse al servidor MySQL.
3. Abrir el archivo `sql/base_datos.sql`.
4. Ejecutar el script completo.
5. Actualizar la conexión desde el panel izquierdo.
6. Comprobar que aparezca la base de datos `nombreBD_`.

El script crea:

- La base de datos.
- Las tablas `alumnos`, `computadores`, `bloques` y `reservas`.
- Datos de prueba.
- El único procedimiento almacenado: `realizar_reserva`.

## 9. Ejecutar la aplicación

Con el entorno virtual activo:

```powershell
python app.py
```

Para cerrar la aplicación desde la terminal:

```text
Ctrl + C
```

## 10. Comandos rápidos para la presentación

Estos son los comandos principales que puede mostrar el estudiante:

```powershell
cd "C:\Users\nombreusuario_\Desktop\proyecto_reservas_flet"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
notepad .env
python app.py
```

## 11. Prueba del CRUD

Una vez iniciada la aplicación, realizar estas pruebas:

1. **Agregar:** registrar una reserva nueva.
2. **Leer:** comprobar que aparezca en la lista.
3. **Actualizar:** presionar el lápiz, modificar un dato y guardar.
4. **Eliminar:** presionar el botón rojo de la reserva.
5. **Validar:** intentar reservar dos veces el mismo computador, fecha y bloque.

## 12. Solución de problemas

### Flet no está instalado

```powershell
python -m pip install --upgrade flet
```

### No se encuentra `mysql.connector`

```powershell
python -m pip install mysql-connector-python
```

### No se encuentra `dotenv`

```powershell
python -m pip install python-dotenv
```

### Comprobar Flet

```powershell
python -c "import flet; print('Flet instalado correctamente')"
```

### Comprobar el conector de MySQL

```powershell
python -c "import mysql.connector; print('Conector MySQL instalado correctamente')"
```

### Error de acceso a MySQL

Revisar en `.env`:

- El usuario de MySQL.
- La contraseña.
- El puerto, normalmente `3306`.
- Que MySQL Server se encuentre iniciado.
- Que la base de datos `reservas_laboratorio` exista.

### Salir del entorno virtual

```powershell
deactivate
```


