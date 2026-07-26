from stable_baselines3 import PPO
from stable_baselines3.common.env_checker import check_env
from stable_baselines3.common.callbacks import CheckpointCallback

from env.combat_env import AetherCombatEnv

def main():
    env = AetherCombatEnv()
    print("Checking environment...")
    check_env(env)
    print("Environment passed!")
    checkpoint_callback = CheckpointCallback(
        save_freq=10000,
        save_path="models/",
        name_prefix="enemy"
    )
    model = PPO(
        policy="MlpPolicy",
        env=env,
        verbose=1,
        learning_rate=3e-4,
        n_steps=2048,
        batch_size=64,
        gamma=0.99,
        gae_lambda=0.95,
        clip_range=0.2,
        ent_coef=0.01,
    )
    print("Training...")
    model.learn(
        total_timesteps=100000,
        callback=checkpoint_callback,
    )
    model.save("models/enemy_final")
    print("Done!")

if __name__ == "__main__":
    main()