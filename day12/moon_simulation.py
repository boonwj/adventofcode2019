"""
Moon Simulation

Given initial positions of moons, determine their velocities and positions
after timesteps
"""

class Moon:
    def __init__(self, name="", position=[0,0,0]):
        self.name = name
        self.position = position
        self.velocity = [0, 0, 0]

    def apply_gravity(self, moon):
        for i in range(len(self.position)):
            if self.position[i] < moon.position[i]:
                self.velocity[i] += 1
                moon.velocity[i] -= 1
            elif self.position[i] > moon.position[i]:
                self.velocity[i] -= 1
                moon.velocity[i] += 1

    def move(self):
        for i, speed in enumerate(self.velocity):
            self.position[i] += speed

    def energy(self):
        pot = sum(map(abs, self.position))
        kin = sum(map(abs, self.velocity))
        return pot * kin

class SpaceSystem:
    def __init__(self, objects = []):
        self.objects = []
        self.pairs = []
        for name, position in objects:
            self.objects.append(Moon(name, position))

        for i in range(len(self.objects)):
            for j in range(i + 1, len(self.objects)):
                self.pairs.append((i, j))

        self.timestep = 0

    def step_forward(self, steps=1):
        for _ in range(steps):
            self.timestep += 1
            self._apply_gravity()
            self._move()

    def _apply_gravity(self):
        for obj1, obj2 in self.pairs:
            self.objects[obj1].apply_gravity(self.objects[obj2])

    def _move(self):
        for obj in self.objects:
            obj.move()

    def total_energy(self):
        energy = 0
        for obj in self.objects:
            energy += obj.energy()

        return energy

if __name__ == "__main__":
    objects = [
        ("Io", [-7, -1, 6]),
        ("Europa", [6, -9, -9]),
        ("Ganymede", [-12, 2, -7]),
        ("Callisto", [4, -17, -12])
    ]
    system = SpaceSystem(objects)
    system.step_forward(1000)
    print(system.total_energy())