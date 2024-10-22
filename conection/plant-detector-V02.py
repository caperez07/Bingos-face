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
