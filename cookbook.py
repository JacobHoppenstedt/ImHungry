import recipe.py
import csv

class cookBook:
    def __init__(self, csv_file):
        self.recipe_hash_table = {}
        self.load_from_csv(csv_file)

    def load_from_csv(self, csv_file):
        with open(csv_file, newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            header = next(reader)  # Assuming the first row contains column headers

            for row in reader:
                if len(row) == len(header):  # Check if the number of columns matches the header
                    dish_name, recipe = row
                    self.add_entry(dish_name, recipe)
                else:
                    print(f"Skipping invalid entry: {row}")

    def add_entry(self, dish_name, recipe):
        self.recipe_hash_table[dish_name] = recipe

    def get_recipe(self, dish_name):
        return self.recipe_hash_table.get(dish_name, "Recipe not found")


# Example usage:
csv_file_path = "your_cookbook.csv"  # Replace with the actual path to your CSV file
cookbook = cookBook(csv_file_path)

# Example: Accessing recipes
dish = "Spaghetti Bolognese"
recipe = cookbook.get_recipe(dish)
print(f"Recipe for {dish}: {recipe}")