import random
import sys

# Racer class
class Racer:
    def __init__(self, name, weight):
        # The name of the racer (Mario, Peach, Funky Kong, etc)
        self.name = name

        # The weight of the racer, which will be Light, Medium, or Heavy
        self.weight = weight

        # Position of the racer (int). We will assign each racer a random position to start in, but for now,
        # we set it to 0.
        self.position = 0

        # Initially, each racer will have no items
        self.item = None

        # Initially, all racers will be behind the start line, so their distance from the start line will be negative.
        # But for now, we set it to 0.
        self.distance_from_start = 0

        # Assigns speed values based on weight. random.uniform(1.0, 1.5) generates a random number between 1.0 and 1.5,
        # and the 23, 25, and 27 are all placeholder numbers that will be changed once we figure out the length of
        # the racetrack. The heavier the character, the faster their speed will be
        if weight == "Light":
            self.speed = 23 * random.uniform(1.0, 1.5)
        if weight == "Medium":
            self.speed = 25 * random.uniform(1.0, 1.5)
        if weight == "Heavy":
            self.speed = 27 * random.uniform(1.0, 1.5)

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


# Item class
class Item:
    def __init__(self, name):

        # The name of the item (Mushroom, Star, POW, etc.)
        self.name = name

        # Sets the speed effect for each item
        # The speed effect is the factor that gets multiplied to either the user's speed or another racer's speed, 
        # depending on the function of the item (see Google doc)
        if (name == "green_shell" or name == "red_shell" or name == "blue_shell" or name == "FIB" or name == "bob_omb"
                or name == "trip_green_shell" or name == "trip_red_shell"):
            self.speed_effect = 0
        if name == "banana" or name == "trip_bananas":
            self.speed_effect = 0.5
        if name == "blooper":
            self.speed_effect = 0.9
        if name == "POW":
            self.speed_effect = 0
        if name == "lightning_bolt":
            self.speed_effect = 0.35
        if name == "mushroom" or name == "trip_mushroom" or name == "gold_mushroom":
            self.speed_effect = 1.25
        if name == "star":
            self.speed_effect = 1.15
        if name == "mega_mushroom" or "lightning_cloud":
            self.speed_effect = 1.10
        if name == "bullet_bill":
            self.speed_effect = 1.50


def update_position(racer1, racer2):
    racer1.position, racer2.position = racer2.position, racer1.position


def update_distance(racer, time):
    # Changes the distance the racer has traveled in a certain time (in this case I used 1 second, but we can change
    # it based on how the race looks and the processing power of our computers). This also assumes the racer speeds
    # are all in m/s
    distance = racer.distance_from_start + (racer.speed * time)
    racer.distance_from_start = distance


def update_speed(racer, time):
    # Adjusts the speed of the racer based on its acceleration. The method assumes 1 second has passed
    speed = racer.speed + racer.acceleration * time
    racer.speed = speed


def choose_item(choices, position):
    total = sum(weight[position] for _, weight in choices)
    r = random.uniform(0, total)
    subtotal = 0

    for item, weight in choices:
        subtotal += weight[position]
        if subtotal >= r:
            return Item(item)


def get_item(racer, num_racers):
    if num_racers == 2:
        item = choose_item(all_items_2, racer.position)
        racer.item = item
    if num_racers == 3:
        item = choose_item(all_items_3, racer.position)
        racer.item = item
    if num_racers == 4:
        item = choose_item(all_items_4, racer.position)
        racer.item = item
    if num_racers == 5:
        item = choose_item(all_items_5, racer.position)
        racer.item = item
    if num_racers == 6:
        item = choose_item(all_items_6, racer.position)
        racer.item = item
    if num_racers == 7:
        item = choose_item(all_items_7, racer.position)
        racer.item = item
    if num_racers == 8:
        item = choose_item(all_items_8, racer.position)
        racer.item = item
    if num_racers == 9:
        item = choose_item(all_items_9, racer.position)
        racer.item = item
    if num_racers == 10:
        item = choose_item(all_items_10, racer.position)
        racer.item = item
    if num_racers == 11:
        item = choose_item(all_items_11, racer.position)
        racer.item = item
    if num_racers == 12:
        item = choose_item(all_items_12, racer.position)
        racer.item = item


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

