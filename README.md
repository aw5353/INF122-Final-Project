# INF122 Final Project  

## Prerequisites  
To run this game, you need to have the latest version of Python installed on your system. You can download and install Python from the [official website](https://www.python.org/downloads/).  

## Running the Game  
1. Ensure you have Python installed. You can check your version by running:  
   ```sh
   python --version
   ```  
   or  
   ```sh
   python3 --version
   ```  
   The game requires the latest version of Python.  

2. Navigate to the root directory of the project.  

3. Run the following command to start the game:  
   ```sh
   python main.py
   ```  
   or  
   ```sh
   python3 main.py
   ```  

Enjoy the game! 🎮  

## Columns
Columns is a two-player tile-matching game where users take turns dropping gems onto the board to compete for the highest score. Player 1 can control their gem via the arrow keys (↑ ↓ → ←). Player 2 can control their gem via the WASD keys. The objective is to match at least 3 of the same colored gems together, which in turn causes them to disappear and add to the player's score. Gems spawn in vertical groups of three. Players can move the column of gems horizontally via → ← or AD. Players can rotate the column of gems using W or ↑, rotating the gems upwards. The players can also force-drop their column of gems using ↓ or S respectively to drop the column to the lowest available level. The game ends when it is unable to spawn anymore columns of gems into the board, at which point the game prompts the user with their statistics for that round, and a option as to whether or not they would like to play again.
