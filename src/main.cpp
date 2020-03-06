#include <Arduino.h>
#include <string.h>
#include <AFMotor.h>

// Connect a stepper motor with 200 steps per revolution
// to motor port #2 (M3 and M4)
AF_Stepper motor(200, 2);

//type of selected product is HIGH
const int PRODUCTAPIN = 22;
const int PRODUCTBPIN = 23;

//status of stations - HIGH when ready
const int BELTSTATEPIN =   2;
const int AREADYPIN =      24;
const int BREADYPIN =      25;
const int CREADYPIN =      26;
const int DREADYPIN =      27;
const int EREADYPIN =      28;

//error pins - HIGH when error
const int AERRORPIN =      29;
const int BERRORPIN =      30;
const int CERRORPIN =      31;
const int DERRORPIN =      32;
const int EERRORPIN =      33;

//check finished pins - HIGH when finished
const int AFIN =          34;
const int BFIN =          35;
const int CFIN =          36;
const int DFIN =          37;
const int EFIN =          38;

//load pins - HIGH when stations need parts
const int ALOAD =          40;
const int BLOAD =          41;
const int CLOAD =          42;
const int DLOAD =          43;
const int ELOAD =          44;

//global variables
int selection=          0;
bool selectedProductA=  0;
bool selectedProductB=  0;
bool errorStationA=     0;
bool errorStationB=     0;
bool errorStationC=     0;
bool errorStationD=     0;
bool errorStationE=     0;
String errorID;

//finished checks
bool stationAfinished = 0;
bool stationBfinished = 0;
bool stationCfinished = 0;
bool stationDfinished = 0;
bool stationEfinished = 0;
bool processFinished =  0;

//Function Prototypes
int productSelection(){
  
  while(!selection){
    if (digitalRead(PRODUCTAPIN))
      selection = 1;
      selectedProductA = true;
    if (digitalRead(PRODUCTBPIN))
      selection = 2;
      selectedProductB = true;
  }
  return selection;
}

bool getErrors(){

  bool errorCheck = 0;

  if (digitalRead(AERRORPIN)){
    errorStationA = 1;
    errorID[1] = 'A';
  }else
  {
    errorStationA = 0;
    errorID[1] = '0';
  }
  

  if (digitalRead(BERRORPIN)){
    errorStationB = 1;
    errorID[2] = 'B';
  }else
  {
    errorStationB = 0;
    errorID[2] = '0';
  }
  

  if (digitalRead(CERRORPIN)){
    errorStationC = 1;
    errorID[3] = 'C';
  }else
  {
    errorStationC = 0;
    errorID[3] = '0';
  }
  

  if (digitalRead(DERRORPIN)){
    errorStationD = 1;
    errorID[4] = 'D';
  }else
  {
    errorStationD = 0;
    errorID[4] = '0';
  }
  

  if (digitalRead(EERRORPIN)){
    errorStationE = 1;
    errorID[5] = 'E';
  }else
  {
    errorStationE = 0;
    errorID[5] = '0';
  }
  
  //print errorString to see the Station where the error occured
  Serial.println(errorID);

  //Send errorString to Raspberry
  for (uint8_t i = 1; i<=errorID.length();i++)
    Serial2.write(errorID[i]);

  if (errorStationA || errorStationB || errorStationC || errorStationD || errorStationE){
    //stop belt because there is an error
    digitalWrite(BELTSTATEPIN,LOW);
    errorCheck = 1;
  }else
  {
    errorCheck = 0;
  }
    
  return errorCheck;
}

void enableMotor(int steps, int speed){
  //accelerate up to 30rpm
  for (uint8_t i = 1; i <= speed; i++){
    motor.setSpeed(i);
    motor.onestep(FORWARD, DOUBLE);
    delay(20);
  }
  //step forward with double mode --> more torque
  motor.step(steps, FORWARD, DOUBLE); 
  motor.release();
}

bool goToStationB(){

  if (BREADYPIN && !BERRORPIN){
    //do motor stuff to Station B

  }

  //Wait until station is finished
  while(!digitalRead(BFIN));

  //write to raspi
  Serial2.write(25);
  return stationBfinished = 1;
}

bool goToStationC(){
  if (CREADYPIN && !CERRORPIN){
    //do motor stuff to Station B
    
  }

  //wait until station is finished
  while(!digitalRead(CFIN));

  //write to raspi
  Serial2.write(50);

  return stationCfinished = 1;
}

bool goToStationD(){
  if (DREADYPIN && !DERRORPIN){
    //do motor stuff to Station B
    
  }

  //wait until station is finished
  while(!digitalRead(DFIN));

  //write to raspi
  Serial2.write(75);

  return stationDfinished = 1;
}

bool goToStationE(){

  if (EREADYPIN && !EERRORPIN){
    //do motor stuff to Station B
    
  }

  //wait until station is finished
  while(!digitalRead(EFIN));

  //write to raspi
  Serial2.write(99);
  return stationEfinished = 1;
}

bool isFinished(){
  if (stationAfinished && stationBfinished && stationCfinished && stationDfinished && stationEfinished){
    processFinished = 1;
    stationAfinished = 0;
    stationBfinished = 0;
    stationCfinished = 0;
    stationDfinished = 0;
    stationEfinished = 0;
    errorStationA =    0;
    errorStationB =    0;
    errorStationC =    0;
    errorStationD =    0;
    errorStationE =    0;
    selection =        0;
    selectedProductA = 0;
    selectedProductB = 0;
  }

  //write to raspi
  Serial2.write(100);

  Serial.println("Process Finished");
  return processFinished;
}

void setup() {

  //Serial Port to PC
  Serial.begin(9600);

  //Serial Port to Raspi
  Serial2.begin(9600);

  //set pinModes
  pinMode(PRODUCTBPIN,INPUT);
  pinMode(PRODUCTAPIN,INPUT);
  pinMode(BELTSTATEPIN,OUTPUT);
  pinMode(AREADYPIN,OUTPUT);
  pinMode(BREADYPIN,INPUT);
  pinMode(CREADYPIN,INPUT);
  pinMode(DREADYPIN,INPUT);
  pinMode(EREADYPIN,INPUT);
  pinMode(AERRORPIN,INPUT);
  pinMode(BERRORPIN,INPUT);
  pinMode(CERRORPIN,INPUT);
  pinMode(DERRORPIN,INPUT);
  pinMode(EERRORPIN,INPUT);
  pinMode(AFIN,INPUT);
  pinMode(BFIN,INPUT);
  pinMode(CFIN,INPUT);
  pinMode(DFIN,INPUT);
  pinMode(EFIN,INPUT);
}

void loop() {
  
  //Wait for product selection
  productSelection();

  while(!getErrors()){
    goToStationB();
    goToStationC();
    goToStationD();
    goToStationE();
    isFinished();
  }
}