# Item list with weights of each item respective to their position. There is a separate list for each possible number
# of racers
all_items_12 = [("lightning_cloud", {1: 0, 2: 0, 3: 0.025, 4: 0.075, 5: 0.075, 6: 0.075, 7: 0.05, 8: 0.05, 9: 0, 10: 0,
                                     11: 0, 12: 0}),
                ("lightning_bolt", {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0.075, 12: 0.2}),
                ("blooper",
                 {1: 0, 2: 0, 3: 0, 4: 0, 5: 0.05, 6: 0.075, 7: 0.075, 8: 0.05, 9: 0.05, 10: 0, 11: 0, 12: 0}),
                ("POW", {1: 0, 2: 0, 3: 0, 4: 0, 5: 0.05, 6: 0.05, 7: 0.075, 8: 0.05, 9: 0.05, 10: 0, 11: 0, 12: 0}),
                ("mushroom", {1: 0, 2: 0.125, 3: 0.175, 4: 0.225, 5: 0.15, 6: 0.125, 7: 0.1, 8: 0, 9: 0, 10: 0, 11: 0,
                              12: 0}),
                ("trip_mushroom", {1: 0, 2: 0, 3: 0, 4: 0.05, 5: 0.1, 6: 0.15, 7: 0.25, 8: 0.325, 9: 0.375, 10: 0.3,
                                   11: 0.125, 12: 0.05}),
                (
                    "gold_mushroom",
                    {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0.025, 7: 0.1, 8: 0.225, 9: 0.275, 10: 0.35, 11: 0.3,
                     12: 0.225}),
                ("mega_mushroom", {1: 0, 2: 0, 3: 0, 4: 0.025, 5: 0.075, 6: 0.1, 7: 0.075, 8: 0.05, 9: 0, 10: 0, 11: 0,
                                   12: 0}),
                ("star", {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0.125, 9: 0.2, 10: 0.275, 11: 0.275, 12: 0.175}),
                ("bullet_bill", {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0.025, 10: 0.075, 11: 0.225,
                                 12: 0.35}),
                ("green_shell", {1: 0.325, 2: 0.175, 3: 0.15, 4: 0.075, 5: 0.05, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0,
                                 12: 0}),
                ("trip_green_shell", {1: 0, 2: 0.05, 3: 0.1, 4: 0.1, 5: 0.075, 6: 0.05, 7: 0.025, 8: 0, 9: 0, 10: 0,
                                      11: 0, 12: 0}),
                ("red_shell", {1: 0, 2: 0.25, 3: 0.25, 4: 0.2, 5: 0.15, 6: 0.1, 7: 0.05, 8: 0.025, 9: 0, 10: 0, 11: 0,
                               12: 0}),
                ("trip_red_shell", {1: 0, 2: 0, 3: 0.05, 4: 0.1, 5: 0.1, 6: 0.1, 7: 0.075, 8: 0.05, 9: 0, 10: 0, 11: 0,
                                    12: 0}),
                (
                    "blue_shell",
                    {1: 0, 2: 0, 3: 0, 4: 0.025, 5: 0.05, 6: 0.075, 7: 0.075, 8: 0.05, 9: 0.025, 10: 0, 11: 0,
                     12: 0}),
                ("bob_omb",
                 {1: 0, 2: 0, 3: 0.025, 4: 0.05, 5: 0.075, 6: 0.075, 7: 0.05, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}),
                ("FIB", {1: 0.2, 2: 0.075, 3: 0.05, 4: 0.025, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}),
                ("banana", {1: 0.375, 2: 0.2, 3: 0.075, 4: 0.025, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}),
                ("trip_bananas",
                 {1: 0.1, 2: 0.125, 3: 0.1, 4: 0.025, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0})]

