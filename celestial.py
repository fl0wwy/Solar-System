from abc import ABC, abstractmethod
import pygame as pg
import math

class Celestial(ABC):
    AU = 149600000000 # 1AU km's
    TIMESTEP = 3600*24 # seconds in a day
    G = 6.67430e-11 

    def __init__(self, x, y, mass, radius, display, color) -> None:
        super().__init__()

        self.mass = mass
        self.radius = radius
        self.x = x * Celestial.AU
        self.y = y * Celestial.AU
        self.distance = 0

        self.orbit = [] # Track orbit points
        self.vel_x = 0
        self.vel_y = 0

        self.display = display
        self.color = color

        self.SCALE = 1 # arbitrary constant number to scale actual radius of the celestial object to fit the simulation dimensions

    def draw(self):
        x = self.x / 1496000000 + (self.display.get_width() / 2)
        y = self.y / 1496000000 + (self.display.get_height() / 2) 
        pg.draw.circle(self.display, self.color, (x, y), self.radius / self.SCALE)      


class Star(Celestial):
    def __init__(self, x, y, mass, radius, display, color) -> None:
        super().__init__(x, y, mass, radius, display, color)
        self.SCALE = 30000


class Planet(Celestial):
    def __init__(self, x, y, mass, radius, display, color, velocity) -> None:
        super().__init__(x, y, mass, radius, display, color)
        
        self.SCALE = 500
        self.vel_y = velocity * 1000 

    def calc_attraction(self, celestial):
        dist_x = celestial.x - self.x
        dist_y = celestial.y - self.y
        r = math.sqrt(dist_x**2 + dist_y**2)

        if isinstance(celestial, Star):
            self.distance = r
            
        force = (Celestial.G * self.mass * celestial.mass) / r**2
        alpha = math.atan2(dist_y, dist_x)
        force_x = math.cos(alpha) * force
        force_y = math.sin(alpha) * force  
        return force_x, force_y

    def update_position(self, celestials):
        total_fx = total_fy = 0
        for body in celestials:
            if body != self:
                fx, fy = self.calc_attraction(body) 
                total_fx += fx
                total_fy += fy
            
        # calculating velocity 
        self.vel_x += total_fx / self.mass * self.TIMESTEP   
        self.vel_y += total_fy / self.mass * self.TIMESTEP

        # updating position
        self.x += self.vel_x * self.TIMESTEP
        self.y += self.vel_y * self.TIMESTEP
        self.orbit.append((self.x, self.y))

    def draw_orbit(self):
        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x / 1496000000 + (self.display.get_width() / 2)
                y = y / 1496000000 + (self.display.get_height() / 2)   
                updated_points.append((x, y))
            pg.draw.lines(self.display, self.color, False, updated_points, 3) 

        if len(self.orbit) >= int(100 * (self.radius/6371)):
            self.orbit.pop(0)     

    def update(self, celestials):
        self.draw_orbit()
        self.draw()    
        self.update_position(celestials)  
              