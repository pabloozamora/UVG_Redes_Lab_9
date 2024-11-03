import json
import matplotlib.pyplot as plt
from kafka import KafkaConsumer
import time

# Inicializar listas para almacenar datos
temps = []
humidities = []
winds = []

def consume_data_from_kafka():
    # Configurar el consumidor de Kafka
    consumer = KafkaConsumer(
        "21780",
        bootstrap_servers='164.92.76.15:9092',
        value_deserializer=lambda m: json.loads(m.decode('utf-8')),
        group_id='grupo_estacion'
    )

    plt.ion()  # Activar modo interactivo para graficar en tiempo real
    fig, (ax_temp, ax_hum, ax_wind) = plt.subplots(3, 1, figsize=(10, 8))

    # Configuración de subgráficos
    ax_temp.set_title("Temperatura en Tiempo Real")
    ax_temp.set_xlabel("Lectura")
    ax_temp.set_ylabel("Temperatura (°C)")
    ax_hum.set_title("Humedad en Tiempo Real")
    ax_hum.set_xlabel("Lectura")
    ax_hum.set_ylabel("Humedad (%)")
    ax_wind.set_title("Dirección del Viento en Tiempo Real")
    ax_wind.axis("off")
    

    try:
        for mensaje in consumer:
            
            # Procesar mensaje recibido
            print("Datos recibidos:", mensaje.value)
            data = json.loads(mensaje.value)
            temps.append(data['temperatura'])
            humidities.append(data['humedad'])
            winds.append(data['direccion_viento'])

            # Limitar la cantidad de datos en las listas para mantener la gráfica manejable
            if len(temps) > 20:
                temps.pop(0)
                humidities.pop(0)
                winds.pop(0)

            # Graficar datos en tiempo real
            ax_temp.clear()
            ax_hum.clear()
            ax_wind.clear()
            
            ax_temp.plot(temps, label="Temperatura")
            ax_hum.plot(humidities, label="Humedad", color="orange")
            ax_temp.legend(loc="upper right")
            ax_hum.legend(loc="upper right")
            
            # Mostrar la dirección del viento como texto
            wind_text = f"Dirección del viento: {winds[-1]}"
            ax_wind.text(0.5, 0.5, wind_text, ha='center', va='center', fontsize=12, transform=ax_wind.transAxes)

            plt.pause(1)  # Pausar para actualizar la gráfica

    except KeyboardInterrupt:
        print("Interrumpido. Finalizando consumo de datos.")
    
    finally:
        plt.ioff()
        plt.show()

if __name__ == "__main__":
    consume_data_from_kafka()
