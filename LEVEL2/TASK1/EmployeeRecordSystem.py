class Employee:
    def __init__(self, emp_id: str, name: str, department: str, salary: float):
        """Initialize employee details."""
        self.emp_id = emp_id
        self.name = name
        self.department = department
        self.salary = salary

    def display(self):
        """Display employee details."""
        print(f"\nEmployee ID   : {self.emp_id}")
        print(f"Name          : {self.name}")
        print(f"Department    : {self.department}")
        print(f"Salary        : ₹{self.salary:.2f}")
        print("-" * 30)


class EmployeeRecordSystem:
    def __init__(self):
        self.employees = []

    def add_employee(self):
        """Add a new employee."""
        print("\n--- Add New Employee ---")
        emp_id = input("Enter Employee ID: ").strip()
        name = input("Enter Name: ").strip()
        department = input("Enter Department: ").strip()
        while True:
            try:
                salary = float(input("Enter Salary (₹): "))
                break
            except ValueError:
                print("Invalid input. Please enter a numeric value for salary.")
        emp = Employee(emp_id, name, department, salary)
        self.employees.append(emp)
        print("✅ Employee added successfully!")

    def display_all_employees(self):
        """Display all employee records."""
        if not self.employees:
            print("\n⚠️ No employee records found.")
        else:
            print("\n=== Employee Records ===")
            for emp in self.employees:
                emp.display()


def main():
    system = EmployeeRecordSystem()
    while True:
        print("\n📋 Employee Record System")
        print("1. Add Employee")
        print("2. Display All Employees")
        print("3. Exit")
        choice = input("Enter your choice (1/2/3): ").strip()

        if choice == '1':
            system.add_employee()
        elif choice == '2':
            system.display_all_employees()
        elif choice == '3':
            print("👋 Exiting Employee Record System. Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please select 1, 2, or 3.")

if __name__ == "__main__":
    main()