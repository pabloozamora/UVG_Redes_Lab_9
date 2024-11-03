# Decodificación de los datos del mensaje de 3 bytes
def decode_data(encoded_data):
    # Convertir bytes a entero
    packed_data = int.from_bytes(encoded_data, byteorder='big')

    # Extraer cada componente usando desplazamientos y máscaras de bits
    temp_scaled = (packed_data >> 10) & 0x3FFF
    humidity = (packed_data >> 3) & 0x7F
    wind_encoded = packed_data & 0x7

    # Reescalar la temperatura
    temperature = (temp_scaled / (2**14 - 1)) * 110

    # Direcciones de viento decodificadas
    wind_directions = ["N", "NO", "O", "SO", "S", "SE", "E", "NE"]
    wind_direction = wind_directions[wind_encoded]

    return {
        "temperatura": round(temperature, 2),
        "humedad": humidity,
        "direccion_viento": wind_direction
    }