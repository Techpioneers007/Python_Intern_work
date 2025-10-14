"""
Mini Quiz Application - Enhanced Version
An interactive quiz game with features:
- Multiple categories (Science, History, Technology, etc.)
- Difficulty levels (Easy, Medium, Hard)
- Question randomization
- Timer (optional)
- Score history and statistics
- Lifelines (50/50, skip)
"""

import json
import os
import random
import time
from typing import Optional
from dataclasses import dataclass, field


@dataclass
class Question:
    """Represents a quiz question."""
    question: str
    options: list[str]
    answer: str
    category: str
    difficulty: str
    explanation: str = ""


@dataclass
class QuizStats:
    """Tracks quiz statistics."""
    total_quizzes: int = 0
    total_questions: int = 0
    correct_answers: int = 0
    best_score: int = 0
    best_percentage: float = 0.0
    category_stats: dict = field(default_factory=dict)
    
    def update(self, score: int, total: int, category: str) -> None:
        """Update statistics after a quiz."""
        self.total_quizzes += 1
        self.total_questions += total
        self.correct_answers += score
        
        percentage = (score / total * 100) if total > 0 else 0
        if percentage > self.best_percentage:
            self.best_percentage = percentage
            self.best_score = score
        
        # Update category stats
        if category not in self.category_stats:
            self.category_stats[category] = {"played": 0, "correct": 0, "total": 0}
        
        self.category_stats[category]["played"] += 1
        self.category_stats[category]["correct"] += score
        self.category_stats[category]["total"] += total
    
    @property
    def overall_accuracy(self) -> float:
        """Calculate overall accuracy percentage."""
        return (self.correct_answers / self.total_questions * 100) if self.total_questions > 0 else 0.0