all_items_11 = [("lightning_cloud", {1: 0, 2: 0, 3: 0.025, 4: 0.075, 5: 0.075, 6: 0.05, 7: 0.05, 8: 0, 9: 0, 10: 0,
                                     11: 0}),
                ("lightning_bolt", {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0.075, 11: 0.2}),
                ("blooper", {1: 0, 2: 0, 3: 0, 4: 0, 5: 0.05, 6: 0.075, 7: 0.05, 8: 0.05, 9: 0, 10: 0, 11: 0}),
                ("POW", {1: 0, 2: 0, 3: 0, 4: 0, 5: 0.05, 6: 0.075, 7: 0.05, 8: 0.05, 9: 0, 10: 0, 11: 0}),
                ("mushroom", {1: 0, 2: 0.125, 3: 0.175, 4: 0.225, 5: 0.15, 6: 0.1, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0}),
                ("trip_mushroom", {1: 0, 2: 0, 3: 0, 4: 0.05, 5: 0.1, 6: 0.25, 7: 0.325, 8: 0.375, 9: 0.3, 10: 0.125,
                                   11: 0.05}),
                ("gold_mushroom",
                 {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0.1, 7: 0.225, 8: 0.275, 9: 0.35, 10: 0.3, 11: 0.225}),
                ("mega_mushroom", {1: 0, 2: 0, 3: 0, 4: 0.025, 5: 0.075, 6: 0.075, 7: 0.05, 8: 0, 9: 0, 10: 0, 11: 0}),
                ("star", {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0.125, 8: 0.2, 9: 0.275, 10: 0.275, 11: 0.175}),
                ("bullet_bill", {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0.025, 9: 0.075, 10: 0.225, 11: 0.35}),
                ("green_shell", {1: 0.325, 2: 0.175, 3: 0.15, 4: 0.075, 5: 0.05, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0}),
                ("trip_green_shell",
                 {1: 0, 2: 0.05, 3: 0.1, 4: 0.1, 5: 0.075, 6: 0.025, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0}),
                ("red_shell", {1: 0, 2: 0.25, 3: 0.25, 4: 0.2, 5: 0.15, 6: 0.05, 7: 0.025, 8: 0, 9: 0, 10: 0, 11: 0}),
                ("trip_red_shell", {1: 0, 2: 0, 3: 0.05, 4: 0.1, 5: 0.1, 6: 0.075, 7: 0.05, 8: 0, 9: 0, 10: 0, 11: 0}),
                ("blue_shell", {1: 0, 2: 0, 3: 0, 4: 0.025, 5: 0.05, 6: 0.075, 7: 0.05, 8: 0.025, 9: 0, 10: 0, 11: 0}),
                ("bob_omb", {1: 0, 2: 0, 3: 0.025, 4: 0.05, 5: 0.075, 6: 0.05, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0}),
                ("FIB", {1: 0.2, 2: 0.075, 3: 0.05, 4: 0.025, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0}),
                ("banana", {1: 0.375, 2: 0.2, 3: 0.075, 4: 0.025, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0}),
                ("trip_bananas", {1: 0.1, 2: 0.125, 3: 0.1, 4: 0.025, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0})]

