from math import tan, pi
from npPirata import normVector, vectorNegative, subtractVectors

class Raytracer(object):
    def __init__(self, screen):
        self.screen = screen
        _,_, self.width, self.height = screen.get_rect()

        self.scene = []
        self.lights = []

        self.camPosition = [0, 0, 0]

        self.rtViewPort(0, 0, self.width, self.height)
        self.rtProjection()

        self.rtClearColor(0, 0, 0)
        self.rtColor(1, 1, 1)
        self.rtClear()
        
    def rtClearColor(self, r, g, b):
        self.clearColor = (r * 255, g * 255, b * 255)

    def rtClear(self):
        self.screen.fill(self.clearColor)

    def rtColor(self, r, g, b):
        self.currColor = (r * 255, g * 255, b * 255)

    def rtPoint(self, x, y, color = None):
        y = self.height - y
        if (0 <= x <= self.width) and (0 <= y <= self.height):
            if color != None:
                color = (int(color[0] * 255), 
                        int(color[1] * 255),
                        int(color[2] * 255))
                self.screen.set_at((x, y), color)
            else:
                self.screen.set_at((x, y), self.currColor)

    def rtCastRay(self, orig, dir, sceneObj = None):
        intersect = None
        hit = None
        depth = float('inf')

        for obj in self.scene:
            if sceneObj != obj:
                intersect = obj.ray_intersect(orig, dir)
                
                if intersect != None:
                    if intersect.distance < depth:
                        hit = intersect
                        depth = intersect.distance

        return hit

    def rtRender(self):
        for x in range(self.vpX, self.vpX + self.vpWidth + 1):
            for y in range(self.vpY, self.vpY + self.vpHeight + 1):
                if (0 <= x <= self.width) and (0 <= y <= self.height):
                    px = ((x + 0.5 - self.vpX) / self.vpWidth) * 2 - 1
                    py = ((y + 0.5 - self.vpY) / self.vpHeight) * 2 - 1

                    px *= self.rightEdge
                    py *= self.topEdge

                    direction = (px, py, -self.nearPlane)
                    direction = normVector(direction)

                    intercept =  self.rtCastRay(self.camPosition, direction)
                    if intercept != None:
                        material = intercept.obj.material
                        surfaceColor = material.diffuse

                        ambientColor = [0, 0, 0]
                        diffuseColor = [0, 0, 0]
                        specularColor =[0, 0, 0]

                        for light in self.lights:
                            if light.lightType == "Ambient":
                                lightColor = light.getLightColor()
                                ambientColor[0] += lightColor[0]
                                ambientColor[1] += lightColor[1]
                                ambientColor[2] += lightColor[2]

                            else:
                                shadowIntersect = None
                                lightDir = None
                                if light.lightType == "Directional":
                                    lightDir = vectorNegative(light.direction)
                                elif light.lightType == "Point":
                                    lightDir = subtractVectors(light.point, intercept.point)
                                    lightDir = normVector(lightDir)

                                shadowIntersect = self.rtCastRay(intercept.point, lightDir, intercept.obj)
                                
                                if shadowIntersect == None:
                                    diffuseLightColor = light.getDifusseColor(intercept)
                                    diffuseColor[0] += diffuseLightColor[0]
                                    diffuseColor[1] += diffuseLightColor[1]
                                    diffuseColor[2] += diffuseLightColor[2]
                                    specularLightColor = light.getSpecularColor(intercept, self.camPosition)
                                    specularColor[0] += specularLightColor[0]
                                    specularColor[1] += specularLightColor[1]
                                    specularColor[2] += specularLightColor[2]

                        #lightColor = ambientColor + diffuseColor + specularColor
                        lightColor = [(ambientColor[i] + diffuseColor[i] + specularColor[i]) for i in range(3)]

                        finalColor = [min(1,(surfaceColor[i] * lightColor[i])) for i in range(3)]

                        self.rtPoint(x, y, finalColor)
                        

    def rtViewPort(self, posX, posY, width, height):
        self.vpX = posX
        self.vpY = posY
        self.vpWidth = width
        self.vpHeight = height

    def rtProjection(self, fov = 60, n = 0.1):
        aspectRatio = self.vpWidth / self.vpHeight
        self.nearPlane = n
        self.topEdge = tan((fov * pi / 180) / 2) * self.nearPlane
        self.rightEdge = self.topEdge * aspectRatio

