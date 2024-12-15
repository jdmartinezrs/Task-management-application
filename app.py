import streamlit as st
import json
from src.crud import create_task, get_all_tasks, get_task_by_id, update_task, delete_task
from src.database import Base, engine

# Crear las tablas en la base de datos (si no existen)
Base.metadata.create_all(engine)

# Inicializar estado para controlar la edición de tareas
if "editing_task_id" not in st.session_state:
    st.session_state.editing_task_id = None

# Mensaje de éxito personalizado
def show_success_message(message):
    # Fallback to st.success if toast is not available
    st.success(message)

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

def export_tasks_to_json():
    """Exportar todas las tareas a un archivo JSON."""
    tasks = get_all_tasks()
    tasks_data = [
        {"id": task.id, "title": task.title, "description": task.description, "status": task.status}
        for task in tasks
    ]
    
    st.download_button(
        label=" Descargar Tareas (JSON)",
        data=json.dumps(tasks_data, indent=4, ensure_ascii=False),
        file_name="tareas_exportadas.json",
        mime="application/json"
    )

def import_tasks_from_json(file):
    try:
        file_content = file.getvalue().decode("utf-8")
        tasks_data = json.loads(file_content)
        imported_count = 0
        for task in tasks_data:
            if all(key in task for key in ["title", "description", "status"]):
                create_task(title=task["title"], description=task.get("description", ""), status=task.get("status", False))
                imported_count += 1
        st.success(f" {imported_count} tareas importadas exitosamente.")
    except json.JSONDecodeError:
        st.error(" El archivo JSON no es válido.")
    except Exception as e:
        st.error(f" Error al importar tareas: {str(e)}")

if choice == "Crear Tarea":
    st.subheader("Crear una nueva tarea")

    # Usar st.form para manejar mejor el envío de formularios
    with st.form(key='create_task_form', clear_on_submit=True):
        title = st.text_input("Título")
        description = st.text_area("Descripción")
        
        # Botón de submit dentro del formulario
        submit_button = st.form_submit_button(label="Crear Tarea")

        if submit_button:
            if title:
                try:
                    # Intentar crear la tarea
                    create_task(title, description)
                    # Usar success para mostrar mensaje de éxito
                    show_success_message("Tarea creada con éxito.")
                except Exception as e:
                    st.error(f"Error al crear la tarea: {str(e)}")
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

    tasks = get_all_tasks()  
    if tasks:
        export_tasks_to_json()
        
        tasks = tasks[::-1]

        with st.container():
            for task in tasks:
                with st.expander(f"{task.title}", expanded=False):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"<p style='font-size:18px; max-width:700px;'>{task.description}</p>", unsafe_allow_html=True)

                    if st.session_state.editing_task_id == task.id:
                        with st.form(key=f'edit_task_form_{task.id}', clear_on_submit=True):
                            edit_title = st.text_input("Nuevo Título", task.title, key=f"edit_title_{task.id}")
                            edit_description = st.text_area("Nueva Descripción", task.description, key=f"edit_description_{task.id}")
                            edit_status = st.checkbox("Marcar como terminada", value=task.status, key=f"edit_status_{task.id}")

                            col1, col2 = st.columns(2)
                            with col1:
                                save_changes = st.form_submit_button("Guardar Cambios")
                            
                            with col2:
                                cancel_edit = st.form_submit_button("Cancelar")

                            if save_changes:
                                update_task(task.id, edit_title, edit_description, edit_status)
                                show_success_message("Tarea actualizada con éxito.")
                                st.session_state.editing_task_id = None
                                st.rerun()  # Use st.rerun() instead of st.experimental_rerun()
                            
                            if cancel_edit:
                                st.session_state.editing_task_id = None
                                st.rerun()  # Use st.rerun() instead of st.experimental_rerun()
                    else:
                        st.write(f"<p style='font-size:16px;'><b>Estado:</b> {'Terminada' if task.status else 'Pendiente'}</p>", unsafe_allow_html=True)

                        col1, col2, col3 = st.columns(3)
                        with col1:
                            if st.button("Cambiar Estado", key=f"toggle_status_{task.id}"):
                                update_task(task.id, task.title, task.description, not task.status)
                                show_success_message("Estado de tarea actualizado.")
                                st.rerun()  # Use st.rerun() instead of st.experimental_rerun()

                        with col2:
                            if st.button(f"Editar", key=f"edit_{task.id}"):
                                st.session_state.editing_task_id = task.id

                        with col3:
                            if st.button(f"Eliminar", key=f"delete_{task.id}"):
                                delete_task(task.id)
                                show_success_message("Tarea eliminada con éxito.")
                                st.rerun()  # Use st.rerun() instead of st.experimental_rerun()
    else:
        st.info("No hay tareas disponibles")