all_items_10 = [("lightning_cloud", {1: 0, 2: 0, 3: 0.025, 4: 0.075, 5: 0.075, 6: 0.05, 7: 0.05, 8: 0, 9: 0, 10: 0}),
                ("lightning_bolt", {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0.075, 10: 0.2}),
                ("blooper", {1: 0, 2: 0, 3: 0, 4: 0.05, 5: 0.075, 6: 0.075, 7: 0.05, 8: 0, 9: 0, 10: 0}),
                ("POW", {1: 0, 2: 0, 3: 0, 4: 0, 5: 0.05, 6: 0.075, 7: 0.05, 8: 0, 9: 0, 10: 0}),
                ("mushroom", {1: 0, 2: 0.125, 3: 0.175, 4: 0.15, 5: 0.125, 6: 0.1, 7: 0, 8: 0, 9: 0, 10: 0}),
                ("trip_mushroom", {1: 0, 2: 0, 3: 0, 4: 0.1, 5: 0.15, 6: 0.25, 7: 0.325, 8: 0.3, 9: 0.125, 10: 0.05}),
                ("gold_mushroom", {1: 0, 2: 0, 3: 0, 4: 0, 5: 0.025, 6: 0.1, 7: 0.225, 8: 0.35, 9: 0.3, 10: 0.225}),
                ("mega_mushroom", {1: 0, 2: 0, 3: 0, 4: 0.075, 5: 0.1, 6: 0.075, 7: 0.05, 8: 0, 9: 0, 10: 0}),
                ("star", {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0.125, 8: 0.275, 9: 0.275, 10: 0.175}),
                ("bullet_bill", {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0.075, 9: 0.225, 10: 0.35}),
                ("green_shell", {1: 0.325, 2: 0.175, 3: 0.15, 4: 0.05, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0}),
                ("trip_green_shell", {1: 0, 2: 0.05, 3: 0.1, 4: 0.075, 5: 0.05, 6: 0.025, 7: 0, 8: 0, 9: 0, 10: 0}),
                ("red_shell", {1: 0, 2: 0.25, 3: 0.25, 4: 0.15, 5: 0.1, 6: 0.05, 7: 0.025, 8: 0, 9: 0, 10: 0}),
                ("trip_red_shell", {1: 0, 2: 0, 3: 0.05, 4: 0.1, 5: 0.1, 6: 0.075, 7: 0.05, 8: 0, 9: 0, 10: 0}),
                ("blue_shell", {1: 0, 2: 0, 3: 0, 4: 0.05, 5: 0.075, 6: 0.075, 7: 0.05, 8: 0, 9: 0, 10: 0}),
                ("bob_omb", {1: 0, 2: 0, 3: 0.025, 4: 0.075, 5: 0.075, 6: 0.05, 7: 0, 8: 0, 9: 0, 10: 0}),
                ("FIB", {1: 0.2, 2: 0.075, 3: 0.05, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0}),
                ("banana", {1: 0.375, 2: 0.2, 3: 0.075, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0}),
                ("trip_bananas", {1: 0.1, 2: 0.125, 3: 0.1, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0})]

all_items_9 = [("lightning_cloud", {1: 0, 2: 0, 3: 0.075, 4: 0.075, 5: 0.05, 6: 0.05, 7: 0, 8: 0, 9: 0}),
               ("lightning_bolt", {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0.075, 9: 0.2}),
               ("blooper", {1: 0, 2: 0, 3: 0, 4: 0.05, 5: 0.075, 6: 0.05, 7: 0.05, 8: 0, 9: 0}),
               ("POW", {1: 0, 2: 0, 3: 0, 4: 0.05, 5: 0.075, 6: 0.05, 7: 0.05, 8: 0, 9: 0}),
               ("mushroom", {1: 0, 2: 0.125, 3: 0.225, 4: 0.15, 5: 0.1, 6: 0, 7: 0, 8: 0, 9: 0}),
               ("trip_mushroom", {1: 0, 2: 0, 3: 0.05, 4: 0.1, 5: 0.25, 6: 0.325, 7: 0.375, 8: 0.125, 9: 0.05}),
               ("gold_mushroom", {1: 0, 2: 0, 3: 0, 4: 0, 5: 0.01, 6: 0.225, 7: 0.275, 8: 0.3, 9: 0.225}),
               ("mega_mushroom", {1: 0, 2: 0, 3: 0.025, 4: 0.075, 5: 0.075, 6: 0.05, 7: 0, 8: 0, 9: 0}),
               ("star", {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0.125, 7: 0.2, 8: 0.275, 9: 0.175}),
               ("bullet_bill", {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0.025, 8: 0.225, 9: 0.35}),
               ("green_shell", {1: 0.325, 2: 0.175, 3: 0.15, 4: 0.05, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}),
               ("trip_green_shell", {1: 0, 2: 0.05, 3: 0.1, 4: 0.075, 5: 0.025, 6: 0, 7: 0, 8: 0, 9: 0}),
               ("red_shell", {1: 0, 2: 0.25, 3: 0.2, 4: 0.15, 5: 0.05, 6: 0.025, 7: 0, 8: 0, 9: 0}),
               ("trip_red_shell", {1: 0, 2: 0, 3: 0.1, 4: 0.1, 5: 0.075, 6: 0.05, 7: 0, 8: 0, 9: 0}),
               ("blue_shell", {1: 0, 2: 0, 3: 0.025, 4: 0.05, 5: 0.075, 6: 0.05, 7: 0.025, 8: 0, 9: 0}),
               ("bob_omb", {1: 0, 2: 0, 3: 0.05, 4: 0.075, 5: 0.05, 6: 0, 7: 0, 8: 0, 9: 0}),
               ("FIB", {1: 0.2, 2: 0.075, 3: 0.025, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}),
               ("banana", {1: 0.375, 2: 0.2, 3: 0.025, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}),
               ("trip_bananas", {1: 0.1, 2: 0.125, 3: 0.025, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0})]

