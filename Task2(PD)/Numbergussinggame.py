import random

def number_guessing_game():
    print("Welcome to the Number Guessing Game!")
    
    # Allow user to select difficulty level
    print("Select Difficulty Level:")
    print("1. Easy (1-50)")
    print("2. Normal (1-100)")
    print("3. Hard (1-200)")
    
    difficulty = input("Enter your choice (1/2/3): ")
    if difficulty == '1':
        max_number = 50
        max_attempts = 7
    elif difficulty == '3':
        max_number = 200
        max_attempts = 5
    else:
        max_number = 100
        max_attempts = 6

    # Randomly pick a number within the range
    secret_number = random.randint(1, max_number)
    print(f"\nI have picked a number between 1 and {max_number}. Can you guess it?")
    print(f"You have {max_attempts} attempts. Good luck!\n")

    # Start the guessing game
    attempts = 0
    while attempts < max_attempts:
        try:
            guess = int(input(f"Attempt {attempts + 1}/{max_attempts}: Enter your guess: "))
            attempts += 1

            if guess < 1 or guess > max_number:
                print(f"Please guess a number between 1 and {max_number}.\n")
                continue

            if guess < secret_number:
                print("Too Low!\n")
            elif guess > secret_number:
                print("Too High!\n")
            else:
                print(f"Congratulations! You guessed the number {secret_number} correctly in {attempts} attempts!")
                break
        except ValueError:
            print("Invalid input! Please enter a valid number.\n")
    
    # If user runs out of attempts
    if attempts == max_attempts and guess != secret_number:
        print(f"Sorry, you've used all your attempts. The correct number was {secret_number}. Better luck next time!")

# Run the game
number_guessing_game()
