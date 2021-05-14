#define PIN 12        // кнопка подключена сюда (PIN --- КНОПКА --- GND)

#include "GyverButton.h"
GButton butt1(PIN);

#include "GyverTimer.h"
GTimer myTimer(MS);               // создать миллисекундный таймер

void setup() {
  //Установить соединение с монитором порта
  Serial.begin(9600);

}
bool flag = false; // Изначально нет движения
void loop() {
  butt1.tick();
  //Считываем пороговое значение с порта А0
  

  if ((analogRead(A0) > 500) && (flag == false))   {
    Serial.println("Motion");
    flag = true;
    myTimer.setTimeout(5000);

  }

  if (butt1.isRelease()) Serial.println("Release");     // отпускание кнопки (+ дебаунс)
  if (butt1.isHolded()) Serial.println("Holded");       // проверка на удержание
  if (myTimer.isReady()) flag = 0;
}
