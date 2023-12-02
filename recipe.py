class Recipe:
    def __init__(self, name, time, rating, ingredients):
        self.name = name
        self.time = time
        self.rating = rating
        self.ingredients = ingredients

    def getIngredients(self):
        return self.ingredients

    def time_in_minutes(self):
        if self.time == 'N/A':
            return float('inf')
        total_minutes = 0
        time_components = self.time.split()

        for component in time_components:
            if 'd' in component and len(time_components) == 6:
                total_minutes = (int(time_components[0]) * 24 * 60) + (int(time_components[2]) * 60) + int(time_components[4])
            elif 'd' in component and len(time_components) == 4:
                if 'h' in component:
                    total_minutes = (int(time_components[0]) * 24 * 60) + (int(time_components[2]) * 60)
                else:
                    total_minutes = (int(time_components[0]) * 24 * 60) + (int(time_components[2]))
            elif 'd' in component and len(time_components) == 2:
                total_minutes = (int(time_components[0]) * 24 * 60)
            elif 'h' in component and len(time_components) == 4:
                total_minutes += (int(time_components[0]) * 60) + int(time_components[2])
            elif 'h' in component and len(time_components) == 2:
                total_minutes += (int(time_components[0]) * 60)
            elif 'm' in component and len(time_components) == 2:
                total_minutes += int(time_components[0])
                
        return total_minutes

