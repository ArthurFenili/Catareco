import serial
import time
from statistics import mean

def ler_valor_arduino(porta_serial, total_bottles, total_cans, total_not_accepted):

    # 1-> chamar camera e ver o que é e quantas tem
    # 2-> se latinha ou pet: chamar o servo motor pra girar pro lado certo
    #     se não: nop
    # 3-> se latinha ou pet: chamar motor de passo pra abrir 45°
    #     se não: chamar motor de passo pra abrir 90°
    # 4-> fazer a leitura da balança x ou y e retornar o peso
    
    try:   
        if total_not_accepted > 0:
            time.sleep(2)
        elif total_bottles > 0 and total_cans == 0:
            porta_serial.write(b"3")
            porta_serial.flush()
            time.sleep(2)
            porta_serial.write(b"l")
            porta_serial.flush()
            time.sleep(2)
            porta_serial.write(b"4")
            porta_serial.flush()
            time.sleep(2)
            porta_serial.write(b"r")
            porta_serial.flush()
            time.sleep(2)
        elif total_cans > 0 and total_bottles == 0:
            porta_serial.write(b"3")
            porta_serial.flush()
            time.sleep(2)
            porta_serial.write(b"p")
            porta_serial.flush()
            time.sleep(2)
            porta_serial.write(b"4")
            porta_serial.flush()
            time.sleep(2)
            porta_serial.write(b"r")
            porta_serial.flush()
            time.sleep(2)


    except Exception as e:
        print(f"Erro ao enviar mensagem para Arduino: {e}")

    valor_pesos = []

    try:
        for i in range(40):
            print("Aguardando leitura...")
            
            # Read data from the serial port
            if total_bottles > 0:
                porta_serial.write(b"2")
            elif total_cans > 0:
                porta_serial.write(b"1")
            else:
                break
            valor_arduino = porta_serial.read(porta_serial.in_waiting).strip()
            
            # Convert the data to integers and filter out non-numeric values
            try:
                valor_float = float(valor_arduino)
                if i > 25:
                    valor_pesos.append(valor_float)
                    print(f"Valor do Arduino: {valor_arduino}")
            except ValueError:
                print(f"Ignore non-numeric value: {valor_arduino}")

            time.sleep(1)
    except KeyboardInterrupt:
        porta_serial.close()

    print(valor_pesos)
    if len(valor_pesos) > 0:
        media_peso = mean(valor_pesos)
    else:
        media_peso = 0
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
