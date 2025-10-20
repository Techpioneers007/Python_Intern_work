"""
Number Guessing Game - Enhanced Version
A fun interactive guessing game with multiple difficulty levels,
hints, statistics tracking, and replay functionality.
"""

import random
from dataclasses import dataclass
from typing import Optional


@dataclass
class DifficultyLevel:
    """Represents a difficulty level configuration."""
    name: str
    max_number: int
    max_attempts: int
    hint_threshold: int  # After how many attempts to give hints


@dataclass
class GameStats:
    """Tracks player statistics across games."""
    games_played: int = 0
    games_won: int = 0
    total_attempts: int = 0
    best_score: Optional[int] = None  # Fewest attempts to win
    
    def update_win(self, attempts: int) -> None:
        """Update stats after a win."""
        self.games_played += 1
        self.games_won += 1
        self.total_attempts += attempts
        
        if self.best_score is None or attempts < self.best_score:
            self.best_score = attempts
    
    def update_loss(self, attempts: int) -> None:
        """Update stats after a loss."""
        self.games_played += 1
        self.total_attempts += attempts
    
    @property
    def win_rate(self) -> float:
        """Calculate win rate percentage."""
        return (self.games_won / self.games_played * 100) if self.games_played > 0 else 0.0
    
    @property
    def avg_attempts(self) -> float:
        """Calculate average attempts per game."""
        return (self.total_attempts / self.games_played) if self.games_played > 0 else 0.0


