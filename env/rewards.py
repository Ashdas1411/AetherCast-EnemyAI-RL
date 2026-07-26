import numpy as np

IDEAL_DISTANCE = 3.0
DISTANCE_TOLERANCE = 1.0

def calculate_reward(env):
    reward = -0.001  # Small living penalty
    enemy = env.enemy
    player = env.player

    # Distance reward
    distance = np.sqrt(
        (enemy.x - player.x) ** 2 +
        (enemy.z - player.z) ** 2
    )
    if abs(distance - IDEAL_DISTANCE) <= DISTANCE_TOLERANCE:
        reward += 0.05

    # Hit rewards
    if env.player_hit:
        reward += 2.0
    if env.enemy_hit:
        reward -= 2.0

    # Terminal rewards
    if not player.alive:
        reward += 20.0
    if not enemy.alive:
        reward -= 20.0

    if env.idle_steps > 3:
        reward -= 0.05

    if env.wasted_attack:
        reward -= 0.10

    return reward