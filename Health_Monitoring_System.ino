#include <Wire.h>
#include <Adafruit_GFX.h>       // Include core graphics library for the display
#include <Adafruit_SSD1306.h>   // Include Adafruit_SSD1306 library to drive the display
#include <Fonts/FreeMonoBold9pt7b.h>  // Add a custom font
#include <Adafruit_MLX90614.h>  //for infrared thermometer
#include <String.h>

#define SCREEN_WIDTH 128 // OLED display width, in pixels
#define SCREEN_HEIGHT 32 // OLED display height, in pixels
#define OLED_RESET -1

int count=0;
int newcount;

Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

Adafruit_MLX90614 mlx = Adafruit_MLX90614();  //for infrared thermometer

//For Capturing and Calculations
int temp;

//Health Feedback based on Temp
const char *healthy[] = {"Your body temperature is great!", "You have the average human temperature.", "You are doing well today!"};
const char *fever[] = {"Warning: You may have a fever.", "Your body temperature higher than usual.", "Are you ok?"};
const char *cold[] = {"Your body temperature is really cold.", "Layer up!", "Are you staying warm?"};

void setup()
{                
  delay(100);  // This delay is needed to let the display to initialize
  display.begin(SSD1306_SWITCHCAPVCC, 0x3C);  // Initialize display with the I2C address of 0x3C
  display.clearDisplay();  // Clear the buffer
  display.setTextColor(WHITE);  // Set color of the text
  mlx.begin();  //start infrared thermometer
  Serial.begin(9600);
  pinMode(8,INPUT);
}

void loop()
{
  temp++;  // Increase value for testing
  if(temp > 43)  // If temp is greater than 150
  {
    temp = 0;  // Set temp to 0
  }

  temp = mlx.readObjectTempC(); //comment this line if you want to test

  display.clearDisplay();  // Clear the display so we can refresh

  // Print text:
  display.setFont();
  display.setCursor(0,0);  // (x,y)
  
  // Array to display temperature
  char string[10];  
  
  // Convert char to a string:
  dtostrf(temp, 4, 0, string);  // (variable, no. of digits we are going to use, no. of decimal digits, string name)
  
  //display.setFont(&FreeMonoBold9pt7b);  // Set a custom font
  
  display.println("Temperature: ");  // Text or value to print

  //Print Temperature
  display.setCursor(72,0);
  display.println(temp);

  //Print Degree Pixels
  display.setCursor(85,0);
  display.write(167);
  
  display.setCursor(95,0);  // (x,y)
  display.println("C");

  
  //If Fever in Celsius(38)  
  if (temp > 37.9 || temp > 100.3){
    display.setCursor(0,10);
    display.println(fever[rand() % 2]);
    delay(1000);
  }
  
  //If average body temperature in Celsius(36.4 - 37.2) or Farenheight (97.5 - 98.8)
  else if (temp > 36.3 && temp < 37.3 || (temp > 97.4 && temp < 98.9)){
    display.setCursor(0,10);
    display.println(healthy[rand() % 2]);
    delay(1000);
  }

  //If cold in celsius(36.3) or farenheight (less than 97.4
  else{
    display.setCursor(0,10);
    display.println(cold[rand() % 2]);
    delay(1000);
  }
    
  //Update Temperature  
  display.display();  
}
