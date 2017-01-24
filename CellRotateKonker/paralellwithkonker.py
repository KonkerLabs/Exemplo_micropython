"""
 Wireframe 3D cube simulation.
 Developed by Adriano R. de Lima <adriano.lima@arlima.com.br> based on code
 developed by Leonel Machava <leonelmachava@gmail.com> - http://codeNtronix.com
"""

import sys, math, pygame
import paho.mqtt.subscribe as subscribe
import json
import pprint
import math

config = {}
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

def readconfig():
    global config
    with open('konker.config', 'r') as config_file:
        config = json.load(config_file)
        #pprint.pprint(config)
        config_file.close()

def geteuler(quat):
    ## Calculations from
    ## https://en.wikipedia.org/wiki/Conversion_between_quaternions_and_Euler_angles#Quaternion_to_Euler_Angles_Conversion

    ysqr = quat[1] * quat[1]

    # roll (x-axis rotation)
    t0 = 2.0 * (quat[3] * quat[0] + quat[1] * quat[2])
    t1 = 1.0 - 2.0 * (quat[0] * quat[0] + ysqr)
    roll = math.atan2(t0, t1);

    # pitch (y-axis rotation)
    t2 = 2.0 * (quat[3] * quat[1] - quat[2]*quat[0])
    if t2 > 1.0:
        t2 = 1.0
    if t2 < -1.0:
        t2 = -1.0
    pitch = math.asin(t2);

    # yaw (z-axis rotation)
    t3 = 2.0 * (quat[3] * quat[2] + quat[0] * quat[1])
    t4 = 1.0 - 2.0 * (ysqr + quat[2] * quat[2])
    yaw = math.atan2(t3, t4)

    return (roll, pitch, yaw);

##### MAIN CODE #####

readconfig()

print ("Starting Graphics !")
# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT),0,32)
pygame.display.set_caption("3D Mobile Movement Simulation")
clock = pygame.time.Clock()

vertices = [
    Point3D(-2, 4, -0.5),
    Point3D(2, 4, -0.5),
    Point3D(2, -4, -0.5),
    Point3D(-2, -4, -0.5),
    Point3D(-2, 4, 0.5),
    Point3D(2, 4, 0.5),
    Point3D(2, -4, 0.5),
    Point3D(-2, -4, 0.5)
]

# Define the vertices that compose each of the 6 faces. These numbers are
# indices to the vertices list defined above.
faces = [(0, 1, 2, 3), (1, 5, 6, 2), (5, 4, 7, 6), (4, 0, 3, 7), (0, 4, 5, 1), (3, 2, 6, 7)]
angleX, angleY, angleZ = 0, 0, 0

while True:
    time_passed = clock.tick(50)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    msg = subscribe.simple(config["SUB"], keepalive=5, retained=False, hostname=config["URL"], auth={'username':config["USER"], 'password':config["PWD"]})
    message = json.loads(msg.payload.decode("utf-8"))
    quat = (message["val1"], message["val2"], message["val3"], message['val4'])
    (angleX, angleY, angleZ) = geteuler(quat)
    (angleX, angleY, angleZ) = (-1.0*(180.0/3.1415926)*angleX, -1.0*(180.0/3.1415926)*angleY, +1.0*(180.0/3.1415926)*angleZ)

    print(angleX, angleY, angleZ)

    t = []
    for v in vertices:
        # Rotate the point around X axis, then around Y axis, and finally around Z axis.
        r = v.rotateX(angleX).rotateY(angleY).rotateZ(angleZ)
        # Transform the point from 3D to 2D
        p = r.project(screen.get_width(), screen.get_height(), 256, 6)
        # Put the point in the list of transformed vertices
        t.append(p)

    screen.fill(BG_COLOR)
    for f in faces:
        pygame.draw.line(screen, (255, 255, 255), (t[f[0]].x, t[f[0]].y), (t[f[1]].x, t[f[1]].y))
        pygame.draw.line(screen, (255, 255, 255), (t[f[1]].x, t[f[1]].y), (t[f[2]].x, t[f[2]].y))
        pygame.draw.line(screen, (255, 255, 255), (t[f[2]].x, t[f[2]].y), (t[f[3]].x, t[f[3]].y))
        pygame.draw.line(screen, (255, 255, 255), (t[f[3]].x, t[f[3]].y), (t[f[0]].x, t[f[0]].y))

    pygame.display.flip()
