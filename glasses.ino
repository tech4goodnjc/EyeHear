#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <WiFiManager.h>

Adafruit_SSD1306 display(128, 64, &Wire, -1);

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  WiFiManager wifiManager;
  wifiManager.resetSettings();
  wifiManager.autoConnect("AP-NAME", "AP-PASSWORD");
 
  while (WiFi.status() != WL_CONNECTED) {
 
    delay(1000);
    Serial.println("Connecting...");
 
  }
  Serial.println("Connected to WiFi Network");
  display.begin();
  display.clearDisplay();

  //Add stuff into the 'display buffer'
  display.setTextWrap(false);
  display.setTextSize(2);
  display.setTextColor(WHITE);
  display.setCursor(0,0);
  display.println("Welcome");
  display.display(); //output 'display buffer' to screen
}

void loop() {
 
  if (WiFi.status() == WL_CONNECTED) { //Check WiFi connection status
 
    HTTPClient http;  //Declare an object of class HTTPClient
 
    http.begin(""); //Specify request destination
 
    int httpCode = http.GET(); //Send the request
 
    if (httpCode == 200) { //Check the returning code
 
      String payload = http.getString();   //Get the request response payload
      Serial.println(payload);
      display.println(payload); //Display the response payload
      display.display();
 
    }
    else {Serial.println("An error ocurred");}
 
    http.end();   //Close connection
 
  }
 
  delay(2000);    //Send a request every 2 seconds
 
}
