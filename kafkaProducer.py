import random
import json
import time
from kafka import KafkaProducer

def generate_data():
    
    # Media y desviación estándar para la generación de temperaturas y humedad
    mu = 30
    sigma = 10
    
    # Generación de datos para cada sensor
    temperature = round(max(0, min(110, random.normalvariate(mu=mu, sigma=sigma))), 2)
    humidity = int(max(0, min(100, random.normalvariate(mu=mu, sigma=sigma))))
    wind = random.choice(["N", "NO", "O", "SO", "S", "SE", "E", "NE"])  # Dirección del viento

    # Crear un diccionario con los datos
    data = {
        "temperatura": temperature,
        "humedad": humidity,
        "direccion_viento": wind
    }

    # Convertir el diccionario a JSON
    data_json = json.dumps(data)
    return data_json

def send_data_to_kafka():
    # Configurar el productor de Kafka
    producer = KafkaProducer(
        bootstrap_servers='164.92.76.15:9092',
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

    topic = "21780"

    try:
        while True:
            # Generar datos del sensor
            data = generate_data()
            print("Enviando datos:", data)

            # Enviar datos al servidor Kafka
            producer.send(topic, value=data)

            # Espera entre 15 y 30 segundos antes de enviar el siguiente dato
            time.sleep(random.randint(15, 30))
    except KeyboardInterrupt:
        print("Interrumpido. Finalizando envío de datos.")
    finally:
        producer.close()

if __name__ == "__main__":
    send_data_to_kafka()
