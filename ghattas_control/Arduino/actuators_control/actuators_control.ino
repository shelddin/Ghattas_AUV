#include <ros.h>
//#include <dht11.h>
#include <std_msgs/String.h>
#include <std_msgs/Empty.h>
#include <std_msgs/Float64.h>
#include <Servo.h>

ros::NodeHandle  nh;

//sensors
int temp_sen = 2;
//dht11 DHT11;

int leak_sen = 11;

//bilge motors
int torpedo_dir = 8;
int torpedo_pwm = 7;
int dropper_dir = 4;
int dropper_pwm = 3;
int grip_dir = 6;
int grip_pwm = 5;

//LEDs
byte led_1 = 12;
byte led_2 = 13;
Servo led1;
Servo led2;

void torpedoCb( const std_msgs::Empty& toggle_msg){
  digitalWrite(torpedo_dir, HIGH);
  analogWrite(torpedo_pwm, 60);
  delay(500);
  analogWrite(torpedo_pwm, 0);
}

void dropperCb( const std_msgs::Empty& toggle_msg){
  digitalWrite(dropper_dir, HIGH);
  analogWrite(dropper_pwm, 60);
  delay(500);
  analogWrite(dropper_pwm, 0);
}

void gripOpenCb( const std_msgs::Empty& toggle_msg){
  digitalWrite(grip_dir, HIGH);
  analogWrite(grip_pwm, 100);
  delay(1000);
  analogWrite(grip_pwm, 0);
}
void gripCloseCb( const std_msgs::Empty& toggle_msg){
  digitalWrite(grip_dir, LOW);
  analogWrite(grip_pwm, 100);
  delay(1000);
  analogWrite(grip_pwm, 0);
}

std_msgs::Float64 temp;
std_msgs::Float64 humd;

ros::Subscriber<std_msgs::Empty> torpedo("arduino/launch_torpedo", &torpedoCb );
ros::Subscriber<std_msgs::Empty> dropper("arduino/open_dropper", &dropperCb );
ros::Subscriber<std_msgs::Empty> gripOpen("arduino/open_gripper", &gripOpenCb );
ros::Subscriber<std_msgs::Empty> gripClose("arduino/close_gripper", &gripCloseCb );
ros::Publisher temp_pub("diagnostics/temprature", &temp);
ros::Publisher humd_pub("diagnostics/humidity", &humd);




void setup()
{
  
  //Bilge Motors
  pinMode(torpedo_dir,OUTPUT);
  pinMode(torpedo_pwm,OUTPUT);

  pinMode(dropper_dir,OUTPUT);
  pinMode(dropper_pwm,OUTPUT);

  pinMode(grip_dir,OUTPUT);
  pinMode(grip_pwm,OUTPUT);

  nh.initNode();
  nh.subscribe(torpedo);
  nh.subscribe(dropper);
  nh.subscribe(gripOpen);
  nh.subscribe(gripClose);
  nh.advertise(temp_pub);
  nh.advertise(humd_pub);



  //Leds setup
  led1.attach(led_1);
  led2.attach(led_2);
  led1.writeMicroseconds(1200);
  led2.writeMicroseconds(1200);

}

void loop()
{
  nh.spinOnce();
  //Diagnostics publishing
//   int chk = DHT11.read(temp_sen);
//   temp.data = DHT11.temperature;
//   humd.data = DHT11.humidity;
//   temp_pub.publish(&temp);
//   humd_pub.publish(&humd);

  delay(500);
}
