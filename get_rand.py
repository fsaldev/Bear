import random

def generate_random_integers_with_sum(target_sum, num_numbers):
    if num_numbers < 1:
        raise ValueError("num_numbers must be at least 1")
    
    # Generate random numbers
    numbers = [random.randint(0, target_sum) for _ in range(num_numbers - 1)]
    
    # Calculate the last number so that the sum is target_sum
    last_number = target_sum - sum(numbers)
    
    # Append the last number to the list
    numbers.append(last_number)

    # Return the list of random numbers
    return numbers

# Example usage:
target_sum = 20
num_numbers = 4
result_list = generate_random_integers_with_sum(target_sum, num_numbers)
print(result_list)
