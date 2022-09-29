# coding=utf-8
"""Texture Quad in 2D"""

# from PIL.Image import LINEAR, NEAREST
from random import randint
import glfw
from OpenGL.GL import *
import numpy as np
from grafica.gpu_shape import GPUShape
import grafica.transformations as tr
import grafica.basic_shapes as bs
import grafica.easy_shaders as es
from grafica.assets_path import getAssetPath
import grafica.scene_graph as sg

# Modelo de casa de piedras amarillas y tejas rojizas
def createCasa1(pipeline):
    # Inicialización de las figuras
    # Cubo con textura para las paredes
    cubo = bs.createTextureCube()
    gpuCubo = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuCubo)
    gpuCubo.fillBuffers(cubo.vertices, cubo.indices, GL_STATIC_DRAW)
    gpuCubo.texture = es.textureSimpleSetup(
        getAssetPath("pared4.jpg"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)

    # Cubo con texturas de puerta
    puerta = bs.createTextureCube2(1/15, 1)
    gpuPuerta = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuPuerta)
    gpuPuerta.fillBuffers(puerta.vertices, puerta.indices, GL_STATIC_DRAW)
    gpuPuerta.texture = es.textureSimpleSetup(
        getAssetPath("puerta m.jpg"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)

    # Cubo con textura de ventana
    ventana = bs.createTextureCube2(1/15, 1)
    gpuVentana = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuVentana)
    gpuVentana.fillBuffers(ventana.vertices, ventana.indices, GL_STATIC_DRAW)
    gpuVentana.texture = es.textureSimpleSetup(
        getAssetPath("ventana madera.jpg"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)

    # Diagonal del techo (Tejas)
    tejas = bs.createTextureCube()
    gpuTejas = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuTejas)
    gpuTejas.fillBuffers(tejas.vertices, tejas.indices, GL_STATIC_DRAW)
    gpuTejas.texture = es.textureSimpleSetup(
        getAssetPath("tejas 2.jpg"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)   

    # "Base" del techo
    techo = bs.createTextureTechop2()
    gpuTecho = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuTecho)
    gpuTecho.fillBuffers(techo.vertices, techo.indices, GL_STATIC_DRAW)
    gpuTecho.texture = es.textureSimpleSetup(
        getAssetPath("pared4.jpg"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)         

    # -----------------------------------------------------------------------------------------------------
    # Grafos
    # Puerta
    puerta = sg.SceneGraphNode('puerta')
    puerta.transform = tr.matmul([tr.translate(-0.2, -0.3, 0.5), tr.scale(0.25,0.4,0.05)])
    puerta.childs += [gpuPuerta]

    #####################################
    # Ventanas
    # Ventana general
    ventana = sg.SceneGraphNode('ventana')
    ventana.transform = tr.scale(0.25,0.3,0.05)
    ventana.childs += [gpuVentana]

    # Ventanas del primer piso ubicadas a la derecha
    ventanaD = sg.SceneGraphNode('ventanaD')
    ventanaD.transform = tr.translate(0.3, -0.2, 0.5)
    ventanaD.childs += [ventana]

    ventanaD2 = sg.SceneGraphNode('ventanaD2')
    ventanaD2.transform = tr.translate(1, -0.2, 0.5)
    ventanaD2.childs += [ventana]

    ventanaD3 = sg.SceneGraphNode('ventanaD3')
    ventanaD3.transform = tr.translate(1, -0.2, -0.5)
    ventanaD3.childs += [ventana]      

    # Ventanas del segundo piso
    ventanaS = sg.SceneGraphNode('ventanaS')
    ventanaS.transform = tr.translate(-0.2, 0.2, 0.5)
    ventanaS.childs += [ventana]

    ventanaS2 = sg.SceneGraphNode('ventanaS2')
    ventanaS2.transform = tr.translate(0.3, 0.2, 0.5)
    ventanaS2.childs += [ventana]

    #####################################
    # Techo
    techo = sg.SceneGraphNode('techo')
    techo.transform = tr.matmul([tr.translate(0, 0, 0), tr.scale(1,0.3,1)])
    techo.childs += [gpuTecho]

    # Paralelepipedo que conforma el lado izquierdo de las tejas
    TejasIzq = sg.SceneGraphNode('tejasIzq')
    TejasIzq.transform = tr.matmul([tr.translate(-0.3, 0, 0), tr.rotationZ(-np.pi/4-0.25),tr.rotationY(np.pi/2), tr.scale(1,0.7,1/20)])
    TejasIzq.childs += [gpuTejas]

    # Paralelepipedo que conforma el lado derecho de las tejas
    TejasDer = sg.SceneGraphNode('tejasDer')
    TejasDer.transform = tr.matmul([tr.translate(0.3, 0, 0), tr.rotationZ(np.pi/4+0.25),tr.rotationY(np.pi/2), tr.scale(1,0.7,1/20)])
    TejasDer.childs += [gpuTejas]

    Tejas = sg.SceneGraphNode('tejas')
    Tejas.transform = tr.scale(1,1,1.2)
    Tejas.childs += [TejasIzq, TejasDer]

    # Techo completo lado izquierdo
    techoC = sg.SceneGraphNode('techoC')
    techoC.transform = tr.matmul([tr.translate(0, 0.65, 0), tr.scale(1,1, 1)])
    techoC.childs += [Tejas, techo]

    techoCD = sg.SceneGraphNode('techoCD')
    techoCD.transform = tr.matmul([tr.translate(1.1, 0.1, 0), tr.rotationY(np.pi/2), tr.scale(1,1, 1)])
    techoCD.childs += [Tejas, techo]           

    ####################################
    # Base de la casa
    # Paredes del lado izquierdo de la casa
    base = sg.SceneGraphNode('base')
    base.transform = tr.translate(0,0,0)
    base.childs += [gpuCubo]

    # Paredes del lado derecho
    base2 = sg.SceneGraphNode('base2')
    base2.transform = tr.matmul([tr.translate(1, -0.25, 0), tr.scale(1.2,0.5,1)])
    base2.childs += [gpuCubo]

    #####################################
    # Casa    
    # Se juntan todas las piezas
    casa = sg.SceneGraphNode('casa')
    casa.childs += [base, base2]
    casa.childs += [techoC, techoCD]
    casa.childs += [puerta]
    casa.childs += [ventanaD, ventanaD2, ventanaD3, ventanaS, ventanaS2]

    return casa

# Modelo de casa blanca y negro
def createCasa2(pipeline):
    # Inicialización de la figura
    # Cubo con textura de la base de la casa
    cubo = bs.createTextureCube()
    gpuCubo = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuCubo)
    gpuCubo.fillBuffers(cubo.vertices, cubo.indices, GL_STATIC_DRAW)
    gpuCubo.texture = es.textureSimpleSetup(
        getAssetPath("pared1.jpg"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)

    # Cubo con textura de madera para el garage
    garage = bs.createTextureCube()
    gpuGarage = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuGarage)
    gpuGarage.fillBuffers(garage.vertices, garage.indices, GL_STATIC_DRAW)
    gpuGarage.texture = es.textureSimpleSetup(
        getAssetPath("madera oscura.jpg"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)

    # Cubo con textura de puerta
    puerta = bs.createTextureCube2(1/15, 1)
    gpuPuerta = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuPuerta)
    gpuPuerta.fillBuffers(puerta.vertices, puerta.indices, GL_STATIC_DRAW)
    gpuPuerta.texture = es.textureSimpleSetup(
        getAssetPath("puerta negra.jpg"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)

    # Cubo con textura de ventana
    ventana = bs.createTextureCube2(1/15, 1)
    gpuVentana = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuVentana)
    gpuVentana.fillBuffers(ventana.vertices, ventana.indices, GL_STATIC_DRAW)
    gpuVentana.texture = es.textureSimpleSetup(
        getAssetPath("ventana negra.jpg"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)

    # Diagonal del techo (tejas)
    tejas = bs.createTextureCube()
    gpuTejas = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuTejas)
    gpuTejas.fillBuffers(tejas.vertices, tejas.indices, GL_STATIC_DRAW)
    gpuTejas.texture = es.textureSimpleSetup(
        getAssetPath("techo negro.jpg"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)  

    # Base del techo
    techo = bs.createTextureTechop2()
    gpuTecho = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuTecho)
    gpuTecho.fillBuffers(techo.vertices, techo.indices, GL_STATIC_DRAW)
    gpuTecho.texture = es.textureSimpleSetup(
        getAssetPath("pared1.jpg"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)


    #-------------------------------------------------------------------------------------------------------
    # Grafos
    # Puerta
    puerta = sg.SceneGraphNode('puerta')
    puerta.transform = tr.matmul([tr.translate(0, -0.3, 0.5), tr.scale(0.25,0.4,0.05)])
    puerta.childs += [gpuPuerta]

    ##################################
    # Ventanas
    # Ventana normal
    ventana = sg.SceneGraphNode('ventana')
    ventana.transform = tr.scale(0.25,0.3,0.05)
    ventana.childs += [gpuVentana]

    # Ventana alargada
    ventanaLarga = sg.SceneGraphNode('ventanaLarga')
    ventanaLarga.transform = tr.scale(0.8,0.3,0.05)
    ventanaLarga.childs += [gpuVentana]    

    # Posiciones de las ventanas
    # Ventanas izquierda y derecha del primer piso
    ventanaD = sg.SceneGraphNode('ventanaD')
    ventanaD.transform = tr.translate(0.3, -0.15, 0.5)
    ventanaD.childs += [ventana]

    ventanaI = sg.SceneGraphNode('ventanaI')
    ventanaI.transform = tr.translate(-0.3, -0.15, 0.5)
    ventanaI.childs += [ventana]

    # Ventana del segundo piso
    # Ventana delantera
    ventanaS = sg.SceneGraphNode('ventanaS')
    ventanaS.transform = tr.translate(0, 0.2, 0.5)
    ventanaS.childs += [ventanaLarga]

    # Ventana trasera
    ventanaST = sg.SceneGraphNode('ventanaST')
    ventanaST.transform = tr.translate(0, 0.2, -0.5)
    ventanaST.childs += [ventanaLarga]

    # Ventanas del tercer piso
    # Ventana de la izquierda
    ventana3I = sg.SceneGraphNode('ventana3I')
    ventana3I.transform = tr.matmul([tr.translate(-0.5, 0.7, 0), tr.rotationY(-np.pi/2)])
    ventana3I.childs += [ventanaLarga]

    # Ventana de la derecha
    ventana3D = sg.SceneGraphNode('ventana3D')
    ventana3D.transform = tr.matmul([tr.translate(0.1, 0.7, 0), tr.rotationY(-np.pi/2)])
    ventana3D.childs += [ventanaLarga] 

    ##################################
    # Garage
    # Techo
    techoG = sg.SceneGraphNode('techoG')
    techoG.transform = tr.matmul([tr.translate(1, 0, 0), tr.scale(1,0.1,1)])
    techoG.childs += [gpuGarage]

    # Pared trasera
    paredTG = sg.SceneGraphNode('paredTG')
    paredTG.transform = tr.matmul([tr.translate(1, -0.25, -0.45), tr.rotationX(np.pi/2),tr.scale(1,0.1,0.5)])
    paredTG.childs += [gpuGarage] 

    # Pared derecha
    paredDG = sg.SceneGraphNode('paredDG')
    paredDG.transform = tr.matmul([tr.translate(1.45, -0.25, 0), tr.rotationZ(np.pi/2),tr.scale(0.5,0.1,1)])
    paredDG.childs += [gpuGarage]        

    ##################################
    # Techo
    techo = sg.SceneGraphNode('techo')
    techo.transform = tr.matmul([tr.translate(0, 0, 0), tr.scale(1,0.3,1)])
    techo.childs += [gpuTecho]

    # Paralelepipedo que conforma el lado izquierdo de las tejas
    TejasIzq = sg.SceneGraphNode('tejasIzq')
    TejasIzq.transform = tr.matmul([tr.translate(-0.3, 0, 0), tr.rotationZ(-np.pi/4-0.25),tr.rotationY(np.pi/2), tr.scale(1,0.7,1/20)])
    TejasIzq.childs += [gpuTejas]

    # Paralelepipedo que conforma el lado derecho de las tejas
    TejasDer = sg.SceneGraphNode('tejasDer')
    TejasDer.transform = tr.matmul([tr.translate(0.3, 0, 0), tr.rotationZ(np.pi/4+0.25),tr.rotationY(np.pi/2), tr.scale(1,0.7,1/20)])
    TejasDer.childs += [gpuTejas]

    Tejas = sg.SceneGraphNode('tejas')
    Tejas.transform = tr.scale(1,1,1.2)
    Tejas.childs += [TejasIzq, TejasDer]        

    # Techo completo lado izquierdo
    techoC = sg.SceneGraphNode('techoC')
    techoC.transform = tr.matmul([tr.translate(-0.2, 1.1, 0), tr.scale(0.6,1, 1)])
    techoC.childs += [Tejas, techo]

    ###################################
    # Bases
    # Base de la casa
    base = sg.SceneGraphNode('base')
    base.transform = tr.translate(0,0,0)
    base.childs += [gpuCubo]

    # Piso extra que se agrega a la casa
    piso2 = sg.SceneGraphNode('piso2')
    piso2.transform = tr.matmul([tr.translate(-0.2, 0.7, 0), tr.scale(0.6,0.5,1)])
    piso2.childs += [gpuCubo]

    ##################################
    # Casa   
    casa = sg.SceneGraphNode('casa')

    casa.childs += [base, piso2]
    casa.childs += [techoC]
    casa.childs += [techoG, paredDG, paredTG]
    casa.childs += [puerta]
    casa.childs += [ventanaD, ventanaI, ventanaS, ventanaST, ventana3I, ventana3D]

    return casa    

# Modelo de casa doble (azul y roja)
def createCasa3(pipeline):
    # Inicialización de las figuras
    # Cubo con textura azul
    cubo = bs.createTextureCube()
    gpuCubo = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuCubo)
    gpuCubo.fillBuffers(cubo.vertices, cubo.indices, GL_STATIC_DRAW)
    gpuCubo.texture = es.textureSimpleSetup(
        getAssetPath("pared azul.jpg"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)

    # Cubo con textura roja
    cubo2 = bs.createTextureCube()
    gpuCubo2 = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuCubo2)
    gpuCubo2.fillBuffers(cubo2.vertices, cubo2.indices, GL_STATIC_DRAW)
    gpuCubo2.texture = es.textureSimpleSetup(
        getAssetPath("pared roja.jpg"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)    

    # Cubo con textura de puerta
    puerta = bs.createTextureCube2(1/15,1)
    gpuPuerta = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuPuerta)
    gpuPuerta.fillBuffers(puerta.vertices, puerta.indices, GL_STATIC_DRAW)
    gpuPuerta.texture = es.textureSimpleSetup(
        getAssetPath("puerta oscura.jpg"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)

    # Cubo con textura de ventana
    ventana = bs.createTextureCube2(1/15, 1)
    gpuVentana = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuVentana)
    gpuVentana.fillBuffers(ventana.vertices, ventana.indices, GL_STATIC_DRAW)
    gpuVentana.texture = es.textureSimpleSetup(
        getAssetPath("ventana aluminio.jpg"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)

    # Diagonal del techo (tejas)
    tejas = bs.createTextureCube()
    gpuTejas = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuTejas)
    gpuTejas.fillBuffers(tejas.vertices, tejas.indices, GL_STATIC_DRAW)
    gpuTejas.texture = es.textureSimpleSetup(
        getAssetPath("tejas amarillas.jpg"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)        

    # "Base" del techo (azul)
    techo1 = bs.createTextureTechop2()
    gpuTecho1 = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuTecho1)
    gpuTecho1.fillBuffers(techo1.vertices, techo1.indices, GL_STATIC_DRAW)
    gpuTecho1.texture = es.textureSimpleSetup(
        getAssetPath("pared azul.jpg"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)

    # "Base" del techo (roja)
    techo2 = bs.createTextureTechop2()
    gpuTecho2 = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuTecho2)
    gpuTecho2.fillBuffers(techo2.vertices, techo2.indices, GL_STATIC_DRAW)
    gpuTecho2.texture = es.textureSimpleSetup(
        getAssetPath("pared roja.jpg"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)

                       

    # -----------------------------------------------------------------------------------------------------
    # Grafos
    # Puertas
    puerta = sg.SceneGraphNode('puerta')
    puerta.transform = tr.matmul([tr.translate(0.32, -0.05, 0.5), tr.scale(0.25,0.4,0.05)])
    puerta.childs += [gpuPuerta]

    puerta2 = sg.SceneGraphNode('puerta2')
    puerta2.transform = tr.matmul([tr.translate(0.67, -0.05, 0.5), tr.scale(0.25,0.4,0.05)])
    puerta2.childs += [gpuPuerta]  

    ############################# 
    # Ventanas
    ventana = sg.SceneGraphNode('ventana')
    ventana.transform = tr.scale(0.4,0.3,0.05)
    ventana.childs += [gpuVentana]

    ventanaI = sg.SceneGraphNode('ventanaI')
    ventanaI.transform = tr.translate(-0.15, 0.0, 0.5)
    ventanaI.childs += [ventana]

    ventanaD = sg.SceneGraphNode('ventanaD')
    ventanaD.transform = tr.translate(1.15, 0.0, 0.5)
    ventanaD.childs += [ventana]    

    #############################   
    # Techo
    # Base del techo de color azul
    techo = sg.SceneGraphNode('techo')
    techo.transform =  tr.scale(1,0.3,1)
    techo.childs += [gpuTecho1]

    # Base del techo de color rojo
    techo2 = sg.SceneGraphNode('techo2')
    techo2.transform = tr.scale(1,0.3,1)
    techo2.childs += [gpuTecho2]

    # Paralelepipedo que conforma el lado izquierdo de las tejas
    TejasIzq = sg.SceneGraphNode('tejasIzq')
    TejasIzq.transform = tr.matmul([tr.translate(-0.3, 0, 0), tr.rotationZ(-np.pi/4-0.25),tr.rotationY(np.pi/2), tr.scale(1,0.7,1/20)])
    TejasIzq.childs += [gpuTejas]

    # Paralelepipedo que conforma el lado derecho de las tejas
    TejasDer = sg.SceneGraphNode('tejasDer')
    TejasDer.transform = tr.matmul([tr.translate(0.3, 0, 0), tr.rotationZ(np.pi/4+0.25),tr.rotationY(np.pi/2), tr.scale(1,0.7,1/20)])
    TejasDer.childs += [gpuTejas]

    # Techo completo lado izquierdo
    techoC = sg.SceneGraphNode('techoC')
    techoC.transform = tr.matmul([tr.translate(0, 0.4, 0), tr.rotationY(np.pi/2)])
    techoC.childs += [TejasIzq, TejasDer, techo]

    # Techo completo lado derecho
    techoC2 = sg.SceneGraphNode('techoC2')
    techoC2.transform = tr.matmul([tr.translate(1, 0.4, 0), tr.rotationY(np.pi/2)])
    techoC2.childs += [TejasIzq, TejasDer, techo2]             

    ############################# 
    # Bases de la casa
    base = sg.SceneGraphNode('base')
    base.transform = tr.scale(1,0.5,1)
    base.childs += [gpuCubo]

    base2 = sg.SceneGraphNode('base2')
    base2.transform = tr.matmul([tr.translate(1, 0, 0), tr.scale(1,0.5,1)])
    base2.childs += [gpuCubo2] 

    #############################
    # Casa completa
    casa = sg.SceneGraphNode('casa')
    casa.childs += [base, base2]
    casa.childs += [techoC, techoC2]
    casa.childs += [puerta, puerta2]
    casa.childs += [ventanaD, ventanaI]

    return casa
