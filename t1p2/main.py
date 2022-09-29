# coding=utf-8
"""Tarea 1 parte 2: Beach Ball"""

import glfw
from OpenGL.GL import *
import grafica.performance_monitor as pm
import grafica.transformations as tr
import grafica.easy_shaders as es
import grafica.basic_shapes as bs
import grafica.constants as ct
import random as rd
import numpy as np

ROTATION = np.pi * ct.ROTATION  # Setting rotation due to not using numpy in constants.py

class Controller:   # A class to control the program # Idea from ex_bouncing_balls.py
    def __init__(self):
        self.camera_theta = np.pi/4
        self.showAxis = True
        self.setStartingCamera = np.array([ct.VIEW_POS[0], ct.VIEW_POS[1], ct.VIEW_POS[2]]) # Changes camera position just once
        self.viewPos = np.array([ct.VIEW_POS[0], ct.VIEW_POS[1], ct.VIEW_POS[2]])   # Changes values after pressing right or left
        self.camUp = np.array([0, 0, 1])
        self.distance = 10      # Speed to which move camera closer or farther
        self.circleCollisions = True
        self.fillPolygon = True
        self.stop = False       # Ball movement
        self.addBall = False
        self.delBall = False

controller = Controller()   # Generating the controller

def cameraChange(camera_theta): # Changes camera position (to the right or left) based on camera_theta
    global controller # Necessary?

    camX = controller.setStartingCamera[0] * np.sin(camera_theta)
    camY = controller.setStartingCamera[0] * np.cos(camera_theta)
    controller.viewPos[0] = camX
    controller.viewPos[1] = camY

def window_resize(window, width, height): # To fix content when resizing window
    glViewport(0, 0, width, height)

def on_key(window, key, scancode, action, mods): # When keys are pressed, does something

    if action != glfw.PRESS:
        return

    global controller

    # The print part explains every statement

    if key == glfw.KEY_ESCAPE:  # Closes the program
        glfw.set_window_should_close(window, True)

    elif key == glfw.KEY_LEFT_CONTROL:
        controller.showAxis = not controller.showAxis
        print("Show Axis?", controller.showAxis)

    elif key == glfw.KEY_SPACE: # Reset camera
        position = np.array([ct.VIEW_POS[0], ct.VIEW_POS[1], ct.VIEW_POS[2]])
        controller.setStartingCamera = np.array([ct.VIEW_POS[0], ct.VIEW_POS[1], ct.VIEW_POS[2]])
        controller.viewPos = position   # The two cannot share the same variable
        controller.camera_theta = np.pi/4
        print("Reseting camera to starting position", position)
    
    elif key == glfw.KEY_A:
        controller.addBall = True
        print("Add another ball?", controller.addBall)

    elif key == glfw.KEY_S:
        controller.stop = not controller.stop
        print("Stop movement?", controller.stop)

    elif key == glfw.KEY_D:
        controller.delBall = True
        if ct.NUMBER_BALLS <= 0:
            print("Current balls", ct.NUMBER_BALLS)
        else:
            print("Delete last ball?", controller.delBall)

    elif key == glfw.KEY_1:
        controller.circleCollisions = not controller.circleCollisions
        print("Collisions?", controller.circleCollisions)

    elif key == glfw.KEY_2:
        controller.fillPolygon = not controller.fillPolygon
        print("Fill polygons?", controller.fillPolygon)

    elif key == glfw.KEY_RIGHT: # Changes camera position based on ROTATION
        controller.camera_theta -= ROTATION
        cameraChange(controller.camera_theta)
        print("Moving camera right")

    elif key == glfw.KEY_LEFT:
        controller.camera_theta += ROTATION
        cameraChange(controller.camera_theta)
        print("Moving camera left")

    else:
        print('Unknown key')

class Shape: # For gpu_shape and easy_shaders
    def __init__(self, vertexData, indexData):
        self.vertices = vertexData
        self.indices = indexData

def createGPUShape(pipeline, shape):
    gpuShape = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuShape)
    gpuShape.fillBuffers(shape.vertices, shape.indices, GL_STATIC_DRAW)
    return gpuShape

def randomColor():  # Generates a random color with two decimals (ex: 0,64)
    return [round(rd.randint(0,255)/255,2),round(rd.randint(0,255)/255,2),round(rd.randint(0,255)/255,2)]

