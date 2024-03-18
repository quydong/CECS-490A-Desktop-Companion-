#include <Wire.h>
#include <Adafruit_GFX.h>       // Include core graphics library for the display
#include <Adafruit_SSD1306.h>   // Include Adafruit_SSD1306 library to drive the display
#include <Fonts/FreeMonoBold9pt7b.h>  // Add a custom font
#include <Adafruit_MLX90614.h>  //for infrared thermometer
#include <String.h>

#define SCREEN_WIDTH 128 // OLED display width, in pixels
#define SCREEN_HEIGHT 32 // OLED display height, in pixels
#define OLED_RESET -1


Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

Adafruit_MLX90614 mlx = Adafruit_MLX90614();  

/*For Capturing and Calculations*/
float temp;  // Create a variable to have something dynamic to show on the display
float tempC;
float tempF;

/*List of all states for FSM*/
enum
{
  DEFAULT_STATE,
  STATE_ON_DEFAULT,
  LOCK_STATE,
  STATE_ON_LOCK,
} state;

const int buttonPin = 8;
int last_button_value = HIGH;   // pin 2 is HIGH when button is not pressed
unsigned long previousMillisButton;
unsigned long previousMillisBlinking;


/*Health Feedback based on Temp*/
const char *healthy[] = {"Your body temperature is great!", "You have the average human temperature", "You are doing well today!"};
const char *fever[] = {"Warning: You may have a fever", "Your body temperature is higher than usual", "Are you ok?"};
const char *cold[] = {"Your body temperature is really cold", "Layer up!", "Are you staying warm?"};

void setup()
{                
  delay(100);  // This delay is needed to let the display to initialize
  display.begin(SSD1306_SWITCHCAPVCC, 0x3C);  // Initialize display with the I2C address of 0x3C
  display.clearDisplay();  // Clear the buffer
  display.setTextColor(WHITE);  // Set color of the text
  mlx.begin();  //start infrared thermometer
  Serial.begin(9600);
  pinMode(buttonPin,INPUT);
}

void loop()
{
  tempF++;  // Increase value for testing

  tempF = mlx.readObjectTempF(); //comment this line if you want to test
  tempC = mlx.readObjectTempC();

  display.clearDisplay();  // Clear the display so we can refresh

  // Print text:
  display.setFont();
  display.setCursor(0,0);  // (x,y)
  
  // Array to display temperature
  char fah[10];  
  char cel[10];
  unsigned long currentMillis = millis();
  bool buttonPressed = false;
  bool buttonReleased = false;
  int button_value = digitalRead( buttonPin);

    temp++;  // Increase value for testing
  if(temp > 43)  // If temp is greater than 150
  {
    temp = 0;  // Set temp to 0
  }

  if( button_value != last_button_value)
  {
    if( button_value == LOW)  // low is button pressed
    {
      buttonPressed = true;
    }
    else
    {
      buttonReleased = true;
    }
    last_button_value = button_value;
  }
  ///////////////////////////////////////
switch(state)
{
  //////////////////////////////////////
case DEFAULT_STATE:
  /*Convert char to a string:*/
  dtostrf(tempF, 4, 0, fah);  // (variable, no. of digits we are going to use, no. of decimal digits, string name)
  dtostrf(tempC, 4, 0, cel);
  
  display.println("Temp: ");

  /*Print Temperature in F*/
  display.setCursor(30,0);
  display.println(tempF,1);

  /*Formating Degree and F*/
  if(tempF > 99){
    //Print Degree Pixels
    display.setCursor(63,0);
    display.write(167);
    display.setCursor(71,0);
    display.println("F");
  }

  else{
    display.setCursor(55,0);
    display.write(167);
    display.setCursor(63,0);
    display.println("F");
  }

  /*Print Temperature in C*/
  display.setCursor(85,0);
  display.println(tempC,1);

  /*Print Degree Pixels*/
  display.setCursor(110,0);
  display.write(167);
  
  display.setCursor(118,0);  // (x,y)
  display.println("C");
  delay(100);

  /*Update screen to update temperature*/  
  display.display();  
  state = STATE_ON_DEFAULT;
  break;

  //////////////////////////////////
  case STATE_ON_DEFAULT:
  if(buttonPressed)
  {
    state = LOCK_STATE;
  }
  else{
    state = DEFAULT_STATE;
  }
  break;
  ///////////////////////////////////
  case LOCK_STATE:
  dtostrf(tempF, 4, 0, fah); 
  dtostrf(tempC, 4, 0, cel);
  
  display.println("Temp: ");

  //Print Temperature in F
  display.setCursor(30,0);
  display.println(tempF,1);

  /*Formating Degree and F*/
  if(tempF > 99){
    //Print Degree Pixels
    display.setCursor(63,0);
    display.write(167);
    display.setCursor(71,0);
    display.println("F");
  }

  else{
    display.setCursor(55,0);
    display.write(167);
    display.setCursor(63,0);
    display.println("F");
  }

  /*Print Temperature in C*/
  display.setCursor(85,0);
  display.println(tempC,1);

  //Print Degree Pixels
  display.setCursor(110,0);
  display.write(167);
  
  display.setCursor(118,0);  // (x,y)
  display.println("C");
  delay(100);
  
  /*If in range of potential fever*/ 
  if (tempC > 37.76 || tempF > 99.9){
    display.setCursor(0,10);
    display.println(fever[rand() % 2]);
    delay(100);
  }
  
  /*If average body temperature*/
  else if (tempC > 36.4 && tempC < 37.77 || (tempF > 96.8 && tempF < 100)){
    display.setCursor(0,10);
    display.println(healthy[rand() % 2]);
    delay(100);
  }

  /*If cold*/
  else if (tempC > 32.2 && tempC < 36.5 || (tempF > 89 && tempF < 96.9)){
    display.setCursor(0,10);
    display.println(cold[rand() % 2]);
    delay(100);
  }

  /*If room temperature*/
  else{
    delay(100);
  }
    
  /*Update LCD to display feedback*/
  display.display();
  state = STATE_ON_LOCK;
  break;

  ////////////////////////////////////
  case STATE_ON_LOCK:
  if(buttonPressed)
{
  state = DEFAULT_STATE;
}
break;
}
}