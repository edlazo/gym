import json
import datetime

# Creamos una lista vacía para almacenar los usuarios
usuarios = []

# Cargamos la lista de usuarios desde un archivo JSON
with open("usuarios.json", "r") as archivo:
    usuarios = json.load(archivo)

# Definimos una función para agregar un nuevo usuario
def agregar_usuario():
    dni = input("Ingresa el DNI del usuario: ")
    nombre = input("Ingresa el nombre del usuario: ")
    mensualidad = float(input("Ingresa el monto de la mensualidad: "))
    vencimiento = input("Ingresa la fecha de vencimiento (DD/MM/YYYY): ")
    vencimiento = datetime.datetime.strptime(vencimiento, '%d/%m/%Y').date()
    
    # Creamos un diccionario con los datos del usuario
    if mensualidad == 3000:
        membresia = "10 clases"
        clases_restantes = 10
    elif mensualidad == 4500:
        membresia = "20 clases"
        clases_restantes = 20
    elif mensualidad == 5000:
        membresia = "Clases ilimitadas"
        clases_restantes = -1  # -1 indica que el usuario tiene clases ilimitadas
    else:
        membresia = "Membresía desconocida"
        clases_restantes = -1
        
    usuario = {
        "dni": dni,
        "nombre": nombre,
        "mensualidad": mensualidad,
        "vencimiento": str(vencimiento),
        "membresia": membresia,
        "clases_restantes": clases_restantes
    }
    
    # Agregamos el usuario a la lista
    usuarios.append(usuario)
    
    # Guardamos la lista de usuarios en un archivo JSON
    with open("usuarios.json", "w") as archivo:
        json.dump(usuarios, archivo)
        
    print("Usuario agregado exitosamente.")

# Definimos una función para mostrar la lista de usuarios
def mostrar_usuarios():
    if len(usuarios) == 0:
        print("No hay usuarios registrados.")
    else:
        fecha_actual = datetime.date.today()
        
        for usuario in usuarios:
            vencimiento = datetime.datetime.strptime(usuario['vencimiento'], '%Y-%m-%d').date()
            
            if fecha_actual > vencimiento:
                estado = "Mensualidad vencida"
            else:
                estado = "Bienvenido"
                
            if usuario['clases_restantes'] == -1:
                clases_restantes = "Clases ilimitadas"
            else:
                clases_restantes = usuario['clases_restantes']
                
            print(f"DNI: {usuario['dni']}, Nombre: {usuario['nombre']}, Estado: {estado}, Membresía: {usuario['membresia']}, Clases restantes: {clases_restantes}")

# Definimos una función para buscar un usuario por su DNI
def buscar_usuario():
    dni = input("Ingresa el DNI del usuario: ")
    usuario_encontrado = None
    
    for usuario in usuarios:
        if usuario['dni'] == dni:
            usuario_encontrado = usuario
            break
    
    if usuario_encontrado:
        if usuario_encontrado['clases_restantes'] == -1:
            clases_restantes = "Clases ilimitadas"
        else:
            clases_restantes = usuario_encontrado['clases_restantes']
            
        print(f"Nombre: {usuario_encontrado['nombre']}, Fecha de vencimiento: {usuario_encontrado['vencimiento']}, Clases restantes: {clases_restantes}")
    else:
        print("Usuario no encontrado.")

# Definimos una función para restar un día a las clases restantes de un usuario
def restar_clase():
    dni = input("Ingresa el DNI del usuario: ")
    usuario_encontrado = None
    
    for usuario in usuarios:
        if usuario['dni'] == dni:
            usuario_encontrado = usuario
            break
    
    if usuario_encontrado:
        if usuario_encontrado['clases_restantes'] == -1:
            print("Este usuario tiene clases ilimitadas.")
        else:
            usuario_encontrado['clases_restantes'] -= 1
            print(f"Clase restada exitosamente. Ahora {usuario_encontrado['nombre']} tiene {usuario_encontrado['clases_restantes']} clases restantes.")
            
            # Guardamos la lista de usuarios en un archivo JSON
            with open("usuarios.json", "w") as archivo:
                json.dump(usuarios, archivo)
    else:
        print("Usuario no encontrado.")
