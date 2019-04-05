#include <ros.h>
#include <std_msgs/String.h>
#include <std_msgs/Empty.h>

ros::NodeHandle  nh;

int torpedo_dir = 1;
int torpedo_pwm = 2;
int dropper_dir = 5;
int dropper_pwm = 6;
int grip_dir = 9;
int grip_pwm = 10;

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
  analogWrite(grip_pwm, 60);
  delay(500);
  analogWrite(grip_pwm, 0);
}
void gripCloseCb( const std_msgs::Empty& toggle_msg){
  digitalWrite(grip_dir, LOW);
  analogWrite(grip_pwm, 60);
  delay(500);
  analogWrite(grip_pwm, 0);
}

ros::Subscriber<std_msgs::Empty> torpedo1("arduino/launch_torpedo", torpedoCb );
ros::Subscriber<std_msgs::Empty> dropper1("arduino/open_dropper", dropperCb );
ros::Subscriber<std_msgs::Empty> gripOpen("arduino/open_gripper", gripOpenCb );
ros::Subscriber<std_msgs::Empty> gripClose("arduino/close_gripper", gripCloseCb );



std_msgs::String str_msg;
ros::Publisher chatter("chatter", &str_msg);


void setup()
{
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
}

void loop()
{
  nh.spinOnce();
  delay(500);
}
