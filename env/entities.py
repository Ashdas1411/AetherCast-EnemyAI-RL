from dataclasses import dataclass

@dataclass
class Character:

    x: float
    z: float
    hp: float
    velocity_x: float = 0.0
    velocity_z: float = 0.0
    attack_cooldown: float = 0.0
    alive: bool = True

    def take_damage(self, damage: float):

        self.hp -= damage
        if self.hp <= 0:
            self.hp = 0
            self.alive = False

@dataclass
class Player(Character):
    pass

@dataclass
class Enemy(Character):
    pass