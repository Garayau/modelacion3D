
# coding=utf-8
"""Vertices and indices for a variety of simple shapes"""

import math
import numpy as np
import sys
import os.path


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from grafica.assets_path import getAssetPath
import grafica.scene_graph as sg
import grafica.transformations as tr
from grafica.gpu_shape import GPUShape
import grafica.easy_shaders as es

__author__ = "Daniel Calderon"
__license__ = "MIT"

# A simple class container to store vertices and indices that define a shape
class Shape:
    def __init__(self, vertices, indices):
        self.vertices = vertices
        self.indices = indices

    def __str__(self):
        return "vertices: " + str(self.vertices) + "\n"\
            "indices: " + str(self.indices)

    

def createTextureQuad(nx, ny):

    # Defining locations and texture coordinates for each vertex of the shape    
    vertices = [
    #   positions        texture
        -0.5, -0.05, -0.5, 0, ny, 1,0,0,
         0.5, -0.05, -0.5, nx, ny, 1,0,0,
         0.5, -0.05,  0.5, nx, 0, 1,0,0,
        -0.5, -0.05,  0.5, 0, 0, 1,0,0]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
         0, 1, 2,
         2, 3, 0]

    return Shape(vertices, indices)



def createTextureCube():

    # Defining locations and texture coordinates for each vertex of the shape  
    vertices = [
    #   positions   texture coordinates   normals
    # Z+
        -0.5, -0.5,  0.5, 0, 1, 0,0,1,
         0.5, -0.5,  0.5, 1, 1, 0,0,1,
         0.5,  0.5,  0.5, 1, 0, 0,0,1,
        -0.5,  0.5,  0.5, 0, 0, 0,0,1,

    # Z-
        -0.5, -0.5, -0.5, 0, 1, 0,0,-1,
         0.5, -0.5, -0.5, 1, 1, 0,0,-1,
         0.5,  0.5, -0.5, 1, 0, 0,0,-1,
        -0.5,  0.5, -0.5, 0, 0, 0,0,-1,
        
    #Se cambia la orientación
    # X+
         0.5, -0.5, -0.5, 1, 1, 1,0,0,
         0.5,  0.5, -0.5, 1, 0, 1,0,0,
         0.5,  0.5,  0.5, 0, 0, 1,0,0,
         0.5, -0.5,  0.5, 0, 1, 1,0,0,
 
    # X-
        -0.5, -0.5, -0.5, 1, 1, -1,0,0,
        -0.5,  0.5, -0.5, 1, 0, -1,0,0,
        -0.5,  0.5,  0.5, 0, 0, -1,0,0,
        -0.5, -0.5,  0.5, 0, 1, -1,0,0,

    # Y+
        -0.5,  0.5, -0.5, 0, 1, 0,1,0,
         0.5,  0.5, -0.5, 1, 1, 0,1,0,
         0.5,  0.5,  0.5, 1, 0, 0,1,0,
        -0.5,  0.5,  0.5, 0, 0, 0,1,0,

    # Y-
        -0.5, -0.5, -0.5, 0, 1, 0,-1,0,
         0.5, -0.5, -0.5, 1, 1, 0,-1,0,
         0.5, -0.5,  0.5, 1, 0, 0,-1,0,
        -0.5, -0.5,  0.5, 0, 0, 0,-1,0
        ]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
          0, 1, 2, 2, 3, 0, # Z+
          7, 6, 5, 5, 4, 7, # Z-
          8, 9,10,10,11, 8, # X+
         15,14,13,13,12,15, # X-
         19,18,17,17,16,19, # Y+
         20,21,22,22,23,20] # Y-

    return Shape(vertices, indices)


# <------------- Nuevas figuras creadas para t1p2 ---------------> 

# se encarga de crear un cubo con textura, pero se le pueden modificar las coordenadas de las texturas con tal de agarrar ciertos pedazo
#  de una imagen y que en las caras "Y" y "X" se vean el pedazo escogido, mientras que en las caras "Z" se vea la imagen completa. Esta fue usada para las puertas
#  y las ventanas de la casa.
def createTextureCube2(nx, ny):

    # Defining locations and texture coordinates for each vertex of the shape  
    vertices = [
    #   positions   texture coordinates     normals
    # Z+
        -0.5, -0.5,  0.5, 0, 1, 0,0,1,
         0.5, -0.5,  0.5, 1, 1, 0,0,1,
         0.5,  0.5,  0.5, 1, 0, 0,0,1,
        -0.5,  0.5,  0.5, 0, 0, 0,0,1,

    # Z-
        -0.5, -0.5, -0.5, 0, 1, 0,0,-1,
         0.5, -0.5, -0.5, 1, 1, 0,0,-1,
         0.5,  0.5, -0.5, 1, 0, 0,0,-1,
        -0.5,  0.5, -0.5, 0, 0, 0,0,-1,
        
    #Se cambia la orientación
    # X+
         0.5, -0.5, -0.5, nx, ny, 1,0,0,
         0.5,  0.5, -0.5, nx, 0, 1,0,0,
         0.5,  0.5,  0.5, 0, 0, 1,0,0,
         0.5, -0.5,  0.5, 0, ny, 1,0,0,
 
    # X-
        -0.5, -0.5, -0.5, nx, ny, -1,0,0,
        -0.5,  0.5, -0.5, nx, 0, -1,0,0,
        -0.5,  0.5,  0.5, 0, 0, -1,0,0,
        -0.5, -0.5,  0.5, 0, ny, -1,0,0,

    # Y+
        -0.5,  0.5, -0.5, 0, ny, 0,1,0,
         0.5,  0.5, -0.5, nx, ny, 0,1,0,
         0.5,  0.5,  0.5, nx, 0, 0,1,0,
        -0.5,  0.5,  0.5, 0, 0, 0,1,0,

    # Y-
        -0.5, -0.5, -0.5, 0, ny, 0,-1,0,
         0.5, -0.5, -0.5, nx, ny, 0,-1,0,
         0.5, -0.5,  0.5, nx, 0, 0,-1,0,
        -0.5, -0.5,  0.5, 0, 0, 0,-1,0
        ]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
          0, 1, 2, 2, 3, 0, # Z+
          7, 6, 5, 5, 4, 7, # Z-
          8, 9,10,10,11, 8, # X+
         15,14,13,13,12,15, # X-
         19,18,17,17,16,19, # Y+
         20,21,22,22,23,20] # Y-

    return Shape(vertices, indices)

