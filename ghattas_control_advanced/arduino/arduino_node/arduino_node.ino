/*
 * Arduino Node to communicate with the mini-pc through ROSSerial
 * subscribe to the specified topics to send commands to the bilge motors
 * performing the following tasks
 * 1- Fire Torpedos
 * 2- drop markers
 * 3- Grapp and release objects using the manipulator
 */

#include <ros.h>
#include <std_msgs/Empty.h>
#include <std_msgs/Bool.h>

ros::NodeHandle  nh;
bool torpedo_1 = false;
bool torpedo_2 = false;
bool grap = false;

// torpedo one connections
int torp_1_f = 1;
int torp_1_b = 2;
int torp_1_pwm = 3;
// torpedo two connections
int torp_2_f = 4;
int torp_2_b = 5;
int torp_2_pwm = 6;
// grapper connections
int grap_f = 7;
int grap_b = 8;
int grap_pwm = 9;

// callback for the first torpedo
void fire_torped_1( const std_msgs::Bool& torpedo_1_state){
  torpedo_1 = torpedo_1_state.data;

}
// callback for the second torpedo
void fire_torped_2( const std_msgs::Bool& torpedo_2_state){
  torpedo_2 = torpedo_2_state.data;
}

// initialzing subscribers
ros::Subscriber<std_msgs::Bool> tp_1("/fire_torpedo_state_1", &fire_torped_1 );// subscribe for the first torpdeo state
ros::Subscriber<std_msgs::Bool> tp_2("/fire_torpedo_state_2", &fire_torped_2 );// subscribe for the second torpdeo state

// intiating the ports mode
void init_ports(void){// start of init ports funciton
  pinMode(torp_1_f,OUTPUT);
  pinMode(torp_1_b,OUTPUT);
  pinMode(torp_1_pwm,OUTPUT);
  pinMode(torp_2_f,OUTPUT);
  pinMode(torp_2_b,OUTPUT);
  pinMode(torp_2_pwm,OUTPUT);
  pinMode(grap_f,OUTPUT);
  pinMode(grap_b,OUTPUT);
  pinMode(grap_pwm,OUTPUT);
}// end of the init ports function

// initiating the ROS connection
void init_ROS(void){
  nh.initNode();
  nh.subscribe(tp_1);
  nh.subscribe(tp_2);
}// end of the init_ROS function

void setup()
{
  init_ports();
  init_ROS();
  Serial.begin(9600);


}// end of the setup

void loop()
{
  if (torpedo_1){// check state if true fire torpdeo 1
    Serial.write("Torpedo one fired");
  }// end of firing torpedo one

  if (torpedo_2){// check state if true fire torpdeo 1
    Serial.write("Torpedo two fired");
  }// end of firing torpedo one

  if (grap){// check state if true fire torpdeo 1
    Serial.write("Torpedo grapped fired");
  }// end of firing torpedo one

}// end of the main loop