all_items_8 = [("lightning_cloud", {1: 0, 2: 0, 3: 0.075, 4: 0.075, 5: 0.05, 6: 0, 7: 0, 8: 0}),
               ("lightning_bolt", {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0.2}),
               ("blooper", {1: 0, 2: 0, 3: 0, 4: 0.075, 5: 0.075, 6: 0.05, 7: 0, 8: 0}),
               ("POW", {1: 0, 2: 0, 3: 0, 4: 0.05, 5: 0.075, 6: 0.05, 7: 0, 8: 0}),
               ("mushroom", {1: 0, 2: 0.125, 3: 0.225, 4: 0.125, 5: 0.1, 6: 0, 7: 0, 8: 0}),
               ("trip_mushroom", {1: 0, 2: 0, 3: 0.05, 4: 0.15, 5: 0.25, 6: 0.375, 7: 0.3, 8: 0.05}),
               ("gold_mushroom", {1: 0, 2: 0, 3: 0, 4: 0.025, 5: 0.1, 6: 0.275, 7: 0.35, 8: 0.225}),
               ("mega_mushroom", {1: 0, 2: 0, 3: 0.025, 4: 0.1, 5: 0.075, 6: 0, 7: 0, 8: 0}),
               ("star", {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0.2, 7: 0.275, 8: 0.175}),
               ("bullet_bill", {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0.025, 7: 0.075, 8: 0.35}),
               ("green_shell", {1: 0.325, 2: 0.175, 3: 0.075, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0}),
               ("trip_green_shell", {1: 0, 2: 0.05, 3: 0.1, 4: 0.05, 5: 0.025, 6: 0, 7: 0, 8: 0}),
               ("red_shell", {1: 0, 2: 0.25, 3: 0.2, 4: 0.1, 5: 0.05, 6: 0, 7: 0, 8: 0}),
               ("trip_red_shell", {1: 0, 2: 0, 3: 0.1, 4: 0.1, 5: 0.075, 6: 0, 7: 0, 8: 0}),
               ("blue_shell", {1: 0, 2: 0, 3: 0.025, 4: 0.075, 5: 0.075, 6: 0.025, 7: 0, 8: 0}),
               ("bob_omb", {1: 0, 2: 0, 3: 0.05, 4: 0.075, 5: 0.05, 6: 0, 7: 0, 8: 0}),
               ("FIB", {1: 0.2, 2: 0.075, 3: 0.025, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0}),
               ("banana", {1: 0.375, 2: 0.2, 3: 0.025, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0}),
               ("trip_bananas", {1: 0.1, 2: 0.125, 3: 0.025, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0})]