class NumberGuessingGame:
    """Main game class handling all game logic."""
    
    DIFFICULTIES = {
        '1': DifficultyLevel("Easy", 50, 7, 4),
        '2': DifficultyLevel("Normal", 100, 6, 3),
        '3': DifficultyLevel("Hard", 200, 5, 2),
        '4': DifficultyLevel("Expert", 500, 4, 1),
    }
    
    def __init__(self):
        """Initialize the game with default stats."""
        self.stats = GameStats()
        self.secret_number: Optional[int] = None
        self.difficulty: Optional[DifficultyLevel] = None
    
    def display_welcome(self) -> None:
        """Display welcome message."""
        print("\n" + "="*60)
        print("🎮 NUMBER GUESSING GAME 🎮".center(60))
        print("="*60)
        print("Try to guess the secret number in as few attempts as possible!")
        print("="*60)
    
    def choose_difficulty(self) -> DifficultyLevel:
        """
        Let player choose difficulty level.
        
        Returns:
            Selected DifficultyLevel object
        """
        print("\n🎯 Select Difficulty Level:")
        for key, level in self.DIFFICULTIES.items():
            print(f"  {key}. {level.name:8} (1-{level.max_number:3}, {level.max_attempts} attempts)")
        
        while True:
            choice = input("\nEnter your choice (1-4) [default: 2]: ").strip() or '2'
            
            if choice in self.DIFFICULTIES:
                return self.DIFFICULTIES[choice]
            else:
                print("❌ Invalid choice. Please select 1, 2, 3, or 4.")
    
    def give_hint(self, guess: int, attempts: int) -> None:
        """
        Provide helpful hints based on how close the guess is.
        
        Args:
            guess: Player's guess
            attempts: Number of attempts so far
        """
        if attempts < self.difficulty.hint_threshold:
            return
        
        difference = abs(guess - self.secret_number)
        max_range = self.difficulty.max_number
        
        if difference <= max_range * 0.05:  # Within 5%
            print("💡 Hint: You're VERY close! 🔥")
        elif difference <= max_range * 0.10:  # Within 10%
            print("💡 Hint: You're getting warm! 🌡️")
        elif difference <= max_range * 0.25:  # Within 25%
            print("💡 Hint: You're in the right zone! 📍")
        else:
            print("💡 Hint: You're quite far... 🥶")
    
    def play_round(self) -> bool:
        """
        Play one round of the game.
        
        Returns:
            True if player won, False if lost
        """
        self.difficulty = self.choose_difficulty()
        self.secret_number = random.randint(1, self.difficulty.max_number)
        
        print(f"\n🎲 I've picked a number between 1 and {self.difficulty.max_number}.")
        print(f"🎯 You have {self.difficulty.max_attempts} attempts. Good luck!\n")
        
        attempts = 0
        
        while attempts < self.difficulty.max_attempts:
            try:
                guess = int(input(f"Attempt {attempts + 1}/{self.difficulty.max_attempts}: Enter your guess: "))
                
                # Validate range
                if guess < 1 or guess > self.difficulty.max_number:
                    print(f"⚠️  Please guess between 1 and {self.difficulty.max_number}.\n")
                    continue
                
                attempts += 1
                
                if guess < self.secret_number:
                    print("📉 Too Low!")
                    self.give_hint(guess, attempts)
                    print()
                elif guess > self.secret_number:
                    print("📈 Too High!")
                    self.give_hint(guess, attempts)
                    print()
                else:
                    self.display_victory(attempts)
                    self.stats.update_win(attempts)
                    return True
                    
            except ValueError:
                print("❌ Invalid input! Please enter a valid number.\n")
            except KeyboardInterrupt:
                print("\n\n⚠️  Game interrupted.")
                raise
        
        # Player lost
        self.display_defeat(attempts)
        self.stats.update_loss(attempts)
        return False
    
    def display_victory(self, attempts: int) -> None:
        """Display victory message with score evaluation."""
        print("\n" + "🎉"*20)
        print(f"🏆 CONGRATULATIONS! You guessed {self.secret_number} correctly!")
        print(f"✨ It took you {attempts} attempt(s)!")
        
        # Score evaluation
        if attempts == 1:
            print("🌟 INCREDIBLE! First try! Are you a mind reader? 🧠")
        elif attempts <= self.difficulty.max_attempts // 3:
            print("🌟 AMAZING! That was lightning fast! ⚡")
        elif attempts <= self.difficulty.max_attempts // 2:
            print("👍 GREAT JOB! Well done! 🎯")
        else:
            print("👏 Good effort! You made it! ✅")
        
        print("🎉"*20 + "\n")
    
    def display_defeat(self, attempts: int) -> None:
        """Display defeat message."""
        print("\n" + "😢"*20)
        print(f"💔 Sorry! You've used all {attempts} attempts.")
        print(f"🔢 The correct number was: {self.secret_number}")
        print("😢"*20 + "\n")
    
    def display_stats(self) -> None:
        """Display player statistics."""
        if self.stats.games_played == 0:
            return
        
        print("\n" + "="*60)
        print("📊 YOUR STATISTICS".center(60))
        print("="*60)
        print(f"Games Played     : {self.stats.games_played}")
        print(f"Games Won        : {self.stats.games_won}")
        print(f"Win Rate         : {self.stats.win_rate:.1f}%")
        print(f"Best Score       : {self.stats.best_score if self.stats.best_score else 'N/A'} attempts")
        print(f"Average Attempts : {self.stats.avg_attempts:.1f}")
        print("="*60)
    
    def play_again(self) -> bool:
        """
        Ask if player wants to play again.
        
        Returns:
            True to play again, False to quit
        """
        while True:
            choice = input("\n🔄 Play again? (y/n): ").strip().lower()
            if choice in ('y', 'yes'):
                return True
            elif choice in ('n', 'no'):
                return False
            else:
                print("Please enter 'y' or 'n'.")
    
    def run(self) -> None:
        """Main game loop."""
        self.display_welcome()
        
        try:
            while True:
                self.play_round()
                self.display_stats()
                
                if not self.play_again():
                    break
            
            print("\n" + "="*60)
            print("👋 Thanks for playing! Goodbye! 🎮".center(60))
            print("="*60 + "\n")
            
        except KeyboardInterrupt:
            print("\n\n⚠️  Game interrupted by user. Goodbye!")


def main() -> None:
    """Entry point for the number guessing game."""
    game = NumberGuessingGame()
    game.run()


if __name__ == "__main__":
    main()
