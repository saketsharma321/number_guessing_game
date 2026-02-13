import random
import time

# ------------------------------
# Utility Functions
# ------------------------------

def generate_number(level_type):
    numbers = list(range(0, 101))

    if level_type == "easy":
        numbers = [n for n in numbers if n % 5 == 0]

    elif level_type == "medium":
        numbers = [n for n in numbers if n % 2 == 0]

    elif level_type == "hard":
        numbers = [n for n in numbers if n % 5 != 0]

    return random.choice(numbers)


def get_level_type():
    while True:
        level = input("Choose difficulty (easy / medium / hard): ").lower()
        if level in ["easy", "medium", "hard"]:
            return level
        else:
            print("Invalid choice. Try again.")


def lose_message():
    messages = [
        "f**k off u brat 😈",
        "you loser 😆",
        "little punk 🤡",
        "u are a loser 💀",
        "try again 😤"
    ]
    print(random.choice(messages))


# ------------------------------
# Single Player - Practice Mode
# ------------------------------

def practice_mode(level_type):
    print("\n--- Practice Mode Started ---")

    while True:
        number = generate_number(level_type)

        print("\nHint: Number is", "above 50" if number > 50 else "50 or below")

        while True:
            guess = int(input("Enter your guess: "))

            if guess == number:
                print("Correct! 🎉 Starting new round...")
                break
            elif guess < number:
                print("Higher ⬆")
            else:
                print("Lower ⬇")


# ------------------------------
# Single Player - Level Mode
# ------------------------------

def level_mode(level_type):
    print("\n--- Level Mode (1 to 10) ---")

    previous_attempts = None

    for level in range(1, 11):
        print(f"\nLEVEL {level}")
        number = generate_number(level_type)

        print("Hint: Number is", "above 50" if number > 50 else "50 or below")

        attempts = 0

        if previous_attempts:
            print(f"You must finish this level in LESS than {previous_attempts} attempts!")

        while True:
            guess = int(input("Enter your guess: "))
            attempts += 1

            if guess == number:
                print(f"Level {level} cleared in {attempts} attempts! ✅")
                if previous_attempts and attempts >= previous_attempts:
                    lose_message()
                    return
                previous_attempts = attempts
                break

            elif guess < number:
                print("Higher ⬆")
            else:
                print("Lower ⬇")

    print("\n🔥 You have made it to the end champ 🔥")


# ------------------------------
# Multiplayer Mode
# ------------------------------

def multiplayer_mode():
    level_type = get_level_type()

    while True:
        num_players = int(input("How many players (1-5): "))
        if 1 <= num_players <= 5:
            break
        print("Invalid number of players.")

    players = []
    for i in range(num_players):
        name = input(f"Enter name of player {i+1}: ")
        players.append(name)

    results = {}

    for player in players:
        print(f"\n--- {player}'s Turn ---")
        start_time = time.time()

        for level in range(1, 11):
            print(f"\nLEVEL {level}")
            number = generate_number(level_type)

            print("Hint: Number is", "above 50" if number > 50 else "50 or below")

            while True:
                guess = int(input("Enter your guess: "))

                if guess == number:
                    print("Correct! ✅")
                    break
                elif guess < number:
                    print("Higher ⬆")
                else:
                    print("Lower ⬇")

        end_time = time.time()
        total_time = end_time - start_time
        results[player] = total_time

        print(f"{player} finished in {round(total_time, 2)} seconds ⏱")

    winner = min(results, key=results.get)

    print("\n🏆 FINAL RESULTS 🏆")
    for player, t in results.items():
        print(f"{player}: {round(t,2)} seconds")

    print(f"\n🔥 Winner is {winner} 🔥")


# ------------------------------
# Main Game Controller
# ------------------------------

def main():
    print("🎮 WELCOME TO ADVANCED NUMBER GUESSING GAME 🎮")

    while True:
        mode = input("Single or Multiplayer? ").lower()

        if mode == "single":
            level_type = get_level_type()

            game_type = input("Play level game or practice? ").lower()

            if game_type == "practice":
                practice_mode(level_type)
            elif game_type == "level":
                level_mode(level_type)
            else:
                print("Invalid option.")

        elif mode == "multiplayer":
            multiplayer_mode()
        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()
