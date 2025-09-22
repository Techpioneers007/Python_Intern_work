# Taking array input from the user
numbers = list(map(int, input("Enter numbers separated by spaces: ").split()))

# Checking if the array has at least two unique numbers
if len(set(numbers)) < 2:
    print("Array must have at least two unique numbers to find the second largest.")
else:
    # Removing duplicates and sorting the array in descending order
    unique_numbers = sorted(set(numbers), reverse=True)
    
    # The second largest number is the second element in the sorted list
    second_largest = unique_numbers[1]
    print("The second largest number is:", second_largest)

