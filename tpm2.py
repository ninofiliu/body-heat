import serial
import time

# Configuration
NUM_LEDS = 678  # Number of LEDs to control
SERIAL_PORT = "/dev/ttyUSB0"  # Replace with your ESP32's serial port
BAUDRATE = 460800  # Match this with WLED's baud rate


def create_tpm2_packet(data: list[tuple[int, int, int]]):
    """
    Create a TPM2 packet from the given data.
    :param data: List of RGB values for each LED.
    :return: TPM2 packet as a bytearray.
    """
    # Flatten the list of tuples into a single list of integers
    flattened_data = [value for pixel in data for value in pixel]

    # Calculate the payload size (number of bytes)
    payload_size = len(flattened_data)

    # Create the TPM2 packet
    packet = bytearray()
    packet.append(0xC9)  # Packet start byte
    packet.append(0xDA)  # Packet type (data frame)
    packet.append((payload_size >> 8) & 0xFF)  # Payload size high byte
    packet.append(payload_size & 0xFF)  # Payload size low byte
    packet.extend(flattened_data)  # Payload (RGB data)
    packet.append(0x36)  # Packet end byte

    return packet


if __name__ == "__main__":
    with serial.Serial(SERIAL_PORT, BAUDRATE) as ser:
        for i in range(NUM_LEDS):
            t0 = time.time()
            tpm2_packet = create_tpm2_packet(
                [(1, 1, 1) if j < i else (10, 10, 10) for j in range(NUM_LEDS)]
            )
            ser.write(tpm2_packet)
            tf = time.time() - t0
            print(tf, 1 / tf)
