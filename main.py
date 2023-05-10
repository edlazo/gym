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
                estado = "Mensualidad vencida"
            else:
                estado = "Mensualidad activa"
                
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
    
    if usuario_encontrado is None:
        print("Usuario no encontrado.")
    else:
        fecha_actual = datetime.date.today()
        vencimiento = datetime.datetime.strptime(usuario_encontrado['vencimiento'], '%Y-%m-%d').date()
        
        if fecha_actual > vencimiento:
            estado = f"Mensualidad vencida ({vencimiento.strftime('%d/%m/%Y')})"
            acceso = False
        else:
            estado = f"{vencimiento.strftime('%d/%m/%Y')}."
            acceso = True
            
        if usuario_encontrado['clases_restantes'] == -1:
            clases_restantes = "Clases ilimitadas"
        else:
            clases_restantes = usuario_encontrado['clases_restantes']
            
        print(f"DNI: {usuario_encontrado['dni']}, Nombre: {usuario_encontrado['nombre']}, Fecha vencimiento: {estado}, Membresía: {usuario_encontrado['membresia']}, Clases restantes: {clases_restantes}")
        print("Ingrese")
        if not acceso or (usuario_encontrado['clases_restantes'] == 0 and usuario_encontrado['mensualidad'] != 5000):
            print("Acceso denegado.")
        else:
            if usuario_encontrado['clases_restantes'] != -1:
                usuario_encontrado['clases_restantes'] -= 1
                
            # Guardamos la lista de usuarios en un archivo JSON
            with open("usuarios.json", "w") as archivo:
                json.dump(usuarios, archivo)


def seleccion_opcion():
    print("Bienvenido que quieres hacer?")
    while True:
        opcion = int(input(print("1- Agregar usuario", "\n2- Mostrar usuario", "\n3- Buscar Usuario", "\n0- Salir")))

        if opcion == 1:
            agregar_usuario()
        elif opcion == 2:
            mostrar_usuarios()
        elif opcion == 3:
            buscar_usuario()
        elif opcion == 0:
            print("Adios!")
            break
        else:
            print("Porfavor selecione una opcion correcta")


seleccion_opcion()
