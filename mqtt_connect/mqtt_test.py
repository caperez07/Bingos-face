import asyncio
from gmqtt import Client as MQTTClient

# Função de callback para quando o cliente se conectar ao broker
def on_connect(client, flags, rc, properties):
    print('Conectado com sucesso!')

# Função de callback para quando a mensagem for publicada
def on_publish(client, mid):
    print(f'Mensagem publicada com sucesso com mid: {mid}')

def on_message(client, userdata, msg):
    print(f"Mensagem recebida no tópico {msg.topic}: {msg.payload.decode()}")

async def send_mqtt():
    # Cria o cliente MQTT com um ID único
    client = MQTTClient("romanelsons")

    # Define as funções de callback
    client.on_connect = on_connect
    client.on_publish = on_publish
    client.on_message = on_message

    # Conecta ao broker público HiveMQ
    await client.connect('mqtt-dashboard.com')
    client.subscribe('bitogay')

    # print(client.on_message)

    # Aguarda um curto intervalo para garantir que a mensagem seja publicada
    await asyncio.sleep(0.5)

    # Desconecta do broker
    await client.disconnect()

# import paho.mqtt.client as mqtt

# def on_subscribe(client, userdata, mid, granted_qos):
#     print("Subscribed: "+str(mid)+" "+str(granted_qos))

# # Função callback quando a conexão for estabelecida com o broker
# def on_connect(client, userdata, flags, rc):
#     print(f"Conectado ao broker MQTT com código de resultado: {rc}")
#     # Inscrevendo-se no tópico desejado após a conexão
#     client.subscribe("bitogay")

# # Função callback quando uma mensagem for recebida
# def on_message(client, userdata, msg):
#     print(f"Mensagem recebida no tópico {msg.topic}: {msg.payload.decode()}")

# # Criar um cliente MQTT
# client = mqtt.Client()

# # Definir as funções de callback
# client.on_subscribe = on_subscribe
# client.on_connect = on_connect
# client.on_message = on_message

# # Conectar ao broker MQTT (substitua "broker.hivemq.com" pelo endereço do seu broker)
# client.connect("mqtt-dashboard.com", 8884, 60)

# # Iniciar o loop de processamento de rede MQTT
# client.loop_forever()
