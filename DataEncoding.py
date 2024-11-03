# Codificación de los datos en un mensaje de 3 bytes
def encode_data(temperature, humidity, wind_direction):
    # Escalar temperatura para ajustarla a un valor entre 0 y 16383 (14 bits)
    temp_scaled = int((temperature / 110) * (2**14 - 1))

    # Direcciones de viento mapeadas a valores de 3 bits
    wind_directions = {"N": 0, "NO": 1, "O": 2, "SO": 3, "S": 4, "SE": 5, "E": 6, "NE": 7}
    wind_encoded = wind_directions[wind_direction]

    # Empaquetar los datos en 3 bytes (24 bits)
    packed_data = (temp_scaled << 10) | (humidity << 3) | wind_encoded

    # Convertir a bytes
    return packed_data.to_bytes(3, byteorder='big')
