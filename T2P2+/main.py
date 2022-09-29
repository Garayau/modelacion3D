# coding=utf-8
"""Texture Quad in 2D"""

from random import randint
import glfw
from OpenGL.GL import *
import numpy as np
import grafica.constants as ct
import grafica.lighting_shaders as ls
import grafica.performance_monitor as pm
import grafica.transformations as tr
import grafica.basic_shapes as bs
import grafica.easy_shaders as es
from auxiliarT5 import *
from grafica.assets_path import getAssetPath
import grafica.scene_graph as sg
from casas import createCasa1, createCasa2, createCasa3



# A class to store the application control
class Controller:
    def __init__(self):
        self.fillPolygon = True
        self.showAxis = True
        self.eye = [0, 0, 2]        # Posición en la que está la cámara inicialmente
        self.at = [0, 0, 2]         # Posición a la que mira la cámara inicialmente
        self.up = [0, 1, 0]
        self.estado = 0             # Estado en el que se encuentra el programa: 0 primera persona, 1 vista desde arriba
        self.Theta = np.pi          # Ánguilo inicial de la cámara       
        self.movSpeed = np.pi/50    # Velocidad a la que se mueve la cámara
        self.sunMoonPos = 3*np.pi/2 # + np.pi/12 # Depends on how slow or fast a day passes
        self.time = 0
       
       
        self.X = 2.0 #posicion X de donde esta el auto
        self.Y = -0.037409 #posicion Y de donde esta el auto
        self.Z = 5.0 #posicion Z de donde esta el auto
        #lo siguiente se creo para poder usar coordenadas esfericas
        self.cameraPhiAngle = -np.pi/4 #inclinacion de la camara 
        self.cameraThetaAngle = np.pi/2 #rotacion con respecto al eje y
        self.r = 2 #radio
                
class Spotlight:
    def __init__(self):
        self.ambient = np.array([0,0,0])
        self.diffuse = np.array([0,0,0])
        self.specular = np.array([0,0,0])
        self.constant = 0
        self.linear = 0
        self.quadratic = 0
        self.position = np.array([0,0,0])
        self.direction = np.array([0,0,0])
        self.cutOff = 0
        self.outerCutOff = 0

class Pointlight:
    def __init__(self):
        self.ambient = np.array([0,0,0])
        self.diffuse = np.array([0,0,0])
        self.specular = np.array([0,0,0])
        self.constant = 0
        self.linear = 0
        self.quadratic = 0
        self.position = np.array([0,0,0])
        self.direction = np.array([0,1,0])
        self.cutOff = 0
        self.outerCutOff = 0

controller = Controller()

spotlightsPool = dict()
pointlightsPool = dict()

