/*
 Name:    LoadCell.ino
 Created: 13.11.2022 09:22:15
 Author:  hpete
*/

// balança
#include <HX711_ADC.h>
#include <ESP32Servo.h>
HX711_ADC loadCell(17,16);

//servo
Servo servomotor;
int pos = 0;

//passo
const int DIR = 12;
const int STEP = 14;
const int  steps_per_rev = 750;


void setup() {
  Serial.begin(9600);

  //balanca
  loadCell.begin();
  loadCell.start(4000);
  loadCell.setCalFactor(2000);

  //servo
  servomotor.attach(23);  // Pinagem do servo (pino GPIO)

  //passo
    pinMode(STEP, OUTPUT);
  pinMode(DIR, OUTPUT);
  digitalWrite(DIR, LOW);
  digitalWrite(STEP, HIGH);
  delayMicroseconds(1000);
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
 
void loop_servo() {
  Serial.print("entrou no loop servo");
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
      }
    
}  

void loop_passo(){
  Serial.print("entrou no loop passo");
  char command = read_serial();

  // Aguarda a primeira entrada no serial

  while(command != 'l' && command != 'r') {
    command = read_serial();
  }

  // Executa continuamente enquanto houver entradas no serial e o programa não estiver concluído
    
      if (command == 'l') {
        rotatePassoLixo();
      }
      if (command == 'r') {
        rotatePassoReciclavel();
      }
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

void rotatePassoLixo() {
  digitalWrite(DIR, LOW);
  Serial.println("Girando no sentido anti-horário...");

  for(int i = 0; i<steps_per_rev; i++)
  {
    digitalWrite(STEP, HIGH);
    delayMicroseconds(1000);
    digitalWrite(STEP, LOW);
    delayMicroseconds(1000);
  }
  delay(1000);

  digitalWrite(DIR, HIGH);
  Serial.println("Girando no sentido horário...");
  
  for(int i = 0; i<steps_per_rev; i++)
  {
    digitalWrite(STEP, HIGH);
    delayMicroseconds(2000);
    digitalWrite(STEP, LOW);
    delayMicroseconds(2000);
  }
  delay(1000); 
}

void rotatePassoReciclavel() {
    digitalWrite(DIR, LOW);
  Serial.println("Girando no sentido anti-horário...");

  for(int i = 0; i<steps_per_rev/2; i++)
  {
    digitalWrite(STEP, HIGH);
    delayMicroseconds(1000);
    digitalWrite(STEP, LOW);
    delayMicroseconds(1000);
  }
  delay(1000);

  digitalWrite(DIR, HIGH);
  Serial.println("Girando no sentido horário...");
  
  for(int i = 0; i<steps_per_rev/2; i++)
  {
    digitalWrite(STEP, HIGH);
    delayMicroseconds(2000);
    digitalWrite(STEP, LOW);
    delayMicroseconds(2000);
  }
  delay(1000); 
}
