# pygame_space_shooting_game

This is a simple 2D pixel vertical scrolling shooting game created by Luke Tseng, a high school student. 

In addition, the game was created through the author's one hour on weekdays and five hours on Saturdays and Sundays.

# Environment

The development environment uses Python 3.12.2 and Pygame 2.6.1.

## Install on Windows PowerShell

Python 3.12 is recommended for this project. Install it with:

```powershell
winget install -e --id Python.Python.3.12
```

Restart PowerShell, open the project directory, and create a virtual environment:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install pygame==2.6.1
```

Verify the installation:

```powershell
python -c "import pygame; print(pygame.version.ver)"
```

If PowerShell blocks the virtual environment activation script, allow it for the
current PowerShell process and try again:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

## Pygame installation error with Python 3.14

Installing `pygame==2.6.1` with Python 3.14 on Windows may produce errors such
as:

```text
ModuleNotFoundError: No module named 'distutils.msvccompiler'
ModuleNotFoundError: No module named 'setuptools._distutils.msvccompiler'
ERROR: Failed to build 'pygame' when getting requirements to build wheel
```

This happens because Pygame 2.6.1 does not provide a compatible Windows wheel
for Python 3.14. Pip downloads the source archive and attempts to compile
Pygame locally, but its build process is not compatible with that Python
environment.

Use the Python 3.12 virtual environment described above instead of installing
additional SDL or Visual C++ build dependencies.

In VS Code, run `Python: Select Interpreter` from the Command Palette and
select:

```text
.\.venv\Scripts\python.exe
```

# Control

Using your mouse or keyboard (you need go to setting UI to change these) : `← → ↑ ↓` to control the character.

# Features

The features of this game can currently be divided into the following five types :

1. Enemies : The enemy images will change every five levels, and the enemy's health and attack power will increase as the level progresses. In every fifth level, such as the fifth, tenth, and fifteenth levels, a BOSS will appear. The three BOSSes have different attack modes, and the difficulty also increases with the level.
2. Player status (Upgrade Store) : There is an upgrade mall built into the main menu, which can currently enhance the player's maximum health, bullet speed, and attack power. To upgrade, you need to spend the corresponding coins. Coins can be obtained by killing enemies.
3. Level : The level operation mechanism is based on the number of points obtained. The points formula is calculated as 100 + (level * 10) * 9. When the specified points are reached, you will enter the next level.
4. Item : When the player kills an enemy, he will currently receive two props, one is a prop that increases health, and the other is a prop that allows the player to gain a shield within a certain period of time.
5. Animation : For example, the explosion animation of the enemy, the flashing animation when the player is hit, the animation when the bullet is shot, etc.

# Image Source

Background : Leonardo.ai

Space Main Ship : https://foozlecc.itch.io/void-main-ship

Enemy 1 Series : https://foozlecc.itch.io/void-fleet-pack-1

Enemy 2 Series : https://foozlecc.itch.io/void-fleet-pack-2

Enemy 3 Series : https://foozlecc.itch.io/void-fleet-pack-3

Enemy 4 Series : https://free-game-assets.itch.io/free-enemy-spaceship-2d-sprites-pixel-art

Items : https://foozlecc.itch.io/void-pickups-pack

Background Music : https://opengameart.org/content/space-shooter-music

Laser Sound Efect : https://pixabay.com/sound-effects/search/laser/

Enemy Explosion Sound Effect : https://pixabay.com/sound-effects/search/boom/

Other Sound Effect : MyEdit

# Video

[![Watch Video](https://img.youtube.com/vi/mKqw35v4tzM/0.jpg)](https://www.youtube.com/watch?v=mKqw35v4tzM)

Click Image to watch

# About Author

This game is made by LukeTseng, a high school stduent. Although there are still some flaws in the code, please forgive me :) 

The original intention of making this game is to realize my dream, a game developer

# About The Game

This game is still undergoing modifications. You can use the code of this game and modify it, I don't mind.

Made by LukeTseng ( 鼓山高中 _ 電腦社社長 ).