def setLights():
    # Primera luz pointlight. Sol
    sun = Spotlight()
    sun.ambient = np.array([0.0, 0.0, 0.0])
    sun.diffuse = np.array([1.0, 1.0, 1.0])
    sun.specular = np.array([1.0, 1.0, 1.0])
    sun.constant = 0.0001
    sun.linear = 0.03
    sun.quadratic = 0.01
    sun.position = np.array([0, 10*np.sin(controller.sunMoonPos), -10*np.cos(controller.sunMoonPos)]) #TAREA4: esta ubicada en esta posición

    # sun.direction = np.array([0, -1, 0]) #TAREA4: está apuntando perpendicularmente hacia el terreno (Y-, o sea hacia abajo)
    # sun.cutOff = np.cos(np.radians(12.5)) #TAREA4: corte del ángulo para la luz
    # sun.outerCutOff = np.cos(np.radians(45)) #TAREA4: la apertura permitida de la luz es de 45°
                                                #mientras más alto es este ángulo, más se difumina su efecto

    pointlightsPool['sun'] = sun # almacenamos la luz en el diccionario, con una clave única

    # Segunda luz pointlight. Luna
    moon = Spotlight()
    moon.ambient = np.array([0.0, 0.0, 0.0])
    moon.diffuse = np.array([1.0, 1.0, 1.0])
    moon.specular = np.array([1.0, 1.0, 1.0])
    moon.constant = 0.0001
    moon.linear = 0.03
    moon.quadratic = 0.01
    moon.position = np.array([0, -10*np.sin(controller.sunMoonPos), 10*np.cos(controller.sunMoonPos)]) #TAREA4: esta ubicada en esta posición

    # moon.direction = np.array([0, -1, 0]) #TAREA4: está apuntando perpendicularmente hacia el terreno (Y-, o sea hacia abajo)
    # moon.cutOff = np.cos(np.radians(12.5)) #TAREA4: corte del ángulo para la luz
    # moon.outerCutOff = np.cos(np.radians(45)) #TAREA4: la apertura permitida de la luz es de 45°
                                                #mientras más alto es este ángulo, más se difumina su efecto

    pointlightsPool['moon'] = moon # almacenamos la luz en el diccionario, con una clave única



    #TAREA4: Primera luz spotlight
    spot1 = Spotlight()
    spot1.ambient = np.array([0, 0, 0])
    spot1.diffuse = np.array([5.0, 1.0, 1.0])
    spot1.specular = np.array([1.0, 1.0, 1.0])
    spot1.constant = 1.0
    spot1.linear = 0.09
    spot1.quadratic = 0.032
    spot1.position = np.array([0.2, 1, 2]) #TAREA4: esta ubicada en esta posición
    spot1.direction = np.array([0, -1, 0]) #TAREA4: está apuntando perpendicularmente hacia el terreno (Y-, o sea hacia abajo)
    spot1.cutOff = np.cos(np.radians(12.5)) #TAREA4: corte del ángulo para la luz
    spot1.outerCutOff = np.cos(np.radians(30)) #TAREA4: la apertura permitida de la luz es de 45°
                                                #mientras más alto es este ángulo, más se difumina su efecto
    
    spotlightsPool['spot1'] = spot1 #TAREA4: almacenamos la luz en el diccionario, con una clave única

    #TAREA4: Segunda luz spotlight
    spot2 = Spotlight()
    spot2.ambient = np.array([0, 0, 0])
    spot2.diffuse = np.array([5.0, 1.0, 1.0])
    spot2.specular = np.array([1.0, 1.0, 1.0])
    spot2.constant = 1.0
    spot2.linear = 0.09
    spot2.quadratic = 0.032
    spot2.position = np.array([1.2, 1, 2]) #TAREA4: Está ubicada en esta posición
    spot2.direction = np.array([0, -1, 0]) #TAREA4: también apunta hacia abajo
    spot2.cutOff = np.cos(np.radians(12.5))
    spot2.outerCutOff = np.cos(np.radians(30)) #TAREA4: Esta luz tiene menos apertura, por eso es más focalizada
    spotlightsPool['spot2'] = spot2 #TAREA4: almacenamos la luz en el diccionario

    #TAREA5: Luces spotlights para los faros de los autos (3 y 4)
    spot3 = Spotlight()
    spot3.ambient = np.array([0, 0, 0])
    spot3.diffuse = np.array([1.0, 1.0, 1.0])
    spot3.specular = np.array([1.0, 1.0, 1.0])
    spot3.constant = 1.0
    spot3.linear = 0.09
    spot3.quadratic = 0.032
    spot3.position = np.array([2.10, 0.15, 4.8]) # posición inicial
    spot3.direction = np.array([0, -0.5, -1]) # dirección inicial
    spot3.cutOff = np.cos(np.radians(12.5)) 
    spot3.outerCutOff = np.cos(np.radians(30)) 
    spotlightsPool['spot3'] = spot3 #TAREA4: almacenamos la luz en el diccionario

    spot4 = Spotlight()
    spot4.ambient = np.array([0, 0, 0])
    spot4.diffuse = np.array([1.0, 1.0, 1.0])
    spot4.specular = np.array([1.0, 1.0, 1.0])
    spot4.constant = 1.0
    spot4.linear = 0.09
    spot4.quadratic = 0.032
    spot4.position = np.array([1.89, 0.15, 4.8])
    spot4.direction = np.array([0, -0.5, -1])
    spot4.cutOff = np.cos(np.radians(12.5))
    spot4.outerCutOff = np.cos(np.radians(30)) 
    spotlightsPool['spot4'] = spot4 #TAREA4: almacenamos la luz en el diccionario

    # Luces de faros (5 y 6)
    spot5 = Spotlight()
    spot5.ambient = np.array([0, 0, 0])
    spot5.diffuse = np.array([5.0, 1.0, 1.0])
    spot5.specular = np.array([1.0, 1.0, 1.0])
    spot5.constant = 1.0
    spot5.linear = 0.09
    spot5.quadratic = 0.032
    spot5.position = np.array([2.2, 1, 2])
    spot5.direction = np.array([0, -1, 0]) 
    spot5.cutOff = np.cos(np.radians(12.5)) 
    spot5.outerCutOff = np.cos(np.radians(30)) 
    spotlightsPool['spot5'] = spot5 #TAREA4: almacenamos la luz en el diccionario

    spot6 = Spotlight()
    spot6.ambient = np.array([0, 0, 0])
    spot6.diffuse = np.array([5.0, 1.0, 1.0])
    spot6.specular = np.array([1.0, 1.0, 1.0])
    spot6.constant = 1.0
    spot6.linear = 0.09
    spot6.quadratic = 0.032
    spot6.position = np.array([3.2, 1, 2])
    spot6.direction = np.array([0, -1, 0]) 
    spot6.cutOff = np.cos(np.radians(12.5))
    spot6.outerCutOff = np.cos(np.radians(30)) 
    spotlightsPool['spot6'] = spot6 #TAREA4: almacenamos la luz en el diccionario

