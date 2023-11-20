import random

# Racer class
class Racer:
    def __init__(self, name, weight, position):
        # The name of the racer (Mario, Peach, Funky Kong, etc)
        self.name = name

        # The weight of the racer, which will be Light, Medium, or Heavy
        self.weight = weight

        # Position of the racer (int). We will assign each racer a random position to start in.
        self.position = position

        # Initially, each racer will have no items
        self.item = None

        # Initially, all racers will be behind the start line, so their distance from the start line will be negative.
        self.distance_from_start = -1 * position

        # Assigns speed values based on weight
        # random.random()/2 + 1 generates a random number between 1.0 and 1.5, and the 23, 25, and 27 are all placeholder numbers
        # that will be changed once we figure out the length of the racetrack.
        # The heavier the character, the faster their speed will be
        if weight == "Light":
            self.speed = 23 * (random.random()/2 + 1)
        if weight == "Medium":
            self.speed = 25 * (random.random()/2 + 1)
        if weight == "Heavy":
            self.speed = 27 * (random.random()/2 + 1)

# Item class
class Item:
    def __init__(self, name):

        # The name of the item (Mushroom, Star, POW, etc.)
        self.name = name

        # Sets the spped effect for each item
        # The speed effect is the factor that gets multiplied to either the user's speed or another racer's speed, 
        # depending on the function of the item (see Google doc)
        if (name == "Green Shell" or name == "Red Shell" or name == "Blue Shell" or name == "FIB" or name == "Bomb"
            or name == "Triple Greens" or name == "Triple Reds"):
            self.speed_effect = 0
        if name == "Banana" or name == "Triple Bananas":
            self.speed_effect = 0.5
        if name == "Blooper":
            self.speed_effect = 0.9
        if name == "POW":
            self.speed_effect = 0
        if name == "Lightning":
            self.speed_effect = 0.35
        if name == "Mushroom" or name == "Triple Mushroom" or name == "Golden Mushroom":
            self.speed_effect = 1.25
        if name == "Star":
            self.speed_effect = 1.15
        if name == "Mega Mushroom" or "Lightning Cloud":
            self.speed_effect = 1.10
        if name == "Bullet Bill":
            self.speed_effect = 1.50
        
        