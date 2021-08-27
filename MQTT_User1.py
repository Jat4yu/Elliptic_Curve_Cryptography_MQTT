import paho.mqtt.client as mqtt
import time
import Elliptic_Curve_Functions
from ast import literal_eval as make_tuple


MESSAGE = 'This00is00a00test00message'
# Since we are using base36 we can not use the space character
# Feel free to change the MESSAGE and try out different combinations
# (Note : Only use Base36, ie any of '0123456789abcedfghijklmnopqrstuvwxyz' character in message)

ec = Elliptic_Curve_Functions.EllipticCurve(2, 3, 211)
G = (8, 113)
User1_Private_Key = 7
User1_Public_Key = ec.pointMultiplication(G, User1_Private_Key)
random_num = 6
receiver_variable = 0


mqttBroker = 'mqtt.eclipseprojects.io'
client = mqtt.Client("Message")
client.connect(mqttBroker)


def on_message(client, userdata, messages):  # Receiving Data from user2
    print("Received Message ", str(messages.payload.decode("utf-8")))
    global receiver_variable
    receiver_variable = messages.payload.decode("utf-8")
    return True


client.loop_start()
client.subscribe("User2")
print("Waiting for User2 Public key")
client.on_message = on_message
time.sleep(3)
client.loop_stop()

received = True
while received:
    message = str(User1_Public_Key)
    client.publish("Message", message)
    print("Publishing Keys " + str(message) + "To topic")
    time.sleep(2)
    client.on_message = on_message
    received_Public_key = receiver_variable
    received_Public_key = make_tuple(received_Public_key)
    if client.on_message:
        received = False

Encrypted_message = str(ec.encryption_user1(7, received_Public_key, message=MESSAGE))
sending_message = True

while sending_message:
    message = Encrypted_message
    client.publish("Message", message)
    print("Published " + str(message) + " To topic Message")
    sending_message = False
