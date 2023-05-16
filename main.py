import json
import datetime
import os

# Creamos una lista vacía para almacenar los usuarios
usuarios = []

# Cargamos la lista de usuarios desde un archivo JSON
with open("usuarios.json", "r") as archivo:
    usuarios = json.load(archivo)

# Definimos una función para agregar un nuevo usuario
def agregar_usuario():
    dni = input("Ingresa el DNI del usuario: ")
    nombre = input("Ingresa el nombre del usuario: ")
    membresia = input("Ingresa el monto de la membresía (3000, 4500 o 5000): ")
    
    if membresia not in ["3000", "4500", "5000"]:
        print("Monto de membresía inválido.")
        return
    
    # Obtenemos la fecha actual y le sumamos 30 días
    vencimiento = (datetime.date.today() + datetime.timedelta(days=30)).strftime('%Y-%m-%d')
    
    # Creamos un nuevo diccionario para el usuario
    usuario = {
        "dni": dni,
        "nombre": nombre,
        "membresia": membresia,
        "vencimiento": vencimiento,
        "clases_restantes": 10 if membresia == "3000" else 20 if membresia == "4500" else -1
    }
    
    # Agregamos el usuario a la lista de usuarios
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
                estado = usuario['vencimiento'] + " Vencida"
            else:
                estado = usuario['vencimiento'] + " Activa"
                
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
    
    if usuario_encontrado is None:
        print("Usuario no encontrado.")
    else:
        fecha_actual = datetime.date.today()
        vencimiento = datetime.datetime.strptime(usuario_encontrado['vencimiento'], '%Y-%m-%d').date()
        
        if fecha_actual > vencimiento:
            estado = "Mensualidad vencida"
            acceso = False
        else:
            estado = usuario_encontrado['vencimiento']
            acceso = True
            
        if usuario_encontrado['clases_restantes'] == -1:
            clases_restantes = "Clases ilimitadas"
        else:
            clases_restantes = usuario_encontrado['clases_restantes']
            if clases_restantes == 20:
                clases_restantes -= 1
        
        if not acceso or (usuario_encontrado['clases_restantes'] == 0 and usuario_encontrado['membresia'] != 5000):
            print(f"DNI: {usuario_encontrado['dni']}, Nombre: {usuario_encontrado['nombre']}, Fecha de vencimiento: {estado}, Clases restantes: {clases_restantes} \nAcceso Denegado")
        else:
            if usuario_encontrado['clases_restantes'] != -1:
                usuario_encontrado['clases_restantes'] -= 1
            print(f"DNI: {usuario_encontrado['dni']}, Nombre: {usuario_encontrado['nombre']}, Fecha de vencimiento: {estado}, Clases restantes: {clases_restantes} \nIngrese")
                
            # Guardamos la lista de usuarios en un archivo JSON
            with open("usuarios.json", "w") as archivo:
                json.dump(usuarios, archivo)


# Definimos una función para renovar la suscripción de un usuario
def renovar_suscripcion():
    dni = input("Ingresa el DNI del usuario: ")
    usuario_encontrado = None
    
    for usuario in usuarios:
        if usuario['dni'] == dni:
            usuario_encontrado = usuario
            break
    
    if usuario_encontrado is None:
        print("Usuario no encontrado.")
    else:
        fecha_vencimiento = datetime.datetime.strptime(usuario_encontrado['vencimiento'], '%Y-%m-%d')
        fecha_nueva_vencimiento = fecha_vencimiento + datetime.timedelta(days=30)
        
        print("Elige una membresía:")
        print("1. 10 clases por $3000")
        print("2. 20 clases por $4500")
        print("3. Clases ilimitadas por $5000")
        opcion = input("Ingresa el número de la membresía que deseas: ")
        
        if opcion == "1":
            clases_disponibles = 10
        elif opcion == "2":
            clases_disponibles = 20
        elif opcion == "3":
            clases_disponibles = -1
        else:
            print("Opción inválida. La suscripción no se ha renovado.")
            return
        
        usuario_encontrado['vencimiento'] = fecha_nueva_vencimiento.strftime('%Y-%m-%d')
        usuario_encontrado['clases_restantes'] = clases_disponibles
        
        print(f"La suscripción del usuario {usuario_encontrado['nombre']} ha sido renovada.")
        print(f"Nueva fecha de vencimiento: {usuario_encontrado['vencimiento']}")
        if clases_disponibles == -1:
            print("El usuario tiene clases ilimitadas.")
        else:
            print(f"El usuario tiene {clases_disponibles} clases disponibles.")
        
        with open("usuarios.json", "w") as archivo:
            json.dump(usuarios, archivo)
        


def menu():
    while True:
        print("Bienvenido al gimnasio", "\n1- Agregar nuevo usuario", "\n2- Mostrar lista de usuarios", "\n3- Buscar usuario", "\n4- Renovar suscripción", "\n0- Salir")
        opcion = int(input("Elige una opcion..."))

        if opcion == 1:
            agregar_usuario()
        elif opcion == 2:
            mostrar_usuarios()
        elif opcion == 3:
            buscar_usuario()
        elif opcion == 4:
            renovar_suscripcion()
        elif opcion == 0:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Adios!")
            break
        else:
            print("Porfavor selecione una opcion correcta")

menu()
