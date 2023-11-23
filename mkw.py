import random
import sys

# Racer class
class Racer:
    def __init__(self, name, weight):
        # The name of the racer (Mario, Peach, Funky Kong, etc)
        self.name = name

        # The weight of the racer, which will be Light, Medium, or Heavy
        self.weight = weight

        # Position of the racer (int). We will assign each racer a random position to start in, but for now, we set it to 0.
        self.position = 0

        # Initially, each racer will have no items
        self.item = None

        # Initially, all racers will be behind the start line, so their distance from the start line will be negative.
        # But for now, we set it to 0.
        self.distance_from_start = 0

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
        
        # Assigns acceleration based on weight
        # The heavier the character, the lower the acceleration
        # We will update these values once we create the race track and get the speed stuff figured out
        # We might randomize the accelerations a little just for fun, but that will be for later
        if weight == "Light":
            self.acceleration = 8
        if weight == "Medium":
            self.acceleration = 6
        if weight == "Heavy":
            self.acceleration = 4
    
    # Function incorporating acceleration
    def accelerate(self):
        pass

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

def update_position(racer1, racer2):
    racer1.position, racer2.position = racer2.position, racer1.position

def update_distance(racer):
    pass

def get_item(racer, num_racers):
    if num_racers == 2:
        return
    if num_racers == 3:
        return
    if num_racers == 4:
        return
    if num_racers == 5:
        return
    if num_racers == 6:
        return
    if num_racers == 7:
        return
    if num_racers == 8:
        return
    if num_racers == 9:
        return
    if num_racers == 10:
        return
    if num_racers == 11:
        return
    if num_racers == 12:
        return
    # TO DO

def use_item(racer):
    pass

mario = Racer("Mario", "Medium")
luigi = Racer("Luigi", "Medium")
peach = Racer("Peach", "Medium")
daisy = Racer("Daisy", "Medium")
yoshi = Racer("Yoshi", "Medium")
diddy_kong = Racer("Diddy Kong", "Medium")
birdo = Racer("Birdo", "Medium")
bowser_jr = Racer("Bowser Jr.", "Medium")
baby_mario = Racer("Baby Mario", "Light")
baby_luigi = Racer("Baby Luigi", "Light")
baby_peach = Racer("Baby Peach", "Light")
baby_daisy = Racer("Baby Daisy", "Light")
toad = Racer("Toad", "Light")
toadette = Racer("Toadette", "Light")
koopa = Racer("Koopa Troopa", "Light")
dry_bones = Racer("Dry Bones", "Light")
bowser = Racer("Bowser", "Heavy")
rosalina = Racer("Rosalina", "Heavy")
funky_kong = Racer("Funky Kong", "Heavy")
donkey_kong = Racer("Donkey Kong", "Heavy")
wario = Racer("Wario", "Heavy")
waluigi = Racer("Waluigi", "Heavy")
dry_bowser = Racer("Dry Bowser", "Heavy")
king_boo = Racer("King Boo", "Heavy")

all_racers = [mario, luigi, peach, daisy, yoshi, diddy_kong, birdo, bowser_jr,
              baby_mario, baby_luigi, baby_peach, baby_daisy, toad, toadette, koopa, dry_bones,
              bowser, rosalina, funky_kong, donkey_kong, wario, waluigi, dry_bowser, king_boo]

# Where we will put everything together and make the animation
def main():
    # Making sure the user inputs an integer
    # The try-except block at the bottom of the code will handle the cases where the user inputs a string
    n = input("Enter the number of racers: ")
    if int(n) != float(n):
        print("Must input an integer between 2 and 12, inclusive.")
        sys.exit()
    num_racers = int(n)
    # TO BE CONTINUED

# Error handling
if len(sys.argv) != 1:
    print("Invalid number of inputs.")
    sys.exit()
else:
    try:
        main()
    except:
        print("Unexpected error occurred. Make sure you input an integer between 2 and 12, inclusive.")