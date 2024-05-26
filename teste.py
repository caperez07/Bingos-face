import PySimpleGUI as sg
import cv2
import numpy as np

# Função para tocar o vídeo
def play_video(video_path):
    cap = cv2.VideoCapture(video_path)
    window_name = 'Video Player'
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow(window_name, frame)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Layout da interface principal
layout = [
    [sg.Text("Clique no botão para ver a reação!")],
    [sg.Button("Mostrar Reação", key='-SHOW_REACTION-')]
]

# Criar a janela principal
window = sg.Window("Olhos de Robo", layout)

# Loop de eventos
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    elif event == '-SHOW_REACTION-':
        # Chame a função para tocar o vídeo
        play_video('robot.gif') 

window.close()