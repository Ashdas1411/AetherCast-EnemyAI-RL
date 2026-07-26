import numpy as np
import env.constants as C

def get_observation(env):
    enemy = env.enemy
    player = env.player
    relative_x = player.x - enemy.x
    relative_z = player.z - enemy.z
    distance = np.sqrt(
        relative_x ** 2 +
        relative_z ** 2
    )
    projectile_distance = 999.0
    for projectile in env.projectiles:
        if not projectile.active:
            continue
        d = np.sqrt(
            (projectile.x - enemy.x) ** 2 +
            (projectile.z - enemy.z) ** 2
        )
        projectile_distance = min(
            projectile_distance,
            d
        )
    observation = np.array(
        [
            relative_x,
            relative_z,
            distance,
            enemy.hp / C.ENEMY_MAX_HP,
            player.hp / C.PLAYER_MAX_HP,
            enemy.attack_cooldown / C.ATTACK_COOLDOWN,
            player.velocity_x,
            player.velocity_z,
            env.enemy_level,
            projectile_distance,
            1.0 if enemy.attack_cooldown <= 0 else 0.0,
            env.current_step / C.MAX_STEPS,
        ],
        dtype=np.float32,
    )
    return observation