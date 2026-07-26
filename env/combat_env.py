import gymnasium as gym
from gymnasium import spaces
import numpy as np

import env.constants as C

from env.actions import EnemyAction
from env.entities import Player, Enemy
from env.observation import get_observation
from env.projectiles import Projectile
from env.rewards import calculate_reward

class AetherCombatEnv(gym.Env):

    metadata = {"render_modes": []}

    def __init__(self, player_mode="stationary"):
        super().__init__()
        self.player_mode = player_mode
        from env.player_ai import ScriptedPlayer
        if self.player_mode == "stationary":
            self.player_ai = ScriptedPlayer()
        elif self.player_mode == "moving":
            # Placeholder for now
            self.player_ai = ScriptedPlayer()

        self.projectiles = []
        self.action_space = spaces.Discrete(len(EnemyAction))
        self.observation_space = spaces.Box(
            low=-np.inf,
            high=np.inf,
            shape=(12,),
            dtype=np.float32
        )
        self.current_step = 0
        self.player = None
        self.enemy = None

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.enemy_hit = False
        self.player_hit = False
        self.wasted_attack = False
        self.current_step = 0
        self.player = Player(
            x=C.PLAYER_START_X,
            z=C.PLAYER_START_Z,
            hp=C.PLAYER_MAX_HP
        )
        self.enemy = Enemy(
            x=C.ENEMY_START_X,
            z=C.ENEMY_START_Z,
            hp=C.ENEMY_MAX_HP
        )
        self.projectiles = []
        self.enemy_level = 1
        self.idle_steps = 0
        observation = get_observation(self)
        return observation, {}

    def step(self, action):
        self.enemy_hit = False
        self.player_hit = False
        self.wasted_attack = False
        self.current_step += 1
        self._update_cooldowns()
        if self.player_mode == "stationary":
            self.player_ai.update(self)
        elif self.player_mode == "moving":
            self.player_ai.update(self)
        self._apply_enemy_action(action)
        self._update_projectiles()
        self._check_collisions()
        self._cleanup_projectiles()
        self._clamp_positions()
        reward = calculate_reward(self)
        terminated = not self.player.alive
        truncated = self.current_step >= C.MAX_STEPS
        observation = get_observation(self)
        return observation, reward, terminated, truncated, {}

    def _move_enemy(self, direction_x, direction_z, speed):
        length = np.sqrt(direction_x ** 2 + direction_z ** 2)
        if length == 0:
            return
        direction_x /= length
        direction_z /= length
        self.enemy.x += direction_x * speed
        self.enemy.z += direction_z * speed

    def _direction_to_player(self):
        dx = self.player.x - self.enemy.x
        dz = self.player.z - self.enemy.z
        return dx, dz

    def _clamp_positions(self):
        self.enemy.x = np.clip(
            self.enemy.x,
            -C.ARENA_WIDTH / 2,
            C.ARENA_WIDTH / 2
        )
        self.enemy.z = np.clip(
            self.enemy.z,
            -C.ARENA_DEPTH / 2,
            C.ARENA_DEPTH / 2
        )

    def _enemy_fireball(self):
        dx, dz = self._direction_to_player()
        if self.enemy.attack_cooldown > 0:
            self.wasted_attack = True
            return
        length = np.sqrt(dx ** 2 + dz ** 2)
        if length == 0:
            return
        dx /= length
        dz /= length
        projectile = Projectile(
            x=self.enemy.x,
            z=self.enemy.z,
            direction_x=dx,
            direction_z=dz,
            speed=C.PROJECTILE_SPEED,
            damage=C.PROJECTILE_DAMAGE,
            owner="enemy"
        )
        self.enemy.attack_cooldown = C.ATTACK_COOLDOWN
        self.projectiles.append(projectile)

    def _player_fireball(self):
        if self.player.attack_cooldown > 0:
            return
        dx = self.enemy.x - self.player.x
        dz = self.enemy.z - self.player.z
        length = np.sqrt(dx ** 2 + dz ** 2)
        if length == 0:
            return
        dx /= length
        dz /= length
        projectile = Projectile(
            x=self.player.x,
            z=self.player.z,
            direction_x=dx,
            direction_z=dz,
            speed=C.PROJECTILE_SPEED,
            damage=C.PROJECTILE_DAMAGE,
            owner="player",
        )
        self.projectiles.append(projectile)
        self.player.attack_cooldown = C.ATTACK_COOLDOWN

    def _update_projectiles(self):
        for projectile in self.projectiles:
            if projectile.active:
                projectile.update()
                if (
                        abs(projectile.x) > C.ARENA_WIDTH / 2
                        or
                        abs(projectile.z) > C.ARENA_DEPTH / 2
                ):
                    projectile.active = False

    def _check_collisions(self):
        for projectile in self.projectiles:
            if not projectile.active:
                continue
            if projectile.owner == "enemy":
                distance = np.sqrt(
                    (projectile.x - self.player.x) ** 2 +
                    (projectile.z - self.player.z) ** 2
                )
                if distance <= C.PROJECTILE_RADIUS:
                    self.player.take_damage(projectile.damage)
                    self.player_hit = True
                    projectile.active = False
            elif projectile.owner == "player":
                distance = np.sqrt(
                    (projectile.x - self.enemy.x) ** 2 +
                    (projectile.z - self.enemy.z) ** 2
                )
                if distance <= C.PROJECTILE_RADIUS:
                    self.enemy.take_damage(projectile.damage)
                    self.enemy_hit = True
                    projectile.active = False

    def _cleanup_projectiles(self):
        self.projectiles = [
            projectile
            for projectile in self.projectiles
            if projectile.active
        ]

    def _update_cooldowns(self):
        if self.enemy.attack_cooldown > 0:
            self.enemy.attack_cooldown = max(
                0,
                self.enemy.attack_cooldown - 1
            )
        if self.player.attack_cooldown > 0:
            self.player.attack_cooldown = max(
                0,
                self.player.attack_cooldown - 1
            )

    def _movement_action(self, action):
        dx, dz = self._direction_to_player()
        if action == EnemyAction.MOVE_FORWARD:
            self._move_enemy(dx, dz, C.MOVE_SPEED)
        elif action == EnemyAction.MOVE_BACKWARD:
            self._move_enemy(-dx, -dz, C.MOVE_SPEED)
        elif action == EnemyAction.STRAFE_LEFT:
            self._move_enemy(-dz, dx, C.STRAFE_SPEED)
        elif action == EnemyAction.STRAFE_RIGHT:
            self._move_enemy(dz, -dx, C.STRAFE_SPEED)
        elif action == EnemyAction.DODGE:
            self._move_enemy(dz, -dx, C.STRAFE_SPEED * 2)

    def _attack_action(self):
        self._enemy_fireball()

    def _apply_enemy_action(self, action):
        action = EnemyAction(action)
        if action in (
                EnemyAction.MOVE_FORWARD,
                EnemyAction.MOVE_BACKWARD,
                EnemyAction.STRAFE_LEFT,
                EnemyAction.STRAFE_RIGHT,
                EnemyAction.DODGE,
        ):
            self._movement_action(action)
        elif action == EnemyAction.FIREBALL:
            self._attack_action()
        elif action == EnemyAction.IDLE:
            self.idle_steps += 1
            return
        self.idle_steps = 0