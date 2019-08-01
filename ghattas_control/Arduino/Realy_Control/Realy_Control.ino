
#define kill_Switch 8

//relays
int relay_minipc = 9;
int relay_battery = 10;
bool relay_flag = 0;


void setup() {
  // kill switch
  pinMode(kill_Switch, INPUT_PULLUP);
  pinMode(relay_battery,OUTPUT);
  pinMode(relay_minipc,OUTPUT);

}

void loop() {
  
  bool switch_state = digitalRead(kill_Switch);
  
  if (switch_state == HIGH) {
    digitalWrite(relay_battery, LOW);
    relay_flag = 0;
  }

  if (switch_state == LOW && relay_flag == 0) {
    digitalWrite(relay_battery, HIGH);
    digitalWrite(relay_minipc, HIGH);
    delay(100);
    digitalWrite(relay_minipc, LOW);
    relay_flag = 1;
  }
}