# Crea la base del techo que básicamente consiste en dos triángulos con las texturas de las paredes de la casa más una base.
def createTextureTechop2():

    # Defining locations and texture coordinates for each vertex of the shape  
    vertices = [
    #   positions         texture coordinates
    # Y-
        -0.5, -0.5, -0.5, 0, 1, 0,-1,0,
         0.5, -0.5, -0.5, 1, 1, 0,-1,0,
         0.5, -0.5,  0.5, 1, 0, 0,-1,0,
        -0.5, -0.5,  0.5, 0, 0, 0,-1,0,

        -0.5, -0.5, -0.5, 0, 1, 0,0,-1, #4
        0.5, -0.5, -0.5, 1, 1,  0,0,-1, #5
        0.0, 0.5, -0.5, 1/2, 0, 0,0,-1,   #6

        -0.5, -0.5, 0.5, 0, 2/3, 0,0,1, #7
        0.5, -0.5, 0.5, 2/3, 2/3,0,0,1,   #8
        0.0, 0.5, 0.5, 1/3, 0,   0,0,1 #9
              
      
        ]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
          0, 1, 2, 2, 3, 0,  # Y-
          4, 5, 6,
          7,8,9,

          ] 

    return Shape(vertices, indices)    


# Crea un triángulo rectángulo con texturas.
def createTriangleTexture():
    # Defining locations and texture coordinates for each vertex of the shape    
    vertices = [
    #   positions   texture     normal
         0.5, -0.05, 0.5, 0, 1, 1,0,0,
         0.0, -0.05, 0.5, 1, 1, 1,0,0,
         0.0, -0.05, -0.5, 1, 0, 1,0,0]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
         0, 1, 2,]

    return Shape(vertices, indices)

def readOFF(filename, color):
    vertices = []
    normals= []
    faces = []

    with open(filename, 'r') as file:
        line = file.readline().strip()
        assert line=="OFF"

        line = file.readline().strip()
        aux = line.split(' ')

        numVertices = int(aux[0])
        numFaces = int(aux[1])

        for i in range(numVertices):
            aux = file.readline().strip().split(' ')
            vertices += [float(coord) for coord in aux[0:]]
        
        vertices = np.asarray(vertices)
        vertices = np.reshape(vertices, (numVertices, 3))
        #print(f'Vertices shape: {vertices.shape}')

        normals = np.zeros((numVertices,3), dtype=np.float32)
        #print(f'Normals shape: {normals.shape}')

        for i in range(numFaces):
            aux = file.readline().strip().split(' ')
            aux = [int(index) for index in aux[0:]]
            faces += [aux[1:]]
            
            vecA = [vertices[aux[2]][0] - vertices[aux[1]][0], vertices[aux[2]][1] - vertices[aux[1]][1], vertices[aux[2]][2] - vertices[aux[1]][2]]
            vecB = [vertices[aux[3]][0] - vertices[aux[2]][0], vertices[aux[3]][1] - vertices[aux[2]][1], vertices[aux[3]][2] - vertices[aux[2]][2]]

            res = np.cross(vecA, vecB)
            normals[aux[1]][0] += res[0]  
            normals[aux[1]][1] += res[1]  
            normals[aux[1]][2] += res[2]  

            normals[aux[2]][0] += res[0]  
            normals[aux[2]][1] += res[1]  
            normals[aux[2]][2] += res[2]  

            normals[aux[3]][0] += res[0]  
            normals[aux[3]][1] += res[1]  
            normals[aux[3]][2] += res[2]  
        #print(faces)
        norms = np.linalg.norm(normals,axis=1)
        normals = normals/norms[:,None]

        color = np.asarray(color)
        color = np.tile(color, (numVertices, 1))

        vertexData = np.concatenate((vertices, color), axis=1)
        vertexData = np.concatenate((vertexData, normals), axis=1)

        #print(vertexData.shape)

        indices = []
        vertexDataF = []
        index = 0

        for face in faces:
            vertex = vertexData[face[0],:]
            vertexDataF += vertex.tolist()
            vertex = vertexData[face[1],:]
            vertexDataF += vertex.tolist()
            vertex = vertexData[face[2],:]
            vertexDataF += vertex.tolist()
            
            indices += [index, index + 1, index + 2]
            index += 3        



        return Shape(vertexDataF, indices)

def createColorSphereTarea2(r,g,b):

    return readOFF(getAssetPath('sphere.off'), (r, g, b))