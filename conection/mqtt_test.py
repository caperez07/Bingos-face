# import asyncio
# from gmqtt import Client as MQTTClient

# # Função de callback para quando o cliente se conectar ao broker
# def on_connect(client, flags, rc, properties):
#     print('Conectado com sucesso!')

# # Função de callback para quando a mensagem for publicada
# def on_publish(client, mid):
#     print(f'Mensagem publicada com sucesso com mid: {mid}')

# def on_message(client, topic, payload, qos, properties):
#     print(f"Mensagem recebida no tópico {topic}: {payload.decode()}")

# async def send_mqtt():
#     # Cria o cliente MQTT com um ID único
#     client = MQTTClient("pedraazul")

#     # Define as funções de callback
#     client.on_connect = on_connect
#     client.on_publish = on_publish
#     client.on_message = on_message

#     # Define o nome de usuário e a senha antes de conectar
#     client.set_auth_credentials(username='PUBLIC', password='public')

#     try:
#         # Conecta ao broker público HiveMQ
#         # await client.connect('broker.hivemq.com', 1883)
#         await client.connect('smartcampus.maua.br', 1883)
#         print("conectado")

#         client.subscribe('/test/test/test/testcaio')

#         # Aguarda e mantém a conexão ativa
#         await asyncio.sleep(60)  # Mantém a conexão por 30 segundos (ou ajuste o tempo)
#     except Exception as e:
#         print(f"Erro no envio MQTT: {e}")
#     finally:
#         print("Client Disconnect!")
#         await client.disconnect()

# IMPORTS ---------------------------------------------------------------------
import paho.mqtt.client as mqtt

# VARIABLES -------------------------------------------------------------------
# MQTT
# HOST = "smartcampus.maua.br"
HOST = "192.168.105.48"
# PORT = 1883
# USER = "PUBLIC"
# PASSWORD = "public"
# SUB_TOPIC = "/test/test/test/testcaio_sub"
# PUB_TOPIC = "/test/test/test/testcaio_pub"
TOPIC = "bingo-teste"


# FUNCTIONS -------------------------------------------------------------------
# MQTT
def on_connect(mqttc, obj, flags, rc):
    print("rc: " + str(rc))


def on_message(mqttc, obj, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    # mqttc.publish(PUB_TOPIC, "PONG!", 0) # CB debug

def on_publish(mqttc, obj, mid):
    print("mid: " + str(mid))

def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

def on_log(mqttc, obj, level, string):
    print(string)

# MAIN ------------------------------------------------------------------------
# MQTT
def main():
    mqttc = mqtt.Client()
    mqttc.on_message = on_message
    mqttc.on_connect = on_connect
    mqttc.on_publish = on_publish
    mqttc.on_subscribe = on_subscribe
    # mqttc.username_pw_set(USER, PASSWORD)
    # mqttc.connect(HOST, PORT, 60)
    mqttc.connect(HOST)
    # mqttc.subscribe(SUB_TOPIC, 0)
    mqttc.subscribe(TOPIC)
    


    mqttc.loop_forever()
    
    
if __name__ == "__main__":
    main()
# -----------------------------------------------------------------------------

