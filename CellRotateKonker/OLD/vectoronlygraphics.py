"""
 Wireframe 3D cube simulation.
 Developed by Adriano R. de Lima <adriano.lima@arlima.com.br> based on code
 developed by Leonel Machava <leonelmachava@gmail.com> - http://codeNtronix.com
"""

import sys, math, pygame
import paho.mqtt.client as mqtt
import json
import pprint

config = {}
message = {}
quat = (0,0,0,0)
SCREEN_WIDTH, SCREEN_HEIGHT = 1024, 768
BG_COLOR = 0,0,0

#Class to manage points in 3D space

class Point3D:
    def __init__(self, x=0, y=0, z=0):
        self.x, self.y, self.z = float(x), float(y), float(z)

    def rotateX(self, angle):
        """ Rotates the point around the X axis by the given angle in degrees. """
        rad = angle * math.pi / 180
        cosa = math.cos(rad)
        sina = math.sin(rad)
        y = self.y * cosa - self.z * sina
        z = self.y * sina + self.z * cosa
        return Point3D(self.x, y, z)

    def rotateY(self, angle):
        """ Rotates the point around the Y axis by the given angle in degrees. """
        rad = angle * math.pi / 180
        cosa = math.cos(rad)
        sina = math.sin(rad)
        z = self.z * cosa - self.x * sina
        x = self.z * sina + self.x * cosa
        return Point3D(x, self.y, z)

    def rotateZ(self, angle):
        """ Rotates the point around the Z axis by the given angle in degrees. """
        rad = angle * math.pi / 180
        cosa = math.cos(rad)
        sina = math.sin(rad)
        x = self.x * cosa - self.y * sina
        y = self.x * sina + self.y * cosa
        return Point3D(x, y, self.z)

    def project(self, win_width, win_height, fov, viewer_distance):
        """ Transforms this 3D point to 2D using a perspective projection. """
        factor = fov / (viewer_distance + self.z)
        x = self.x * factor + win_width / 2
        y = -self.y * factor + win_height / 2
        return Point3D(x, y, 1)



print ("Starting Graphics !")
# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT),0,32)
pygame.display.set_caption("3D Mobile Moviment Simulation")
clock = pygame.time.Clock()

vector = Point3D(1,1,1)

while True:
    time_passed = clock.tick(50)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    screen.fill(BG_COLOR)

    p = vector.project(screen.get_width(), screen.get_height(), 256, 6)

    pygame.draw.line(screen, (255, 255, 255), (0, 0), (p.x, p.y))

    pygame.display.flip()
