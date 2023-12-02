class Recipe:
    def __init__(self, name, time, rating, ingredients):
        self.name = name
        self.time = time
        self.rating = rating
        self.ingredients = ingredients

    def getIngredients(self):
        return self.ingredients

def read_recipe_csv(file_path):
    recipes = []
    with open(file_path, 'r') as file:
        for line in file:

            recipe_info = line.strip().split(', ')

            name = recipe_info[0]
            time = recipe_info[1]
            rating = float(recipe_info[2])

            ingredients = recipe_info[3].split('//')

            recipe = Recipe(name, time, rating, ingredients)
            recipes.append(recipe)

    return recipes