```python
# temp_converter.py

def c_to_f(c):
    """Convert Celsius to Fahrenheit."""
    return (c * 9/5) + 32

def f_to_c(f):
    """Convert Fahrenheit to Celsius."""
    return (f - 32) * 5/9

def c_to_k(c):
    """Convert Celsius to Kelvin."""
    return c + 273.15

def k_to_c(k):
    """Convert Kelvin to Celsius."""
    return k - 273.15

def get_float_input(prompt):
    """Get a float input from the user with validation."""
    while True:
        try:
            value = float(input(prompt))
            return value
        except ValueError:
            print("Invalid input! Please enter a numeric value.")

# CLI Menu
def main():
    print("=== Temperature Converter ===")
    print("1. Celsius to Fahrenheit")
    print("2. Fahrenheit to Celsius")
    print("3. Celsius to Kelvin")
    print("4. Kelvin to Celsius")
    print("5. Exit")
    
    while True:
        choice = input("\nSelect an option (1-5): ").strip()
        
        if choice == '1':
            c = get_float_input("Enter temperature in Celsius: ")
            result = c_to_f(c)
            print(f"{c}°C is {result:.2f}°F")
            
        elif choice == '2':
            f = get_float_input("Enter temperature in Fahrenheit: ")
            result = f_to_c(f)
            print(f"{f}°F is {result:.2f}°C")
            
        elif choice == '3':
            c = get_float_input("Enter temperature in Celsius: ")
            result = c_to_k(c)
            print(f"{c}°C is {result:.2f}K")
            
        elif choice == '4':
            k = get_float_input("Enter temperature in Kelvin: ")
            result = k_to_c(k)
            print(f"{k}K is {result:.2f}°C")
            
        elif choice == '5':
            print("Exiting...")
            break
            
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
```