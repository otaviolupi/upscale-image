import time
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
import subprocess
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from PIL import Image
import time

class HandlerOrigin(FileSystemEventHandler):
    def on_created(self, event):
        filename = os.path.basename(event.src_path)
        print(f'Novo arquivo {filename} foi adicionado.')
        subprocess.call('realesrgan-ncnn-vulkan.exe -i input -o output', shell=True)



class HandlerDestiny(FileSystemEventHandler):
    def on_created(self, event):
        time.sleep(1)  # espera um pouco para garantir que o arquivo esteja completamente escrito
        file_path = event.src_path  # obtemos o caminho completo do arquivo
        filename = os.path.basename(file_path)

        if os.path.isfile(file_path):
            # Converte a imagem em PDF
            output_filename = filename.rsplit(".", 1)[0] + ".pdf"  # Nome do arquivo PDF
            pdf_path = "C:/Users/otavi/OneDrive/Área de Trabalho/realesrgan-ncnn-vulkan-20220424-windows/print/" + output_filename
            img = Image.open(file_path)
            img = img.resize((int(43*inch/2.54), int(100*inch/2.54)), Image.ANTIALIAS)  # Redimensiona a imagem
            img.save(file_path)  # Salva a imagem redimensionada

            c = canvas.Canvas(pdf_path, pagesize=(43*inch/2.54, 100*inch/2.54))  # Tamanho específico em cm
            c.drawImage(file_path, 0, 0, 43*inch/2.54, 100*inch/2.54)  # Desenha a imagem no PDF
            c.save()  # Salva o arquivo PDF
            print(f"PDF {pdf_path} foi criado.")
            
            input_path = "C:/Users/otavi/OneDrive/Área de Trabalho/realesrgan-ncnn-vulkan-20220424-windows/input/" + filename
            if os.path.isfile(input_path):
                os.remove(input_path)
                print(f"Arquivo {input_path} foi deletado.")
        else:
            print("Arquivo não encontrado.")

def monitorar_pasta_origem(pasta):
    event_handler = HandlerOrigin()
    observer = Observer()
    observer.schedule(event_handler, pasta, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

def monitorar_pasta_destino(pasta):
    event_handler = HandlerDestiny()
    observer = Observer()
    observer.schedule(event_handler, pasta, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == '__main__':
    threading.Thread(target=monitorar_pasta_origem, args=('C:/Users/otavi/OneDrive/Área de Trabalho/realesrgan-ncnn-vulkan-20220424-windows/input',)).start()
    threading.Thread(target=monitorar_pasta_destino, args=('C:/Users/otavi/OneDrive/Área de Trabalho/realesrgan-ncnn-vulkan-20220424-windows/output',)).start()
