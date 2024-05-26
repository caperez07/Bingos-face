import PySimpleGUI as sg
import cv2
import numpy as np
from PIL import Image, ImageTk

# Função para capturar frames do vídeo e convertê-los para um formato que o PySimpleGUI possa exibir
def get_frame(video_path):
    cap = cv2.VideoCapture(video_path)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.resize(frame, (640, 480))  # Ajustar o tamanho do frame se necessário
        imgbytes = cv2.imencode('.png', frame)[1].tobytes()
        yield imgbytes
    cap.release()

# Layout da interface principal com um elemento de imagem para exibir o vídeo
layout = [
    [sg.Image(filename='', key='-IMAGE-')],
]

# Criar a janela principal
window = sg.Window("Olhos de Robo", layout)

# Inicializar o gerador de frames
frame_generator = get_frame('videos/robot.gif')

# Loop de eventos
while True:
    event, values = window.read(timeout=20)  # Tempo de timeout para atualizar o vídeo
    if event == sg.WIN_CLOSED:
        break
    try:
        # Atualizar o frame no elemento de imagem
        frame = next(frame_generator)
        window['-IMAGE-'].update(data=frame)
    except StopIteration:
        # Quando o vídeo terminar, reinicializar o gerador de frames
        frame_generator = get_frame('videos/robot.gif')

window.close()
