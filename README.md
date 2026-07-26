#  AetherCast Enemy AI RL

A reinforcement learning powered enemy AI built using **Gymnasium**, **Stable-Baselines3**, and **Proximal Policy Optimization (PPO)** for the AetherCast gesture-controlled action game.

Instead of relying on a traditional Finite State Machine (FSM), this project trains an enemy agent to make combat decisions autonomously through reinforcement learning.

---

##  Project Goal

The objective of this project is to design and train an intelligent enemy capable of learning combat behaviour inside a custom-built arena environment and later integrate the trained policy into **AetherCast**, a gesture-controlled 3D spellcasting game.

---

## Features

-  Custom Gymnasium combat environment
-  PPO training pipeline
-  Custom reward shaping
-  Projectile-based combat simulation
-  Cooldown management
-  Scripted player opponent
-  Model checkpointing
-  Evaluation pipeline
-  Trained PPO model
-  Integration into AetherCast

---

## Tech Stack

- Python
- Gymnasium
- Stable-Baselines3
- PyTorch
- NumPy
- Matplotlib
- Jupyter Notebook

---

## Project Structure

```text
AetherCast-EnemyAI-RL
│
├── env/
│   ├── combat_env.py
│   ├── entities.py
│   ├── rewards.py
│   ├── player.py
│   └── projectile.py
│
├── training/
│   ├── train.py
│   └── evaluate.py
│
├── models/
│   ├── enemy_final.zip
│   └── checkpoints/
│
├── notebooks/
│
├── requirements.txt
└── README.md
```

---

## Observation Space

The PPO agent observes combat information including:

- Relative player position
- Relative enemy position
- Health values
- Cooldowns
- Distance
- Projectile information

The observation space is intentionally designed to remain compatible with future gameplay improvements such as player movement and additional spells.

---

## Action Space

| Action ID | Action |
|-----------|--------|
| 0 | Move Forward |
| 1 | Move Backward |
| 2 | Strafe Left |
| 3 | Strafe Right |
| 4 | Fireball |
| 5 | Dodge |
| 6 | Idle |

---

## Reward Function

The reward function encourages tactical combat behaviour by rewarding:

- Successful hits
- Eliminating the opponent
- Maintaining effective combat distance

while penalizing:

- Taking damage
- Dying
- Excessive idling
- Wasted attacks

---

## Training

Train the PPO agent:

```bash
python -m training.train
```

---

## Evaluation

Evaluate the trained model:

```bash
python -m training.evaluate
```

---

## Current Results

The trained PPO agent is capable of:

- Maintaining combat distance
- Launching projectile attacks
- Dodging and repositioning
- Defeating the scripted player consistently

The current model serves as the decision-making component for integration into **AetherCast**.

---

## Future Work

- Integration into AetherCast
- Dynamic player movement
- Multiple spell types
- Curriculum learning
- Multi-agent combat
- Advanced reward shaping
- Smarter scripted opponents

---

## Related Project

This repository is part of the larger **AetherCast** project, a gesture-controlled 3D spellcasting game featuring reinforcement learning-powered enemies.

---

## License

MIT License
