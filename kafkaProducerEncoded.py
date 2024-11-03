import random
import time
from kafka import KafkaProducer

from DataEncoding import encode_data

def generate_data():
    
    # Media y desviación estándar para la generación de temperaturas y humedad
    mu = 30
    sigma = 10
    
    # Generación de datos para cada sensor
    temperature = round(max(0, min(110, random.normalvariate(mu=mu, sigma=sigma))), 2)
    humidity = int(max(0, min(100, random.normalvariate(mu=mu, sigma=sigma))))
    wind = random.choice(["N", "NO", "O", "SO", "S", "SE", "E", "NE"])  # Dirección del viento
    
    return temperature, humidity, wind

def send_data_to_kafka():
    producer = KafkaProducer(bootstrap_servers='164.92.76.15:9092')
    topic = "21780"

    try:
        while True:
            # Generar datos del sensor
            temperature, humidity, wind_direction = generate_data()
            
            data = {
                "temperatura": temperature,
                "humedad": humidity,
                "direccion_viento": wind_direction
            }
            
            print('Datos generados:', data)
            encodedData = encode_data(temperature, humidity, wind_direction)
            print("Enviando datos codificados:", encodedData)
            print('\n')

            # Enviar datos al servidor Kafka
            producer.send(topic, value=encodedData)
            time.sleep(random.randint(15, 30))

    except KeyboardInterrupt:
        print("Interrumpido. Finalizando envío de datos.")
    finally:
        producer.close()

if __name__ == "__main__":
    send_data_to_kafka()
