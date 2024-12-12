from database import Base, engine
from crud import create_task, get_all_tasks, get_task_by_id, update_task, delete_task

# Crear todas las tablas en la base de datos
Base.metadata.create_all(engine)

if __name__ == "__main__":
    # Crear tareas
    create_task("Comprar comida", "Comprar frutas y verduras")
    create_task("Hacer ejercicio", "Correr 5 kilometros")

    # Imprimir todas las tareas
    print("Todas las tareas:", get_all_tasks())

    # Obtener tarea por ID
    print("Tarea con Id 1:", get_task_by_id(1))

    # Actualizar tarea
    updated_task = update_task(1, status=True)
    print("Tarea actualizada:", updated_task)

    # Eliminar tarea
    deleted_task = delete_task(2)
    print("Tarea eliminada:", deleted_task)

    # Imprimir todas las tareas después de eliminación
    print("Todas las tareas:", get_all_tasks())
