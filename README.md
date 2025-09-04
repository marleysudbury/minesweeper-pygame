# Minesweeper in Pygame

Originally written in MonkeyX for my A level project, now recreated in Python with the Pygame library.

![Screenshot of game](https://marleysudbury.github.io/minesweeper/screen_py.png)

## Improvements on the original

* The leaderboard actually works
* You can right click twice to put a question mark
* Cross platform (MonkeyX is supposed to be cross-platform, but it was always glitchy/broken on MacOS)

## Requires

* Python 3
* Pygame

## Installation

1. Ensure Python is installed onto your system.
2. Navigate to the directory where you want to install the game.
3. Clone the repository with `git clone https://github.com/marleysudbury/minesweeper-pygame` (if you don't have git, you can download the repository as a .zip).
4. Then go into the folder (`cd minesweeper-pygame`).
5. Create virtual environment (venv) with `python -m venv venv`.
6. Activate the venv with `source venv/bin/activate` on Linux and MacOS or `venv\Scripts\activate.bat` on Windows.
7. Install Pygame in the venv with `pip install pygame`.

## Running

Whilst in the venv, run the command `python game.py`.

If you wish to get straight into a game, you can run `python game.py -quick`, `python game.py -quick medium` or `python game.py -quick hard`. For touchscreen compatibility (WIP), try `python game.py -touch`.

When you are finished playing press the Escape key from the main menu to close the program.

## Other

* To see the page about my Minesweeper implementations on my website, click [here](https://marleysudbury.github.io/minesweeper).
* To see the code for the original MonkeyX version, click [here](https://github.com/marleysudbury/Minesweeper).
* To see a newer Minesweeper made in Godot, click [here](https://github.com/marleysudbury/minesweeper-godot).
* This version is not yet fully complete (see [issues](https://github.com/marleysudbury/minesweeper-pygame/issues)).