all_items_7 = [("lightning_cloud", {1: 0, 2: 0, 3: 0.025, 4: 0.075, 5: 0.05, 6: 0, 7: 0}),
               ("lightning_bolt", {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0.2}),
               ("blooper", {1: 0, 2: 0, 3: 0.05, 4: 0.075, 5: 0.05, 6: 0, 7: 0}),
               ("POW", {1: 0, 2: 0, 3: 0.05, 4: 0.075, 5: 0.05, 6: 0, 7: 0}),
               ("mushroom", {1: 0, 2: 0.175, 3: 0.15, 4: 0.1, 5: 0, 6: 0, 7: 0}),
               ("trip_mushroom", {1: 0, 2: 0, 3: 0.1, 4: 0.25, 5: 0.375, 6: 0.3, 7: 0.05}),
               ("gold_mushroom", {1: 0, 2: 0, 3: 0, 4: 0.1, 5: 0.275, 6: 0.35, 7: 0.225}),
               ("mega_mushroom", {1: 0, 2: 0, 3: 0.075, 4: 0.075, 5: 0, 6: 0, 7: 0}),
               ("star", {1: 0, 2: 0, 3: 0, 4: 0, 5: 0.2, 6: 0.275, 7: 0.175}),
               ("bullet_bill", {1: 0, 2: 0, 3: 0, 4: 0, 5: 0.025, 6: 0.075, 7: 0.35}),
               ("green_shell", {1: 0.325, 2: 0.15, 3: 0.05, 4: 0, 5: 0, 6: 0, 7: 0}),
               ("trip_green_shell", {1: 0, 2: 0.1, 3: 0.075, 4: 0.025, 5: 0, 6: 0, 7: 0}),
               ("red_shell", {1: 0, 2: 0.25, 3: 0.15, 4: 0.05, 5: 0, 6: 0, 7: 0}),
               ("trip_red_shell", {1: 0, 2: 0.05, 3: 0.1, 4: 0.075, 5: 0, 6: 0, 7: 0}),
               ("blue_shell", {1: 0, 2: 0, 3: 0.05, 4: 0.075, 5: 0.025, 6: 0, 7: 0}),
               ("bob_omb", {1: 0, 2: 0.025, 3: 0.075, 4: 0.05, 5: 0, 6: 0, 7: 0}),
               ("FIB", {1: 0.2, 2: 0.05, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0}),
               ("banana", {1: 0.375, 2: 0.075, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0}),
               ("trip_bananas", {1: 0.1, 2: 0.1, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0})]

all_items_6 = [("lightning_cloud", {1: 0, 2: 0.025, 3: 0.075, 4: 0.05, 5: 0, 6: 0}),
               ("lightning_bolt", {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0.075}),
               ("blooper", {1: 0, 2: 0, 3: 0.05, 4: 0.075, 5: 0.05, 6: 0}),
               ("POW", {1: 0, 2: 0, 3: 0.05, 4: 0.075, 5: 0.05, 6: 0}),
               ("mushroom", {1: 0, 2: 0.175, 3: 0.15, 4: 0.1, 5: 0, 6: 0}),
               ("trip_mushroom", {1: 0, 2: 0, 3: 0.1, 4: 0.25, 5: 0.375, 6: 0.125}),
               ("gold_mushroom", {1: 0, 2: 0, 3: 0, 4: 0.1, 5: 0.275, 6: 0.35}),
               ("mega_mushroom", {1: 0, 2: 0, 3: 0.075, 4: 0.075, 5: 0, 6: 0}),
               ("star", {1: 0, 2: 0, 3: 0, 4: 0, 5: 0.2, 6: 0.275}),
               ("bullet_bill", {1: 0, 2: 0, 3: 0, 4: 0, 5: 0.025, 6: 0.225}),
               ("green_shell", {1: 0.325, 2: 0.15, 3: 0.05, 4: 0, 5: 0, 6: 0}),
               ("trip_green_shell", {1: 0, 2: 0.1, 3: 0.075, 4: 0.025, 5: 0, 6: 0}),
               ("red_shell", {1: 0, 2: 0.25, 3: 0.15, 4: 0.05, 5: 0, 6: 0}),
               ("trip_red_shell", {1: 0, 2: 0.05, 3: 0.1, 4: 0.075, 5: 0, 6: 0}),
               ("blue_shell", {1: 0, 2: 0, 3: 0.05, 4: 0.075, 5: 0.025, 6: 0}),
               ("bob_omb", {1: 0, 2: 0.025, 3: 0.075, 4: 0.05, 5: 0, 6: 0}),
               ("FIB", {1: 0.2, 2: 0.05, 3: 0, 4: 0, 5: 0, 6: 0}),
               ("banana", {1: 0.375, 2: 0.075, 3: 0, 4: 0, 5: 0, 6: 0}),
               ("trip_bananas", {1: 0.1, 2: 0.1, 3: 0, 4: 0, 5: 0, 6: 0})]

