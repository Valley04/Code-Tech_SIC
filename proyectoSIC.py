import pandas as pd
import time
import os
import matplotlib.pyplot as plt
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

def ahorro_personalizado():
    porcentaje = 100
    gastos = int(input("Porcentaje destinado para gastos: "))

    if gastos <= porcentaje & gastos >= 0:
        porcentaje -= gastos
        ahorro = int(input("Porcentaje destinado para ahorro: "))

        if ahorro <= porcentaje & ahorro >= 0:
            porcentaje -= ahorro
            ocio = porcentaje
            return gastos, ahorro, ocio
        else:
            print("Porcentaje no valido")
            return
    else:
        print("Porcentaje no valido")
        return

# Selecciona un plan de ahorro y devuelve las proporciones correspondientes.
def seleccionar_plan_ahorro():

    while True:
        print("\nSelecciona un plan de ahorro:")
        print("1. 60% Gastos, 20% Ahorro, 20% Ocio")
        print("2. 50% Gastos, 20% Ahorro, 30% Ocio")
        print("3. 70% Gastos, 20% Ahorro, 10% Ocio")
        print("4. Personalizar plan de ahorro...")

        try:
            opcion = int(input("Elige una opción: "))
            if opcion == 1:
                return 0.60, 0.30, 0.10
            elif opcion == 2:
                return 0.50, 0.35, 0.15
            elif opcion == 3:
                return 0.70, 0.20, 0.10
            elif opcion == 4:
                ahorro_personalizado()
            else:
                print("Opción no válida, selecciona nuevamente.")
        except ValueError:
            print("Entrada no válida, ingresa un número (1, 2, o 3).")

# Calcula la distribución del ingreso según el plan de ahorro seleccionado.
def calcular_distribucion(ingresos, plan):
    gastos_fijos = ingresos * plan[0]
    ahorro = ingresos * plan[1]
    ocio = ingresos * plan[2]
    return gastos_fijos, ahorro, ocio

# Muestra una gráfica de barras con la distribución del ingreso.
def mostrar_grafica(gastos_fijos, ahorro, ocio):
    categorias = ['Gastos Fijos', 'Ahorro', 'Ocio']
    valores = [gastos_fijos, ahorro, ocio]

    plt.figure(figsize=(10, 5))
    barras = plt.bar(categorias, valores, color=['blue', 'green', 'red'])
    plt.xlabel('Categorías')
    plt.ylabel('Monto')
    plt.title('Distribución del Ingreso')

    # Añadir etiquetas con la cantidad exacta de dinero
    for barra in barras:
        altura = barra.get_height()
        plt.annotate(f'{altura:.2f}', xy=(barra.get_x() + barra.get_width() / 2, altura),
                     xytext=(0, 3),  # 3 puntos de desplazamiento vertical
                     textcoords="offset points", ha='center', va='bottom')
    plt.show()

# Función que muestra un menú para usuarios en sesión activa
def menu_sesion(user):
    intentos = 0
    max_intentos = 3  # Número máximo de intentos permitidos
    index = usuarios.loc[usuarios['User'] == user].index[0]
    ingresos_totales = usuarios.loc[index, "Balance"]

    while True:
        print("\nBienvenido a Finance")
        print("1. Registrar ingreso/egreso")
        print("2. Seleccionar plan de ahorro")
        print("3. Mostrar historial de transacciones")
        print("4. Cerrar sesión")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            registro_balance(user)
            intentos = 0  # Reiniciar contador de intentos tras una acción válida
        elif opcion == '2':
            if ingresos_totales > 0:
                    gastos_fijos, ahorro, ocio = calcular_distribucion(ingresos_totales, seleccionar_plan_ahorro())
                    mostrar_grafica(gastos_fijos, ahorro, ocio)
                    intentos = 0
            else:
                print("Por favor, ingrese un monto antes de seleccionar un plan de ahorro.")
        elif opcion == '3':
            print("Proximamente...")
            time.sleep(2)
            return
        elif opcion == "4":
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