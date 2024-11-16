import pandas as pd
import time
import os
from getpass import getpass
from datetime import datetime
from tkinter import Tk, Label, Entry, Button, StringVar, messagebox

try:
    usuarios = pd.read_csv('usuarios.csv')
except Exception as e:
    usuarios = pd.DataFrame(columns=["Nombre del cliente", "I.D.", "Ocupación", 
                                      "Ingreso Mensual", "Meta de Ahorro", "User", 
                                      "Correo", "Contraseña", "Balance"])

try:
    balance_df = pd.read_csv('gastos.csv')

except Exception as e:
    balance_df = pd.DataFrame(columns=["Tipo", "I.D.", "Fecha", "Categoría", "Monto", "Descripción"])

# Función de inicio de sesión de usuario
def iniciar_sesion():

    print("Inicio de sesión\n")

    print("Si desea salir ingrese '0'")
    usuario = input("Nombre de usuario: ")

    # Condicional para salir al menu de inicio
    if usuario == '0':
        menu()

    # Se busca en el dataframe si el usuario existe
    for user in usuarios['User']:
        if usuario == user:
            index = usuarios.loc[usuarios['User'] == usuario].index[0]
            contraseña = input("Contraseña: ")

            # Se confirma si la contraseña es correcta
            if contraseña == usuarios.loc[index, "Contraseña"]:
                print("¡Inicio de Sesión Exitoso!")
                time.sleep(2)
                menu_sesion(usuario)
                return  # Detener la función tras iniciar sesión correctamente

    print("Usuario no registrado. Intente de nuevo")
    menu()


# Función para registrar un nuevo usuario
def registrar_usuario():

    global usuarios
    
    print("Registro de usuario nuevo\n")

    # Ingreso de datos socioeconómicos
    nombre = input("Nombre y Apellido: ")
    while True:
        try:
            user_id = int(input("Cédula de Identidad: "))
            break
        except ValueError:
            print("Error: Ingrese un número válido.")

    ocupacion = input("Ocupación: ")
    ingreso = float(input("Ingreso Mensual: "))
    meta_ahorro = float(input("Meta de Ahorro: "))
    user = input("Nombre de usuario: ")
    correo = input("Correo: ")
    contraseña = getpass("Contraseña: ")
    balance = 0.00

    # Se almacenan los datos en un diccionario
    nuevo_usuario = {"Nombre del cliente": nombre, 
                     "I.D.": user_id, 
                     "Ocupación": ocupacion, 
                     "Ingreso Mensual": ingreso, 
                     "Meta de Ahorro": meta_ahorro, 
                     "User": user, 
                     "Correo": correo, 
                     "Contraseña": contraseña,
                     "Balance": balance}
    
    # Convertir el nuevo usuario en un DataFrame y usar pd.concat para agregarlo al DataFrame global
    nuevo_usuario_df = pd.DataFrame([nuevo_usuario])
    global usuarios  # Asegurarse de que modificamos el DataFrame global
    usuarios = pd.concat([usuarios, nuevo_usuario_df], ignore_index=True)
    
    # Guardar los datos en un archivo CSV
    usuarios.to_csv("usuarios.csv", index=False)
    
    print("¡Usuario registrado exitosamente!")
    time.sleep(2)


# Función para registrar un ingreso/egreso
def registro_balance(user):

    index = usuarios.loc[usuarios['User'] == user].index[0]
    balance_actual = usuarios.loc[index, "Balance"]
    user_id = usuarios.loc[index, "I.D."]

    print(f"Balance en cuenta: {balance_actual}")

    print("\n¿Que operación desea realizar?")
    print("1. Ingreso")
    print("2. Egreso")

    opcion = input("Seleccione una opción: ")

    if opcion == "1":
        tipo = "ingreso"
        while True:
            fecha = input("Fecha del ingreso (YYYY-MM-DD): ")
            try:
                datetime.strptime(fecha, '%Y-%m-%d')
                break
            except ValueError:
                print("Formato de fecha inválido. Intente nuevamente.")
        categoria = input("Categoría del ingreso: ")
        monto = float(input("Monto del ingreso: "))
        descripcion = input("Descripción: ")  

        usuarios.loc[index, "Balance"] += monto

    elif opcion == "2":
        tipo = "gasto"
        while True:
            fecha = input("Fecha del egreso (YYYY-MM-DD): ")
            try:
                datetime.strptime(fecha, '%Y-%m-%d')
                break
            except ValueError:
                print("Formato de fecha inválido. Intente nuevamente.")
        categoria = input("Categoría del gasto: ")
        monto = float(input("Monto del gasto: "))
        descripcion = input("Descripción: ")

        usuarios.loc[index, "Balance"] -= monto

    else:
        print("Opción no válida")
        menu_sesion(user)

    nuevo_registro = {"Tipo": tipo, 
                      "I.D.": user_id, 
                      "Fecha": fecha, 
                      "Categoría": categoria, 
                      "Monto": monto, 
                      "Descripción": descripcion}
    
    global balance_df  # Asegurarse de que modificamos el DataFrame global
    nuevo_registro_df = pd.DataFrame([nuevo_registro])
    balance_df = pd.concat([balance_df, nuevo_registro_df], ignore_index=True)
    
    # Guardar los registros de balance en un archivo CSV
    balance_df.to_csv("gastos.csv", index=False)

    print("Operación registrada exitosamente!")
    time.sleep(2)


# Función que muestra un menú para usuarios en sesión activa
def menu_sesion(user):
    intentos = 0
    max_intentos = 3  # Número máximo de intentos permitidos

    while True:
        print("\nBienvenido a Finance")
        print("1. Registrar ingreso/egreso")
        print("2. Cerrar sesión")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            registro_balance(user)
            intentos = 0  # Reiniciar contador de intentos tras una acción válida
        elif opcion == "2":
            print("Cerrando sesión...")
            time.sleep(2)
            menu()
            return
        else:
            print("Opción no válida. Intente nuevamente.")
            intentos += 1

        if intentos >= max_intentos:
            print("Demasiados intentos fallidos. Regresando al menú principal...")
            time.sleep(2)
            menu()
            return


# Función para mostrar el menú y gestionar las opciones de registro
def menu():
    intentos = 0
    max_intentos = 3  # Número máximo de intentos permitidos

    while True:
        print("\nMenu de inicio:")
        print("1. Iniciar sesion")
        print("2. Registrarse")
        print("3. Salir del programa")

        opcion = input("Seleccione una opcion: ")

        if opcion == "1":
            iniciar_sesion()
            intentos = 0  # Reiniciar contador de intentos tras una acción válida
        elif opcion == "2":
            registrar_usuario()
            intentos = 0
        elif opcion == "3":
            print("Saliendo del programa...")
            return
        else:
            print("Opción no válida. Intente nuevamente.")
            intentos += 1

        if intentos >= max_intentos:
            print("Demasiados intentos fallidos. Cerrando el programa...")
            time.sleep(2)
            return

# Ejecutar el menú de inicio
menu()