def c_to_f(c):
    if not isinstance(c, (int, float)):
        raise ValueError("Input must be a number")
    return (c * 9/5) + 32

def f_to_c(f):
    if not isinstance(f, (int, float)):
        raise ValueError("Input must be a number")
    return (f - 32) * 5/9

def c_to_k(c):
    if not isinstance(c, (int, float)):
        raise ValueError("Input must be a number")
    return c + 273.15

def k_to_c(k):
    if not isinstance(k, (int, float)):
        raise ValueError("Input must be a number")
    return k - 273.15

def main():
    while True:
        print("Choose an option:")
        print("1. Celsius to Fahrenheit")
        print("2. Fahrenheit to Celsius")
        print("3. Celsius to Kelvin")
        print("4. Kelvin to Celsius")
        print("5. Exit")
        choice = input("Enter your choice (1-5): ")
        if choice == '5':
            break
        try:
            choice = int(choice)
            if choice < 1 or choice > 4:
                raise ValueError("Invalid choice")
            temp = float(input("Enter temperature: "))
            if choice == 1:
                print(f"{temp} C is {c_to_f(temp)} F")
            elif choice == 2:
                print(f"{temp} F is {f_to_c(temp)} C")
            elif choice == 3:
                print(f"{temp} C is {c_to_k(temp)} K")
            elif choice == 4:
                print(f"{temp} K is {k_to_c(temp)} C")
        except ValueError as e:
            print(e)

if __name__ == "__main__":
    main()

import unittest

class TestTemperatureConverter(unittest.TestCase):
    def test_c_to_f(self):
        self.assertEqual(c_to_f(0), 32)
        self.assertEqual(c_to_f(100), 212)

    def test_f_to_c(self):
        self.assertEqual(f_to_c(32), 0)
        self.assertEqual(f_to_c(212), 100)

    def test_c_to_k(self):
        self.assertEqual(c_to_k(0), 273.15)
        self.assertEqual(c_to_k(-273.15), 0)

    def test_k_to_c(self):
        self.assertEqual(k_to_c(273.15), 0)
        self.assertEqual(k_to_c(0), -273.15)

    def test_non_numeric_input_c_to_f(self):
        with self.assertRaises(ValueError):
            c_to_f("a")

    def test_non_numeric_input_f_to_c(self):
        with self.assertRaises(ValueError):
            f_to_c("a")

    def test_non_numeric_input_c_to_k(self):
        with self.assertRaises(ValueError):
            c_to_k("a")

    def test_non_numeric_input_k_to_c(self):
        with self.assertRaises(ValueError):
            k_to_c("a")

if __name__ == "__main__":
    unittest.main()
