import paho.mqtt.client as mqtt
import threading
from InterfaceVisualBingo import listen_face

HOST = "192.168.105.48"
TOPIC = "bingo-teste"

def on_connect(mqttc, obj, flags, rc):
    print("rc: " + str(rc))

def on_message(mqttc, obj, msg):
    byte_string = msg.payload
    decoded_string = byte_string.decode('utf-8')
    clean_string = decoded_string.strip('"')
    print("MENSAGEM: " + str(clean_string))

    listen_face()
    # return clean_string

def on_publish(mqttc, obj, mid):
    print("mid: " + str(mid))

def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

def on_log(mqttc, obj, level, string):
    print(string)

# def recieve_mqtt():
# def main():
#     mqttc = mqtt.Client()
#     mqttc.on_message = on_message
#     mqttc.on_connect = on_connect
#     mqttc.on_publish = on_publish
#     mqttc.on_subscribe = on_subscribe

#     mqttc.connect(HOST)
#     mqttc.subscribe(TOPIC)

#     mqttc.loop_forever()

# Função que roda o loop MQTT em uma thread separada
def mqtt_thread():
    mqttc = mqtt.Client()
    mqttc.on_message = on_message
    mqttc.on_connect = on_connect
    mqttc.on_publish = on_publish
    mqttc.on_subscribe = on_subscribe

    mqttc.connect(HOST)
    mqttc.subscribe(TOPIC)
    
    mqttc.loop_forever()  # Este loop rodará em uma thread separada

# Função para iniciar o cliente MQTT em uma thread
def start_mqtt():
    mqtt_thread_instance = threading.Thread(target=mqtt_thread)
    mqtt_thread_instance.daemon = True  # Daemon permite que o programa feche corretamente
    mqtt_thread_instance.start()

    
# if __name__ == "__main__":
#     main()

