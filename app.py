import streamlit as st
import json
import os

from crud import create_task, get_all_tasks, get_task_by_id, update_task, delete_task
from database import Base, engine

# Crear las tablas en la base de datos (si no existen)
Base.metadata.create_all(engine)

# Inicializar estado para controlar recargas
if "reload" not in st.session_state:
    st.session_state.reload = False

# Inicializar estado para controlar la edición de tareas
if "editing_task_id" not in st.session_state:
    st.session_state.editing_task_id = None

# Título de la aplicación
st.title("Gestión de Tareas")

# Incluir el CSS para personalizar los botones
st.markdown("""
    <style>
        .stButton button {
            font-size: 18px;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

# Opciones del menú
menu = ["Crear Tarea", "Ver Tareas"]
choice = st.sidebar.selectbox("Menú", menu)

def trigger_reload():
    """Función para simular recarga utilizando session_state."""
    st.session_state.reload = not st.session_state.reload
    # Reiniciar el estado de edición después de la recarga
    st.session_state.editing_task_id = None

def export_tasks_to_json():
    """Exportar todas las tareas a un archivo JSON."""
    tasks = get_all_tasks()
    
    # Convertir las tareas a un formato serializable
    tasks_data = [
        {
            "id": task.id, 
            "title": task.title, 
            "description": task.description, 
            "status": task.status
        } for task in tasks
    ]
    
    # Abrir diálogo para guardar archivo
    st.download_button(
        label=" Descargar Tareas (JSON)",
        data=json.dumps(tasks_data, indent=4, ensure_ascii=False),
        file_name="tareas_exportadas.json",
        mime="application/json"
    )

def import_tasks_from_json(file):
    try:
        # Leer el contenido del archivo
        file_content = file.getvalue().decode("utf-8")
        tasks_data = json.loads(file_content)
        
        # Contador de tareas importadas
        imported_count = 0
        
        # Importar cada tarea
        for task in tasks_data:
            # Verificar que la tarea tenga los campos necesarios
            if all(key in task for key in ["title", "description", "status"]):
                # Asegúrate de pasar el campo 'status' a create_task
                create_task(
                    title=task["title"], 
                    description=task.get("description", ""),
                    status=task.get("status", False)  # Pasar el valor de status
                )
                imported_count += 1
        
        st.success(f" {imported_count} tareas importadas exitosamente.")
        trigger_reload()
    
    except json.JSONDecodeError:
        st.error(" El archivo JSON no es válido.")
    except Exception as e:
        st.error(f" Error al importar tareas: {str(e)}")


if choice == "Crear Tarea":
    st.subheader("Crear una nueva tarea")

    # Formulario para crear una tarea
    title = st.text_input("Título")
    description = st.text_area("Descripción")
    
    # Crear tarea
    if st.button("Crear Tarea"):
        if title:
            create_task(title, description)
            st.success("Tarea creada con éxito.")
            trigger_reload()  # Forzar actualización al cambiar el estado
        else:
            st.error("El título es obligatorio")

    # Sección de Importación (después de Crear Tarea)
    st.write("###  Importar Tareas")
    uploaded_file = st.file_uploader("Selecciona un archivo JSON", type=['json'])
    if uploaded_file is not None:
        if st.button("Importar Tareas"):
            import_tasks_from_json(uploaded_file)

elif choice == "Ver Tareas":
    st.subheader("Todas las Tareas")

    tasks = get_all_tasks()  # Obtiene todas las tareas de la base de datos
    if tasks:
        # Botón para exportar tareas (junto a Todas las Tareas)
        export_tasks_to_json()
        
        # Invertir el orden de las tareas para mostrar las más recientes primero
        tasks = tasks[::-1]

        # Crear un contenedor para las tareas
        with st.container():
            for task in tasks:
                # Agregar cada tarea en un contenedor individual con 'expanded=False' para que esté plegada por defecto
                with st.expander(f"{task.title}", expanded=False):
                    # Mostrar descripción con tamaño estándar
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"<p style='font-size:18px; max-width:700px;'>{task.description}</p>", unsafe_allow_html=True)

                    # Verificar si esta tarea está en modo edición
                    if st.session_state.editing_task_id == task.id:
                        # Modo edición
                        edit_title = st.text_input("Nuevo Título", task.title, key=f"edit_title_{task.id}")
                        edit_description = st.text_area("Nueva Descripción", task.description, key=f"edit_description_{task.id}")
                        edit_status = st.checkbox("Marcar como terminada", value=task.status, key=f"edit_status_{task.id}")

                        col1, col2 = st.columns(2)
                        with col1:
                            if st.button("Guardar Cambios", key=f"save_{task.id}"):
                                update_task(task.id, edit_title, edit_description, edit_status)
                                trigger_reload()

                        with col2:
                            if st.button("Cancelar", key=f"cancel_{task.id}"):
                                st.session_state.editing_task_id = None
                    else:
                        # Modo visualización
                        st.write(f"<p style='font-size:16px;'><b>Estado:</b> {'Terminada' if task.status else 'Pendiente'}</p>", unsafe_allow_html=True)

                        col1, col2, col3 = st.columns(3)
                        with col1:
                            # Botón para cambiar el estado de la tarea
                            if st.button(
                                "Cambiar Estado",
                                key=f"toggle_status_{task.id}",
                            ):
                                update_task(
                                    task.id, task.title, task.description, not task.status
                                )
                                trigger_reload()  # Forzar actualización al cambiar el estado

                        with col2:
                            # Botón para editar la tarea
                            if st.button(f"Editar", key=f"edit_{task.id}"):
                                st.session_state.editing_task_id = task.id

                        with col3:
                            # Botón para eliminar la tarea
                            if st.button(f"Eliminar", key=f"delete_{task.id}"):
                                delete_task(task.id)
                                trigger_reload()  # Forzar actualización al eliminar la tarea
    else:
        st.info("No hay tareas disponibles")

