import os
import webbrowser
import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename

# Import creativos hehehe
try:
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    from webdriver_manager.chrome import ChromeDriverManager
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False


driver_preview = None

def abrirArchivo():
    """
    Abrir una archivo del explorador del sistema, usa tkinter
    """
    fn = askopenfilename()
    print("user chose", fn)
    try:
        with open(fn, "r", encoding="utf-8") as f:
            return f.read()
        print("¡Archivo abierto!")
    except Exception as e:
        print(f"Error: {e}")
    

def save_file(content):
    """
    Abrir una archivo del explorador del sistema, usa tkinter

    content (str)  = Contenido del todo el archivo
    """
    fn = asksaveasfilename()
    print("user chose", fn)
    try:
        with open(fn, "w", encoding="utf-8") as f:
            return f.write(content)
        print("¡Archivo abierto!")
    except Exception as e:
        print(f"Error: {e}")
        
# Memoria (Historia_undo, historial_redo) ?
def undo_function(historial_undo, historial_redo, contenido_actual):
    """
    La funcionalidad de undo, usa un stack como si fuese una memoria

    historial_undo (stack)  = Una pila de contenido borrado del usuario.
    historial_redo (stack) = Para guardar lo que el usuario viro
    contenido_actual (str)  = Contenido del todo el archivo
    """
    print('Called undo_function: ', historial_undo, historial_redo)
    if len(historial_undo) > 0:
        # Guardar lo que se va a eliminar
        historial_redo.append(contenido_actual)
        # hacemos undo
        return historial_undo.pop()
    return contenido_actual

def redo_function(historial_undo, historial_redo, contenido_actual):
    """
    La funcionalidad de redo, usa un stack como si fuese una memoria

    historial_undo (stack)  = Para guardar lo que el usuario viro
    historial_redo (stack) = Una pila de contenido del redo del usuario.
    contenido_actual (str)  = Contenido del todo el archivo
    """
    print('Called redo_function: ', historial_undo, historial_redo)
    if len(historial_redo) > 0:
        # Si rehacemos, guardamos lo actual en Undo
        historial_undo.append(contenido_actual)
        # hacemos redo
        return historial_redo.pop()
    return contenido_actual

def paste_function(contenido_total, texto_a_pegar, posicion_cursor):
    """
    Inserta el texto en la posición específica del cursor. Cortamos en dos pedazos para colocar el texto en el medio(cursor)

    contenido_total (str)  = Para guardar lo que el usuario viro
    texto_a_pegar (str) = Una pila de contenido del redo del usuario.
    posicion_cursor (int)  = Contenido del todo el archivo
    """
    nuevo_contenido = contenido_total[:posicion_cursor] + texto_a_pegar + contenido_total[posicion_cursor:]
    return nuevo_contenido

def visualizar_html(contenido):
    """
    Esta funcionalidad está sucia, (no funciona correctamente), la idea es visualizar el código escrito y lo hace pero JUUMM. 
    Quiero que recargué(refresh) la página si el archivo se llama igual a una pestaña del navegador por defecto que usa el 
    usuario y si no pues abre el navegador con la visualización del HTML/CSS

    contenido (str)  = Contenido del todo el archivo
    """
    global driver_preview
    nombre_archivo = "preview_temp.html"
    
    # 1. Siempre actualizamos el archivo físico primero
    try:
        with open(nombre_archivo, "w", encoding="utf-8") as f:
            f.write(contenido)
        ruta_absoluta = os.path.abspath(nombre_archivo)
        url_local = "file://" + ruta_absoluta
    except Exception as e:
        print(f"Error al escribir archivo temporal: {e}")
        return

    # 2. Intentamos la ruta "Pro" (Selenium para refrescar pestaña)
    if SELENIUM_AVAILABLE:
        try:
            navegador_vivo = False
            if driver_preview is not None:
                try:
                    _ = driver_preview.window_handles 
                    navegador_vivo = True
                except:
                    navegador_vivo = False

            if not navegador_vivo:
                chrome_options = Options()
                # Modo silencioso para que no ensucie la terminal
                chrome_options.add_argument("--log-level=3") 
                
                service = Service(ChromeDriverManager().install())
                driver_preview = webdriver.Chrome(service=service, options=chrome_options)
                driver_preview.get(url_local)
            else:
                driver_preview.refresh()
            
            print("Visualización optimizada (Selenium)")
            return # Si llegamos aquí, tuvimos éxito
        except Exception as e:
            print(f"Selenium no pudo iniciar (posible falta de Chromium). Usando navegador del sistema...")
            driver_preview = None # Limpiamos para el próximo intento

    # 3. Fallback: El método infalible (Navegador por defecto del sistema)
    # Esto abrirá una pestaña nueva, pero funcionará en cualquier PC del mundo.
    try:
        webbrowser.open(url_local)
        print("Visualización estándar (webbrowser)")
    except Exception as e:
        print(f"Error fatal: No se pudo abrir ningún navegador. {e}")