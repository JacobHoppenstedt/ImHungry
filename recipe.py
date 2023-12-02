class Recipe:
    def __init__(self, name, time, rating, ingredients):
        self.name = name
        self.time = time
        self.rating = rating
        self.ingredients = ingredients

    def getIngredients(self):
        return self.ingredients

    def time_in_minutes(self):
        # return time in minutes for sorting
        if self.time == 'N/A':
            return float('inf')  # or any large value to place 'N/A' at the end

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
            else:
                # Assume it's only minutes if no unit is specified
                total_minutes += int(component) if component else 0

        return total_minutes
