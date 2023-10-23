from celestial import *

class Simulation:
    def __init__(self) -> None:
        pg.init()
        self.WIN = pg.display.set_mode((800, 800))
        self.CLOCK = pg.time.Clock()
        pg.display.set_caption("Solar System")

        self.sun = Star(0, 0, 1.989 * 10**30, 695950, self.WIN, '#FFCC33', 'sun')
        self.earth = Planet(-1, 0, 5.972 * 10**24, 6052, self.WIN, 'deepskyblue3', 29.78, 'earth')
        self.mars = Planet(-1.52, 0, 0.64 * 10**24, 3390, self.WIN, '#c1440e', 24, 'mars')
        self.saturn = Planet(9.54, 0, 586 * 10**24, 60268, self.WIN, '#ceb8b8', 9.7, 'saturn')
        self.mercury = Planet(0.39, 0, 0.33 * 10 ** 24, 2438, self.WIN, '#8c8c94', 47.9, 'mercury')
        self.venus = Planet(0.72, 0, 4.87 * 10**24, 6052, self.WIN, '#e39e1c', 35, 'venus')
        self.jupiter = Planet(-5.2, 0, 1898.60 * 10**24, 71492, self.WIN, '#d0a47a', 13.1, 'jupiter')
        self.uranus = Planet(19.2, 0, 86.62 * 10**24, 24973, self.WIN, '#8dc9ee', 6.8, 'uranus')
        self.neptune = Planet(-30.06, 0, 102.42 * 10**24, 24764, self.WIN, '#1f2255', 5.4, 'neptune') 
        self.pluto = Planet(39, 0, 0.01 * 10**24, 1152, self.WIN, 'azure3', 4.64, 'pluto')

        self.bodies = [self.earth, self.mars, self.sun, self.saturn, self.mercury,
                        self.venus, self.jupiter, self.uranus, self.neptune, self.pluto]


    def update_sim(self) -> None:
        """Updates display and sets fps
        """
        pg.display.update()
        self.CLOCK.tick(60)

    def check_events(self) -> None:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()
            if event.type == pg.KEYDOWN:
                self.resize_display() 

    def resize_display(self) -> None:
        """Resize window dimensions using arrow keys
        """
        scale = 0 
        if pg.key.get_pressed()[pg.K_UP]:
            scale = 1.1
        elif pg.key.get_pressed()[pg.K_DOWN]:  
            scale = 0.9  

        if scale <= 0:
            return
        
        for body in self.bodies:
            body.SCALE *= scale
            body.orbit_scale *= scale             

    def run(self) -> None:
        while True:
            self.check_events()
            self.WIN.fill('black')

            self.sun.draw()
            for body in self.bodies:
                if isinstance(body, Planet):
                    body.update(self.bodies)  

            self.update_sim()                    

if __name__ == "__main__":
    sim = Simulation()
    sim.run()