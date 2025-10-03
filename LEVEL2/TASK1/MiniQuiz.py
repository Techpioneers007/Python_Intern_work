def run_quiz():
    questions = [
        {
            "question": "1. What is the capital of India?",
            "options": ["A. Mumbai", "B. Delhi", "C. Kolkata", "D. Chennai"],
            "answer": "B"
        },
        {
            "question": "2. Which language is used for Data Science?",
            "options": ["A. Java", "B. C++", "C. Python", "D. HTML"],
            "answer": "C"
        },
        {
            "question": "3. Who is known as the father of computers?",
            "options": ["A. Charles Babbage", "B. Alan Turing", "C. Bill Gates", "D. Steve Jobs"],
            "answer": "A"
        },
        {
            "question": "4. What does CPU stand for?",
            "options": ["A. Central Process Unit", "B. Computer Processing Unit", "C. Central Processing Unit", "D. Control Processing Unit"],
            "answer": "C"
        },
        {
            "question": "5. Which planet is known as the Red Planet?",
            "options": ["A. Earth", "B. Mars", "C. Jupiter", "D. Venus"],
            "answer": "B"
        }
    ]

    score = 0

    print("🧠 Welcome to the Quiz!\nChoose the correct option (A/B/C/D):\n")

    for q in questions:
        print(q["question"])
        for option in q["options"]:
            print(option)
        user_answer = input("Your answer: ").strip().upper()

        if user_answer == q["answer"]:
            print("✅ Correct!\n")
            score += 1
        else:
            print(f"❌ Wrong! The correct answer was {q['answer']}.\n")

    print(f"🎯 Final Score: {score} out of {len(questions)}")
    if score == len(questions):
        print("🏆 Excellent! You nailed it.")
    elif score >= 3:
        print("👍 Good job! Keep learning.")
    else:
        print("📚 Keep practicing. You'll get better!")

if __name__ == "__main__":
    run_quiz()