class BeachBall: # Balls class. Makes easier to configure each of them
    def __init__(self, pipeline, position, vel, ac, radius):
        self.pipeline = pipeline
        self.position = np.array([position[0], position[1], position[2]], dtype="complex")
        self.vel = np.array([vel[0], vel[1], vel[2]], dtype="complex")
        self.ac = np.array([ac[0], ac[1], ac[2]])
        self.radius = radius
        self.ballColor = randomColor()
        self.gpuShape = createGPUShape(self.pipeline, self.createSphere())

    def update(self, dt):   # Updates position and speed of the ball
        self.position[0] += self.vel[0]*dt
        self.position[1] += self.vel[1]*dt
        self.position[2] += self.vel[2]*dt

        self.vel[0] += self.ac[0]*dt
        self.vel[1] += self.ac[1]*dt
        self.vel[2] += self.ac[2]*dt
        
    def draw(self): # From ex_collisions.py, draws the balls
        glUniformMatrix4fv(glGetUniformLocation(self.pipeline.shaderProgram, "model"), 1, GL_TRUE,
            tr.translate(self.position[0], self.position[1], self.position[2])
        )
        self.pipeline.drawCall(self.gpuShape)

    def checkCollideWithBorder(self):   # To check and fix when balls collide with cube's borders
        # only affects vel except in Z axis where it bugs out because of the requirement that when touching the ceiling speed is 0.
        # X axis
        if self.position[0] + self.radius > ct.L/2:
            self.vel[0] = -abs(self.vel[0])
        if self.position[0] - self.radius < -ct.L/2:
            self.vel[0] = abs(self.vel[0])
        # Y axis
        if self.position[1] + self.radius > ct.L/2:
            self.vel[1] = -abs(self.vel[1])
        if self.position[1] - self.radius < -ct.L/2:
            self.vel[1] = abs(self.vel[1])
        # Z axis
        if self.position[2] + self.radius > ct.L/2:
            self.vel[2] = 0
            self.position[2] = self.position[2] - ct.RADIUS/20  #Translate the ball from the celing to not bug out
        if self.position[2] - self.radius < -ct.L/2:
            self.vel[2] = abs(self.vel[2])        

    def createSphere(self): # Internet es una salvacion :) # Generates the balls vertexData and indexData 
        X_SEGMENTS = 50
        Y_SEGMENTS = 50
        vertexData = []
        indexData = []

        # Vertixes of sphere
        for y in range(Y_SEGMENTS+1):
            for x in range(X_SEGMENTS+1):
                xSegment = x / X_SEGMENTS
                ySegment = y / Y_SEGMENTS
                xPos = ct.RADIUS*np.cos(xSegment * 2.0 * np.pi) * np.sin(ySegment * np.pi)
                yPos = ct.RADIUS*np.cos(ySegment * np.pi)
                zPos = ct.RADIUS*np.sin(xSegment * 2.0 * np.pi) * np.sin(ySegment * np.pi)
                vertexData += xPos, yPos, zPos, self.ballColor[0], self.ballColor[1], self.ballColor[2]

        # Indexes of sphere
        for i in range(Y_SEGMENTS):
            for j in range(X_SEGMENTS):
                indexData += [i * (X_SEGMENTS + 1) + j]
                indexData += [(i + 1) * (X_SEGMENTS + 1) + j]
                indexData += [(i + 1) * (X_SEGMENTS + 1) + j+1]
                indexData += [i* (X_SEGMENTS + 1) + j]
                indexData += [(i + 1) * (X_SEGMENTS + 1) + j + 1]
                indexData += [i * (X_SEGMENTS + 1) + j + 1]

        return Shape(vertexData, indexData)

def areColliding(circle1, circle2): # From ex_collisions.py # Checks if balls are colliding with each other # Returns True or False
    # In collide() we use this same code but it is more efficient first checking if balls are colliding
    
    assert isinstance(circle1, BeachBall)                   
    assert isinstance(circle2, BeachBall)

    difference = circle2.position - circle1.position
    distance = np.linalg.norm(difference)               # norm is current distance between centers
    collisionDistance = circle2.radius + circle1.radius # ideal distance between centers (2*RADIUS)
    return distance < collisionDistance