all_items_5 = [("lightning_cloud", {1: 0, 2: 0.025, 3: 0.075, 4: 0.05, 5: 0}),
               ("lightning_bolt", {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}),
               ("blooper", {1: 0, 2: 0, 3: 0.05, 4: 0.075, 5: 0}),
               ("POW", {1: 0, 2: 0, 3: 0.05, 4: 0.075, 5: 0}),
               ("mushroom", {1: 0, 2: 0.175, 3: 0.15, 4: 0.1, 5: 0}),
               ("trip_mushroom", {1: 0, 2: 0, 3: 0.1, 4: 0.25, 5: 0.3}),
               ("gold_mushroom", {1: 0, 2: 0, 3: 0, 4: 0.1, 5: 0.35}),
               ("mega_mushroom", {1: 0, 2: 0, 3: 0.075, 4: 0.075, 5: 0}),
               ("star", {1: 0, 2: 0, 3: 0, 4: 0, 5: 0.275}),
               ("bullet_bill", {1: 0, 2: 0, 3: 0, 4: 0, 5: 0.075}),
               ("green_shell", {1: 0.325, 2: 0.15, 3: 0.05, 4: 0, 5: 0}),
               ("trip_green_shell", {1: 0, 2: 0.1, 3: 0.075, 4: 0.025, 5: 0}),
               ("red_shell", {1: 0, 2: 0.25, 3: 0.15, 4: 0.05, 5: 0}),
               ("trip_red_shell", {1: 0, 2: 0.05, 3: 0.1, 4: 0.075, 5: 0}),
               ("blue_shell", {1: 0, 2: 0, 3: 0.05, 4: 0.075, 5: 0}),
               ("bob_omb", {1: 0, 2: 0.025, 3: 0.075, 4: 0.05, 5: 0}),
               ("FIB", {1: 0.2, 2: 0.05, 3: 0, 4: 0, 5: 0}),
               ("banana", {1: 0.375, 2: 0.075, 3: 0, 4: 0, 5: 0}),
               ("trip_bananas", {1: 0.1, 2: 0.1, 3: 0, 4: 0, 5: 0})]

all_items_4 = [("lightning_cloud", {1: 0, 2: 0.025, 3: 0.075, 4: 0}),
               ("lightning_bolt", {1: 0, 2: 0, 3: 0, 4: 0}),
               ("blooper", {1: 0, 2: 0, 3: 0.075, 4: 0.05}),
               ("POW", {1: 0, 2: 0, 3: 0.05, 4: 0.05}),
               ("mushroom", {1: 0, 2: 0.175, 3: 0.125, 4: 0}),
               ("trip_mushroom", {1: 0, 2: 0, 3: 0.15, 4: 0.375}),
               ("gold_mushroom", {1: 0, 2: 0, 3: 0.025, 4: 0.275}),
               ("mega_mushroom", {1: 0, 2: 0, 3: 0.1, 4: 0}),
               ("star", {1: 0, 2: 0, 3: 0, 4: 0.2}),
               ("bullet_bill", {1: 0, 2: 0, 3: 0, 4: 0.025}),
               ("green_shell", {1: 0.325, 2: 0.15, 3: 0, 4: 0}),
               ("trip_green_shell", {1: 0, 2: 0.1, 3: 0.05, 4: 0}),
               ("red_shell", {1: 0, 2: 0.25, 3: 0.1, 4: 0}),
               ("trip_red_shell", {1: 0, 2: 0.05, 3: 0.1, 4: 0}),
               ("blue_shell", {1: 0, 2: 0, 3: 0.075, 4: 0.025}),
               ("bob_omb", {1: 0, 2: 0.025, 3: 0.075, 4: 0}),
               ("FIB", {1: 0.2, 2: 0.05, 3: 0, 4: 0}),
               ("banana", {1: 0.375, 2: 0.075, 3: 0, 4: 0}),
               ("trip_bananas", {1: 0.1, 2: 0.1, 3: 0, 4: 0})]

