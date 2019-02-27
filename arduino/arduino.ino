void setup() {
  pinMode(6, OUTPUT); //zaplon
  pinMode(7, OUTPUT); //rozruch
  pinMode(A3, OUTPUT); //przekaznik ledow
  pinMode(A4, INPUT); //wejscie dzielnika napiecia z fotoresyztorem
  pinMode(4, OUTPUT); //drzwi
  
  digitalWrite(7, LOW); //rozruch
  digitalWrite(6, LOW); //zaplon
  digitalWrite(A3, LOW); //ledy off
  digitalWrite(4, LOW);
  
  Serial.begin(9600);
}

int fotorezystor(){
  digitalWrite(A3, HIGH);
  delay(50);
  int a = analogRead(A4);
  digitalWrite(A3, LOW);
  return(a);
}

void zaplon_on(){
    digitalWrite(6, HIGH); //zapłon
}

void zaplon_off(){
  digitalWrite(6, LOW);
}

void rozruch(int ms){
  digitalWrite(7, HIGH);
  delay(ms);
  digitalWrite(7, LOW);
}

void drzwi(){
  digitalWrite(4, HIGH);
  delay(100);
  digitalWrite(4, LOW);
}

void loop() {
  String s;
  if(Serial.available()){
    s = Serial.readString();
    if(s == "zaplon_off") zaplon_off();
    else if(s == "zaplon_on") zaplon_on();
    else if(s == "foto") Serial.println(fotorezystor());
    else if(s == "drzwi") drzwi();
    else if(s.startsWith("rozruch")){
      int ms = s.substring(7).toInt();
      if(ms > 200 && ms < 3000) rozruch(ms);
      else Serial.println("Czas rozruchu poza dopuszczalnymi granicami!");
    }
    s = "";
  }
}
