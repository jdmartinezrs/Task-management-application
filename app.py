import streamlit as st
from crud import create_task, get_all_tasks, get_task_by_id, update_task, delete_task
from database import Base, engine

# Crear las tablas en la base de datos (si no existen)
Base.metadata.create_all(engine)

# Título de la aplicación
st.title("Gestión de Tareas")

# Opciones del menú
menu = ["Crear Tarea", "Ver Tareas", "Actualizar Tarea", "Eliminar Tarea"]
choice = st.sidebar.selectbox("Menú", menu)

if choice == "Crear Tarea":
    st.subheader("Crear una nueva tarea")

    # Formulario para crear una tarea
    title = st.text_input("Título")
    description = st.text_area("Descripción")
    if st.button("Crear Tarea"):
        if title:
            new_task = create_task(title, description)
            st.success(f"Tarea creada: {new_task}")
        else:
            st.error("El título es obligatorio")

elif choice == "Ver Tareas":
    st.subheader("Todas las Tareas")

    tasks = get_all_tasks()
    if tasks:
        for task in tasks:
            st.write(f"ID: {task.id} | Título: {task.title} | Descripción: {task.description} | Estado: {'Terminada' if task.status else 'Pendiente'}")
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
            updated_task = update_task(task_id, title, description, status)
            st.success(f"Tarea actualizada: {updated_task}")
    else:
        st.error("No se encontró la tarea con ese ID")

elif choice == "Eliminar Tarea":
    st.subheader("Eliminar una tarea")

    task_id = st.number_input("ID de la tarea", min_value=1, step=1)
    task = get_task_by_id(task_id)

    if task:
        st.write(f"Título: {task.title} | Descripción: {task.description} | Estado: {'Terminada' if task.status else 'Pendiente'}")
        if st.button("Eliminar Tarea"):
            delete_task(task_id)
            st.success("Tarea eliminada")
    else:
        st.error("No se encontró la tarea con ese ID")