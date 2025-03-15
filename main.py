import importlib
import os

def list_games():
    games = []
    games_dir = "games"
    if os.path.exists(games_dir) and os.path.isdir(games_dir):
        for folder in os.listdir(games_dir):
            folder_path = os.path.join(games_dir, folder)
            if os.path.isdir(folder_path) and os.path.exists(os.path.join(folder_path, "gui.py")):
                games.append(folder)
    return games

def run_game(game_name):
    try:
        game_module = importlib.import_module(f"games.{game_name}.gui")
        if hasattr(game_module, "Application"):
            print(f"Launching {game_name}...\n")
            app = game_module.Application()
            app.run()
        else:
            print(f"Error: {game_name} does not have an 'Application' class with a 'run' method.")
    except ModuleNotFoundError:
        print(f"Error: Game '{game_name}' not found.")

def main():
    while True:
        games = list_games()
        if not games:
            print("No games found in the 'games' folder.")
            break

        print("Available Games:")
        for idx, game in enumerate(games, 1):
            print(f"{idx}. {game}")

        choice = input("Enter the number of the game to play (or 'q' to quit): ")
        if choice.lower() == 'q':
            print("Exiting game launcher.")
            break
        
        if choice.isdigit():
            choice = int(choice)
            if 1 <= choice <= len(games):
                run_game(games[choice - 1])
            else:
                print("Invalid selection. Try again.")
        else:
            print("Invalid input. Try again.")

if __name__ == "__main__":
    main()
