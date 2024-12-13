import streamlit as st
from crud import create_task, get_all_tasks, get_task_by_id, update_task, delete_task
from database import Base, engine

# Crear las tablas en la base de datos (si no existen)
Base.metadata.create_all(engine)

# Inicializar estado para controlar recargas
if "reload" not in st.session_state:
    st.session_state.reload = False

# Título de la aplicación
st.title("Gestión de Tareas")

# Opciones del menú
menu = ["Crear Tarea", "Ver Tareas", "Actualizar Tarea"]
choice = st.sidebar.selectbox("Menú", menu)

def trigger_reload():
    """Función para simular recarga utilizando session_state."""
    st.session_state.reload = not st.session_state.reload

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
                    st.write(f"**Descripción:** {task.description}")
                    st.write(f"**Estado:** {'Terminada' if task.status else 'Pendiente'}")

                    # Botón para cambiar el estado de la tarea
                    if st.button(
                        "Cambiar Estado",
                        key=f"toggle_status_{task.id}",
                    ):
                        update_task(
                            task.id, task.title, task.description, not task.status
                        )
                        trigger_reload()  # Forzar actualización al cambiar el estado

                    # Botón para eliminar la tarea
                    if st.button(f"🗑️ Eliminar Tarea", key=f"delete_{task.id}"):
                        delete_task(task.id)
                        trigger_reload()  # Forzar actualización al eliminar la tarea
    else:
        st.info("No hay tareas disponibles")

elif choice == "Actualizar Tarea":
    st.subheader("Actualizar una tarea existente")

    task_id = st.number_input("ID de la tarea", min_value=1, step=1)
    task = get_task_by_id(task_id)

    if task:
        title = st.text_input("Nuevo Título", task.title)
        description = st.text_area("Nueva Descripción", task.description)
        status = st.checkbox("Marcar como terminada", value=task.status)

        if st.button("Actualizar Tarea"):
            update_task(task_id, title, description, status)
            st.success("Tarea actualizada con éxito.")
            trigger_reload()  # Forzar actualización al actualizar la tarea
    else:
        st.error("No se encontró la tarea con ese ID")
