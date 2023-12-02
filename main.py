from recipe import Recipe
from cookbook import CookBook

# Example usage:
csv_file_path = "food_recipes.csv"  # Replace with the actual path to your CSV file
cookbook = CookBook(csv_file_path)

# Example: Accessing recipes
dish = "Golden Crescent Rolls"
recipe = cookbook.get_recipe(dish)
print(f"Recipe for {dish}: {recipe}")

# print("\nBefore sorting:")
for recipe in range(0, 100):
    print(cookbook.recipe_list[recipe].name, cookbook.recipe_list[recipe].time)
# Sorting by time
# cookbook.quicksort_by_time()

# # After sorting
# print("\nAfter sorting:")
# for recipe in range(0, 100):
#     print(cookbook.recipe_list[recipe].name, cookbook.recipe_list[recipe].time)

# Sort recipes by rating using mergesort
cookbook.mergesort_by_rating()

# Print recipes and their ratings after sorting by rating
print("\nRecipes and Ratings (Sorted by Rating):")
for recipe in cookbook.recipe_list:
    print(f"{recipe.name}: {recipe.rating}")