def setPlot(texPipeline, axisPipeline, lightPipeline):
    projection = tr.perspective(60, float(ct.WIDTH)/float(ct.HEIGHT), 0.1, 100) #el primer parametro se cambia a 60 para que se vea más escena

    glUseProgram(axisPipeline.shaderProgram)
    glUniformMatrix4fv(glGetUniformLocation(axisPipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)

    #TAREA4: Como tenemos 2 shaders con múltiples luces, tenemos que enviar toda esa información a cada shader
    #TAREA4: Primero al shader de color
    glUseProgram(lightPipeline.shaderProgram)
    glUniformMatrix4fv(glGetUniformLocation(lightPipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
    
    #TAREA4: Enviamos la información de la luz puntual y del material
    #TAREA4: La luz puntual está desactivada por defecto (ya que su componente ambiente es 0.0, 0.0, 0.0), pero pueden usarla
    # para añadir más realismo a la escena. AHORA HA SIDO ACTIVADA

    for i, (k,v) in enumerate(pointlightsPool.items()):
        baseString = "pointLights[" + str(i) + "]."
        glUniform3fv(glGetUniformLocation(lightPipeline.shaderProgram, baseString + "ambient"), 1, v.ambient)
        glUniform3fv(glGetUniformLocation(lightPipeline.shaderProgram, baseString + "diffuse"), 1, v.diffuse)
        glUniform3fv(glGetUniformLocation(lightPipeline.shaderProgram, baseString + "specular"), 1, v.specular)
        glUniform1f(glGetUniformLocation(lightPipeline.shaderProgram, baseString + "constant"), v.constant)
        glUniform1f(glGetUniformLocation(lightPipeline.shaderProgram, baseString + "linear"), v.linear)
        glUniform1f(glGetUniformLocation(lightPipeline.shaderProgram, baseString + "quadratic"), v.quadratic)
        glUniform3fv(glGetUniformLocation(lightPipeline.shaderProgram, baseString + "position"), 1, v.position)
        # glUniform3fv(glGetUniformLocation(lightPipeline.shaderProgram, baseString + "direction"), 1, v.direction)
        # glUniform1f(glGetUniformLocation(lightPipeline.shaderProgram, baseString + "cutOff"), v.cutOff)
        # glUniform1f(glGetUniformLocation(lightPipeline.shaderProgram, baseString + "outerCutOff"), v.outerCutOff)

    # glUniform3f(glGetUniformLocation(lightPipeline.shaderProgram, "pointLights[0].ambient"), 0.2, 0.2, 0.2)
    # glUniform3f(glGetUniformLocation(lightPipeline.shaderProgram, "pointLights[0].diffuse"), 0.0, 0.0, 0.0)
    # glUniform3f(glGetUniformLocation(lightPipeline.shaderProgram, "pointLights[0].specular"), 0.0, 0.0, 0.0)
    # glUniform1f(glGetUniformLocation(lightPipeline.shaderProgram, "pointLights[0].constant"), 0.1)
    # glUniform1f(glGetUniformLocation(lightPipeline.shaderProgram, "pointLights[0].linear"), 0.1)
    # glUniform1f(glGetUniformLocation(lightPipeline.shaderProgram, "pointLights[0].quadratic"), 0.01)
    # glUniform3f(glGetUniformLocation(lightPipeline.shaderProgram, "pointLights[0].position"), 5, 5, 5)

    glUniform3f(glGetUniformLocation(lightPipeline.shaderProgram, "material.ambient"), 0.2, 0.2, 0.2)
    glUniform3f(glGetUniformLocation(lightPipeline.shaderProgram, "material.diffuse"), 0.9, 0.9, 0.9)
    glUniform3f(glGetUniformLocation(lightPipeline.shaderProgram, "material.specular"), 1.0, 1.0, 1.0)
    glUniform1f(glGetUniformLocation(lightPipeline.shaderProgram, "material.shininess"), 32)

    #TAREA4: Aprovechamos que las luces spotlight están almacenadas en el diccionario para mandarlas al shader
    if controller.time in range(0,8) or controller.time in range(18, 24):
        for i, (k,v) in enumerate(spotlightsPool.items()):
            baseString = "spotLights[" + str(i) + "]."
            glUniform3fv(glGetUniformLocation(lightPipeline.shaderProgram, baseString + "ambient"), 1, v.ambient)
            glUniform3fv(glGetUniformLocation(lightPipeline.shaderProgram, baseString + "diffuse"), 1, v.diffuse)
            glUniform3fv(glGetUniformLocation(lightPipeline.shaderProgram, baseString + "specular"), 1, v.specular)
            glUniform1f(glGetUniformLocation(lightPipeline.shaderProgram, baseString + "constant"), v.constant)
            glUniform1f(glGetUniformLocation(lightPipeline.shaderProgram, baseString + "linear"), 0.09)
            glUniform1f(glGetUniformLocation(lightPipeline.shaderProgram, baseString + "quadratic"), 0.032)
            glUniform3fv(glGetUniformLocation(lightPipeline.shaderProgram, baseString + "position"), 1, v.position)
            glUniform3fv(glGetUniformLocation(lightPipeline.shaderProgram, baseString + "direction"), 1, v.direction)
            glUniform1f(glGetUniformLocation(lightPipeline.shaderProgram, baseString + "cutOff"), v.cutOff)
            glUniform1f(glGetUniformLocation(lightPipeline.shaderProgram, baseString + "outerCutOff"), v.outerCutOff)
    else:
        for i, (k,v) in enumerate(spotlightsPool.items()):
            baseString = "spotLights[" + str(i) + "]."
            glUniform3fv(glGetUniformLocation(lightPipeline.shaderProgram, baseString + "ambient"), 1, v.ambient)
            glUniform3fv(glGetUniformLocation(lightPipeline.shaderProgram, baseString + "diffuse"), 1, v.diffuse)
            glUniform3fv(glGetUniformLocation(lightPipeline.shaderProgram, baseString + "specular"), 1, v.specular)
            glUniform1f(glGetUniformLocation(lightPipeline.shaderProgram, baseString + "constant"), v.constant)
            glUniform1f(glGetUniformLocation(lightPipeline.shaderProgram, baseString + "linear"), 0.09)
            glUniform1f(glGetUniformLocation(lightPipeline.shaderProgram, baseString + "quadratic"), 0.032)
            glUniform3fv(glGetUniformLocation(lightPipeline.shaderProgram, baseString + "position"), 1, [0,-60,0])
            glUniform3fv(glGetUniformLocation(lightPipeline.shaderProgram, baseString + "direction"), 1, v.direction)
            glUniform1f(glGetUniformLocation(lightPipeline.shaderProgram, baseString + "cutOff"), v.cutOff)
            glUniform1f(glGetUniformLocation(lightPipeline.shaderProgram, baseString + "outerCutOff"), v.outerCutOff)

    #TAREA4: Ahora repetimos todo el proceso para el shader de texturas con mútiples luces
    glUseProgram(texPipeline.shaderProgram)
    glUniformMatrix4fv(glGetUniformLocation(texPipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
    
    for i, (k,v) in enumerate(pointlightsPool.items()):
        baseString = "pointLights[" + str(i) + "]."
        glUniform3fv(glGetUniformLocation(texPipeline.shaderProgram, baseString + "ambient"), 1, v.ambient)
        glUniform3fv(glGetUniformLocation(texPipeline.shaderProgram, baseString + "diffuse"), 1, v.diffuse)
        glUniform3fv(glGetUniformLocation(texPipeline.shaderProgram, baseString + "specular"), 1, v.specular)
        glUniform1f(glGetUniformLocation(texPipeline.shaderProgram, baseString + "constant"), v.constant)
        glUniform1f(glGetUniformLocation(texPipeline.shaderProgram, baseString + "linear"), v.linear)
        glUniform1f(glGetUniformLocation(texPipeline.shaderProgram, baseString + "quadratic"), v.quadratic)
        glUniform3fv(glGetUniformLocation(texPipeline.shaderProgram, baseString + "position"), 1, v.position)
        # glUniform3fv(glGetUniformLocation(texPipeline.shaderProgram, baseString + "direction"), 1, v.direction)
        # glUniform1f(glGetUniformLocation(texPipeline.shaderProgram, baseString + "cutOff"), v.cutOff)
        # glUniform1f(glGetUniformLocation(texPipeline.shaderProgram, baseString + "outerCutOff"), v.outerCutOff)

    # glUniform3f(glGetUniformLocation(texPipeline.shaderProgram, "pointLights[0].ambient"), 0.2, 0.2, 0.2)
    # glUniform3f(glGetUniformLocation(texPipeline.shaderProgram, "pointLights[0].diffuse"), 0.0, 0.0, 0.0)
    # glUniform3f(glGetUniformLocation(texPipeline.shaderProgram, "pointLights[0].specular"), 0.0, 0.0, 0.0)
    # glUniform1f(glGetUniformLocation(texPipeline.shaderProgram, "pointLights[0].constant"), 0.1)
    # glUniform1f(glGetUniformLocation(texPipeline.shaderProgram, "pointLights[0].linear"), 0.1)
    # glUniform1f(glGetUniformLocation(texPipeline.shaderProgram, "pointLights[0].quadratic"), 0.01)
    # glUniform3f(glGetUniformLocation(texPipeline.shaderProgram, "pointLights[0].position"), 5, 5, 5)

    glUniform3f(glGetUniformLocation(texPipeline.shaderProgram, "material.ambient"), 0.2, 0.2, 0.2)
    glUniform3f(glGetUniformLocation(texPipeline.shaderProgram, "material.diffuse"), 0.9, 0.9, 0.9)
    glUniform3f(glGetUniformLocation(texPipeline.shaderProgram, "material.specular"), 1.0, 1.0, 1.0)
    glUniform1f(glGetUniformLocation(texPipeline.shaderProgram, "material.shininess"), 32)

    if controller.time in range(0,8) or controller.time in range(18, 24):
        for i, (k,v) in enumerate(spotlightsPool.items()):
            baseString = "spotLights[" + str(i) + "]."
            glUniform3fv(glGetUniformLocation(texPipeline.shaderProgram, baseString + "ambient"), 1, v.ambient)
            glUniform3fv(glGetUniformLocation(texPipeline.shaderProgram, baseString + "diffuse"), 1, v.diffuse)
            glUniform3fv(glGetUniformLocation(texPipeline.shaderProgram, baseString + "specular"), 1, v.specular)
            glUniform1f(glGetUniformLocation(texPipeline.shaderProgram, baseString + "constant"), v.constant)
            glUniform1f(glGetUniformLocation(texPipeline.shaderProgram, baseString + "linear"), 0.09)
            glUniform1f(glGetUniformLocation(texPipeline.shaderProgram, baseString + "quadratic"), 0.032)
            glUniform3fv(glGetUniformLocation(texPipeline.shaderProgram, baseString + "position"), 1, v.position)
            glUniform3fv(glGetUniformLocation(texPipeline.shaderProgram, baseString + "direction"), 1, v.direction)
            glUniform1f(glGetUniformLocation(texPipeline.shaderProgram, baseString + "cutOff"), v.cutOff)
            glUniform1f(glGetUniformLocation(texPipeline.shaderProgram, baseString + "outerCutOff"), v.outerCutOff)
    else:
        for i, (k,v) in enumerate(spotlightsPool.items()):
            baseString = "spotLights[" + str(i) + "]."
            glUniform3fv(glGetUniformLocation(texPipeline.shaderProgram, baseString + "ambient"), 1, v.ambient)
            glUniform3fv(glGetUniformLocation(texPipeline.shaderProgram, baseString + "diffuse"), 1, v.diffuse)
            glUniform3fv(glGetUniformLocation(texPipeline.shaderProgram, baseString + "specular"), 1, v.specular)
            glUniform1f(glGetUniformLocation(texPipeline.shaderProgram, baseString + "constant"), v.constant)
            glUniform1f(glGetUniformLocation(texPipeline.shaderProgram, baseString + "linear"), 0.09)
            glUniform1f(glGetUniformLocation(texPipeline.shaderProgram, baseString + "quadratic"), 0.032)
            glUniform3fv(glGetUniformLocation(texPipeline.shaderProgram, baseString + "position"), 1, [0,-60,0])
            glUniform3fv(glGetUniformLocation(texPipeline.shaderProgram, baseString + "direction"), 1, v.direction)
            glUniform1f(glGetUniformLocation(texPipeline.shaderProgram, baseString + "cutOff"), v.cutOff)
            glUniform1f(glGetUniformLocation(texPipeline.shaderProgram, baseString + "outerCutOff"), v.outerCutOff)


def setView(texPipeline, axisPipeline, lightPipeline, view, projection):
    #la idea de usar coordenadas esfericas para la camara fue extraida del auxiliar 6
    #como el auto reposa en el plano XZ, no sera necesaria la coordenada Y esferica.
    # Xesf = controller.r * np.sin(controller.cameraPhiAngle)*np.cos(controller.cameraThetaAngle) #coordenada X esferica
    # Zesf = controller.r * np.sin(controller.cameraPhiAngle)*np.sin(controller.cameraThetaAngle) #coordenada Y esferica

    #viewPos = np.array([controller.X-Xesf,0.5,controller.Z-Zesf])
    # view = tr.lookAt(
    #         viewPos, #eye
    #         np.array([controller.X,controller.Y,controller.Z]),     #at
    #         np.array([0, 1, 0])   #up
    #     )

    glUseProgram(axisPipeline.shaderProgram)
    glUniformMatrix4fv(glGetUniformLocation(axisPipeline.shaderProgram, "view"), 1, GL_TRUE, view)

    glUseProgram(texPipeline.shaderProgram)
    glUniformMatrix4fv(glGetUniformLocation(texPipeline.shaderProgram, "view"), 1, GL_TRUE, view)
    # glUniform3f(glGetUniformLocation(texPipeline.shaderProgram, "viewPosition"), viewPos[0], viewPos[1], viewPos[2])
    glUniformMatrix4fv(glGetUniformLocation(texPipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)

    glUseProgram(lightPipeline.shaderProgram)
    glUniformMatrix4fv(glGetUniformLocation(lightPipeline.shaderProgram, "view"), 1, GL_TRUE, view)
    glUniformMatrix4fv(glGetUniformLocation(lightPipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)

# Función que indica qué acción realizar al recibir ciertos inputs
def on_key(window, key, scancode, action, mods):

    if action != glfw.PRESS:
        return
    
    global controller

    if key == glfw.KEY_0:
        controller.fillPolygon = not controller.fillPolygon

    elif key == glfw.KEY_ESCAPE:
        glfw.set_window_should_close(window, True)

    #####################################################################
    # Alternar entre las 2 cámaras
    elif key == glfw.KEY_SPACE:
        controller.estado = (controller.estado + 1)%2       

# Función encarga del movimiento de la cámara
# Se hace uso de cámara en coordenadas cilíndricas tal que puedas girar la cámara entorno al punto en el que uno está parado.
def check_key_inputs(window):
    # Futuras coordenadas x y z respectivamente al moverse por el mapa, es decir, corresponden a las coordenadas en las cuales estará la
    # cámara al presionar w o s
    coordx = controller.eye[0] + (controller.at[0] - controller.eye[0]) * 0.05
    coordz = controller.eye[2] + (controller.at[2] - controller.eye[2]) * 0.05

    coord_x = controller.eye[0] - (controller.at[0] - controller.eye[0]) * 0.05
    coord_z = controller.eye[2] - (controller.at[2] - controller.eye[2]) * 0.05     

    if controller.estado == 0:   # Si se encuentra en primera persona, es posible moverse. Así se evita que cuando este en vista panorámica la cámara se pueda mover
        # Controles de la camara
        # Moverse hacia adelante
        if glfw.get_key(window, glfw.KEY_W) == glfw.PRESS:
            # Se establecen los límites de la cámara en x y z. La última condición determina que no puede pasar la diagonal del mapa.
            if coordx < 7.6\
                and coordx > -7.6\
                and coordz < 5.4\
                and coordz > -4.4\
                and coordx < 3.3*coordz + 14.52:

                controller.eye += (controller.at - controller.eye) * 0.05
                controller.at += (controller.at - controller.eye) * 0.05        

        # Moverse para atrás
        if glfw.get_key(window, glfw.KEY_S) == glfw.PRESS:
            if coord_x < 7.6\
                and coord_x > -7.6\
                and coord_z < 5.4\
                and coord_z > -4.4\
                and coord_x < 3.3*coord_z + 14.52:

                controller.eye -= (controller.at - controller.eye) * 0.05
                controller.at -= (controller.at - controller.eye) * 0.05        

        # Girar hacia la derecha
        if glfw.get_key(window, glfw.KEY_A) == glfw.PRESS:
            controller.Theta -= controller.movSpeed

        # Girar hacia la izquierda
        if glfw.get_key(window, glfw.KEY_D) == glfw.PRESS:
             controller.Theta += controller.movSpeed

        # Subir
        if glfw.get_key(window, glfw.KEY_UP) == glfw.PRESS:
            controller.eye[1] += controller.movSpeed        # Se aumenta la posición en y tanto de la cámara como el punto al que se mira
            controller.at[1] += controller.movSpeed

        # Bajar
        if glfw.get_key(window, glfw.KEY_DOWN) == glfw.PRESS:
            if controller.eye[1] > -0.47:                   # No puede traspasar el suelo
                controller.eye[1] -= controller.movSpeed
                controller.at[1] -= controller.movSpeed
                
def window_resize(window, width, height): # To fix content when resizing window
    glViewport(0, 0, width, height)

#####################################################################
# Función que se encarga de colocar todos los elementos del piso
def createAmbiente(pipeline):
    # Se inicializa la figura
    cuadrado = bs.createTextureQuad(5,1)
    gpuCuadrado = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuCuadrado)
    gpuCuadrado.fillBuffers(cuadrado.vertices, cuadrado.indices, GL_STATIC_DRAW)
    gpuCuadrado.texture = es.textureSimpleSetup(
        getAssetPath("pavimento2.jpg"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)

    acera = bs.createTextureQuad(5,1)
    gpuAcera = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuAcera)
    gpuAcera.fillBuffers(acera.vertices, acera.indices, GL_STATIC_DRAW)
    gpuAcera.texture = es.textureSimpleSetup(
        getAssetPath("acera.jpg"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)

    triangulo = bs.createTriangleTexture()
    gpuTriangulo = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuTriangulo)
    gpuTriangulo.fillBuffers(triangulo.vertices, triangulo.indices, GL_STATIC_DRAW)
    gpuTriangulo.texture = es.textureSimpleSetup(
        getAssetPath("acera.jpg"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)

    tierra = bs.createTriangleTexture()
    gpuTierra = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuTierra)
    gpuTierra.fillBuffers(tierra.vertices, tierra.indices, GL_STATIC_DRAW)
    gpuTierra.texture = es.textureSimpleSetup(
        getAssetPath("tierra.jpg"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)

    cesped = bs.createTextureQuad(1,1)
    gpuCesped = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuCesped)
    gpuCesped.fillBuffers(cesped.vertices, cesped.indices, GL_STATIC_DRAW)
    gpuCesped.texture = es.textureSimpleSetup(
        getAssetPath("cesped.jpg"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)                                     

    # ----------------------------------------------------------------------------------
    # Grafos
    calle = sg.SceneGraphNode('calle')
    calle.transform = tr.scale(14,1,1)
    calle.childs += [gpuCuadrado]

    calleI = sg.SceneGraphNode('calleI')
    calleI.transform = tr.translate(0, -0.48, -1)
    calleI.childs += [calle]

    calleI2 = sg.SceneGraphNode('calleI2')
    calleI2.transform = tr.matmul([tr.translate(-3.5, -0.48, -4), tr.scale(1/2,1,1)])
    calleI2.childs += [calle]

    calleI3 = sg.SceneGraphNode('calleI3')
    calleI3.transform = tr.matmul([tr.translate(3.8, -0.481, -2.85), tr.shearing(0,0,0,0.3,0,0),tr.scale(0.55,1,1)])
    calleI3.childs += [calle]            

    calleC = sg.SceneGraphNode('calleC')
    calleC.transform = tr.translate(0, -0.48, 2)
    calleC.childs += [calle]

    calleD = sg.SceneGraphNode('calleD')
    calleD.transform = tr.translate(0, -0.48, 5)
    calleD.childs += [calle]

    calleA = sg.SceneGraphNode('calleA')
    calleA.transform = tr.matmul([tr.translate(-7.3, -0.48, 0.5), tr.rotationY(np.pi/2), tr.scale(0.71, 1, 0.7)])
    calleA.childs += [calle]

    calleS = sg.SceneGraphNode('calleS')
    calleS.transform = tr.matmul([tr.translate(7.3, -0.48, 2), tr.rotationY(np.pi/2), tr.scale(1/2, 1, 0.7)])
    calleS.childs += [calle]                  

    tierraC = sg.SceneGraphNode('tierraC')
    tierraC.transform = tr.matmul([tr.translate(0, -0.48, 0.5), tr.scale(14,1,2)])
    tierraC.childs += [gpuAcera]

    tierraI = sg.SceneGraphNode('tierraI')
    tierraI.transform = tr.matmul([tr.translate(-3.5, -0.48, -2.5), tr.scale(7,1,2)])
    tierraI.childs += [gpuAcera]

    tierraD = sg.SceneGraphNode('tierraD')
    tierraD.transform = tr.matmul([tr.translate(0, -0.48, 3.5), tr.scale(14,1,2)])
    tierraD.childs += [gpuAcera]

    triangle = sg.SceneGraphNode('triangle')
    triangle.transform = tr.matmul([tr.translate(0, -0.48, -2.5), tr.scale(14,1,2)])
    triangle.childs += [gpuTriangulo]

    triangleC = sg.SceneGraphNode('triangleC')
    triangleC.transform = tr.matmul([tr.translate(0, -0.48, -2.5), tr.scale(14*0.8,1*0.8,2*0.8)])
    triangleC.childs += [gpuTierra]
 

    cespedB = sg.SceneGraphNode('cespedB')
    cespedB.transform = tr.matmul([tr.translate(0.5, -0.48, -2.4), tr.scale(1/2,1/2,1.2)])
    cespedB.childs += [gpuCesped]
    

    cesped = sg.SceneGraphNode('cesped')
    cesped.transform = tr.scale(1/4,1/4,1/4)
    cesped.childs += [gpuCesped]

    cesped1 = sg.SceneGraphNode('cesped1')
    cesped1.transform = tr.translate(1.3, -0.48, -2) 
    cesped1.childs += [cesped]

    cesped2 = sg.SceneGraphNode('cesped2')
    cesped2.transform = tr.translate(1.3, -0.48, -2.5) 
    cesped2.childs += [cesped]

    cesped3 = sg.SceneGraphNode('cesped3')
    cesped3.transform = tr.translate(1.8, -0.48, -2) 
    cesped3.childs += [cesped]

    cesped4 = sg.SceneGraphNode('cesped4')
    cesped4.transform = tr.translate(1.8, -0.48, -2.5) 
    cesped4.childs += [cesped]

    cesped5 = sg.SceneGraphNode('cesped5')
    cesped5.transform = tr.matmul([tr.translate(2.8, -0.48, -2), tr.scale(4,1,1)]) 
    cesped5.childs += [cesped]            

    # Escena
    escena = sg.SceneGraphNode("escena")
    escena.childs += [calleI, calleI2, calleI3, calleC, calleD, calleA, calleS, tierraC, tierraI, tierraD, triangle, triangleC, cespedB, cesped1, cesped2, cesped3, cesped4, cesped5]

    return escena

# N = Cantidad de casas por línea
# Coord = Coordenadas en la que se desea colocar las casas
def createBarrio(pipeline, N, coord):
    # Modelo de casa con ladrillos amarillos
    casa1 = sg.SceneGraphNode("casa1")
    casa1.childs += [createCasa1(pipeline)] 

    # Modelo de casa blanca
    casa2 = sg.SceneGraphNode("casa2")
    casa2.childs += [createCasa2(pipeline)]

    # Modelo de casa doble (azul y rojo)
    casa3 = sg.SceneGraphNode("casa3")
    casa3.transform = tr.translate(0, -0.25, 0)
    casa3.childs += [createCasa3(pipeline)]

    OpcionesCasa = [casa1, casa3, casa2]
    baseName = "casa"

    escena = sg.SceneGraphNode("escena2")
    for i in range(N):
    
        opcion1 = randint(0,2) # Se escoge al azar un modelo de casa
        newNode = sg.SceneGraphNode(baseName + str(i))
        newNode.transform = tr.matmul([tr.translate( 1.5*i-6, -0.3, coord), tr.rotationY(np.pi), tr.scale(0.5, 0.5, 0.5)]) # Se colocan la casas deseadas con la misma separación en el eje x
        newNode.childs += [OpcionesCasa[opcion1]]

        # Análogo, pero esta vez desplaza una unidad en z con tal de que estén alineadas a las otras casas
        opcion2 = randint(0,2)
        newNode2 = sg.SceneGraphNode(baseName + str(i+N))
        newNode2.transform = tr.matmul([tr.translate(  1.5*i-6, -0.3, coord+1), tr.scale(0.5, 0.5, 0.5)])
        newNode2.childs += [OpcionesCasa[opcion2]]

        
        escena.childs += [newNode, newNode2]

    return escena

def createSunMoon(pipeline):
    def createGPUShape(pipeline, shape):
        gpuShape = es.GPUShape().initBuffers()
        pipeline.setupVAO(gpuShape)
        gpuShape.fillBuffers(shape.vertices, shape.indices, GL_STATIC_DRAW)
        return gpuShape

    yellowSphere = createGPUShape(pipeline, bs.createColorSphereTarea2(1.0, 1.0, 0.0))
    
    # Nodo de esfera
    sphereNode = sg.SceneGraphNode('sphere')
    sphereNode.transform = tr.uniformScale(0.2)
    sphereNode.childs += [yellowSphere]

    # Nodo para mover la esfera
    sunPosNode = sg.SceneGraphNode('sun')
    sunPosNode.childs += [sphereNode]

    # Nodo para mover la esfera
    moonPosNode = sg.SceneGraphNode('moon')
    moonPosNode.transform = tr.translate(0,-3, 0)
    moonPosNode.childs += [sphereNode]

    escena = sg.SceneGraphNode('escena')
    escena.childs += [sunPosNode]
    escena.childs += [moonPosNode]

    return escena

def createPostes(pipeline):
    def readFaceVertex(faceDescription):

        aux = faceDescription.split('/')

        assert len(aux[0]), "Vertex index has not been defined."

        faceVertex = [int(aux[0]), None, None]

        assert len(aux) == 3, "Only faces where its vertices require 3 indices are defined."

        if len(aux[1]) != 0:
            faceVertex[1] = int(aux[1])

        if len(aux[2]) != 0:
            faceVertex[2] = int(aux[2])

        return faceVertex

    def readOBJ(filename, color):

        vertices = []
        normals = []
        textCoords= []
        faces = []

        with open(filename, 'r') as file:
            for line in file.readlines():
                aux = line.strip().split(' ')
                
                if aux[0] == 'v':
                    vertices += [[float(coord) for coord in aux[1:]]]

                elif aux[0] == 'vn':
                    normals += [[float(coord) for coord in aux[1:]]]

                elif aux[0] == 'vt':
                    assert len(aux[1:]) == 2, "Texture coordinates with different than 2 dimensions are not supported"
                    textCoords += [[float(coord) for coord in aux[1:]]]

                elif aux[0] == 'f':
                    N = len(aux)                
                    faces += [[readFaceVertex(faceVertex) for faceVertex in aux[1:4]]]
                    for i in range(3, N-1):
                        faces += [[readFaceVertex(faceVertex) for faceVertex in [aux[i], aux[i+1], aux[1]]]]

            vertexData = []
            indices = []
            index = 0

            # Per previous construction, each face is a triangle
            for face in faces:

                # Checking each of the triangle vertices
                for i in range(0,3):
                    vertex = vertices[face[i][0]-1]
                    normal = normals[face[i][2]-1]

                    vertexData += [
                        vertex[0], vertex[1], vertex[2],
                        color[0], color[1], color[2],
                        normal[0], normal[1], normal[2]
                    ]

                # Connecting the 3 vertices to create a triangle
                indices += [index, index + 1, index + 2]
                index += 3        

            return bs.Shape(vertexData, indices)

    # creating car and light posts gpuShapes
    shapePost1 = readOBJ(getAssetPath('lamp_post.obj'), (0.5, 0.8, 0.9))
    gpuPost1 = createGPUShape(pipeline, shapePost1)
    shapePost2 = readOBJ(getAssetPath('lamp_post.obj'), (0.5, 0.8, 0.9))
    gpuPost2 = createGPUShape(pipeline, shapePost2)
    shapePost3 = readOBJ(getAssetPath('lamp_post.obj'), (0.5, 0.8, 0.9))
    gpuPost3 = createGPUShape(pipeline, shapePost3)
    shapePost4 = readOBJ(getAssetPath('lamp_post.obj'), (0.5, 0.8, 0.9))
    gpuPost4 = createGPUShape(pipeline, shapePost4)

    postes = [gpuPost1, gpuPost2, gpuPost3, gpuPost4]

    return postes

def createScene(pipeline):
    Ambiente = createAmbiente(pipeline)      # Corresponde a todo el suelo 
    Casas1 = createBarrio(pipeline, 9, 0)    # Casas del centro
    Casas2 = createBarrio(pipeline, 9, 3)    # Casas de la derecha
    Casas3 = createBarrio(pipeline, 4, -3)   # Casas de la izquierda

    scene = sg.SceneGraphNode('scene')
    scene.childs += [Ambiente, Casas1, Casas2, Casas3]

    return scene

# global controller as communication with the callback function
controller = Controller()

def main():

    # Initialize glfw
    if not glfw.init():
        glfw.set_window_should_close(window, True)


    window = glfw.create_window(ct.WIDTH, ct.HEIGHT, ct.TITLE, None, None)

    if not window:
        glfw.terminate()
        glfw.set_window_should_close(window, True)

    glfw.make_context_current(window)
    glfw.set_window_size_callback(window, window_resize)

    # Connecting the callback function 'on_key' to handle keyboard events
    glfw.set_key_callback(window, on_key)

    # Se crean los pipelineas para texturas y figuras
    axisPipeline = ls.SimpleGouraudShaderProgram()
    texPipeline = ls.MultipleLightTexturePhongShaderProgram()
    lightPipeline = ls.MultipleLightPhongShaderProgram()

    # Setting up the clear screen color
    glClearColor(0.45, 0.61, 0.89, 1.0)

    glEnable(GL_DEPTH_TEST)

    #loadTextures()
    setLights()

    # <--------------- Creación de las figuras --------------->
    # Se crea el barrio
    escena = createScene(texPipeline)
    car = createCarScene(lightPipeline)
    sunMoon = createSunMoon(lightPipeline)
    postes = createPostes(axisPipeline)

     ##TAREA5: Necesitamos los parámetros de posición y direcciones de las luces para manipularlas en el bucle principal
    lightSunPos = np.append(pointlightsPool['sun'].position, 1)
    lightMoonPos = np.append(pointlightsPool['moon'].position, 1)
    dir_inicial_Sun = np.append(pointlightsPool['sun'].direction, 1)
    dir_inicial_Moon = np.append(pointlightsPool['moon'].direction, 1)

    light1pos = np.append(spotlightsPool['spot3'].position, 1)
    light2pos = np.append(spotlightsPool['spot4'].position, 1)
    dir_inicial = np.append(spotlightsPool['spot3'].direction, 1)

    # <-------- Proyecciones -------->
    # Proyección en perspectiva para la cámara en primera persona
    projection1 = tr.perspective(45, float(ct.WIDTH)/float(ct.HEIGHT), 0.1, 100)

    # Proyección ortográfica para la cámara aérea
    projection2 = tr.ortho(-15, 1, -15, 1, 0.1, 100)
    # <------------------------------>

    perfMonitor = pm.PerformanceMonitor(glfw.get_time(), 0.5)

    # Used later for checking if time advanced a second
    t0 = -1

    #parametro iniciales
    coord_X = 0 
    coord_Z = -3
    angulo = np.pi/2

    while not glfw.window_should_close(window):        
        # Using GLFW to check for input events
        glfw.poll_events()

        check_key_inputs(window)        

        # Measuring performance
        perfMonitor.update(glfw.get_time())
        glfw.set_window_title(window, ct.TITLE + str(perfMonitor))

        # Se obtiene la diferencia de tiempo entre iteraciones
        t1 = glfw.get_time()
        tCycle = t1 % ct.DAY_NIGHT_CYCLE# Cycle of 0 to a constant value
        controller.time = tCycle // (ct.DAY_NIGHT_CYCLE/24) # Cycle of 1 to 24
        
        if controller.time != t0:               # If passed a second
            if controller.time < 10:
                print("Time: 0"+ str(round(controller.time)) + ":00")
            else:
                print("Time: "+ str(round(controller.time)) + ":00")
            controller.sunMoonPos -= np.pi/12
        t0 = controller.time                    # Readies for next iteration

        # <-------- Cámara -------->
        # Vista en First Person
        # La cámara se ajusta de forma que quede en coordenadas polares
        atX = controller.eye[0] + np.cos(controller.Theta)      #  Posición de la cámara en el eje x
        atZ = controller.eye[2] + np.sin(controller.Theta)      #  Posición de la cámara en el eje z
        controller.at = np.array([atX, controller.at[1], atZ]) 

        # Vista panorámica
        eye = np.array([-7, 15, 7])
        at = np.array([-7, 0, 7])
        up = np.array([0, 0, 1])

        # Se definen las matrices de view para cada caso
        FP = tr.lookAt(controller.eye, controller.at, controller.up)
        VP = tr.lookAt(eye, at, up)

        # Caso inicial corresponde a la cámara en primera persona
        view = FP
        projection = projection1

        # En función de en qué estado se encuentre el controlador, se alterna la cámara cambiando la matriz view
        if controller.estado == 0:
            view = FP
            projection = projection1

        if controller.estado == 1:
            view = VP
            projection = projection2
            
        # <----------------------------> 

        if (controller.fillPolygon):
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT| GL_DEPTH_BUFFER_BIT)

    ########################################################################################################################################################################

        setView(texPipeline, axisPipeline, lightPipeline, view, projection)
        setPlot(texPipeline, axisPipeline,lightPipeline)


        glUseProgram(texPipeline.shaderProgram)
        sg.drawSceneGraphNode(escena, texPipeline, "model")

        glUseProgram(axisPipeline.shaderProgram)
        for i in range(len(postes)):
            glUniformMatrix4fv(glGetUniformLocation(axisPipeline.shaderProgram, "model"), 1, GL_TRUE,
            tr.matmul([
                tr.translate(i,-0.55,2.5),
                tr.uniformScale(0.001)])
        )
            axisPipeline.drawCall(postes[i])


        glUseProgram(lightPipeline.shaderProgram)

        #aqui se mueve el auto
        sg.drawSceneGraphNode(car, lightPipeline, "model")
        Auto = sg.findNode(car,'system-car')
        Auto.transform = tr.matmul([tr.translate(coord_X+2,-0.52,coord_Z+5),tr.rotationY(np.pi+angulo),tr.rotationY(-np.pi),tr.translate(-2,0,-5)])
        #transformación que hace que el auto se ponga en el origen, para luego trasladarlo al punto (2.0, −0.037409, 5.0) para despés poder moverlo.

        #TAREA5: Las posiciones de las luces se transforman de la misma forma que el objeto
        posicion_transform = tr.matmul([tr.translate(coord_X + 2, -0.037409, coord_Z + 5),
                                        tr.rotationY(np.pi + angulo),
                                        tr.rotationY(-np.pi),
                                        tr.translate(-2, 0.037409, -5)])

        posicion3 = tr.matmul([posicion_transform, light1pos])
        posicion4 = tr.matmul([posicion_transform, light2pos])
        spotlightsPool['spot3'].position = posicion3
        spotlightsPool['spot4'].position = posicion4

        #TAREA5: la dirección se rota con respecto a la rotación del objeto
        direccion = tr.matmul([tr.rotationY(angulo), dir_inicial])
        spotlightsPool['spot3'].direction = direccion
        spotlightsPool['spot4'].direction = direccion


        sg.drawSceneGraphNode(sunMoon, lightPipeline, "model")
        sun = sg.findNode(sunMoon, "sun")
        moon = sg.findNode(sunMoon, "moon")
        
        sunPos = [0, 10*np.sin(controller.sunMoonPos), -10*np.cos(controller.sunMoonPos)]
        moonPos = [0, -10*np.sin(controller.sunMoonPos), 10*np.cos(controller.sunMoonPos)]
        sun.transform = tr.translate(sunPos[0], sunPos[1], sunPos[2])
        moon.transform = tr.translate(moonPos[0], moonPos[1], moonPos[2])

        # Las posiciones de las luces se transforman de la misma forma que el objeto

        sun_Posicion_transform = tr.matmul([#tr.translate(coord_X + 2, -0.037409, coord_Z + 5),
                                        tr.rotationY(np.pi + angulo),
                                        tr.rotationY(-np.pi),
                                        tr.translate(0, 10*np.sin(controller.sunMoonPos), -10*np.cos(controller.sunMoonPos))])

        moon_Posicion_transform = tr.matmul([#tr.translate(coord_X + 2, -0.037409, coord_Z + 5),
                                        tr.rotationY(np.pi + angulo),
                                        tr.rotationY(-np.pi),
                                        tr.translate(0, -10*np.sin(controller.sunMoonPos), 10*np.cos(controller.sunMoonPos))])

        posicionSun = tr.matmul([sun_Posicion_transform, lightSunPos])
        posicionMoon = tr.matmul([moon_Posicion_transform, lightMoonPos])
        pointlightsPool['sun'].position = posicionSun
        pointlightsPool['moon'].position = posicionMoon

        #TAREA5: la dirección se rota con respecto a la rotación del objeto
        # direccionSun = tr.matmul([tr.rotationY(angulo), dir_inicial_Sun])
        # direccionMoon = tr.matmul([tr.rotationY(angulo), dir_inicial_Moon])
        # pointlightsPool['sun'].direction = direccionSun
        # pointlightsPool['moon'].direction = direccionMoon

        # Once the render is done, buffers are swapped, showing only the complete scene.
        glfw.swap_buffers(window)
    
    # freeing GPU memory
    escena.clear()


    glfw.terminate()

if __name__ == "__main__":
    main()