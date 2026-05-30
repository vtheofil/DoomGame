# 🎮 DoomGame

A **3D first-person shooter** inspired by the classic DOOM, built entirely from scratch in Python using Pygame. The game implements a software raycasting engine — the same technique used in the original DOOM (1993) — without any 3D libraries or game engines.

---

## 🚀 Demo

> Run locally with Python — no installation needed beyond dependencies.

---

## 🧠 How It Works

The game uses a **raycasting algorithm** to simulate a 3D environment on a 2D map grid. For each vertical column of pixels on the screen, a ray is cast from the player's position. When the ray hits a wall, the engine calculates how far away it is and draws a scaled wall column with the correct texture — creating the illusion of 3D depth.

This is the exact technique used by id Software in Wolfenstein 3D (1992) and DOOM (1993).

---

## ✨ Features

- **Custom Raycasting Engine** — Software-rendered pseudo-3D graphics from scratch, no OpenGL or 3D libraries
- **Textured Walls** — Each wall tile maps to a texture, with correct horizontal offset (UV mapping)
- **Animated Sprites** — Enemies and objects use sprite sheets for frame-by-frame animation
- **NPC Enemies** — Enemies with states: patrol → chase → attack → death
- **Pathfinding (BFS)** — NPCs navigate the map using a graph-based search algorithm to find the player
- **Player Combat** — Shooting mechanic with animated weapon and hit detection
- **Sound System** — Background music and sound effects using `pygame.mixer`
- **HUD** — On-screen health/ammo display using digit sprites
- **Game Loop** — Delta-time based loop for frame-rate independent movement

---

## 🗂️ Project Structure

```
DoomGame/
├── main.py              # Entry point — initializes all systems and runs the game loop
├── settings.py          # Global constants: screen resolution, FOV, FPS, tile size, etc.
├── map.py               # Loads and stores the 2D grid world map
├── player.py            # Player movement, rotation, mouse input, collision detection
├── raycasting.py        # Core raycasting algorithm — computes wall depths and textures per column
├── object_renderer.py   # Renders walls, floor, ceiling, HUD using raycasting results
├── sprite_object.py     # Base class for static and animated billboard sprites
├── object_handler.py    # Manages all NPC and sprite objects in the scene
├── npc.py               # NPC enemy AI: states, movement, attack logic
├── pathfinding.py       # BFS-based pathfinding for NPC navigation
├── weapon.py            # Animated weapon rendering and shooting logic
├── sound.py             # Loads and manages all audio (music + SFX)
├── animatedSprites/     # Sprite sheet images for animated objects/enemies
├── npc/                 # NPC-specific sprite assets
├── digits/              # HUD digit images for score/health display
└── PerigrafiDoomGame.pdf  # Project documentation (Greek)
```

---

## ⚙️ Technologies

| Technology | Usage |
|---|---|
| Python 3.x | Core language |
| Pygame | Window, input, rendering, audio |
| math (stdlib) | Trigonometry for raycasting |
| collections (stdlib) | BFS deque for pathfinding |

---

## 🔧 Installation & Run

```bash
# 1. Clone the repository
git clone https://github.com/vtheofil/DoomGame.git
cd DoomGame

# 2. Install dependencies
pip install pygame

# 3. Run the game
python main.py
```

**Controls:**
| Key | Action |
|---|---|
| W / A / S / D | Move |
| Mouse | Look / Rotate |
| Left Click | Shoot |
| ESC | Quit |

---

## 📐 Technical Details

### Raycasting Algorithm
For each of the `NUM_RAYS` screen columns, the engine:
1. Casts a ray at angle `player_angle ± HALF_FOV`
2. Uses **DDA (Digital Differential Analysis)** to step through grid cells
3. Checks both horizontal and vertical wall intersections
4. Picks the closer hit and computes `projected_height = SCREEN_DIST / depth`
5. Applies a **fisheye correction** using `cos(angle_offset)`

### NPC AI State Machine
```
IDLE → WALK (player in range) → ATTACK (player in sight) → PAIN (hit) → DEATH
```

### Pathfinding
BFS graph search runs periodically on the game grid. NPCs receive a next-step direction toward the player, avoiding walls.

---

## 📄 License

This project was developed as a university assignment. Feel free to use it for educational purposes.
