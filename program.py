import redis
import json

# Conexión a Redis
r = redis.Redis(host='localhost', port=6379, db=0)

# Función para agregar una nueva receta
def add_recipe():
    name = input("Nombre de la receta: ")
    ingredients = add_ingredients()
    steps = add_steps()
    
    recipe = {
        "ingredients": ingredients,
        "steps": steps
    }
    
    r.set(name, json.dumps(recipe))  # Almacena la receta en Redis como un string JSON

# Función para agregar ingredientes a una receta
def add_ingredients():
    ingredients = []
    print("Agregar ingredientes (dejar vacío para terminar):")
    while True:
        ingredient = input("Ingrediente: ")
        if ingredient == "":
            break
        ingredients.append(ingredient)
    return ingredients

# Función para agregar pasos a una receta
def add_steps():
    steps = []
    print("Agregar pasos (dejar vacío para terminar):")
    while True:
        step = input("Paso: ")
        if step == "":
            break
        steps.append(step)
    return steps

# Función para actualizar una receta existente
def update_recipe():
    list_recipes()
    recipe_name = input("Nombre de la receta a actualizar: ")
    if r.exists(recipe_name):
        option = input("Actualizar (1) Ingredientes o (2) Pasos: ")
        recipe = json.loads(r.get(recipe_name))
        if option == "1":
            ingredients = add_ingredients()
            recipe["ingredients"] = ingredients
        elif option == "2":
            steps = add_steps()
            recipe["steps"] = steps
        r.set(recipe_name, json.dumps(recipe))
    else:
        print("Receta no encontrada.")

# Función para eliminar una receta existente
def delete_recipe():
    list_recipes()
    recipe_name = input("Nombre de la receta a eliminar: ")
    if r.exists(recipe_name):
        r.delete(recipe_name)
    else:
        print("Receta no encontrada.")

# Función para ver todas las recetas
def list_recipes():
    keys = r.keys()
    for key in keys:
        print(key.decode('utf-8'))

# Función para buscar los ingredientes y pasos de una receta
def search_recipe():
    list_recipes()
    recipe_name = input("Nombre de la receta a buscar: ")
    if r.exists(recipe_name):
        recipe = json.loads(r.get(recipe_name))
        print("\nIngredientes:")
        for ingredient in recipe['ingredients']:
            print(f"- {ingredient}")
        
        print("\nPasos:")
        for step in recipe['steps']:
            print(f"- {step}")
    else:
        print("Receta no encontrada.")

# Función principal del menú
def menu():
    while True:
        print("\nLibro de Recetas")
        print("1. Agregar nueva receta")
        print("2. Actualizar receta existente")
        print("3. Eliminar receta existente")
        print("4. Ver listado de recetas")
        print("5. Buscar ingredientes y pasos de receta")
        print("6. Salir")

        option = input("Seleccione una opción: ")

        if option == "1":
            add_recipe()
        elif option == "2":
            update_recipe()
        elif option == "3":
            delete_recipe()
        elif option == "4":
            list_recipes()
        elif option == "5":
            search_recipe()
        elif option == "6":
            break
        else:
            print("Opción no válida. Intente de nuevo.")

if __name__ == "__main__":
    menu()
