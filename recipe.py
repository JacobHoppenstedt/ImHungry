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
            return -1
        total_minutes = 0
        time_components = self.time.split()

        for component in time_components:
            if 'd' in component:
                days = component.replace('d', '')
                total_minutes += int(days) * 24 * 60 if days else 0
            elif 'h' in component:
                hours = component.replace('h', '')
                total_minutes += int(hours) * 60 if hours else 0
            elif 'm' in component:
                minutes = component.replace('m', '')
                total_minutes += int(minutes) if minutes else 0

        return total_minutes

