import datetime
import paho.mqtt.client as mqtt
import time
from threading import Thread
import psycopg2 as psycopg2
from datetime import datetime, timezone

MQTT_HOST = '34.95.158.211'
MQTT_PORT = 1883
MQTT_CLIENT_ID = 'conecttec_sub'
MQTT_USER = 'FIC'
MQTT_PASSWORD = 'ConectTecOnly'
TOPIC_Status = 'FIC/+/FP/+/Status'
TOPIC_Reserve = 'FIC/+/FP/+/Reserve'
TOPIC_Delivery = 'FIC/+/FP/+/Delivery'
TOPIC_Authorize = 'FIC/+/FP/+/Authorize'
TOPIC_Versao = 'FIC/+/FP/+/Authorize'
Topic_Online = 'FIC/SerialNumber/+/Status'


#Conexão postgres
db_conn = psycopg2.connect(host='192.168.3.101',
                         database='postgres',
                         user='postgres',
                         password='01042006')


def on_connect_status(mqtt_client, user_data, flags, conn_result):
    mqtt_client.subscribe(TOPIC_Status)


def on_connect_reserva(mqtt_client, user_data, flags, conn_result):
    mqtt_client.subscribe(TOPIC_Reserve)


def on_connect_Delivery(mqtt_client, user_data, flags, conn_result):
    mqtt_client.subscribe(TOPIC_Delivery)


def on_connect_authorize(mqtt_client, user_data, flags, conn_result):
    mqtt_client.subscribe(TOPIC_Authorize)


def on_connect_online(mqtt_client, user_data, flags, conn_result):
    mqtt_client.subscribe(Topic_Online, 0)


def on_message(mqtt_client, user_data, message):
    payload = message.payload.decode('ISO-8859-1')
    db_conn = user_data['db_conn']
    cursor = db_conn.cursor()
    dt = datetime.now(timezone.utc)
    cursor.execute("ROLLBACK")
    cursor.execute("INSERT INTO sensors_data (topic, payload, created_at) VALUES (%s, %s, %s)", (message.topic, payload, dt,))
    print(f"Received `{message.payload.decode('ISO-8859-1')}` from `{message.topic}` topic")
    db_conn.commit()
    cursor.close()


def main():
    db_conn = psycopg2.connect(host='192.168.3.101',
                               database='postgres',
                               user='postgres',
                               password='01042006')
    # db_conn = sqlite3.connect(DATABASE_FILE)
    sql = """
            CREATE TABLE IF NOT EXISTS sensors_data (
                topic TEXT NOT NULL,
                payload TEXT NOT NULL,
                created_at INTEGER NOT NULL,
                logged TEXT
                )
            """
    cursor = db_conn.cursor()
    cursor.execute(sql)
    cursor.close()

    t1 = Thread(target=status)
    t2 = Thread(target=reserva)
    t3 = Thread(target=authorize)
    t4 = Thread(target=delivery)
    t5 = Thread(target=online)

    t1.start()
    time.sleep(3)
    t2.start()
    time.sleep(3)
    t3.start()
    time.sleep(3)
    t4.start()
    time.sleep(3)
    t5.start()



def status():

    mqtt_client = mqtt.Client(MQTT_CLIENT_ID)
    mqtt_client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
    mqtt_client.user_data_set({'db_conn': db_conn})

    mqtt_client.on_connect = on_connect_status
    mqtt_client.on_message = on_message

    mqtt_client.connect(MQTT_HOST, MQTT_PORT)
    mqtt_client.loop_forever()


def reserva():

    mqtt_client = mqtt.Client(MQTT_CLIENT_ID)
    mqtt_client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
    mqtt_client.user_data_set({'db_conn': db_conn})

    mqtt_client.on_connect = on_connect_reserva
    mqtt_client.on_message = on_message

    mqtt_client.connect(MQTT_HOST, MQTT_PORT)
    mqtt_client.loop_forever()


def online():
    mqtt_client = mqtt.Client()

    mqtt_client.user_data_set({'db_conn': db_conn})

    mqtt_client.on_connect = on_connect_online
    mqtt_client.on_message = on_message

    mqtt_client.connect(MQTT_HOST, MQTT_PORT)

    mqtt_client.loop_forever()


def delivery():

    mqtt_client = mqtt.Client(MQTT_CLIENT_ID)
    mqtt_client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
    mqtt_client.user_data_set({'db_conn': db_conn})

    mqtt_client.on_connect = on_connect_Delivery
    mqtt_client.on_message = on_message

    mqtt_client.connect(MQTT_HOST, MQTT_PORT)
    mqtt_client.loop_forever()


def authorize():

    mqtt_client = mqtt.Client(MQTT_CLIENT_ID)
    mqtt_client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
    mqtt_client.user_data_set({'db_conn': db_conn})

    mqtt_client.on_connect = on_connect_authorize
    mqtt_client.on_message = on_message

    mqtt_client.connect(MQTT_HOST, MQTT_PORT)
    mqtt_client.loop_forever()


main()

