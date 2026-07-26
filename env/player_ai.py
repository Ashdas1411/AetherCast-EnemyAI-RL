import numpy as np
import env.constants as C


class ScriptedPlayer:

    def update(self, env):

        enemy = env.enemy
        player = env.player

        dx = enemy.x - player.x
        dz = enemy.z - player.z

        distance = np.sqrt(dx ** 2 + dz ** 2)

        if distance > 6:

            dx /= distance
            dz /= distance

            player.x += dx * C.PLAYER_SPEED
            player.z += dz * C.PLAYER_SPEED

        elif distance < 4:

            player.x += 0.05

        if player.attack_cooldown <= 0:

            env._player_fireball()

            player.attack_cooldown = C.ATTACK_COOLDOWN