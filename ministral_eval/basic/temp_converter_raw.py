```python
import unittest

def c_to_f(c):
    try:
        c = float(c)
        return c * 9/5 + 32
    except ValueError:
        raise ValueError("Invalid input: must be numeric")

def f_to_c(f):
    try:
        f = float(f)
        return (f - 32) * 5/9
    except ValueError:
        raise ValueError("Invalid input: must be numeric")

def c_to_k(c):
    try:
        c = float(c)
        return c + 273.15
    except ValueError:
        raise ValueError("Invalid input: must be numeric")

def k_to_c(k):
    try:
        k = float(k)
        return k - 273.15
    except ValueError:
        raise ValueError("Invalid input: must be numeric")

def get_float_input(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Invalid input. Please enter a numeric value.")

def main():
    while True:
        print("\nTemperature Converter")
        print("1. Celsius to Fahrenheit")
        print("2. Fahrenheit to Celsius")
        print("3. Celsius to Kelvin")
        print("4. Kelvin to Celsius")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ")

        if choice == '1':
            c = get_float_input("Enter temperature in Celsius: ")
            print(f"{c}°C = {c_to_f(c):.2f}°F")
        elif choice == '2':
            f = get_float_input("Enter temperature in Fahrenheit: ")
            print(f"{f}°F = {f_to_c(f):.2f}°C")
        elif choice == '3':
            c = get_float_input("Enter temperature in Celsius: ")
            print(f"{c}°C = {c_to_k(c):.2f}K")
        elif choice == '4':
            k = get_float_input("Enter temperature in Kelvin: ")
            print(f"{k}K = {k_to_c(k):.2f}°C")
        elif choice == '5':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")

class TestTemperatureConverter(unittest.TestCase):
    def test_c_to_f_normal(self):
        self.assertAlmostEqual(c_to_f(0), 32)
        self.assertAlmostEqual(c_to_f(100), 212)
        self.assertAlmostEqual(c_to_f(-40), -40)

    def test_f_to_c_normal(self):
        self.assertAlmostEqual(f_to_c(32), 0)
        self.assertAlmostEqual(f_to_c(212), 100)
        self.assertAlmostEqual(f_to_c(-40), -40)

    def test_c_to_k_normal(self):
        self.assertAlmostEqual(c_to_k(0), 273.15)
        self.assertAlmostEqual(c_to_k(100), 373.15)
        self.assertAlmostEqual(c_to_k(-273.15), 0)

    def test_k_to_c_normal(self):
        self.assertAlmostEqual(k_to_c(273.15), 0)
        self.assertAlmostEqual(k_to_c(373.15), 100)
        self.assertAlmostEqual(k_to_c(0), -273.15)

    def test_c_to_f_edge(self):
        self.assertAlmostEqual(c_to_f(1e6), 1800000)
        self.assertAlmostEqual(c_to_f(-1e6), -1758000)

    def test_f_to_c_edge(self):
        self.assertAlmostEqual(f_to_c(1e6), 554545.454545)
        self.assertAlmostEqual(f_to_c(-1e6), -566454.545455)

    def test_invalid_input(self):
        with self.assertRaises(ValueError):
            c_to_f("abc")
        with self.assertRaises(ValueError):
            f_to_c("xyz")
        with self.assertRaises(ValueError):
            c_to_k("123abc")
        with self.assertRaises(ValueError):
            k_to_c("test")

if __name__ == "__main__":
    unittest.main(argv=[''], exit=False)
    main()
```

