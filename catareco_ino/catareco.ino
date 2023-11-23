/*
 Name:    LoadCell.ino
 Created: 13.11.2022 09:22:15
 Author:  hpete
*/

// the setup function runs once when you press reset or power the board
#include <HX711_ADC.h>
#include <ESP32Servo.h>

Servo servomotor;
int pos = 0;

HX711_ADC loadCell(17,16);

void setup() {
  Serial.begin(9600);

  servomotor.attach(23);  // Pinagem do servo (pino GPIO)
  
  loadCell.begin();
  loadCell.start(4000);
  loadCell.setCalFactor(2000);
}

void loop() {
  char command = Serial.read();
  if (command == '1') {
    loop_balanca();
  }
  if (command == '2') {
    loop_servo();
  }
  if(command == '3') {
    loop_passo();
  }



}

// the loop function runs over and over again until power down or reset
void loop_balanca() {
  static float load = 0.0;
  static unsigned long waitTime = millis();

  if (loadCell.update()) load = loadCell.getData();

  if ((millis() - waitTime) > 250) {
    //Serial.print("Load value: ");
    Serial.println(load);
    delay(1000);
    waitTime = millis();
  }
  
}


char read_serial(){
  char command;
  while (!Serial.available()) {
    // Aqui você pode adicionar outros processamentos ou atrasos, se necessário
    if (Serial.available() > 0) {
      command = Serial.read();
      return command;
    }
  }
}
 
void loop_servo() {
  Serial.print("SERVO");
  char command = read_serial();

  // Aguarda a primeira entrada no serial

  while(command != 'p' && command != 'l') {
    command = read_serial();
  }

  // Executa continuamente enquanto houver entradas no serial e o programa não estiver concluído
    
      if (command == 'l') {
        rotateServoLata();
      }
      if (command == 'p') {
        rotateServoPet();
        Serial.println("saiu");
      }
    
}  

void loop_passo(){

}




void rotateServoLata() {
  for (pos = 0; pos <= 70; pos += 1) {
    servomotor.write(pos);
    delay(10);
  }
}

void rotateServoPet() {
  for (pos = 70; pos >= 0; pos -= 1){
    servomotor.write(pos);
    delay(10);
  }
}
