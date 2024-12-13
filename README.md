# Task management application

Una aplicación de gestión de tareas construida con Streamlit y SQLAlchemy/SQLite3.

## Características

- Crear tareas
- Editar tareas
- Eliminar tareas
- Exportar e importar tareas en formato JSON
- Interfaz simple e intuitiva

## Video

![Video](https://img.youtube.com/vi/IRWg2tMIVlg/0.jpg)
[Ver el funcionamiento de la app](https://www.youtube.com/watch?v=IRWg2tMIVlg)

## Instalación

python version : 3.10.11

1. **Clonar el repositorio**

   ```
   git clone https://github.com/jdmartinezrs/Task-management-application.git
   ```

2. **Crear un entorno virtual**
   Ejecuta el siguiente comando para crear un entorno virtual:

   ```python
   python -m venv es1
   ```

3. **Activar el entorno virtual**
   Para activar el entorno virtual, usa este comando:

   ```python
   es1\Scripts\activate
   ```

   **Nota:** Si obtienes un error como el siguiente:

   ```
   plaintextCopiar códigoPS C:\Users\Usuario\Desktop\Task-management-application-1> python -m venv es1
   PS C:\Users\Usuario\Desktop\Task-management-application-1> es1\Scripts\activate
   es1\Scripts\activate : No se puede cargar el archivo C:\Users\Usuario\Desktop\Task-management-application-1\es1\Scripts\Activate.ps1 porque la ejecución de scripts está 
   deshabilitada en este sistema. Para obtener más información, consulta el tema about_Execution_Policies en https:/go.microsoft.com/fwlink/?LinkID=135170.
   En línea: 1 Carácter: 1
   + es1\Scripts\activate
   + ~~~~~~~~~~~~~~~~~~~~
       + CategoryInfo          : SecurityError: (:) [], PSSecurityException
       + FullyQualifiedErrorId : UnauthorizedAccess
   PS C:\Users\Usuario\Desktop\Task-management-application-1>
   ```

   Esto ocurre debido a la configuración de la política de ejecución de scripts en PowerShell. Comprueba la política actual con el siguiente comando:

   ```
   Get-ExecutionPolicy
   ```

   Si el resultado es `Restricted`, necesitas cambiarla ejecutando:

   ```
   Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
   ```

   Luego, intenta activar el entorno virtual nuevamente:

   ```python
   es1\Scripts\activate
   ```

4. **Instalar las dependencias**
   Una vez activado el entorno virtual, instala las dependencias necesarias desde el archivo `requirements.txt`:

   ```python
   pip install -r requirements.txt
   ```

5. **Ejecutar la aplicación en Streamlit**
   Inicia la aplicación con el siguiente comando:

   ```python
   streamlit run app.py
   ```



------



## Funciones Disponibles

### 1. `create_task(title, description, status=False)`

Crea una nueva tarea en la base de datos.

**Parámetros:**

- `title` (str): Título de la tarea.
- `description` (str): Descripción de la tarea.
- `status` (bool, opcional): Estado inicial de la tarea. Por defecto es `False`.

**Devuelve:**

- Una instancia de la tarea creada.



### 2. `get_all_tasks()`

Recupera todas las tareas existentes en la base de datos.

**Devuelve:**

- Una lista de todas las tareas.

  

### 3. `get_task_by_id(task_id)`

Obtiene una tarea específica mediante su ID.

**Parámetros:**

- `task_id` (int): ID de la tarea a buscar.

**Devuelve:**

- La tarea correspondiente al ID o `None` si no existe.



### 4. `update_task(task_id, title=None, description=None, status=None)`

Actualiza una tarea existente en la base de datos.

**Parámetros:**

- `task_id` (int): ID de la tarea a actualizar.
- `title` (str, opcional): Nuevo título de la tarea.
- `description` (str, opcional): Nueva descripción de la tarea.
- `status` (bool, opcional): Nuevo estado de la tarea.

**Devuelve:**

- La tarea actualizada

  

### 5. `delete_task(task_id)`

Elimina una tarea existente de la base de datos.

**Parámetros:**

- `task_id` (int): ID de la tarea a eliminar.

**Devuelve:**

- La tarea eliminada o `None` si no existe.

### Funciones de la Aplicación:

1. **`create_task`**:
   - **Excepción**: No se documenta una excepción específica, pero si falla la creación de la tarea, generalmente puede estar asociada a un error de base de datos o validación. Se debe manejar adecuadamente con un mensaje como `st.error("Error al crear la tarea")`.
   - **Retorno Exitoso**: Si la tarea se crea correctamente, se muestra el mensaje `st.success("Tarea creada con éxito.")`.
2. **`get_all_tasks`**:
   - **Excepción**: No hay manejo explícito de excepciones, pero si ocurre un error en la base de datos, como una conexión fallida, se debe capturar con un `try-except` y mostrar `st.error("Error al obtener las tareas.")`.
   - **Retorno Exitoso**: Retorna una lista de tareas obtenidas de la base de datos. Si no hay tareas, se muestra el mensaje `st.info("No hay tareas disponibles")`.
3. **`get_task_by_id`**:
   - **Excepción**: Si no se encuentra una tarea con el `id` proporcionado, se puede manejar con una excepción y mostrar `st.error("Tarea no encontrada.")`.
   - **Retorno Exitoso**: Retorna los detalles de la tarea solicitada, pero no se invoca directamente en el código dado.
4. **`update_task`**:
   - **Excepción**: Si ocurre un error al actualizar una tarea, como una falla en la base de datos o validación, se maneja con un `try-except` y se muestra el mensaje `st.error("Error al actualizar la tarea.")`.
   - **Retorno Exitoso**: Después de actualizar una tarea, se ejecuta el mensaje `st.success("Tarea actualizada con éxito.")` en caso de éxito.
5. **`delete_task`**:
   - **Excepción**: Si ocurre un error al eliminar la tarea, se maneja con un `try-except` y se muestra el mensaje `st.error("Error al eliminar la tarea.")`.
   - **Retorno Exitoso**: Al eliminar una tarea con éxito, se muestra el mensaje `st.success("Tarea eliminada con éxito.")`.

------



### Funciones de Importación y Exportación de JSON:

- **`export_tasks_to_json`**:
  - **Excepción**: No se gestionan excepciones específicas, pero si algo sale mal durante el proceso de exportación (por ejemplo, si `get_all_tasks` falla), se podría capturar con un `try-except` y mostrar un mensaje de error, como `st.error("Error al exportar las tareas.")`.
  - **Retorno Exitoso**: Se genera un archivo descargable con las tareas exportadas en formato JSON.
- **`import_tasks_from_json`**:
  - Excepción
    - Si el archivo JSON tiene un formato inválido, se captura un error con `json.JSONDecodeError` y se muestra el mensaje `st.error("El archivo JSON no es válido.")`.
    - Si ocurre un error general durante la importación, se captura con `Exception` y se muestra el mensaje `st.error(f"Error al importar tareas: {str(e)}")`.
  - **Retorno Exitoso**: Si la importación es exitosa, se muestra el mensaje `st.success(f"{imported_count} tareas importadas exitosamente.")`.