class QuizGame:
    """Main quiz game class."""
    
    def __init__(self):
        """Initialize the quiz game."""
        self.questions_db = self._load_questions()
        self.stats = self._load_stats()
        self.current_score = 0
        self.lifelines = {"50_50": 1, "skip": 1}
    
    def _load_questions(self) -> dict[str, list[Question]]:
        """Load questions from the database."""
        questions = {
            "Science": [
                Question(
                    "What is the chemical symbol for water?",
                    ["A. H2O", "B. CO2", "C. O2", "D. H2SO4"],
                    "A", "Science", "Easy",
                    "Water is composed of two hydrogen atoms and one oxygen atom (H2O)."
                ),
                Question(
                    "Which planet is known as the Red Planet?",
                    ["A. Earth", "B. Mars", "C. Jupiter", "D. Venus"],
                    "B", "Science", "Easy",
                    "Mars appears red due to iron oxide (rust) on its surface."
                ),
                Question(
                    "What is the speed of light?",
                    ["A. 300,000 km/s", "B. 150,000 km/s", "C. 450,000 km/s", "D. 600,000 km/s"],
                    "A", "Science", "Medium",
                    "Light travels at approximately 299,792 km/s in a vacuum."
                ),
                Question(
                    "What is the powerhouse of the cell?",
                    ["A. Nucleus", "B. Mitochondria", "C. Ribosome", "D. Chloroplast"],
                    "B", "Science", "Easy",
                    "Mitochondria generate ATP, the cell's energy currency."
                ),
                Question(
                    "What is the atomic number of Carbon?",
                    ["A. 6", "B. 12", "C. 14", "D. 8"],
                    "A", "Science", "Medium",
                    "Carbon has 6 protons, giving it an atomic number of 6."
                ),
            ],
            "Technology": [
                Question(
                    "Which language is primarily used for Data Science?",
                    ["A. Java", "B. C++", "C. Python", "D. HTML"],
                    "C", "Technology", "Easy",
                    "Python's libraries like pandas, NumPy, and scikit-learn make it ideal for data science."
                ),
                Question(
                    "What does CPU stand for?",
                    ["A. Central Process Unit", "B. Computer Processing Unit", 
                     "C. Central Processing Unit", "D. Control Processing Unit"],
                    "C", "Technology", "Easy",
                    "CPU is the Central Processing Unit, the brain of the computer."
                ),
                Question(
                    "Who is known as the father of computers?",
                    ["A. Charles Babbage", "B. Alan Turing", "C. Bill Gates", "D. Steve Jobs"],
                    "A", "Technology", "Medium",
                    "Charles Babbage designed the first mechanical computer, the Analytical Engine."
                ),
                Question(
                    "What does HTTP stand for?",
                    ["A. HyperText Transfer Protocol", "B. High Transfer Text Protocol",
                     "C. HyperText Transmission Protocol", "D. High Text Transfer Protocol"],
                    "A", "Technology", "Medium",
                    "HTTP is the protocol used for transmitting web pages on the internet."
                ),
                Question(
                    "Which company developed the Java programming language?",
                    ["A. Microsoft", "B. Sun Microsystems", "C. Apple", "D. IBM"],
                    "B", "Technology", "Hard",
                    "Java was developed by Sun Microsystems in 1995, now owned by Oracle."
                ),
            ],
            "Geography": [
                Question(
                    "What is the capital of India?",
                    ["A. Mumbai", "B. Delhi", "C. Kolkata", "D. Chennai"],
                    "B", "Geography", "Easy",
                    "New Delhi is the capital of India."
                ),
                Question(
                    "Which is the largest ocean?",
                    ["A. Atlantic", "B. Indian", "C. Pacific", "D. Arctic"],
                    "C", "Geography", "Easy",
                    "The Pacific Ocean covers about 46% of Earth's water surface."
                ),
                Question(
                    "What is the longest river in the world?",
                    ["A. Amazon", "B. Nile", "C. Yangtze", "D. Mississippi"],
                    "B", "Geography", "Medium",
                    "The Nile River in Africa is approximately 6,650 km long."
                ),
                Question(
                    "Which country has the most time zones?",
                    ["A. USA", "B. Russia", "C. France", "D. China"],
                    "C", "Geography", "Hard",
                    "France has 12 time zones due to its overseas territories."
                ),
                Question(
                    "What is the smallest country in the world?",
                    ["A. Monaco", "B. Vatican City", "C. Liechtenstein", "D. San Marino"],
                    "B", "Geography", "Easy",
                    "Vatican City is about 0.44 square kilometers."
                ),
            ],
            "History": [
                Question(
                    "Who was the first President of the United States?",
                    ["A. Thomas Jefferson", "B. George Washington", 
                     "C. Abraham Lincoln", "D. John Adams"],
                    "B", "History", "Easy",
                    "George Washington served as president from 1789 to 1797."
                ),
                Question(
                    "In which year did World War II end?",
                    ["A. 1943", "B. 1944", "C. 1945", "D. 1946"],
                    "C", "History", "Medium",
                    "World War II ended in 1945 with Japan's surrender."
                ),
                Question(
                    "Who wrote the Declaration of Independence?",
                    ["A. George Washington", "B. Thomas Jefferson", 
                     "C. Benjamin Franklin", "D. John Adams"],
                    "B", "History", "Medium",
                    "Thomas Jefferson was the primary author of the Declaration of Independence."
                ),
                Question(
                    "Which ancient wonder is still standing?",
                    ["A. Hanging Gardens", "B. Colossus of Rhodes", 
                     "C. Great Pyramid of Giza", "D. Lighthouse of Alexandria"],
                    "C", "History", "Medium",
                    "The Great Pyramid of Giza is the only ancient wonder still in existence."
                ),
                Question(
                    "Who discovered America?",
                    ["A. Christopher Columbus", "B. Amerigo Vespucci", 
                     "C. Leif Erikson", "D. Ferdinand Magellan"],
                    "A", "History", "Easy",
                    "Christopher Columbus reached the Americas in 1492."
                ),
            ]
        }
        return questions
    
    def _load_stats(self) -> QuizStats:
        """Load quiz statistics from file."""
        stats_file = "quiz_stats.json"
        if os.path.exists(stats_file):
            try:
                with open(stats_file, 'r') as f:
                    data = json.load(f)
                    stats = QuizStats(**data)
                    return stats
            except Exception:
                pass
        return QuizStats()
    
    def _save_stats(self) -> None:
        """Save quiz statistics to file."""
        try:
            with open("quiz_stats.json", 'w') as f:
                json.dump({
                    "total_quizzes": self.stats.total_quizzes,
                    "total_questions": self.stats.total_questions,
                    "correct_answers": self.stats.correct_answers,
                    "best_score": self.stats.best_score,
                    "best_percentage": self.stats.best_percentage,
                    "category_stats": self.stats.category_stats
                }, f, indent=2)
        except Exception as e:
            print(f"⚠️  Could not save stats: {e}")
    
    def display_welcome(self) -> None:
        """Display welcome screen."""
        print("\n" + "="*60)
        print("🧠 MINI QUIZ GAME 🧠".center(60))
        print("="*60)
        print("Test your knowledge across multiple categories!")
        print("="*60)
    
    def select_category(self) -> str:
        """Let player select a quiz category."""
        categories = list(self.questions_db.keys())
        
        print("\n📚 Available Categories:")
        for i, cat in enumerate(categories, 1):
            q_count = len(self.questions_db[cat])
            print(f"  {i}. {cat} ({q_count} questions)")
        print(f"  {len(categories) + 1}. Random Mix")
        
        while True:
            try:
                choice = int(input(f"\nSelect category (1-{len(categories) + 1}): "))
                if 1 <= choice <= len(categories):
                    return categories[choice - 1]
                elif choice == len(categories) + 1:
                    return "Mixed"
                else:
                    print("❌ Invalid choice.")
            except ValueError:
                print("❌ Please enter a number.")
    
    def select_difficulty(self) -> Optional[str]:
        """Let player select difficulty level."""
        print("\n⚡ Select Difficulty:")
        print("  1. Easy")
        print("  2. Medium")
        print("  3. Hard")
        print("  4. All Levels")
        
        choice = input("\nEnter choice (1-4) [default: 4]: ").strip() or "4"
        
        difficulty_map = {"1": "Easy", "2": "Medium", "3": "Hard", "4": None}
        return difficulty_map.get(choice, None)
    
    def get_questions(self, category: str, difficulty: Optional[str], count: int = 5) -> list[Question]:
        """Get random questions based on selection."""
        if category == "Mixed":
            all_questions = []
            for questions in self.questions_db.values():
                all_questions.extend(questions)
        else:
            all_questions = self.questions_db[category]
        
        # Filter by difficulty if specified
        if difficulty:
            all_questions = [q for q in all_questions if q.difficulty == difficulty]
        
        # Randomize and select
        random.shuffle(all_questions)
        return all_questions[:min(count, len(all_questions))]
    
    def use_fifty_fifty(self, question: Question) -> list[str]:
        """Use 50/50 lifeline to remove two wrong answers."""
        if self.lifelines["50_50"] <= 0:
            print("❌ No 50/50 lifelines remaining!")
            return question.options
        
        self.lifelines["50_50"] -= 1
        correct_answer = question.answer
        correct_option = [opt for opt in question.options if opt.startswith(correct_answer)][0]
        
        # Keep correct answer and one random wrong answer
        wrong_options = [opt for opt in question.options if not opt.startswith(correct_answer)]
        remaining_wrong = random.choice(wrong_options)
        
        return [correct_option, remaining_wrong]
    
    def ask_question(self, question: Question, q_num: int, total: int, timed: bool = False) -> bool:
        """Ask a single question and return if answered correctly."""
        print("\n" + "="*60)
        print(f"Question {q_num}/{total}".center(60))
        print("="*60)
        print(f"Category: {question.category} | Difficulty: {question.difficulty}")
        print("-"*60)
        print(f"\n{question.question}\n")
        
        options = question.options.copy()
        
        # Display options
        for option in options:
            print(f"  {option}")
        
        print(f"\n💡 Lifelines: 50/50 ({self.lifelines['50_50']}) | Skip ({self.lifelines['skip']})")
        
        start_time = time.time()
        
        while True:
            user_input = input("\nYour answer (A/B/C/D) or use lifeline (type '50' or 'skip'): ").strip().upper()
            
            if user_input == "50":
                options = self.use_fifty_fifty(question)
                print("\n🎯 50/50 used! Remaining options:")
                for option in options:
                    print(f"  {option}")
                continue
            elif user_input == "SKIP":
                if self.lifelines["skip"] > 0:
                    self.lifelines["skip"] -= 1
                    print("⏭️  Question skipped!")
                    return False
                else:
                    print("❌ No skip lifelines remaining!")
                    continue
            elif user_input in ['A', 'B', 'C', 'D']:
                break
            else:
                print("❌ Invalid input. Enter A, B, C, D, '50', or 'skip'.")
        
        elapsed = time.time() - start_time
        
        if user_input == question.answer:
            print("\n✅ Correct!")
            if question.explanation:
                print(f"💡 {question.explanation}")
            if timed:
                print(f"⏱️  Time taken: {elapsed:.1f} seconds")
            return True
        else:
            print(f"\n❌ Wrong! The correct answer was {question.answer}.")
            if question.explanation:
                print(f"💡 {question.explanation}")
            return False
    
    def run_quiz(self) -> None:
        """Run a quiz session."""
        category = self.select_category()
        difficulty = self.select_difficulty()
        
        # Ask if timed
        timed = input("\n⏱️  Enable timer? (y/n) [default: n]: ").strip().lower() == 'y'
        
        # Ask number of questions
        try:
            num_questions = int(input("How many questions? (1-20) [default: 5]: ") or "5")
            num_questions = max(1, min(20, num_questions))
        except ValueError:
            num_questions = 5
        
        questions = self.get_questions(category, difficulty, num_questions)
        
        if not questions:
            print("\n⚠️  No questions available for selected criteria.")
            return
        
        print(f"\n🎮 Starting quiz: {len(questions)} questions")
        input("Press Enter to begin...")
        
        self.current_score = 0
        self.lifelines = {"50_50": 1, "skip": 1}
        
        for i, question in enumerate(questions, 1):
            if self.ask_question(question, i, len(questions), timed):
                self.current_score += 1
        
        # Display results
        self.display_results(len(questions), category)
    
    def display_results(self, total: int, category: str) -> None:
        """Display quiz results."""
        percentage = (self.current_score / total * 100) if total > 0 else 0
        
        print("\n" + "🎉"*20)
        print("QUIZ COMPLETED!".center(60))
        print("🎉"*20)
        print(f"\n🎯 Final Score: {self.current_score}/{total} ({percentage:.1f}%)")
        
        # Performance message
        if percentage == 100:
            print("🏆 PERFECT! You're a genius! 🌟")
        elif percentage >= 80:
            print("🌟 EXCELLENT! Great job! 👏")
        elif percentage >= 60:
            print("👍 GOOD! Well done! 📚")
        elif percentage >= 40:
            print("📖 NOT BAD! Keep practicing! 💪")
        else:
            print("📚 Keep learning! You'll improve! 🎯")
        
        print("🎉"*20)
        
        # Update stats
        self.stats.update(self.current_score, total, category)
        self._save_stats()
    
    def display_statistics(self) -> None:
        """Display player statistics."""
        if self.stats.total_quizzes == 0:
            print("\n⚠️  No quiz history yet. Play a quiz first!")
            return
        
        print("\n" + "="*60)
        print("📊 YOUR STATISTICS".center(60))
        print("="*60)
        print(f"Total Quizzes Played  : {self.stats.total_quizzes}")
        print(f"Total Questions       : {self.stats.total_questions}")
        print(f"Correct Answers       : {self.stats.correct_answers}")
        print(f"Overall Accuracy      : {self.stats.overall_accuracy:.1f}%")
        print(f"Best Score            : {self.stats.best_score} ({self.stats.best_percentage:.1f}%)")
        
        if self.stats.category_stats:
            print("\n📚 Category Performance:")
            for cat, data in sorted(self.stats.category_stats.items()):
                accuracy = (data["correct"] / data["total"] * 100) if data["total"] > 0 else 0
                print(f"  {cat:15} : {data['played']:2} quiz(es), {accuracy:5.1f}% accuracy")
        
        print("="*60)
    
    def menu(self) -> None:
        """Display main menu."""
        self.display_welcome()
        
        while True:
            print("\n" + "="*60)
            print("MAIN MENU".center(60))
            print("="*60)
            print("1. Start Quiz")
            print("2. View Statistics")
            print("3. Exit")
            print("="*60)
            
            choice = input("Enter your choice (1-3): ").strip()
            
            try:
                if choice == '1':
                    self.run_quiz()
                elif choice == '2':
                    self.display_statistics()
                elif choice == '3':
                    print("\n👋 Thanks for playing! Keep learning! 📚")
                    break
                else:
                    print("❌ Invalid choice. Please select 1-3.")
            except KeyboardInterrupt:
                print("\n\n⚠️  Quiz interrupted. Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ An error occurred: {e}")


def main() -> None:
    """Entry point for the quiz game."""
    game = QuizGame()
    game.menu()


if __name__ == "__main__":
    main()