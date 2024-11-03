from kafka import KafkaConsumer
import matplotlib.pyplot as plt

from DataDecoding import decode_data

# Inicializar listas para almacenar datos
temperaturas = []
humedades = []
direcciones_viento = []

def consume_data_from_kafka():
    consumer = KafkaConsumer(
        "21780",
        bootstrap_servers='164.92.76.15:9092',
        group_id='grupo_estacion'
    )

    plt.ion()
    fig, (ax_temp, ax_hum, ax_wind) = plt.subplots(3, 1, figsize=(10, 8))
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
            
            print("Datos recibidos:", mensaje.value)
            data = decode_data(mensaje.value) # Decodificar el mensaje de 24 bits
            
            print('Datos decodificados:', data)
            print('\n')
            
            temperaturas.append(data['temperatura'])
            humedades.append(data['humedad'])
            direcciones_viento.append(data['direccion_viento'])

            if len(temperaturas) > 20:
                temperaturas.pop(0)
                humedades.pop(0)
                direcciones_viento.pop(0)

            ax_temp.clear()
            ax_hum.clear()
            ax_wind.clear()
            
            ax_temp.plot(temperaturas, label="Temperatura")
            ax_hum.plot(humedades, label="Humedad", color="orange")
            ax_temp.legend(loc="upper right")
            ax_hum.legend(loc="upper right")

            wind_text = f"Dirección del viento: {direcciones_viento[-1]}"
            ax_wind.text(0.5, 0.5, wind_text, ha='center', va='center', fontsize=12, transform=ax_wind.transAxes)

            plt.pause(1)
    except KeyboardInterrupt:
        print("Interrumpido. Finalizando consumo de datos.")
    finally:
        plt.ioff()
        plt.show()

if __name__ == "__main__":
    consume_data_from_kafka()
