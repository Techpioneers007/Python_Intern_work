"""
Employee Record System - Enhanced Version
A comprehensive employee management system with features:
- CRUD operations (Create, Read, Update, Delete)
- Data persistence (JSON)
- Search and filter functionality
- Salary statistics and analysis
- CSV export capability
- Department-wise reports
"""

import json
import csv
import os
from typing import Optional
from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class Employee:
    """Represents an employee with their details."""
    emp_id: str
    name: str
    department: str
    salary: float
    position: str = "Staff"
    hire_date: str = ""
    
    def __post_init__(self):
        """Set hire date if not provided."""
        if not self.hire_date:
            self.hire_date = datetime.now().strftime("%Y-%m-%d")
    
    def display(self) -> str:
        """Return formatted employee details."""
        return (
            f"\n{'='*50}\n"
            f"Employee ID   : {self.emp_id}\n"
            f"Name          : {self.name}\n"
            f"Position      : {self.position}\n"
            f"Department    : {self.department}\n"
            f"Salary        : ₹{self.salary:,.2f}\n"
            f"Hire Date     : {self.hire_date}\n"
            f"{'='*50}"
        )
    
    def to_dict(self) -> dict:
        """Convert employee to dictionary."""
        return asdict(self)


class EmployeeRecordSystem:
    """Main class for managing employee records."""
    
    def __init__(self, data_file: str = "employees_data.json"):
        """Initialize the employee record system."""
        self.employees: dict[str, Employee] = {}
        self.data_file = data_file
        self.load_data()
    
    def load_data(self) -> None:
        """Load employee data from JSON file."""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                    for emp_data in data:
                        emp = Employee(**emp_data)
                        self.employees[emp.emp_id] = emp
                print(f"✅ Loaded {len(self.employees)} employee record(s) from {self.data_file}")
            except Exception as e:
                print(f"⚠️  Error loading data: {e}")
        else:
            print(f"📝 No existing data file found. Starting fresh.")
    
    def save_data(self) -> None:
        """Save employee data to JSON file."""
        try:
            data = [emp.to_dict() for emp in self.employees.values()]
            with open(self.data_file, 'w') as f:
                json.dump(data, f, indent=2)
            print(f"💾 Data saved successfully to {self.data_file}")
        except Exception as e:
            print(f"❌ Error saving data: {e}")
    
    def generate_employee_id(self) -> str:
        """Generate a unique employee ID."""
        if not self.employees:
            return "EMP001"
        
        # Extract numbers from existing IDs and find max
        ids = [int(eid.replace("EMP", "")) for eid in self.employees.keys()]
        next_id = max(ids) + 1
        return f"EMP{next_id:03d}"
    
    def add_employee(self) -> None:
        """Add a new employee."""
        print("\n" + "="*50)
        print("➕ ADD NEW EMPLOYEE")
        print("="*50)
        
        emp_id = self.generate_employee_id()
        print(f"Generated Employee ID: {emp_id}")
        
        name = input("Enter Name: ").strip()
        if not name:
            print("❌ Name cannot be empty.")
            return
        
        position = input("Enter Position (e.g., Manager, Developer, Analyst): ").strip() or "Staff"
        department = input("Enter Department: ").strip()
        
        while True:
            try:
                salary = float(input("Enter Salary (₹): "))
                if salary < 0:
                    print("⚠️  Salary cannot be negative.")
                    continue
                break
            except ValueError:
                print("❌ Invalid input. Please enter a numeric value.")
        
        emp = Employee(emp_id, name, department, salary, position)
        self.employees[emp_id] = emp
        
        print(f"\n✅ Employee {name} (ID: {emp_id}) added successfully!")
        print(emp.display())
    
    def search_employee(self) -> Optional[Employee]:
        """Search for an employee by ID or name."""
        query = input("\n🔍 Enter Employee ID or Name: ").strip().lower()
        
        # Search by ID
        for eid, emp in self.employees.items():
            if eid.lower() == query or emp.name.lower() == query:
                return emp
        
        # Partial name match
        matches = [e for e in self.employees.values() if query in e.name.lower()]
        if matches:
            if len(matches) == 1:
                return matches[0]
            else:
                print(f"\n📋 Found {len(matches)} matching employees:")
                for i, emp in enumerate(matches, 1):
                    print(f"  {i}. {emp.name} ({emp.emp_id}) - {emp.department}")
                
                try:
                    choice = int(input("Select employee number: ")) - 1
                    if 0 <= choice < len(matches):
                        return matches[choice]
                except (ValueError, IndexError):
                    pass
        
        print("❌ Employee not found.")
        return None
    
    def update_employee(self) -> None:
        """Update an existing employee's information."""
        emp = self.search_employee()
        if not emp:
            return
        
        print(f"\n✏️  Updating Employee: {emp.name} ({emp.emp_id})")
        print("Leave blank to keep current value.\n")
        
        name = input(f"Name [{emp.name}]: ").strip() or emp.name
        position = input(f"Position [{emp.position}]: ").strip() or emp.position
        department = input(f"Department [{emp.department}]: ").strip() or emp.department
        
        salary_input = input(f"Salary [{emp.salary:.2f}]: ").strip()
        if salary_input:
            try:
                salary = float(salary_input)
            except ValueError:
                print("⚠️  Invalid salary. Keeping current value.")
                salary = emp.salary
        else:
            salary = emp.salary
        
        # Update employee
        emp.name = name
        emp.position = position
        emp.department = department
        emp.salary = salary
        
        print("\n✅ Employee updated successfully!")
        print(emp.display())
    
    def delete_employee(self) -> None:
        """Delete an employee from the system."""
        emp = self.search_employee()
        if not emp:
            return
        
        print(emp.display())
        confirm = input(f"\n⚠️  Are you sure you want to delete {emp.name}? (yes/no): ").strip().lower()
        
        if confirm in ('yes', 'y'):
            del self.employees[emp.emp_id]
            print(f"✅ Employee {emp.name} deleted successfully.")
        else:
            print("❌ Deletion cancelled.")
    
    def display_employee(self) -> None:
        """Display details of a specific employee."""
        emp = self.search_employee()
        if emp:
            print(emp.display())
    
    def display_all_employees(self) -> None:
        """Display all employee records."""
        if not self.employees:
            print("\n⚠️  No employee records found.")
            return
        
        print("\n" + "="*50)
        print("📋 ALL EMPLOYEE RECORDS".center(50))
        print("="*50)
        
        for emp in sorted(self.employees.values(), key=lambda e: e.name):
            print(emp.display())
    
    def display_by_department(self) -> None:
        """Display employees grouped by department."""
        if not self.employees:
            print("\n⚠️  No employee records found.")
            return
        
        # Group by department
        by_dept = {}
        for emp in self.employees.values():
            if emp.department not in by_dept:
                by_dept[emp.department] = []
            by_dept[emp.department].append(emp)
        
        print("\n" + "="*60)
        print("🏢 EMPLOYEES BY DEPARTMENT".center(60))
        print("="*60)
        
        for dept in sorted(by_dept.keys()):
            print(f"\n📂 {dept.upper()} ({len(by_dept[dept])} employees)")
            print("-" * 60)
            for emp in sorted(by_dept[dept], key=lambda e: e.name):
                print(f"  • {emp.name:20} | {emp.position:15} | ₹{emp.salary:,.2f}")
    
    def salary_statistics(self) -> None:
        """Display salary statistics."""
        if not self.employees:
            print("\n⚠️  No employee records found.")
            return
        
        employees = list(self.employees.values())
        salaries = [emp.salary for emp in employees]
        
        print("\n" + "="*60)
        print("💰 SALARY STATISTICS".center(60))
        print("="*60)
        print(f"Total Employees   : {len(employees)}")
        print(f"Average Salary    : ₹{sum(salaries) / len(salaries):,.2f}")
        print(f"Highest Salary    : ₹{max(salaries):,.2f} ({max(employees, key=lambda e: e.salary).name})")
        print(f"Lowest Salary     : ₹{min(salaries):,.2f} ({min(employees, key=lambda e: e.salary).name})")
        print(f"Total Payroll     : ₹{sum(salaries):,.2f}")
        
        # Salary ranges
        print("\n📊 Salary Distribution:")
        ranges = [
            (0, 30000, "Below 30K"),
            (30000, 50000, "30K - 50K"),
            (50000, 75000, "50K - 75K"),
            (75000, 100000, "75K - 100K"),
            (100000, float('inf'), "Above 100K")
        ]
        
        for low, high, label in ranges:
            count = sum(1 for s in salaries if low <= s < high)
            if count > 0:
                percentage = count / len(salaries) * 100
                bar = '█' * int(percentage / 5)
                print(f"  {label:15} : {bar:20} {count} ({percentage:.1f}%)")
        
        # Department-wise average
        by_dept = {}
        for emp in employees:
            if emp.department not in by_dept:
                by_dept[emp.department] = []
            by_dept[emp.department].append(emp.salary)
        
        print("\n💼 Average Salary by Department:")
        for dept in sorted(by_dept.keys()):
            avg = sum(by_dept[dept]) / len(by_dept[dept])
            print(f"  {dept:20} : ₹{avg:,.2f}")
        
        print("="*60)
    
    def filter_employees(self) -> None:
        """Filter employees by various criteria."""
        print("\n🔎 Filter Options:")
        print("  1. By Department")
        print("  2. By Salary Range")
        print("  3. By Position")
        
        choice = input("\nSelect filter (1-3): ").strip()
        
        filtered = []
        
        if choice == '1':
            dept = input("Enter Department: ").strip()
            filtered = [e for e in self.employees.values() if dept.lower() in e.department.lower()]
        elif choice == '2':
            try:
                min_sal = float(input("Enter minimum salary: "))
                max_sal = float(input("Enter maximum salary: "))
                filtered = [e for e in self.employees.values() if min_sal <= e.salary <= max_sal]
            except ValueError:
                print("❌ Invalid salary range.")
                return
        elif choice == '3':
            pos = input("Enter Position: ").strip()
            filtered = [e for e in self.employees.values() if pos.lower() in e.position.lower()]
        
        if filtered:
            print(f"\n✅ Found {len(filtered)} employee(s):")
            for emp in sorted(filtered, key=lambda e: e.name):
                print(emp.display())
        else:
            print("\n⚠️  No employees match the criteria.")
    
    def export_to_csv(self) -> None:
        """Export employee data to CSV file."""
        if not self.employees:
            print("\n⚠️  No employee records to export.")
            return
        
        filename = f"employees_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                fieldnames = ['emp_id', 'name', 'position', 'department', 'salary', 'hire_date']
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                
                writer.writeheader()
                for emp in self.employees.values():
                    writer.writerow(emp.to_dict())
            
            print(f"✅ Data exported successfully to {filename}")
        except Exception as e:
            print(f"❌ Error exporting data: {e}")
    
    def menu(self) -> None:
        """Display main menu and handle user choices."""
        while True:
            print("\n" + "="*60)
            print("👥 EMPLOYEE RECORD SYSTEM".center(60))
            print("="*60)
            print("1.  Add Employee")
            print("2.  Search & View Employee")
            print("3.  Update Employee")
            print("4.  Delete Employee")
            print("5.  Display All Employees")
            print("6.  Display by Department")
            print("7.  Salary Statistics")
            print("8.  Filter Employees")
            print("9.  Export to CSV")
            print("10. Save Data")
            print("11. Exit")
            print("="*60)
            
            choice = input("Enter your choice (1-11): ").strip()
            
            try:
                if choice == '1':
                    self.add_employee()
                elif choice == '2':
                    self.display_employee()
                elif choice == '3':
                    self.update_employee()
                elif choice == '4':
                    self.delete_employee()
                elif choice == '5':
                    self.display_all_employees()
                elif choice == '6':
                    self.display_by_department()
                elif choice == '7':
                    self.salary_statistics()
                elif choice == '8':
                    self.filter_employees()
                elif choice == '9':
                    self.export_to_csv()
                elif choice == '10':
                    self.save_data()
                elif choice == '11':
                    self.save_data()
                    print("\n👋 Thank you for using Employee Record System!")
                    break
                else:
                    print("❌ Invalid choice. Please select 1-11.")
            except KeyboardInterrupt:
                print("\n\n⚠️  Interrupted. Saving data...")
                self.save_data()
                break
            except Exception as e:
                print(f"\n❌ An error occurred: {e}")


def main() -> None:
    """Entry point for the Employee Record System."""
    system = EmployeeRecordSystem()
    system.menu()


if __name__ == "__main__":
    main()