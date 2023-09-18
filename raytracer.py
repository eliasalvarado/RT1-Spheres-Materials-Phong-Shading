import pygame as pg
from pygame.locals import *
from rt import Raytracer
from figures import *
from materials import *
from lights import *


width = 512
height = 640

pg.init()

screen = pg.display.set_mode((width, height), pg.DOUBLEBUF | pg.HWACCEL | pg.HWSURFACE)
screen.set_alpha(None)

raytracer = Raytracer(screen=screen)

raytracer.rtClearColor(0.25, 0.25, 0.25)

snow = Material(diffuse=(1, 1, 1), specular=8, ks=0.01)
rock = Material(diffuse=(0, 0, 0), specular=2, ks=0.01)
carrot = Material(diffuse=(0.57, 0.35, 0.08), specular=8, ks=0.01)
eye = Material(diffuse=(0.999, 0.999, 0.999), specular=2, ks=0.01)

#Body
raytracer.scene.append(Sphere(position=(0, -2, -7), radius=1, material=snow)) #Parte baja
raytracer.scene.append(Sphere(position=(0, -0.5, -7), radius=0.8, material=snow)) #Parte media
raytracer.scene.append(Sphere(position=(0, 0.6, -7), radius=0.5, material=snow)) #Cabeza

#Cabeza
    #Boca
raytracer.scene.append(Sphere(position=(0, 0.3, -5), radius=0.035, material=rock))
raytracer.scene.append(Sphere(position=(0.1, 0.3, -5), radius=0.035, material=rock))
raytracer.scene.append(Sphere(position=(-0.1, 0.3, -5), radius=0.035, material=rock))
raytracer.scene.append(Sphere(position=(0.2, 0.35, -5), radius=0.035, material=rock))
raytracer.scene.append(Sphere(position=(-0.2, 0.35, -5), radius=0.035, material=rock))
    #Nariz
raytracer.scene.append(Sphere(position=(0, 0.45, -5), radius=0.05, material=carrot))
    #Ojos
raytracer.scene.append(Sphere(position=(0.15, 0.62, -5), radius=0.05, material=eye)) #Ojo derecho
raytracer.scene.append(Sphere(position=(0.14, 0.63, -4.9), radius=0.015, material=rock)) #Iris de ojo derecho
raytracer.scene.append(Sphere(position=(-0.15, 0.62, -5), radius=0.05, material=eye)) #Ojo izquierdo
raytracer.scene.append(Sphere(position=(-0.16, 0.63, -4.9), radius=0.015, material=rock)) #Iris de ojo izquierdo

#Buttons
raytracer.scene.append(Sphere(position=(0, -1.3, -5), radius=0.2, material=rock)) #Botón parte baja
raytracer.scene.append(Sphere(position=(0, -0.75, -5), radius=0.15, material=rock)) #Botón parte media
raytracer.scene.append(Sphere(position=(0, -0.2, -5), radius=0.1, material=rock)) #Botón parte media

#Lights
raytracer.lights.append(AmbientLight(0.1))
raytracer.lights.append(DirectionalLight(direction=(-1, -1, -1), intensity=0.7))
    #Luces de apoyo para hacer una mejor vista de los ojos
raytracer.lights.append(PointLight(point=(0.15, 0.62, -4.7), intensity=0.025, color=(1, 1, 1)))
raytracer.lights.append(PointLight(point=(-0.15, 0.62, -4.7), intensity=0.025, color=(1, 1, 1)))

isRunning = True
while(isRunning):
    for event in pg.event.get():
        if event.type == pg.QUIT:
            isRunning = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                isRunning = False
            elif event.key == pg.K_s:
                pg.image.save(screen, "image.bmp")
    raytracer.rtClear()
    raytracer.rtRender()
    pg.display.flip()



pg.quit()
