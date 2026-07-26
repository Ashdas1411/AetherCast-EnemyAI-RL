from stable_baselines3 import PPO
from env.combat_env import AetherCombatEnv

def main():
    env = AetherCombatEnv()
    model = PPO.load("models/enemy_final")
    obs, _ = env.reset()
    done = False
    truncated = False
    step = 0
    while not (done or truncated):
        action, _ = model.predict(
            obs,
            deterministic=True
        )
        obs, reward, done, truncated, _ = env.step(action)
        print(
            f"Step {step:3} | "
            f"Action: {int(action)} | "
            f"Enemy HP: {env.enemy.hp:3} | "
            f"Player HP: {env.player.hp:3} | "
            f"Reward: {reward:.2f}"
        )
        step += 1
    print("\nEpisode Finished")
    print("Enemy HP :", env.enemy.hp)
    print("Player HP:", env.player.hp)

if __name__ == "__main__":
    main()