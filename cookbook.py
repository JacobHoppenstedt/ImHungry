import recipe.py

class cookBook:

    def __init__(self, name, time, rating, ingredients):
        self.name = name
        self.time = time
        self.rating = rating
        self.ingredients = ingredients

    

def read_recipe_csv(file_path):
    recipes = []
    with open(file_path, 'r') as file:
        for line in file:

            recipe_info = line.strip().split(', ')

            name = recipe_info[0]
            time = recipe_info[1]
            rating = float(recipe_info[2])

            ingredients = recipe_info[3].split('//')

            recipe_dict = {
                'name': name,
                'time': time,
                'rating': rating,
                'ingredients': ingredients
            }

            recipe = Recipe(**recipe_dict)
            recipes.append(recipe)

    return recipes