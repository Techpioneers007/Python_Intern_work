"""
Student Report Generator - Enhanced Version
A comprehensive student management system with features:
- Multi-subject grade tracking
- Automatic grade calculation and grading
- Data persistence (JSON)
- Search and filter functionality
- Detailed statistical reports
"""

import json
import os
from typing import Optional
from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class Student:
    """Represents a student with their academic information."""
    student_id: str
    name: str
    marks: dict[str, float]  # Subject: Mark
    
    def __post_init__(self):
        """Calculate computed fields after initialization."""
        self._total: Optional[float] = None
        self._average: Optional[float] = None
        self._grade: Optional[str] = None
    
    @property
    def total(self) -> float:
        """Calculate total marks across all subjects."""
        if self._total is None:
            self._total = sum(self.marks.values())
        return self._total
    
    @property
    def average(self) -> float:
        """Calculate average marks."""
        if self._average is None:
            self._average = self.total / len(self.marks) if self.marks else 0.0
        return self._average
    
    @property
    def grade(self) -> str:
        """Determine letter grade based on average."""
        if self._grade is None:
            avg = self.average
            if avg >= 90:
                self._grade = 'A+'
            elif avg >= 80:
                self._grade = 'A'
            elif avg >= 70:
                self._grade = 'B'
            elif avg >= 60:
                self._grade = 'C'
            elif avg >= 50:
                self._grade = 'D'
            else:
                self._grade = 'F'
        return self._grade
    
    @property
    def status(self) -> str:
        """Determine pass/fail status."""
        return "PASS ✅" if self.grade != 'F' and all(m >= 40 for m in self.marks.values()) else "FAIL ❌"
    
    def get_report(self) -> str:
        """Return formatted student report."""
        subjects_str = "\n".join([f"  {subj:12} : {mark:6.2f}" for subj, mark in self.marks.items()])
        
        return (
            f"\n{'='*50}\n"
            f"Student ID : {self.student_id}\n"
            f"Name       : {self.name}\n"
            f"{'-'*50}\n"
            f"Subjects & Marks:\n{subjects_str}\n"
            f"{'-'*50}\n"
            f"Total      : {self.total:6.2f}\n"
            f"Average    : {self.average:6.2f}\n"
            f"Grade      : {self.grade}\n"
            f"Status     : {self.status}\n"
            f"{'='*50}"
        )


