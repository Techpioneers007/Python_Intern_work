"""
Palindrome Checker - Enhanced Version
A utility to check if a given string is a palindrome.
Supports multiple checking modes: standard, strict (no spaces), and alphanumeric only.
"""

import re
from typing import Literal


def is_palindrome(
    text: str, 
    mode: Literal["standard", "strict", "alphanumeric"] = "standard"
) -> bool:
    """
    Check if a string is a palindrome based on the specified mode.
    
    Args:
        text: The string to check for palindrome property
        mode: The checking mode:
            - "standard": Ignores spaces and case
            - "strict": Case-sensitive, includes spaces
            - "alphanumeric": Only considers alphanumeric characters
    
    Returns:
        True if the string is a palindrome, False otherwise
    
    Examples:
        >>> is_palindrome("A man a plan a canal Panama")
        True
        >>> is_palindrome("Hello")
        False
        >>> is_palindrome("Was it a car or a cat I saw?", mode="alphanumeric")
        True
    """
    if not text:
        return True
    
    if mode == "standard":
        # Remove spaces and convert to lowercase
        cleaned = ''.join(text.lower().split())
    elif mode == "strict":
        # Keep everything as-is (case-sensitive)
        cleaned = text
    elif mode == "alphanumeric":
        # Keep only alphanumeric characters, case-insensitive
        cleaned = re.sub(r'[^a-zA-Z0-9]', '', text).lower()
    else:
        raise ValueError(f"Invalid mode: {mode}. Use 'standard', 'strict', or 'alphanumeric'")
    
    # Check if the string equals its reverse
    return cleaned == cleaned[::-1]


def get_user_input() -> tuple[str, str]:
    """
    Get string input and checking mode from the user.
    
    Returns:
        A tuple of (text, mode)
    """
    print("\n" + "="*50)
    print("🔄 PALINDROME CHECKER 🔄".center(50))
    print("="*50)
    
    text = input("\n📝 Enter a string to check: ").strip()
    
    print("\n🔧 Select checking mode:")
    print("  1. Standard (ignore spaces and case)")
    print("  2. Strict (case-sensitive, includes spaces)")
    print("  3. Alphanumeric (only letters and numbers)")
    
    mode_choice = input("\nEnter your choice (1/2/3) [default: 1]: ").strip() or "1"
    
    mode_map = {"1": "standard", "2": "strict", "3": "alphanumeric"}
    mode = mode_map.get(mode_choice, "standard")
    
    return text, mode


def display_result(text: str, is_palin: bool, mode: str) -> None:
    """
    Display the palindrome check result in a formatted manner.
    
    Args:
        text: The original input string
        is_palin: Whether the string is a palindrome
        mode: The mode used for checking
    """
    print("\n" + "-"*50)
    print("📊 RESULT".center(50))
    print("-"*50)
    print(f"Input Text : {text}")
    print(f"Mode       : {mode.capitalize()}")
    
    if is_palin:
        print("\n✅ The string IS a palindrome! 🎉")
    else:
        print("\n❌ The string is NOT a palindrome.")
    print("-"*50)


def main() -> None:
    """Main function to run the palindrome checker."""
    try:
        text, mode = get_user_input()
        
        if not text:
            print("\n⚠️  Empty string entered. An empty string is considered a palindrome.")
            return
        
        result = is_palindrome(text, mode)
        display_result(text, result, mode)
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Program interrupted by user.")
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")


if __name__ == "__main__":
    main()
