
int a_speed=0;

int i_speed = A15;    
int j51_but_right = 33;//CW     
int j51_but_left = 32;//CCW
int j52_but_up = 30;     
int j52_but_down = 31; 

int j51_EN=38;
int j51_DIR=39;
int j51_PUL=40;

int j52_EN=41;
int j52_DIR=42;
int j52_PUL=43;

void setup() {
  pinMode(j51_but_right, INPUT);
  pinMode(j51_but_left, INPUT); 
  pinMode(j52_but_up, INPUT); 
  pinMode(j52_but_down, INPUT);
  
  pinMode(j51_EN, OUTPUT);
  pinMode(j51_DIR, OUTPUT);
  pinMode(j51_PUL, OUTPUT);
 
  pinMode(j52_EN, OUTPUT);
  pinMode(j52_DIR, OUTPUT);
  pinMode(j52_PUL, OUTPUT); 
  
  digitalWrite(j51_EN, LOW);
  digitalWrite(j51_DIR, LOW);
  digitalWrite(j51_PUL, LOW);
  digitalWrite(j52_EN, LOW);
  digitalWrite(j52_DIR, LOW);
  digitalWrite(j52_PUL, LOW);
  
  Serial.begin(9600);
}


void move(int pul_port, int dir_port, int en_port, int but_val, int speed_val, int dir_val){
  digitalWrite(en_port, HIGH);
  digitalWrite(dir_port, dir_val);
  digitalWrite(pul_port, HIGH);
  delayMicroseconds(speed_val);
  digitalWrite(pul_port, LOW); 
  delayMicroseconds(speed_val);
  digitalWrite(en_port, LOW);
}

void loop() {
//  a_speed = analogRead(i_speed);    
  if(analogRead(i_speed)>=1000){
    a_speed = 1;
  }else if(analogRead(i_speed)>=800){
    a_speed = 20;
  }else if(analogRead(i_speed)>=600){
    a_speed = 35;
  }else if(analogRead(i_speed)>=400){
    a_speed = 40;
  }else{
    a_speed = 45;
  }

  if(digitalRead(j51_but_right)==1){
    Serial.println("right");
    Serial.println(a_speed);
    move(j51_PUL,j51_DIR,j51_EN,j51_but_right,a_speed,HIGH);
  }
  if(digitalRead(j51_but_left)==1){
    Serial.println("left");
    Serial.println(a_speed);
    move(j51_PUL,j51_DIR,j51_EN,j51_but_left,a_speed,LOW);
  }
  if(digitalRead(j52_but_up)==1){
    Serial.println("up");
    Serial.println(a_speed);
    move(j52_PUL,j52_DIR,j52_EN,j52_but_up,a_speed,HIGH);
  }
  if(digitalRead(j52_but_down)==1){
    Serial.println("down");
    Serial.println(a_speed);
    move(j52_PUL,j52_DIR,j52_EN,j52_but_down,a_speed,LOW);
  }
}

















//
// a_speed = analogRead(i_speed);    
//  
//  if(digitalRead(j51_but_right)==1){
//    digitalWrite(j51_DIR, HIGH);
//    while(digitalRead(j51_but_right)==1){
//     digitalWrite(j51_PUL, HIGH);
//     delayMicroseconds(a_speed);
//     digitalWrite(j51_PUL, LOW); 
//     delayMicroseconds(a_speed);
//    }
//  }
//  if(digitalRead(j51_but_left)==1){
//    digitalWrite(j51_DIR, LOW);
//    while(digitalRead(j51_but_left)==1){
//     digitalWrite(j51_PUL, HIGH);
//     delayMicroseconds(a_speed);
//     digitalWrite(j51_PUL, LOW); 
//     delayMicroseconds(a_speed);
//    }
//  }
//  if(digitalRead(j52_but_up)==1){
//    digitalWrite(j52_DIR, HIGH);
//    while(digitalRead(j52_but_up)==1){
//     digitalWrite(j52_PUL, HIGH);
//     delayMicroseconds(a_speed);
//     digitalWrite(j52_PUL, LOW); 
//     delayMicroseconds(a_speed);
//    }
//  }
//  if(digitalRead(j52_but_down)==1){
//    digitalWrite(j52_DIR, LOW);
//    while(digitalRead(j52_but_down)==1){
//     digitalWrite(j52_PUL, HIGH);
//     delayMicroseconds(a_speed);
//     digitalWrite(j52_PUL, LOW); 
//     delayMicroseconds(a_speed);
//    }
//  }
