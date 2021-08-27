import paho.mqtt.client as mqtt
import time
import Elliptic_Curve_Functions
import  ast


ec = Elliptic_Curve_Functions.EllipticCurve(2, 3, 211)
G = (8,113)
User2_private_Key = 13
User2_Public_Key =ec.pointMultiplication(G,User2_private_Key)
key2 = str(User2_Public_Key)
receiver_variable = 0


mqttBroker = 'mqtt.eclipseprojects.io'
client = mqtt.Client("User2")
client.connect(mqttBroker)


def on_message(client, userdata, message):
    print("Recieved Message ", str(message.payload.decode("utf-8")))
    global receiver_variable
    receiver_variable = message.payload.decode("utf-8")
    return(message.payload.decode("utf-8"))


client.loop_start()
time.sleep(5)
client.subscribe("Message")
client.publish("User2",key2)
print("Sending Keys To User1" + key2)
client.on_message = on_message
encrypted_message = receiver_variable
print("Waiting for Public Keys from User1")

time.sleep(5)
client.loop_stop()

while True:
    encrypted_message = ast.literal_eval(receiver_variable)
    Decrypt = ec.decrpyt_user2(User2_private_Key,encrypted_message)
    time.sleep(2)
    break