all_items_3 = [("lightning_cloud", {1: 0, 2: 0.025, 3: 0.075}),
               ("lightning_bolt", {1: 0, 2: 0, 3: 0}),
               ("blooper", {1: 0, 2: 0, 3: 0.075}),
               ("POW", {1: 0, 2: 0, 3: 0.05}),
               ("mushroom", {1: 0, 2: 0.175, 3: 0.125}),
               ("trip_mushroom", {1: 0, 2: 0, 3: 0.15}),
               ("gold_mushroom", {1: 0, 2: 0, 3: 0.025}),
               ("mega_mushroom", {1: 0, 2: 0, 3: 0.1}),
               ("star", {1: 0, 2: 0, 3: 0}),
               ("bullet_bill", {1: 0, 2: 0, 3: 0}),
               ("green_shell", {1: 0.325, 2: 0.15, 3: 0}),
               ("trip_green_shell", {1: 0, 2: 0.1, 3: 0.05}),
               ("red_shell", {1: 0, 2: 0.25, 3: 0.1}),
               ("trip_red_shell", {1: 0, 2: 0.05, 3: 0.1}),
               ("blue_shell", {1: 0, 2: 0, 3: 0.075}),
               ("bob_omb", {1: 0, 2: 0.025, 3: 0.075}),
               ("FIB", {1: 0.2, 2: 0.05, 3: 0}),
               ("banana", {1: 0.375, 2: 0.075, 3: 0}),
               ("trip_bananas", {1: 0.1, 2: 0.1, 3: 0})]

all_items_2 = [("lightning_cloud", {1: 0, 2: 0.075}),
               ("lightning_bolt", {1: 0, 2: 0}),
               ("blooper", {1: 0, 2: 0}),
               ("POW", {1: 0, 2: 0}),
               ("mushroom", {1: 0, 2: 0.225}),
               ("trip_mushroom", {1: 0, 2: 0.05}),
               ("gold_mushroom", {1: 0, 2: 0}),
               ("mega_mushroom", {1: 0, 2: 0.025}),
               ("star", {1: 0, 2: 0}),
               ("bullet_bill", {1: 0, 2: 0}),
               ("green_shell", {1: 0.325, 2: 0.075}),
               ("trip_green_shell", {1: 0, 2: 0.1}),
               ("red_shell", {1: 0, 2: 0.2}),
               ("trip_red_shell", {1: 0, 2: 0.1}),
               ("blue_shell", {1: 0, 2: 0.025}),
               ("bob_omb", {1: 0, 2: 0.05}),
               ("FIB", {1: 0.2, 2: 0.025}),
               ("banana", {1: 0.375, 2: 0.025}),
               ("trip_bananas", {1: 0.1, 2: 0.025})]

# Where all the other functions will get called and where we will create the animation
def main():
    # Checks if the user inputs an integer between 2 and 12
    # The error handling at the bottom will handle the cases where the user inputs a string
    n = input("Enter number of racers: ")
    if (int(n) != float(n)) or (float(n) < 2.0) or (float(n) > 12.0):
        print("Must input an integer between 2 and 12, inclusive.")
        sys.exit()
    num_racers = int(n)

    # Select int(n) racers at random from the list of all racers
    participants = random.sample(all_racers, num_racers)
    initial_positions = [i for i in range(1, num_racers + 1)]

    # Assign each participant an initial position and initial distance from the starting line
    # Will probably need to change the -1 to something else depending on the size of the race track
    for j in range(len(participants)):
        participants[j].position = initial_positions[j]
        participants[j].distance_from_start = -1 * initial_positions[j]
        
    # TO BE CONTINUED

# Error handling
if len(sys.argv) != 1:
    print("Invalid number of inputs.")
    sys.exit()
else:
    try:
        main()
    except:
        print("Unexpected error occurred. Must input an integer between 2 and 12, inclusive.")