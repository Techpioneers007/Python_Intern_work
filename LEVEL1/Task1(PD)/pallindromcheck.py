# Function to check if a string is a palindrome
def is_palindrome(string):
    # Remove spaces and convert to lowercase for uniformity
    cleaned_string = ''.join(string.lower().split())
    # Check if the string is equal to its reverse
    return cleaned_string == cleaned_string[::-1]

# Input from the user
user_input = input("Enter a string to check if it's a palindrome: ")

# Check and display the result
if is_palindrome(user_input):
    print("The string is a palindrome!")
else:
    print("The string is NOT a palindrome.")
