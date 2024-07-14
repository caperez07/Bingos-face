import PySimpleGUI as sg
import cv2
import time

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

# Vídeo padrão
default_video = 'videos/padraorobot.gif'
# Vídeos de reação específicos
loverobot_video = 'videos/loverobot.gif'
angryrobot_video = 'videos/angryrobot.gif'

# Layout da interface principal com um elemento de imagem para exibir o vídeo
layout = [
    [sg.Image(filename='', key='-IMAGE-', enable_events=True)],  # Habilita eventos para o elemento de imagem
]

# Criar a janela principal
window = sg.Window("Olhos de Robo", layout, finalize=True)

# Bind mouse down and mouse up events
window['-IMAGE-'].bind('<ButtonPress-1>', '-MOUSEDOWN-')
window['-IMAGE-'].bind('<ButtonRelease-1>', '-MOUSEUP-')

# Inicializar o vídeo atual e o gerador de frames
current_video = default_video
frame_generator = get_frame(current_video)

# Variáveis para detectar clique longo
mouse_down_time = None
long_click_duration = 0.5  # Duração em segundos para considerar um clique longo

# Loop de eventos
while True:
    event, values = window.read(timeout=20)  # Tempo de timeout para atualizar o vídeo
    if event == sg.WIN_CLOSED:
        break
    elif event == '-IMAGE--MOUSEDOWN-':  # Detecta mouse down
        mouse_down_time = time.time()
        print("Mouse down detected")
    elif event == '-IMAGE--MOUSEUP-':  # Detecta mouse up
        if mouse_down_time is not None:
            click_duration = time.time() - mouse_down_time
            mouse_down_time = None
            if click_duration >= long_click_duration:
                current_video = angryrobot_video  # Clique longo
                print("clique longo")
            else:
                current_video = loverobot_video  # Clique curto
                print("clique rapido")
            frame_generator = get_frame(current_video)

    try:
        # Atualizar o frame no elemento de imagem
        frame = next(frame_generator)
        window['-IMAGE-'].update(data=frame)
    except StopIteration:
        # Quando o vídeo terminar, voltar ao vídeo padrão
        current_video = default_video
        frame_generator = get_frame(current_video)

window.close()