class ReportGenerator:
    """Main class for managing student records and generating reports."""
    
    def __init__(self, data_file: str = "students_data.json"):
        """Initialize the report generator with optional data file."""
        self.students: dict[str, Student] = {}
        self.data_file = data_file
        self.subjects = ["Math", "Science", "English"]  # Default subjects
        self.load_data()
    
    def load_data(self) -> None:
        """Load student data from JSON file."""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                    for student_data in data:
                        student = Student(
                            student_id=student_data['student_id'],
                            name=student_data['name'],
                            marks=student_data['marks']
                        )
                        self.students[student.student_id] = student
                print(f"✅ Loaded {len(self.students)} student record(s) from {self.data_file}")
            except Exception as e:
                print(f"⚠️  Error loading data: {e}")
        else:
            print(f"📝 No existing data file found. Starting fresh.")
    
    def save_data(self) -> None:
        """Save student data to JSON file."""
        try:
            data = []
            for student in self.students.values():
                data.append({
                    'student_id': student.student_id,
                    'name': student.name,
                    'marks': student.marks
                })
            with open(self.data_file, 'w') as f:
                json.dump(data, f, indent=2)
            print(f"💾 Data saved successfully to {self.data_file}")
        except Exception as e:
            print(f"❌ Error saving data: {e}")
    
    def configure_subjects(self) -> None:
        """Allow customization of subjects."""
        print("\n🎓 Configure Subjects")
        print(f"Current subjects: {', '.join(self.subjects)}")
        
        choice = input("Do you want to customize subjects? (y/n): ").strip().lower()
        if choice == 'y':
            num_subjects = int(input("How many subjects? "))
            self.subjects = []
            for i in range(num_subjects):
                subject = input(f"Enter subject {i+1} name: ").strip()
                self.subjects.append(subject)
            print(f"✅ Subjects set to: {', '.join(self.subjects)}")
    
    def generate_student_id(self) -> str:
        """Generate a unique student ID."""
        if not self.students:
            return "STU001"
        
        # Extract numbers from existing IDs and find max
        ids = [int(sid.replace("STU", "")) for sid in self.students.keys()]
        next_id = max(ids) + 1
        return f"STU{next_id:03d}"
    
    def add_student(self) -> None:
        """Add a new student with marks."""
        print("\n" + "="*50)
        print("➕ ADD NEW STUDENT")
        print("="*50)
        
        student_id = self.generate_student_id()
        print(f"Generated Student ID: {student_id}")
        
        name = input("Enter student name: ").strip()
        if not name:
            print("❌ Name cannot be empty.")
            return
        
        marks = {}
        print(f"\nEnter marks for {len(self.subjects)} subjects:")
        for subject in self.subjects:
            while True:
                try:
                    mark = float(input(f"  {subject}: "))
                    if 0 <= mark <= 100:
                        marks[subject] = mark
                        break
                    else:
                        print("    ⚠️  Marks must be between 0 and 100.")
                except ValueError:
                    print("    ❌ Invalid input. Please enter a number.")
        
        student = Student(student_id, name, marks)
        self.students[student_id] = student
        
        print(f"\n✅ Student {name} (ID: {student_id}) added successfully!")
        print(student.get_report())
    
    def search_student(self) -> Optional[Student]:
        """Search for a student by ID or name."""
        query = input("\n🔍 Enter Student ID or Name: ").strip().lower()
        
        # Search by ID
        for sid, student in self.students.items():
            if sid.lower() == query or student.name.lower() == query:
                return student
        
        # Partial name match
        matches = [s for s in self.students.values() if query in s.name.lower()]
        if matches:
            if len(matches) == 1:
                return matches[0]
            else:
                print(f"\n📋 Found {len(matches)} matching students:")
                for i, student in enumerate(matches, 1):
                    print(f"  {i}. {student.name} ({student.student_id})")
                
                choice = int(input("Select student number: ")) - 1
                if 0 <= choice < len(matches):
                    return matches[choice]
        
        print("❌ Student not found.")
        return None
    
    def display_student_report(self) -> None:
        """Display report for a specific student."""
        student = self.search_student()
        if student:
            print(student.get_report())
    
    def display_all_reports(self) -> None:
        """Display reports for all students."""
        if not self.students:
            print("\n⚠️  No student records found.")
            return
        
        print("\n" + "="*50)
        print("📊 ALL STUDENT REPORTS".center(50))
        print("="*50)
        
        for student in sorted(self.students.values(), key=lambda s: s.name):
            print(student.get_report())
    
    def display_class_statistics(self) -> None:
        """Display overall class statistics."""
        if not self.students:
            print("\n⚠️  No student records found.")
            return
        
        students = list(self.students.values())
        
        print("\n" + "="*60)
        print("📈 CLASS STATISTICS".center(60))
        print("="*60)
        print(f"Total Students    : {len(students)}")
        print(f"Pass Rate         : {sum(1 for s in students if 'PASS' in s.status) / len(students) * 100:.1f}%")
        print(f"Average Score     : {sum(s.average for s in students) / len(students):.2f}")
        print(f"Highest Average   : {max(students, key=lambda s: s.average).average:.2f} ({max(students, key=lambda s: s.average).name})")
        print(f"Lowest Average    : {min(students, key=lambda s: s.average).average:.2f} ({min(students, key=lambda s: s.average).name})")
        
        # Grade distribution
        print("\n📊 Grade Distribution:")
        grades = {}
        for student in students:
            grades[student.grade] = grades.get(student.grade, 0) + 1
        
        for grade in ['A+', 'A', 'B', 'C', 'D', 'F']:
            count = grades.get(grade, 0)
            percentage = count / len(students) * 100
            bar = '█' * int(percentage / 5)
            print(f"  {grade:3} : {bar:20} {count} ({percentage:.1f}%)")
        
        print("="*60)
    
    def filter_students(self) -> None:
        """Filter students by various criteria."""
        print("\n🔎 Filter Options:")
        print("  1. By Grade")
        print("  2. By Pass/Fail Status")
        print("  3. By Minimum Average")
        
        choice = input("\nSelect filter (1-3): ").strip()
        
        filtered = []
        
        if choice == '1':
            grade = input("Enter grade (A+, A, B, C, D, F): ").strip().upper()
            filtered = [s for s in self.students.values() if s.grade == grade]
        elif choice == '2':
            status = input("Enter status (pass/fail): ").strip().lower()
            filtered = [s for s in self.students.values() if status in s.status.lower()]
        elif choice == '3':
            min_avg = float(input("Enter minimum average: "))
            filtered = [s for s in self.students.values() if s.average >= min_avg]
        
        if filtered:
            print(f"\n✅ Found {len(filtered)} student(s):")
            for student in filtered:
                print(student.get_report())
        else:
            print("\n⚠️  No students match the criteria.")
    
    def menu(self) -> None:
        """Display main menu and handle user choices."""
        while True:
            print("\n" + "="*60)
            print("🎓 STUDENT REPORT GENERATOR".center(60))
            print("="*60)
            print("1. Configure Subjects")
            print("2. Add Student")
            print("3. Search & View Student Report")
            print("4. Display All Reports")
            print("5. Class Statistics")
            print("6. Filter Students")
            print("7. Save Data")
            print("8. Exit")
            print("="*60)
            
            choice = input("Enter your choice (1-8): ").strip()
            
            try:
                if choice == '1':
                    self.configure_subjects()
                elif choice == '2':
                    self.add_student()
                elif choice == '3':
                    self.display_student_report()
                elif choice == '4':
                    self.display_all_reports()
                elif choice == '5':
                    self.display_class_statistics()
                elif choice == '6':
                    self.filter_students()
                elif choice == '7':
                    self.save_data()
                elif choice == '8':
                    self.save_data()
                    print("\n👋 Thank you for using Student Report Generator!")
                    break
                else:
                    print("❌ Invalid choice. Please select 1-8.")
            except KeyboardInterrupt:
                print("\n\n⚠️  Interrupted. Saving data...")
                self.save_data()
                break
            except Exception as e:
                print(f"\n❌ An error occurred: {e}")


def main() -> None:
    """Entry point for the Student Report Generator."""
    generator = ReportGenerator()
    generator.menu()


if __name__ == "__main__":
    main()