def collide(circle1, circle2): # From ex_collisions.py # Adds bounce to balls
    """
    If there are a collision between the circles, it modifies the velocity of
    both circles in a way that preserves energy and momentum.
    """
    
    assert isinstance(circle1, BeachBall)
    assert isinstance(circle2, BeachBall)
    
    # Moves one sphere to the side if they share the same position (Start of the program)
    if np.array_equal(circle1.position, circle2.position):
        circle2.position += ct.RADIUS*2

    # Getting normalized vector between ball centers
    normal = circle2.position - circle1.position
    normal /= np.linalg.norm(normal)

    # Formula to get circles bounce in an elastic way 
    vi1 = circle1.vel                           # Initial speed
    vf1 = np.dot(circle1.vel, normal) * normal  # Final speed direction
    circle1.vel = vi1 - (2*vf1)                 # Elastic speed

    vi2 = circle2.vel                           # Initial speed
    vf2 = np.dot(circle2.vel, normal) * normal  # Final speed direction
    circle2.vel = vi2 - (2*vf2)                 # Elastic speed

    # To fix beach balls getting stuck together
    difference = circle2.position - circle1.position
    distance = np.linalg.norm(difference) # norm is current distance between centers
    collisionDistance = circle2.radius + circle1.radius # ideal distance between centers

    # To fix balls stucking together and balls sometimes teleporting to other position
    # when that happens the balls are separated until all position coordinates are 2*RADIUS distance apart
    if circle1.position[0] > circle2.position[0]:               # X Axis
        circle1.position[0] += (collisionDistance - distance)
    else:
        circle2.position[0] += (collisionDistance - distance)
    if circle1.position[1] > circle2.position[1]:               # Y Axis
        circle1.position[1] += (collisionDistance - distance)
    else:
        circle2.position[1] += (collisionDistance - distance)
    if circle1.position[2] > circle2.position[2]:               # Z Axis
        circle1.position[2] += (collisionDistance - distance)
    else:
        circle2.position[2] += (collisionDistance - distance)
        
def createCube(): # Genereates a cube's vertexData and indexData

    vertexData = np.array([
        # positions                 # colors
        -ct.L/2, -ct.L/2,  ct.L/2,  1.0, 1.0, 1.0,   # 0 Bottom left
         ct.L/2, -ct.L/2,  ct.L/2,  1.0, 1.0, 1.0,   # 1 Bottom front
         ct.L/2,  ct.L/2,  ct.L/2,  1.0, 1.0, 1.0,   # 2 Top front
        -ct.L/2,  ct.L/2,  ct.L/2,  1.0, 1.0, 1.0,   # 3 Top left
 
        -ct.L/2, -ct.L/2, -ct.L/2,  1.0, 1.0, 1.0,   # 4 Bottom back
         ct.L/2, -ct.L/2, -ct.L/2,  1.0, 1.0, 1.0,   # 5 Bottom right
         ct.L/2,  ct.L/2, -ct.L/2,  1.0, 1.0, 1.0,   # 6 Top right
        -ct.L/2,  ct.L/2, -ct.L/2,  1.0, 1.0, 1.0    # 7 Top back
    ], dtype=np.float32)

    indexData = np.array([
        0, 1, 1, 5, 5, 4, 4, 0, # Left square
        3, 2, 2, 6, 6, 7, 7, 3, # Right square
        0, 3, 1, 2, 5, 6, 4, 7  # Horizontal lines (Left, Front, Right, Back)
    ])

    return Shape(vertexData, indexData)

