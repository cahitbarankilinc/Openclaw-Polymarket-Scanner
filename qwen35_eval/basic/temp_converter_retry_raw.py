import unittest
import sys

def c_to_f(celsius):
    return (celsius * 9/5) + 32

def f_to_c(fahrenheit):
    return (fahrenheit - 32) * 5/9

def c_to_k(celsius):
    return celsius + 273.15

def k_to_c(kelvin):
    return kelvin - 273.15

def main():
    while True:
        print("\n--- Temperature Converter ---")
        print("1. Celsius to Fahrenheit")
        print("2. Fahrenheit to Celsius")
        print("3. Celsius to Kelvin")
        print("4. Kelvin to Celsius")
        print("5. Exit")
        
        choice = input("Select an option (1-5): ").strip()
        
        if choice == '1':
            try:
                val = float(input("Enter temperature in Celsius: "))
                result = c_to_f(val)
                print(f"{val}°C is {result:.2f}°F")
            except ValueError:
                print("Invalid input.")
        elif choice == '2':
            try:
                val = float(input("Enter temperature in Fahrenheit: "))
                result = f_to_c(val)
                print(f"{val}°F is {result:.2f}°C")
            except ValueError:
                print("Invalid input.")
        elif choice == '3':
            try:
                val = float(input("Enter temperature in Celsius: "))
                result = c_to_k(val)
                print(f"{val}°C is {result:.2f}K")
            except ValueError:
                print("Invalid input.")
        elif choice == '4':
            try:
                val = float(input("Enter temperature in Kelvin: "))
                result = k_to_c(val)
                print(f"{val}K is {result:.2f}°C")
            except ValueError:
                print("Invalid input.")
        elif choice == '5':
            print("Exiting...")
            break
        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()

class TestTemperatureConverter(unittest.TestCase):
    
    def test_c_to_f_basic(self):
        self.assertEqual(c_to_f(0), 32.0)
    
    def test_c_to_f_negative(self):
        self.assertAlmostEqual(c_to_f(-40), -40.0)
    
    def test_c_to_f_positive(self):
        self.assertAlmostEqual(c_to_f(100), 212.0)
    
    def test_f_to_c_basic(self):
        self.assertEqual(f_to_c(32), 0.0)
    
    def test_f_to_c_negative(self):
        self.assertAlmostEqual(f_to_c(-40), -40.0)
    
    def test_f_to_c_positive(self):
        self.assertAlmostEqual(f_to_c(212), 100.0)
    
    def test_c_to_k_basic(self):
        self.assertEqual(c_to_k(0), 273.15)
    
    def test_k_to_c_basic(self):
        self.assertEqual(k_to_c(273.15), 0.0)

if __name__ == "__main__":
    unittest.main()