# Image Based Path Planning
#### Guide : Prof. Arpita Sinha | SURP 2022
Documentation->

Traditionally, path planning for field robotic systems is performed in Cartesian space: sensor readings are transformed into terrain costs in a (Cartesian) costmap, and a path to the goal is planned in that map. 
I will implement something different : plan a path for the robot in the image-space of an on-board camera. 
Then, apply a learned color- to-cost mapping to transform a raw image into a cost-image, which then undergoes a pseudo-configuration-space transform. 
Finally, a search is made in the resulting cost-image for a path to the projected goal point in the image. 
One benefit of this approach is the ability to react to obstacles at ranges well beyond the 3D sensor's range - Range increases by 17.6 times

Steps to be following:
(1) Take a raw image from the camera and convert it into a cost-image, where a pixel value represents the terrain cost of the patch of the world projected onto that pixel.
(2) Apply a pseudo-configuration-space transform to the cost image to account for the size of the robot.
(3) Project the goal point into the image-space (unless the goal can be visually identified in the image).
(4) Plan a pixel-to-pixel path from a pixel at the bottom of the image (a point right in front of the robot) to the goal pixel