def main():
    # Initialize glfw
    if not glfw.init():
        glfw.set_window_should_close(window, True)
    
    # Creating window
    window = glfw.create_window(ct.WINDOW_WIDTH, ct.WINDOW_HEIGHT, ct.WINDOW_TITLE, None, None)

    if not window:
        glfw.terminate()
        glfw.set_window_should_close(window, True)
    
    # Set the position of window and make context current. Also when windows is resized it resizes the content
    glfw.set_window_pos(window, 150, 50) 
    glfw.make_context_current(window)
    glfw.set_window_size_callback(window, window_resize)
 
    # Connecting the callback function 'on_key' to handle keyboard events
    glfw.set_key_callback(window, on_key) # From Tarea0

    # Creating our shader program
    pipeline = es.SimpleModelViewProjectionShaderProgram()
    glUseProgram(pipeline.shaderProgram)

    # Creating shapes on GPU memory
    #Cube
    cube = createCube()
    gpuCube = createGPUShape(pipeline, cube)
    
    # Axis
    axis = bs.createAxis(8)
    gpuAxis = createGPUShape(pipeline, axis)

    # Generating beach balls (comes with their GPU shape)
    def npArray(array):
        npArray = np.array(array, dtype=np.float32)
        return npArray
    balls = []
    for i in range(ct.NUMBER_BALLS):
        balls += [BeachBall(pipeline, npArray(ct.POSITION), np.array(ct.VEL), np.array(ct.ACCELERATION), ct.RADIUS)]
      
    # Generating camera placement
    projection = tr.perspective(30, float(ct.WINDOW_WIDTH)/float(ct.WINDOW_HEIGHT), 0.1, 100)

    # Background color
    glClearColor(ct.BACKGROUND_COLOR[0], ct.BACKGROUND_COLOR[1], ct.BACKGROUND_COLOR[2], 1.0)

    # Gives depth to figures
    glEnable(GL_DEPTH_TEST)

    # To monitor the performance
    perfMonitor = pm.PerformanceMonitor(glfw.get_time(), 0.5)

    while not glfw.window_should_close(window):
        # Using GLFW to check for input events
        glfw.poll_events()

        # Measuring performance
        perfMonitor.update(glfw.get_time())
        deltaTime = perfMonitor.getDeltaTime()
        glfw.set_window_title(window, ct.WINDOW_TITLE + str(perfMonitor))

        # From ex_bouncing_balls.py and ex_height_plotter.py # Controls camera placement
        view = tr.lookAt( 
            controller.viewPos,
            np.array([0,0,0]),
            controller.camUp
        )

        # To move the camera closer or farther
        def closerFartherCamera(operator):
            if operator == "-":
                op = "+"
                inv = "-"
            elif operator == "+":
                op = "-"
                inv = "+"
            # X Axis
            if controller.setStartingCamera[0] >= 0:# Closes in from positive axis
                controller.setStartingCamera[0] = eval(str(controller.setStartingCamera[0]) + op + str(controller.distance * deltaTime))
            else:                                   # Closes in from negative axis
                controller.setStartingCamera[0] = eval(str(controller.setStartingCamera[0]) + inv + str(controller.distance * deltaTime))

            if controller.viewPos[0] >= 0:# Closes in from positive axis
                controller.viewPos[0] = eval(str(controller.viewPos[0]) + op + str(controller.distance * deltaTime))
            else:                         # Closes in from negative axis
                controller.viewPos[0] = eval(str(controller.viewPos[0]) + inv + str(controller.distance * deltaTime))
            # Y axis
            if controller.setStartingCamera[1] >= 0:# Closes in from positive axis
                controller.setStartingCamera[1] = eval(str(controller.setStartingCamera[1]) + op + str(controller.distance * deltaTime))
            else:                                   # Closes in from negative axis
                controller.setStartingCamera[1] = eval(str(controller.setStartingCamera[1]) + inv + str(controller.distance * deltaTime))

            if controller.viewPos[1] >= 0:# Closes in from positive axis
                controller.viewPos[1] = eval(str(controller.viewPos[1]) + op + str(controller.distance * deltaTime))
            else:                         # Closes in from negative axis
                controller.viewPos[1] = eval(str(controller.viewPos[1]) + inv + str(controller.distance * deltaTime))

        if (glfw.get_key(window, glfw.KEY_UP) == glfw.PRESS):   # Camera closer
            closerFartherCamera("+")
            controller.camera_theta = np.pi/4

        if (glfw.get_key(window, glfw.KEY_DOWN) == glfw.PRESS): # Camera farther
            closerFartherCamera("-")
            controller.camera_theta = np.pi/4

        # Clearing the screen and changing background color
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # They all affect objects position due to easy_shaders.py
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)

        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "view"), 1, GL_TRUE, view)

        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, tr.matmul([
            tr.translate(0.0, 0.0, 0.0),          
            tr.scale(1.0, 1.0, 1.0)
        ]))

        # To show/hide axis lines
        if controller.showAxis:
            pipeline.drawCall(gpuAxis, GL_LINES)

        pipeline.drawCall(gpuCube, GL_LINES)

        # Beach Balls:

        # Add balls
        if controller.addBall:
            balls += [BeachBall(pipeline, npArray(ct.POSITION), np.array(ct.VEL), np.array(ct.ACCELERATION), ct.RADIUS)]
            controller.addBall = not controller.addBall
            ct.NUMBER_BALLS += 1
            print("Current balls:", ct.NUMBER_BALLS)
        # Delete balls
        if controller.delBall:
            controller.delBall = not controller.delBall
            if len(balls) > 0:
                balls = balls[:len(balls)-1]
                ct.NUMBER_BALLS -= 1
                print("Current balls:", ct.NUMBER_BALLS)

        # Filling or not the shapes depending on the controller state
        if (controller.fillPolygon):
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
            
        # Checking and processing collisions among circles # Obtained from ex_collision.py
        if controller.circleCollisions and (len(balls) >= 2):
            for i in range(ct.NUMBER_BALLS):
                for j in range(i+1, ct.NUMBER_BALLS):
                    if areColliding(balls[i], balls[j]):
                        collide(balls[i], balls[j])

        # Drawing balls. Movement stops if controller.stop == True
        if controller.stop:
            for gpuBall in balls:
                gpuBall.checkCollideWithBorder()
                gpuBall.draw()
        else: 
            for gpuBall in balls:
                gpuBall.update(deltaTime)
                gpuBall.checkCollideWithBorder()
                gpuBall.draw()
        
        # Once the drawing is rendered, buffers are swap so an uncomplete drawing is never seen.
        glfw.swap_buffers(window)

    # Clearing GPU memory
    gpuCube.clear()
    gpuAxis.clear()

    glfw.terminate()

if __name__ == "__main__":
    main()