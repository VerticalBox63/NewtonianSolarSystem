import pygame
import numpy as np
import sys

class Planet:
    def __init__(self, mass, radius, color, name):
        self.vel = pygame.Vector2(0,0)
        self.pos = pygame.Vector2(0,0)
        self.mass = mass
        self.color = color
        self.radius = radius
        self.trail = []
        self.name = name
        self.Collision = False
        self.collider = None
    
    #Update Velocity
    def GetAcceleration(self, bodies, pos):
        G = 6.674*10**-11
        acceleration = []
        for body in bodies:
            if body != self:                
                #Calculate Force,
                r = -pos + body.pos # in pixels

                if r.magnitude() < self.radius+body.radius:
                    self.Collision = True
                    self.collider = body

                Force = (G*body.mass*self.mass)/(r.length()**3)*r
                acceleration.append(Force/self.mass)
        Final = pygame.Vector2(0,0)
        for a in acceleration:
            Final += a
        return Final
    
    def RungeKutta(self, dt, bodies):

        x1 = self.pos
        v1 = self.vel
        a1 = self.GetAcceleration(bodies, x1)

        # k2
        x2 = x1 + v1 * dt/2
        v2 = v1 + a1 * dt/2
        a2 = self.GetAcceleration(bodies, x2)

        # k3
        x3 = x1 + v2 * dt/2
        v3 = v1 + a2 * dt/2
        a3 = self.GetAcceleration(bodies, x3)

        # k4
        x4 = x1 + v3 * dt
        v4 = v1 + a3 * dt
        a4 = self.GetAcceleration(bodies, x4)

        # Update position and velocity
        return self.pos + dt/6 * (v1 + 2*v2 + 2*v3 + v4), self.vel + dt/6 * (a1 + 2*a2 + 2*a3 + a4)

