from flask import Flask, request
from flask_cors import CORS, cross_origin  # Adicione esta linha
import base64
import os

app = Flask(__name__)
CORS(app)  # Adicione esta linha

@app.route('/upload', methods=['POST'])
@cross_origin()  # Adicione esta linha
def upload():

    image_name = request.get_json()['name']

    # obtém a string base64 da imagem do corpo da solicitação
    image_string = request.get_json()['image']
    
    # remove a parte 'data:image/png;base64,' da string
    image_string = image_string.split(",")[-1]

    # converte a string base64 de volta para bytes
    image_data = base64.b64decode(image_string)
    
    # cria um arquivo de imagem na pasta 'input'
    with open(f"C:/Users/otavi/OneDrive/Área de Trabalho/realesrgan-ncnn-vulkan-20220424-windows/input/{image_name}.png", 'wb') as f:
        f.write(image_data)

    return "Imagem recebida e salva com sucesso.", 200

if __name__ == '__main__':
    app.run(port=5000)

