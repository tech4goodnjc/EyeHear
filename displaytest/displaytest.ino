#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#define OLED_RESET 0  // GPIO0
//Adafruit_SSD1306 display(OLED_RESET);
Adafruit_SSD1306 display(128, 64, &Wire, OLED_RESET); // initialise display
//Adafruit_SSD1306 OLED(128, 64);

 
void setup() 
{
   display.begin(SSD1306_SWITCHCAPVCC, 0x3C);
   display.setTextSize(2);
   display.setTextColor(WHITE);
}
 
void loop() {
 
  // Clear the buffer.
  display.clearDisplay();
 
  display.setCursor(0, 0); 
  display.println("Hello world!@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@");
 
  display.display();
  delay(1000);
 
}
 
//void setup()   {
//  OLED.begin();
//  OLED.clearDisplay();
//
//  //Add stuff into the 'display buffer'
//  OLED.setTextWrap(false);
//  OLED.setTextSize(2);
//  OLED.setTextColor(WHITE);
//  OLED.setCursor(0,0);
//  OLED.println("vanakkam");
//  OLED.display(); //output 'display buffer' to screen  
//} 
// 
//void loop() {
//  OLED.println("vanakkam");
//  OLED.display(); //output 'display buffer' to screen 
//}
