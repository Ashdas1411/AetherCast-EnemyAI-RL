from enum import IntEnum

class EnemyAction(IntEnum):
    MOVE_FORWARD = 0
    MOVE_BACKWARD = 1
    STRAFE_LEFT = 2
    STRAFE_RIGHT = 3
    FIREBALL = 4
    DODGE = 5
    IDLE = 6