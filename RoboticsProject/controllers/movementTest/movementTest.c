/*
 * File:          movementTest.c
 * Date:
 * Description:
 * Author:
 * Modifications:
 */

/*
 * You may need to add include files like <webots/distance_sensor.h> or
 * <webots/motor.h>, etc.
 */
#include <webots/robot.h>


/*
 * This is the main program.
 * The arguments of the main function can be specified by the
 * "controllerArgs" field of the Robot node
 */
#include <webots/keyboard.h>
#include <webots/robot.h>

#include <include/arm.h>
#include <src/arm.c>
#include <include/base.h>
#include <src/base.c>
#include <include/gripper.h>
#include <src/gripper.c>
#include <include/tiny_math.h>
#include <src/tiny_math.c>

#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define TIME_STEP 32
#define KEY_W 87
#define KEY_A 65
#define KEY_S 83
#define KEY_D 68
#define KEY_R 82
#define KEY_H 72
#define KEY_C 67
#define KEY_Z 90
#define KEY_G 71
#define KEY_F 70
#define KEY_I 73

static void step() {
  if (wb_robot_step(TIME_STEP) == -1) {
    wb_robot_cleanup();
    exit(EXIT_SUCCESS);
  }
}

static void passive_wait(double sec) {
  double start_time = wb_robot_get_time();
  do {
    step();
  } while (start_time + sec > wb_robot_get_time());
}

static void automatic_behavior() {
  passive_wait(2.0);
  gripper_release();
  arm_set_height(ARM_FRONT_CARDBOARD_BOX);
  passive_wait(4.0);
  gripper_grip();
  passive_wait(1.0);
  arm_set_height(ARM_BACK_PLATE_LOW);
  passive_wait(3.0);
  gripper_release();
  passive_wait(1.0);
  arm_reset();
  base_strafe_left();
  passive_wait(5.0);
  gripper_grip();
  base_reset();
  passive_wait(1.0);
  base_turn_left();
  passive_wait(1.0);
  base_reset();
  gripper_release();
  arm_set_height(ARM_BACK_PLATE_LOW);
  passive_wait(3.0);
  gripper_grip();
  passive_wait(1.0);
  arm_set_height(ARM_RESET);
  passive_wait(2.0);
  arm_set_height(ARM_FRONT_PLATE);
  arm_set_orientation(ARM_RIGHT);
  passive_wait(4.0);
  arm_set_height(ARM_FRONT_FLOOR);
  passive_wait(2.0);
  gripper_release();
  passive_wait(1.0);
  arm_set_height(ARM_FRONT_PLATE);
  passive_wait(2.0);
  arm_set_height(ARM_RESET);
  passive_wait(2.0);
  arm_reset();
  gripper_grip();
  passive_wait(2.0);
}

static void display_helper_message() {
  printf("Control commands:\n");
  printf(" Arrows:       Move the robot\n");
  printf(" Page Up/Down: Rotate the robot\n");
  printf(" +/-:          (Un)grip\n");
  printf(" Shift + arrows:   Handle the arm\n");
  printf(" Space: Reset\n");
}

int main(int argc, char **argv) {
  wb_robot_init();

  base_init();
  arm_init();
  gripper_init();
  passive_wait(2.0);

  if (argc > 1 && strcmp(argv[1], "demo") == 0)
    automatic_behavior();

  display_helper_message();

  int pc = 0;
  wb_keyboard_enable(TIME_STEP);

  while (true) {
    step();

    int c = wb_keyboard_get_key();
    if ((c >= 0) && c != pc) {
      switch (c) {
        case KEY_W:
          printf("Increase arm height\n");
          arm_increase_height();
          break;
        case KEY_A:
          printf("Decrease arm orientation\n");
          arm_decrease_orientation();
          break;
         case KEY_S:
          printf("Decrease arm height\n");
          arm_decrease_height();
          break;
         case KEY_D:
          printf("Increase arm orientation\n");
          arm_increase_orientation();
          break;
        case WB_KEYBOARD_UP:
          printf("Go forwards\n");
          base_forwards();
          break;
        case WB_KEYBOARD_DOWN:
          printf("Go backwards\n");
          base_backwards();
          break;
        case WB_KEYBOARD_LEFT:
          printf("Turn left\n");
          base_turn_left();
          break;
        case WB_KEYBOARD_RIGHT:
          printf("Turn right\n");
          base_turn_right();
          break;
        case WB_KEYBOARD_PAGEUP:
          printf("Turn left\n");
          base_turn_left();
          break;
        case WB_KEYBOARD_PAGEDOWN:
          printf("Turn right\n");
          base_turn_right();
          break;
        case KEY_Z:
          printf("Zero the Arm Orientations\n");
          arm_set_sub_arm_rotation(ARM1, 0);
          arm_set_sub_arm_rotation(ARM2, 0);
          arm_set_sub_arm_rotation(ARM3, 0);
          arm_set_sub_arm_rotation(ARM4, 0);
          arm_set_sub_arm_rotation(ARM5, 0);
          break;
        case KEY_F:
          printf("Reach Far\n");
          arm_set_sub_arm_rotation(ARM1, 0);
          arm_set_sub_arm_rotation(ARM2, -1.13);
          arm_set_sub_arm_rotation(ARM3, -0.4);
          arm_set_sub_arm_rotation(ARM4, -0.4);
          arm_set_sub_arm_rotation(ARM5, 0);
          gripper_release();
          break;
        case KEY_H:
          printf("Reach High\n");
          arm_set_sub_arm_rotation(ARM1, 0);
          arm_set_sub_arm_rotation(ARM2, 0);
          arm_set_sub_arm_rotation(ARM3, 0);
          arm_set_sub_arm_rotation(ARM4, -1.57);
          arm_set_sub_arm_rotation(ARM5, 0);
          gripper_release();
          break;
        case KEY_I:
          printf("Reach In-Front\n");
          arm_set_sub_arm_rotation(ARM1, 0);
          arm_set_sub_arm_rotation(ARM2, -0.5);
          arm_set_sub_arm_rotation(ARM3, -1);
          arm_set_sub_arm_rotation(ARM4, -1.57);
          arm_set_sub_arm_rotation(ARM5, 0);
          gripper_release();
          break;
        case KEY_C:
          printf("Collect\n");
          gripper_grip();
          arm_set_sub_arm_rotation(ARM1, 0);
          arm_set_sub_arm_rotation(ARM2, 0.5);
          arm_set_sub_arm_rotation(ARM3, 0.5);
          arm_set_sub_arm_rotation(ARM4, 1.6);
          arm_set_sub_arm_rotation(ARM5, 1.57);
          break;
        case KEY_G:
          printf("Grip\n");
          gripper_grip();
          break;
        case KEY_R:
          printf("Release\n");
          gripper_release();
          arm_reset();
          break;
        case ' ':
          printf("Reset\n");
          base_reset();
          arm_reset();
          break;
        /*
        case '-':
        case 332:
        */
        default:
          fprintf(stderr, "Wrong keyboard input\n");
          printf("%i\n",c);
          break;
      }
    }
    pc = c;
  }

  wb_robot_cleanup();

  return 0;
}

