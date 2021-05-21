#include <FastLED.h>

FASTLED_USING_NAMESPACE
#if defined(FASTLED_VERSION) && (FASTLED_VERSION < 3001000)
#warning "Requires FastLED 3.1 or later; check github for latest code."
#endif


#define PIN 12        // кнопка подключена сюда (PIN --- КНОПКА --- GND)
#define DATA_PIN    13
#define LED_TYPE    WS2812B
#define COLOR_ORDER GRB
#define NUM_LEDS    5

#define BRIGHTNESS          255
#define FRAMES_PER_SECOND  120


CRGB leds[NUM_LEDS];

#include "GyverButton.h"
GButton butt1(PIN);

#include "GyverTimer.h"
GTimer myTimer(MS);               // создать миллисекундный таймер

void setup() {
  //Установить соединение с монитором порта
  Serial.begin(9600);
  FastLED.addLeds<LED_TYPE, DATA_PIN, COLOR_ORDER>(leds, NUM_LEDS).setCorrection(TypicalLEDStrip);
  FastLED.setBrightness(BRIGHTNESS);

}
bool flag = false; // Изначально нет движения

typedef void (*SimplePatternList[])();
SimplePatternList gPatterns = {confetti, rainbow, sinelon, juggle};

uint8_t gCurrentPatternNumber = 0; // Index number of which pattern is current
uint8_t gHue = 0; // rotating "base color" used by many of the patterns

void loop() {
  butt1.tick();
  //Считываем пороговое значение с порта А0
  if ((analogRead(A0) > 500) && (flag == false))   {
    Serial.println("Motion");
    flag = true;
    myTimer.setTimeout(5000);
    if (butt1.state()) {
      gCurrentPatternNumber = 0;
    }
    
    
  }



  if (butt1.isRelease()) Serial.println("Release");     // отпускание кнопки (+ дебаунс)


  if (butt1.isHolded()) Serial.println("Holded");       // проверка на удержание
  if (myTimer.isReady()){ 
    flag = 0;
    gCurrentPatternNumber = random(1,3); 
  }

  gPatterns[gCurrentPatternNumber]();
  // send the 'leds' array out to the actual LED strip
  FastLED.show();
  // insert a delay to keep the framerate modest
  FastLED.delay(1000 / FRAMES_PER_SECOND);

  EVERY_N_MILLISECONDS( 20 ) {
    gHue++;  // slowly cycle the "base color" through the rainbow
  }



}


void rainbow()
{
  // FastLED's built-in rainbow generator
  fill_rainbow( leds, NUM_LEDS, gHue, 15);
}

void confetti()
{
  // random colored speckles that blink in and fade smoothly
  fadeToBlackBy(leds, NUM_LEDS, 30);
  int pos = random16(NUM_LEDS);
  leds[pos] += CHSV( gHue + random8(64), 200, 255);
}

void sinelon()
{
  // a colored dot sweeping back and forth, with fading trails
  fadeToBlackBy( leds, NUM_LEDS, 20);
  int pos = beatsin16( 13, 0, NUM_LEDS - 1 );
  leds[pos] += CHSV( gHue, 255, 192);
}

void juggle() {
  // eight colored dots, weaving in and out of sync with each other
  fadeToBlackBy( leds, NUM_LEDS, 20);
  byte dothue = 0;
  for ( int i = 0; i < 8; i++) {
    leds[beatsin16( i + 7, 0, NUM_LEDS - 1 )] |= CHSV(dothue, 200, 255);
    dothue += 32;
  }
}
