import math
import pygame

pygame.init()
width = 2560
height = 1440
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
FPS = 60

class Obj:
    def __init__(self, position=(width // 2, height // 2), mass=1.9891*10**30, radius=695700, velocity=(0, 0), acceleration=(0, 0), orbiting=False, orb=None, orb_dist=None, color="white"):
        self.pos = pygame.Vector2(position)
        self.mass = mass
        self.rad = radius*rad_scale
        self.vel = pygame.Vector2(velocity)
        self.acc = pygame.Vector2(acceleration)
        self.clr = color

        self.orbiting = orbiting
        self.orb = orb

        try:
            self.orb_dist = orb_dist*dist_mult
        except TypeError:
            self.orb_dist = None

        self.add_vel = (0, None)
        self.orb_vel = None
        self.trail_hist = []

        self.calc_orb_vel()
        objects.append(self)

    def update_trail_hist(self):
        if len(self.trail_hist) >= 1:
            self.trail_hist.pop(0)

        self.trail_hist.append(self.pos.copy())

    def calc_orb_vel(self):
        if self.orbiting:
            self.orb_vel = math.sqrt(G * self.orb.mass / (self.orb_dist * scale))

            if self.orb.orbiting:
                self.vel = pygame.Vector2(self.orb.vel.x, self.orb.vel.y - self.orb_vel)
            else:
                self.vel = pygame.Vector2(0, -self.orb_vel)


scale = 1e9
rad_scale = 1
dist_mult = 1

dt = 43200 * math.sqrt(dist_mult)
G = 6.6743 * 10 ** -11

objects = []
collisions = []
def run(*args):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        screen.fill("black")
        collisions.clear()

        for i in objects:
            i.pos += i.vel * dt / scale + 0.5 * i.acc * (dt ** 2) / scale

        for i in objects:
            old_acc = i.acc.copy()
            i.acc = pygame.Vector2(0, 0)

            for j in objects:
                if j == i:
                    continue

                r_vec = j.pos - i.pos
                distance = pygame.Vector2.magnitude(r_vec) * scale
                if distance < (i.rad + j.rad) * 1e5 / 2:
                    if (j, i) not in collisions:
                        collisions.append((i, j))
                    continue

                force_mag = G * j.mass * i.mass / (distance ** 2)
                force_vec = (r_vec / pygame.Vector2.magnitude(r_vec)) * force_mag

                i.acc += force_vec / i.mass

            i.vel += 0.5 * (old_acc + i.acc) * dt

        for i, j in collisions:
            if i not in objects or j not in objects:
                continue

            t_mass = i.mass + j.mass

            vel = pygame.Vector2((i.vel * i.mass + j.vel * j.mass) / t_mass)
            pos = (i.pos * i.mass + j.pos * j.mass) / t_mass
            rad = (i.rad**3 + j.rad**3) ** (1/3)

            if i.mass > j.mass:
                clr = i.clr
            else:
                clr = j.clr

            merged = Obj(pos, t_mass, rad / rad_scale, vel, color=clr)

            objects.remove(i)
            objects.remove(j)
        
        for i in objects:
            i.update_trail_hist()

            if len(i.trail_hist) > 1:
                pygame.draw.lines(screen, i.clr, False, i.trail_hist, 1)

            pygame.draw.circle(screen, i.clr, (int(i.pos.x), int(i.pos.y)), max(int(i.rad / 2e4), 1))
        
        for arg in args:
            print(arg)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    run()
