import random
import time
import os

def clear_screen():
    """Clear the console screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    """Display game banner"""
    print("=" * 50)
    print("🎮  NUMBER GUESSING GAME  🎮".center(50))
    print("=" * 50)
    print()

def get_valid_input(prompt, valid_options):
    """Get valid input from user"""
    while True:
        choice = input(prompt).strip().lower()
        if choice in valid_options:
            return choice
        print(f"❌ Invalid input! Please choose from: {', '.join(valid_options)}")

def get_number_range(difficulty):
    """Get valid numbers based on difficulty"""
    if difficulty == 'easy':
        # Multiples of 5 between 0 and 101
        return [i for i in range(0, 101) if i % 5 == 0]
    elif difficulty == 'medium':
        # Multiples of 2 between 0 and 101
        return [i for i in range(0, 101) if i % 2 == 0]
    else:  # hard
        # All numbers except multiples of 5
        return [i for i in range(0, 101) if i % 5 != 0]

def get_losing_message():
    """Return a random losing message"""
    messages = [
        "F**k off u brat! 😤",
        "You loser! 🤦",
        "Little punk! 😏",
        "U are a loser! 💀",
        "Try again! 🔄"
    ]
    return random.choice(messages)

def give_hint(number, guess=None):
    """Give hints about the number"""
    if guess is None:
        # Initial hint
        if number > 50:
            return "🔼 The number is ABOVE 50"
        else:
            return "🔽 The number is BELOW or equal to 50"
    else:
        # Hint after guess
        if guess < number:
            return "⬆️  HIGHER! The number is greater than your guess."
        else:
            return "⬇️  LOWER! The number is less than your guess."

def play_single_level(difficulty, level, max_attempts=None):
    """Play a single level and return (success, attempts_used)"""
    valid_numbers = get_number_range(difficulty)
    target_number = random.choice(valid_numbers)
    
    print(f"\n{'='*50}")
    print(f"🎯 LEVEL {level}".center(50))
    print(f"{'='*50}")
    
    if max_attempts:
        print(f"⏱️  You have a MAXIMUM of {max_attempts} attempts!")
    else:
        print("⏱️  Unlimited attempts - Take your time!")
    
    print(give_hint(target_number))
    print()
    
    attempts = 0
    
    while True:
        if max_attempts and attempts >= max_attempts:
            print(f"\n❌ Out of attempts! The number was {target_number}")
            return False, attempts
        
        try:
            guess = int(input(f"Attempt {attempts + 1}: Enter your guess (0-100): "))
            
            if guess < 0 or guess > 100:
                print("⚠️  Please enter a number between 0 and 100!")
                continue
            
            attempts += 1
            
            if guess == target_number:
                print(f"\n🎉 CORRECT! You got it in {attempts} attempt(s)!")
                return True, attempts
            else:
                print(give_hint(target_number, guess))
                
        except ValueError:
            print("⚠️  Please enter a valid number!")

def play_practice_mode(difficulty):
    """Practice mode - single games with no progression"""
    print("\n🎮 PRACTICE MODE")
    print("Play as many rounds as you want!\n")
    
    while True:
        play_single_level(difficulty, level=1, max_attempts=None)
        
        play_again = get_valid_input("\nPlay another round? (yes/no): ", ['yes', 'y', 'no', 'n'])
        if play_again in ['no', 'n']:
            print("\n👋 Thanks for practicing!")
            break
        clear_screen()
        print_banner()

def play_level_mode(difficulty):
    """Level mode - 10 levels with attempt restrictions"""
    print("\n🏆 LEVEL MODE")
    print("Complete all 10 levels to win!")
    print("Each level must be completed in fewer attempts than the previous one!\n")
    
    input("Press Enter to start...")
    
    max_attempts = None
    
    for level in range(1, 11):
        clear_screen()
        print_banner()
        
        success, attempts = play_single_level(difficulty, level, max_attempts)
        
        if not success:
            print(f"\n💥 GAME OVER at Level {level}!")
            print(get_losing_message())
            return
        
        # Set max attempts for next level (must be less than current)
        max_attempts = attempts - 1
        
        if max_attempts < 1:
            print("\n😱 Wow! You beat it in 1 attempt!")
            print("Next level will also allow 1 attempt - good luck!")
            max_attempts = 1
        
        if level < 10:
            print(f"\n✅ Level {level} complete!")
            print(f"⚡ Next level: You must complete it in LESS than {attempts} attempts (max {max_attempts})!")
            input("\nPress Enter to continue to next level...")
    
    # Completed all 10 levels!
    clear_screen()
    print_banner()
    print("🏆" * 25)
    print("\n🎊 YOU HAVE MADE IT TO THE END CHAMP! 🎊\n")
    print("🏆" * 25)

def play_multiplayer_mode(difficulty):
    """Multiplayer mode - timed competition"""
    print("\n👥 MULTIPLAYER MODE")
    
    # Get number of players
    while True:
        try:
            num_players = int(input("How many players? (1-5): "))
            if 1 <= num_players <= 5:
                break
            print("❌ Please enter a number between 1 and 5!")
        except ValueError:
            print("❌ Please enter a valid number!")
    
    # Get player names
    players = []
    for i in range(num_players):
        name = input(f"Enter name for Player {i+1}: ").strip()
        if not name:
            name = f"Player {i+1}"
        players.append({"name": name, "time": 0})
    
    print("\n📋 RULES:")
    print("- Complete all 10 levels as fast as possible")
    print("- Unlimited attempts per level")
    print("- Fastest time wins!")
    input("\nPress Enter to start the competition...\n")
    
    # Each player plays
    for idx, player in enumerate(players):
        clear_screen()
        print_banner()
        print(f"🎮 {player['name']}'s Turn!")
        input("Press Enter when ready...")
        
        start_time = time.time()
        
        # Play all 10 levels
        completed = True
        for level in range(1, 11):
            clear_screen()
            print_banner()
            print(f"👤 Player: {player['name']}")
            
            success, _ = play_single_level(difficulty, level, max_attempts=None)
            
            if not success:  # This shouldn't happen with unlimited attempts, but just in case
                completed = False
                break
            
            if level < 10:
                input("\n✅ Press Enter for next level...")
        
        end_time = time.time()
        
        if completed:
            player['time'] = end_time - start_time
            clear_screen()
            print_banner()
            print(f"🎉 {player['name']} completed all levels!")
            print(f"⏱️  Time: {player['time']:.2f} seconds")
        else:
            player['time'] = float('inf')
            print(f"\n❌ {player['name']} did not complete all levels!")
        
        if idx < len(players) - 1:
            input("\nPress Enter for next player...")
    
    # Display results
    clear_screen()
    print_banner()
    print("🏆 FINAL RESULTS 🏆\n")
    
    # Sort by time
    completed_players = [p for p in players if p['time'] != float('inf')]
    completed_players.sort(key=lambda x: x['time'])
    
    if completed_players:
        print("✅ Players who completed all levels:\n")
        for idx, player in enumerate(completed_players):
            medal = "🥇" if idx == 0 else "🥈" if idx == 1 else "🥉" if idx == 2 else "  "
            print(f"{medal} {idx+1}. {player['name']}: {player['time']:.2f} seconds")
        
        print(f"\n🎊 WINNER: {completed_players[0]['name']}! 🎊")
    
    # Show players who didn't complete
    incomplete_players = [p for p in players if p['time'] == float('inf')]
    if incomplete_players:
        print("\n❌ Did not complete:")
        for player in incomplete_players:
            print(f"   - {player['name']}")

def main():
    """Main game loop"""
    while True:
        clear_screen()
        print_banner()
        
        # Choose game mode
        print("Choose game mode:")
        print("1. Single Player")
        print("2. Multiplayer")
        mode = get_valid_input("Enter choice (1/2): ", ['1', '2'])
        
        # Choose difficulty
        print("\nChoose difficulty:")
        print("1. Easy (Multiples of 5)")
        print("2. Medium (Multiples of 2)")
        print("3. Hard (No multiples of 5)")
        diff_choice = get_valid_input("Enter choice (1/2/3): ", ['1', '2', '3'])
        
        difficulty_map = {'1': 'easy', '2': 'medium', '3': 'hard'}
        difficulty = difficulty_map[diff_choice]
        
        if mode == '1':
            # Single player - choose level or practice
            print("\nChoose mode:")
            print("1. Level Mode (1-10 levels with attempt restrictions)")
            print("2. Practice Mode (Free play)")
            game_mode = get_valid_input("Enter choice (1/2): ", ['1', '2'])
            
            clear_screen()
            print_banner()
            
            if game_mode == '1':
                play_level_mode(difficulty)
            else:
                play_practice_mode(difficulty)
        else:
            # Multiplayer
            clear_screen()
            print_banner()
            play_multiplayer_mode(difficulty)
        
        # Play again?
        print("\n" + "="*50)
        play_again = get_valid_input("Play again? (yes/no): ", ['yes', 'y', 'no', 'n'])
        if play_again in ['no', 'n']:
            clear_screen()
            print_banner()
            print("👋 Thanks for playing! See you next time! 🎮\n")
            break

if __name__ == "__main__":
    main()
