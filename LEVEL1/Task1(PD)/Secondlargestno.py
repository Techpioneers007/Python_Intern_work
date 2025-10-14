"""
Second Largest Number Finder - Enhanced Version
Find the second largest number in a list using multiple algorithms.
Supports both O(n log n) and O(n) time complexity approaches.
"""

from typing import Optional


def find_second_largest_sorting(numbers: list[int]) -> Optional[int]:
    """
    Find second largest using sorting approach - O(n log n).
    
    Args:
        numbers: List of integers
    
    Returns:
        The second largest number, or None if not found
    
    Examples:
        >>> find_second_largest_sorting([1, 5, 3, 9, 2])
        5
        >>> find_second_largest_sorting([5, 5, 5])
        None
    """
    if len(numbers) < 2:
        return None
    
    unique_numbers = sorted(set(numbers), reverse=True)
    
    if len(unique_numbers) < 2:
        return None
    
    return unique_numbers[1]


def find_second_largest_linear(numbers: list[int]) -> Optional[int]:
    """
    Find second largest using linear scan - O(n) - More efficient!
    
    Args:
        numbers: List of integers
    
    Returns:
        The second largest number, or None if not found
    
    Examples:
        >>> find_second_largest_linear([1, 5, 3, 9, 2])
        5
        >>> find_second_largest_linear([5, 5, 5])
        None
    """
    if len(numbers) < 2:
        return None
    
    largest = second_largest = float('-inf')
    
    for num in numbers:
        if num > largest:
            second_largest = largest
            largest = num
        elif num > second_largest and num != largest:
            second_largest = num
    
    # Check if second_largest was actually updated
    if second_largest == float('-inf'):
        return None
    
    return int(second_largest)


def get_numbers_from_user() -> list[int]:
    """
    Get a list of numbers from user input with validation.
    
    Returns:
        A list of integers
    
    Raises:
        ValueError: If input is invalid
    """
    while True:
        try:
            user_input = input("\n📝 Enter numbers separated by spaces: ").strip()
            
            if not user_input:
                print("⚠️  No input provided. Please enter at least one number.")
                continue
            
            numbers = list(map(int, user_input.split()))
            
            if not numbers:
                print("⚠️  No valid numbers found. Please try again.")
                continue
            
            return numbers
            
        except ValueError:
            print("❌ Invalid input! Please enter only integers separated by spaces.")
            print("   Example: 10 5 23 7 15")


def display_analysis(numbers: list[int], second_largest: Optional[int], method: str) -> None:
    """
    Display detailed analysis of the results.
    
    Args:
        numbers: The input list of numbers
        second_largest: The found second largest number or None
        method: The algorithm used
    """
    print("\n" + "="*60)
    print("📊 ANALYSIS RESULTS".center(60))
    print("="*60)
    print(f"Original List    : {numbers}")
    print(f"Unique Numbers   : {sorted(set(numbers), reverse=True)}")
    print(f"Total Count      : {len(numbers)}")
    print(f"Unique Count     : {len(set(numbers))}")
    print(f"Algorithm Used   : {method}")
    print("-"*60)
    
    if second_largest is not None:
        print(f"✅ Second Largest: {second_largest}")
        print(f"   Largest       : {max(numbers)}")
        print(f"   Smallest      : {min(numbers)}")
    else:
        print("❌ Second largest number not found!")
        if len(numbers) < 2:
            print("   Reason: List has fewer than 2 elements")
        elif len(set(numbers)) < 2:
            print("   Reason: All numbers are identical")
    
    print("="*60)


def choose_algorithm() -> str:
    """
    Let user choose which algorithm to use.
    
    Returns:
        Algorithm choice: 'sorting' or 'linear'
    """
    print("\n🔧 Choose Algorithm:")
    print("  1. Sorting Method (O(n log n) - Simple)")
    print("  2. Linear Scan (O(n) - Efficient)")
    
    choice = input("\nEnter your choice (1/2) [default: 2]: ").strip() or "2"
    
    return "linear" if choice == "2" else "sorting"


def main() -> None:
    """Main function to run the second largest number finder."""
    print("\n" + "="*60)
    print("🔢 SECOND LARGEST NUMBER FINDER 🔢".center(60))
    print("="*60)
    
    try:
        numbers = get_numbers_from_user()
        algorithm = choose_algorithm()
        
        # Find second largest using chosen method
        if algorithm == "linear":
            second_largest = find_second_largest_linear(numbers)
            method_name = "Linear Scan O(n)"
        else:
            second_largest = find_second_largest_sorting(numbers)
            method_name = "Sorting O(n log n)"
        
        display_analysis(numbers, second_largest, method_name)
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Program interrupted by user.")
    except Exception as e:
        print(f"\n❌ An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()