class SimScreen:
    def __init__(self):
        self.screen = pygame.Surface((1080, 720))
        self.Pixels_per_metre = 200 / (1.496e+11*0.5)
        self.centre_factor = pygame.Vector2(1080/2, 720/2)
        self.bodies = []#
        self.tracking = False
        self.tracked_body = None
        self.dragging = False
        
    def Draw(self, bodies):
        self.screen.fill((0,0,0))
        for body in bodies:
            if len(body.trail) > 1:
                if len(body.trail) > 2000:
                    body.trail.pop(0)
                pygame.draw.lines(self.screen, body.color, False, np.array(body.trail)*self.Pixels_per_metre+self.centre_factor, 1)
            print(body.color, body.pos*self.Pixels_per_metre+self.centre_factor)
            if body == bodies[-1]:
                print(body.trail)
            pygame.draw.circle(self.screen, body.color, body.pos*self.Pixels_per_metre+self.centre_factor, body.radius*self.Pixels_per_metre)

    def Pan(self, dx, dy):
        self.centre_factor.x += dx
        self.centre_factor.y += dy

    def Track(self, body):
        self.centre_factor = -body.pos*self.Pixels_per_metre + pygame.Vector2(1080/2, 720/2)

    def LoadSolarSystem(self):
       #Planet Define
        Sun = Planet(1.99e30, 6.96e9, "yellow", "Sun")
        Mercury = Planet(3.3011e23, 1e7, "silver", "Mercury")
        Venus = Planet(4.8675e24, 1e7, "red", "Venus")

        Earth = Planet(5.972e24, 6.3e7, "light blue", "Earth")
        Moon = Planet(7.35e22, 1.737e7, "grey", "Moon")
        Mars = Planet(0.107*Earth.mass, 3.3e8, "orange", "Mars")
        Jupiter = Planet(317.8*Earth.mass, 0.10276*Sun.radius, "brown", "Jupiter")
        Saturn = Planet(95.159*Earth.mass, 1e11, "brown", "Saturn")
        Uranus = Planet(17.147*Earth.mass, 1e11, "Aqua", "Uranus")
        Neptune = Planet(14.536*Earth.mass, 1e11, "White", "Neptune")
        

        #Starting Conditions

        Mercury.pos.y = 57.91e9
        Mercury.vel.x = 47.36e3

        Venus.pos.y = 108.21e9
        Venus.vel.x = 35.02e3


        Earth.pos.y = 1.496e11 #1au
        Earth.vel.x = 29284.8 # m/s

        Moon.pos.y = Earth.pos.y + 384400e3-4.67e3 #1au
        Moon.vel.x = Earth.vel.x + 1.022e3 # m/s

        Mars.pos = 1.524*Earth.pos
        Mars.vel.x = 24.3e3

        Jupiter.pos = 5.2038*Earth.pos
        Jupiter.vel.x = 13.06e3

        Saturn.pos = 9.5826*Earth.pos
        Saturn.vel.x = 9.68e3

        Uranus.pos = 19.191*Earth.pos
        Uranus.vel.x = 6.80e3


        Neptune.pos = 30.07*Earth.pos
        Neptune.vel.x = 5.45e3


        self.bodies = [Sun, Mercury, Venus, Earth, Moon, Mars, Jupiter, Saturn, Uranus, Neptune] 

    def LoadSandbox(self):
        Sun = Planet(1.99e30, 6.96e9, "yellow", "Sun")
        Sun.vel.x= 1e3
        self.bodies.append(Sun)

    def AddRandomBody(self):
        num = np.random.random()
        num*=2
        self.bodies.append(Planet(num*self.bodies[0].mass, num**0.3333*self.bodies[0].radius, "white", "Planet"))
        #Velocity
        velocity = pygame.Vector2(1,0)
        angle = np.random.uniform(0, 360)
        velocity.rotate_ip(angle)

        r = np.random.random()

        velocity.scale_to_length(1.7e4+10e4*r)

        position = pygame.Vector2(1,1)
        angle = np.random.uniform(0, 360)
        position.rotate_ip(angle)

        r = np.random.random()

        position.scale_to_length(1e6 + r*1e11)

        self.bodies[-1].pos = position
        self.bodies[-1].vel = velocity

    def CheckCollison(self):
        for body in list(self.bodies):
            if body.Collision == True:
                
                p1 = body.mass*body.vel
                p2 = body.collider.mass*body.collider.vel

                p3 = p1 + p2

                oldmass = body.mass
                body.mass += body.collider.mass
                body.radius = body.radius * (body.mass/oldmass)**0.3333
                body.vel = p3/body.mass

                self.bodies.remove(body.collider)
                body.collider.Collision = False
                body.collider.collider = None
                body.collider = None
                body.Collision = False
                






class LaunchScreen:
        def __init__(self):
            self.screen = pygame.Surface((1080, 720))
            
        def DrawMenu(self):
            my_font = pygame.font.SysFont(None, 24)
            screenCentre = pygame.Vector2(self.screen.get_width()//2, self.screen.get_height()//2)
            text_surface = my_font.render('Newtonian Orbital Simulations', False, "white")
            self.screen.blit(text_surface, screenCentre + pygame.Vector2(0, -100))


            text_surface = my_font.render('1. Solar System', False, "white")
            self.screen.blit(text_surface, screenCentre + pygame.Vector2(0, 0))

            text_surface = my_font.render('2. Empty', False, "white")
            self.screen.blit(text_surface, screenCentre + pygame.Vector2(0, 100))


            
def UpdatePositions(dt, bodies):
    new_pos = []
    new_vel = []

    for body in bodies:
        x, v = body.RungeKutta(dt, bodies)
        new_pos.append(x)
        new_vel.append(v)
        if len(body.trail)>1:
            if (body.trail[-1] - x).magnitude() > 1e9:
                body.trail.append(x)
        else:
            body.trail.append(body.pos)

    for i, body in enumerate(bodies):
        body.pos = new_pos[i]
        body.vel = new_vel[i]


