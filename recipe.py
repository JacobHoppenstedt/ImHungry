class Recipe:
    def __init__(self, name, time, rating, ingredients):
        self.name = name
        self.time = time
        self.rating = rating
        self.ingredients = ingredients
        self.time_in_minutes = 0

    def getIngredients(self):
        return self.ingredients

    def time_in_minutes(self):
        if self.time == 'N/A':
            return float('inf')
        total_minutes = 0
        time_components = self.time.split()

        for component in time_components:
            if 'd' in component and len(time_components) == 6:
                time_in_minutes = (int(time_components[0]) * 24 * 60) + (int(time_components[2]) * 60) + int(time_components[4])
            elif 'd' in component and len(time_components) == 4:
                if 'h' in component:
                    time_in_minutes = (int(time_components[0]) * 24 * 60) + (int(time_components[2]) * 60)
                else:
                    time_in_minutes = (int(time_components[0]) * 24 * 60) + (int(time_components[2]))
            elif 'd' in component and len(time_components) == 2:
                time_in_minutes = (int(time_components[0]) * 24 * 60)
            elif 'h' in component and len(time_components) == 4:
                time_in_minutes += (int(time_components[0]) * 60) + int(time_components[2])
            elif 'h' in component and len(time_components) == 2:
                time_in_minutes += (int(time_components[0]) * 60)
            elif 'm' in component and len(time_components) == 2:
                time_in_minutes += int(time_components[0])

        total_time = time_in_minutes
        return total_time

