from dataclasses import dataclass

@dataclass
class Projectile:
    x: float
    z: float

    direction_x: float
    direction_z: float

    speed: float
    damage: float

    owner: str

    active: bool = True

    def update(self):
        self.x += self.direction_x * self.speed
        self.z += self.direction_z * self.speed