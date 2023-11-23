import serial
import time
from statistics import mean

def ler_valor_arduino(porta_serial):

    porta_serial.write(b"2")
    time.sleep(2)
    porta_serial.write(b'p')
    time.sleep(2)
    print("ALOP")
    valor_pesos = []

    try:
        for i in range(20):
            print("Aguardando leitura...")
            
            # Read data from the serial port
            porta_serial.write(b"1")
            valor_arduino = porta_serial.read(porta_serial.in_waiting).strip()
            
            # Convert the data to integers and filter out non-numeric values
            try:
                valor_float = float(valor_arduino)
                valor_pesos.append(valor_float)
                print(f"Valor do Arduino: {valor_arduino}")
            except ValueError:
                print(f"Ignore non-numeric value: {valor_arduino}")

            time.sleep(1)
    except KeyboardInterrupt:
        porta_serial.close()

    print(valor_pesos)
    media_peso = mean(valor_pesos)
    print(media_peso)
    return media_peso



# Abre a porta serial - ajuste a porta conforme necessário
# porta_serial = serial.Serial('COM4', 9600, timeout=1)

# Esta parte só será executada se este script for executado diretamente
#if __name__ == "__main__":
   # ler_valor_arduino(porta_serial)
def valor_arduino(esp_instance):
    setup = b"S"
    esp_instance.write(setup)
    for i in range(10):
        print("Aguardando leitura...")
        esp_instance.write(setup)

        # Assuming this is where you read data from the Arduino
        valor = esp_instance.readline()
       # print(esp_instance)
        # Decode the byte data to a string
        valor_str = valor.decode('latin-1')

        setup = b"Q"
        
        if valor_str:
            print(f"Valor do Arduino: {valor_str}")
        else:
            print("No data received from Arduino")

        #colocar comentarios no codigo arduino do catareco pra ver pq o motor nao mexe