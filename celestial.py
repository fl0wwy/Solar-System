from abc import ABC
import pygame as pg
import math
import locale
from typing import Any

class Celestial(ABC):
    """Abstract class that represents a celestial body in space.
    has basic properties such as position (x,y), mass, radius and color

    static variables:
    AU - the distance in km from Earth to the Sun
    TIMESTEP - the amount of time between each change in the positions is made in seconds
    G - the gravitatonal constant
    """
    AU = 149600000000 # 1AU in km
    TIMESTEP = 3600*24 # seconds in a day
    G = 6.67430e-11 # gravitational constant

    def __init__(self, x: float, y: float, mass: float, radius: float, display: Any, color: Any, name: str) -> None:
        super().__init__()

        self.mass = mass
        self.radius = radius
        self.x = x * Celestial.AU
        self.y = y * Celestial.AU
        self.distance = 0 # distance from the star

        self.orbit = [] # Track orbit points
        self.vel_x = 0 # velocity in the x axis
        self.vel_y = 0 # velocity in the y axis

        self.display = display
        self.color = color

        self.orbit_scale = 1496000000 # 1AU = 100px default value
        self.name = name

        self.SCALE = 1 # arbitrary constant number to scale actual radius of the celestial object to fit the simulation dimensions

    def draw(self) -> None:
        """Draws the body on the display to scale
        """
        x = self.x / self.orbit_scale + (self.display.get_width() / 2)
        y = self.y / self.orbit_scale + (self.display.get_height() / 2)
        pg.draw.circle(self.display, self.color, (x, y), self.radius / self.SCALE) 

    def format_number(self, number: int) -> str:
        # Set the locale to the user's default for proper formatting
        locale.setlocale(locale.LC_ALL, '')

        # Format the number with commas as thousands separators
        formatted_number = locale.format_string("%d", number, grouping=True)

        return formatted_number         


class Star(Celestial):
    """Child class of Celestial. 
    Represents a star at the center of the solar system

    """
    def __init__(self, x, y, mass, radius, display, color, name) -> None:
        super().__init__(x, y, mass, radius, display, color, name)
        self.SCALE = 30000


class Planet(Celestial):
    """Child class of Celestial.
    Represents a planet.

    Requires an extra argument velocity.
    velocity - The oribtal speed of the planet around its star in km/s

    """
    def __init__(self, x, y, mass, radius, display, color, velocity: float, name) -> None:
        super().__init__(x, y, mass, radius, display, color, name)
        
        self.SCALE = 500
        self.vel_y = velocity * 1000 

    def calc_attraction(self, celestial) -> float:
        """Calculates the forces applied on the planet by all bodies in the solar system using Newton's law of universal gravitation.
        Since this is a 2D simulation, the forces are calculated for the X and Y axes only using trigonometry
        and the pythagorean theorem

        Args:
            celestial (Celestial): the celestial body the function will calculate the force it applies on self.

        Returns:
            forces applied on X and Y axes
        """
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

    def update_position(self, celestials: list) -> None:
        """Applies forces calculated for each celestial body and updates the position of self accordingly

        Args:
            celestials (list): List of all celestial bodies in the system
        """
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

    def draw_orbit(self) -> None:
        """Draws the orbit of the planet by using the points in self.orbit
        """
        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x / self.orbit_scale + (self.display.get_width() / 2)
                y = y / self.orbit_scale + (self.display.get_height() / 2)  
                updated_points.append((x, y))
            pg.draw.lines(self.display, self.color, False, updated_points, 3) 

        if self.distance <= 500000000000:
            if len(self.orbit) >= int(100 * (self.radius/6371)):
                self.orbit.pop(0)     

    def distance_from_sun(self) -> None:
        """Draws the distance to the star in km
        """
        x = self.x / self.orbit_scale + (self.display.get_width() / 2)
        y = self.y / self.orbit_scale + (self.display.get_height() / 2)  
        
        font = pg.font.SysFont('arial', 10)
        dist = font.render(f'{self.format_number(round(self.distance/1000))}km', True, 'white', (31, 31, 31))
        name = font.render(self.name.capitalize(), True, 'white', (31, 31, 31))
        
        self.display.blit(name, (x, y - 10))
        self.display.blit(dist, (x,y))        

    def update(self, celestials: list) -> None:
        """Executes all the functions of the class

        Args:
            celestials (list): List of all celestial bodies in the system
        """
        self.draw_orbit()
        self.draw()    
        self.update_position(celestials)  
        self.distance_from_sun()
              