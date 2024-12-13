import streamlit as st
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

# Opciones del menú
menu = ["Crear Tarea", "Ver Tareas"]
choice = st.sidebar.selectbox("Menú", menu)

def trigger_reload():
    """Función para simular recarga utilizando session_state."""
    st.session_state.reload = not st.session_state.reload
    # Reiniciar el estado de edición después de la recarga
    st.session_state.editing_task_id = None

if choice == "Crear Tarea":
    st.subheader("Crear una nueva tarea")

    # Formulario para crear una tarea
    title = st.text_input("Título")
    description = st.text_area("Descripción")
    if st.button("Crear Tarea"):
        if title:
            create_task(title, description)
            st.success("Tarea creada con éxito.")
            trigger_reload()  # Forzar actualización al cambiar el estado
        else:
            st.error("El título es obligatorio")

elif choice == "Ver Tareas":
    st.subheader("Todas las Tareas")

    tasks = get_all_tasks()  # Obtiene todas las tareas de la base de datos
    if tasks:
        # Invertir el orden de las tareas para mostrar las más recientes primero
        tasks = tasks[::-1]

        # Crear un contenedor para las tareas
        with st.container():
            for task in tasks:
                # Agregar cada tarea en un contenedor individual
                with st.expander(f"Tarea ID: {task.id} - {task.title}", expanded=True):
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
                        st.write(f"**Descripción:** {task.description}")
                        st.write(f"**Estado:** {'Terminada' if task.status else 'Pendiente'}")

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