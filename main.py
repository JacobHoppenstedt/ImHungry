from recipe import Recipe
from cookbook import CookBook

# Example usage:
csv_file_path = "food_recipes.csv"  # Replace with the actual path to your CSV file
cookbook = CookBook(csv_file_path)

# Example: Accessing recipes
dish = "Golden Crescent Rolls"
recipe = cookbook.get_recipe(dish)
print(f"Recipe for {dish}: {recipe}")

# Sorting by time
cookbook.quicksort_by_time()

# After sorting
print("\nAfter sorting:")
for recipe in cookbook.recipe_list:
    print(recipe.name, recipe.time)