---
sidebar_position: 4
title: "Practical Examples"
---

# Practical Examples in ROS 2

This chapter provides hands-on examples that demonstrate the practical application of ROS 2 concepts in robotics. Each example builds upon the theoretical knowledge from previous chapters.

## TurtleBot 3 Simulation

One of the most common examples in ROS 2 is controlling the TurtleBot 3 in simulation. This example demonstrates nodes, topics, and services in a practical context.

### Setup

First, make sure you have the TurtleBot 3 packages installed:

```bash
sudo apt install ros-humble-turtlebot3*
```

### Controlling the Robot

The following example shows how to programmatically move the TurtleBot 3:

```python
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class TurtleController(Node):
    def __init__(self):
        super().__init__('turtle_controller')
        self.publisher = self.create_publisher(Twist, '/cmd_vel', 10)
        self.timer = self.create_timer(0.1, self.move_turtle)
        
    def move_turtle(self):
        msg = Twist()
        msg.linear.x = 0.5  # Move forward at 0.5 m/s
        msg.angular.z = 0.2  # Rotate at 0.2 rad/s
        self.publisher.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    controller = TurtleController()
    rclpy.spin(controller)
    controller.destroy_node()
    rclpy.shutdown()
```

## Custom Message Example

Creating custom messages is a common requirement in robotics projects. Here's an example of defining and using a custom message:

```python
# In your package, create msg/CustomSensorData.msg:
# float64 temperature
# int32 sensor_id
# string sensor_name
```

## Exercise: Distance Monitor

Create a node that monitors a distance sensor and publishes warnings when objects are too close.

## References

1. ROS 2 Documentation. (2023). "Tutorials". https://docs.ros.org/en/rolling/Tutorials.html
2. Palomer, F. (2022). "ROS 2 Robotics Projects". Packt Publishing.
3. Kamga, D. (2023). "Building Robot Applications with ROS 2". Packt Publishing.
4. Morgan, Q. (2020). "Programming Robots with ROS". O'Reilly Media.
5. Galdames, J. P., & Zamora, L. (2020). "Mastering ROS for Robotics Programming". Packt Publishing.

## Diagram Placeholder

[Diagram showing TurtleBot 3 simulation with ROS 2 nodes and topics]