#include <ros.h>
#include <std_msgs/String.h>
#include <std_msgs/Empty.h>

ros::NodeHandle  nh;

int torpedo1_dir = 1;
int torpedo1_pwm = 2;
int dropper1_dir = 5;
int dropper1_pwm = 6;
int grip_dir = 9;
int grip_pwm = 10;

void torpedo1Cb( const std_msgs::Empty& toggle_msg){
  digitalWrite(torpedo1_dir, HIGH);
  analogWrite(torpedo1_pwm, 60);
  delay(500);
  analogWrite(torpedo1_pwm, 0);
}

void dropper1Cb( const std_msgs::Empty& toggle_msg){
  digitalWrite(dropper1_dir, HIGH);
  analogWrite(dropper1_pwm, 60);
  delay(500);
  analogWrite(dropper1_pwm, 0);
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

ros::Subscriber<std_msgs::Empty> torpedo1("launch_torpedo1", torpedo1Cb );
ros::Subscriber<std_msgs::Empty> dropper1("open_dropper1", dropper1Cb );
ros::Subscriber<std_msgs::Empty> gripOpen("open_gripper", gripOpenCb );
ros::Subscriber<std_msgs::Empty> gripClose("close_gripper", gripCloseCb );



std_msgs::String str_msg;
ros::Publisher chatter("chatter", &str_msg);


void setup()
{
  pinMode(torpedo1_dir,OUTPUT);
  pinMode(torpedo1_pwm,OUTPUT);

  pinMode(dropper1_dir,OUTPUT);
  pinMode(dropper1_pwm,OUTPUT);

  pinMode(grip_dir,OUTPUT);
  pinMode(grip_pwm,OUTPUT);

  nh.initNode();
  nh.subscribe(torpedo1);
  nh.subscribe(dropper1);
  nh.subscribe(gripOpen);
  nh.subscribe(gripClose);
}

void loop()
{
  nh.spinOnce();
  delay(500);
}
