class Student:
    def __init__(self, name: str, marks: list[float]):
        """Initialize student with name and marks for 3 subjects."""
        self.name = name
        self.marks = marks
        self.total = 0.0
        self.average = 0.0

    def calculate_total_and_average(self):
        """Compute total and average marks."""
        self.total = sum(self.marks)
        self.average = self.total / len(self.marks)

    def get_report(self) -> str:
        """Return formatted student report."""
        return (
            f"Name     : {self.name}\n"
            f"Marks    : {self.marks}\n"
            f"Total    : {self.total:.2f}\n"
            f"Average  : {self.average:.2f}\n"
            f"{'-'*30}"
        )


class ReportGenerator:
    def __init__(self):
        self.students = []

    def input_student_data(self):
        """Collect student data from user."""
        try:
            num_students = int(input("Enter number of students: "))
            for i in range(num_students):
                print(f"\n--- Student {i+1} ---")
                name = input("Enter student name: ").strip()
                marks = []
                for j in range(3):
                    while True:
                        try:
                            mark = float(input(f"Enter marks for Subject {j+1}: "))
                            if 0 <= mark <= 100:
                                marks.append(mark)
                                break
                            else:
                                print("Marks must be between 0 and 100.")
                        except ValueError:
                            print("Invalid input. Please enter a number.")
                student = Student(name, marks)
                student.calculate_total_and_average()
                self.students.append(student)
        except ValueError:
            print("Invalid number of students.")

    def display_all_reports(self):
        """Display reports for all students."""
        print("\n=== Student Reports ===")
        for student in self.students:
            print(student.get_report())


def main():
    generator = ReportGenerator()
    generator.input_student_data()
    generator.display_all_reports()


if __name__ == "__main__":
    main()