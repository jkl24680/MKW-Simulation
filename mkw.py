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
        # Before the race starts, everyone has a speed pf 0.
        if weight == "Light":
            s = 23 * random.uniform(1.0, 1.5)
            self.speed = 0
            self.max_speed = s
        if weight == "Medium":
            s = 25 * random.uniform(1.0, 1.5)
            self.speed = 0
            self.max_speed = s
        if weight == "Heavy":
            s = 27 * random.uniform(1.0, 1.5)
            self.speed = 0
            self.max_speed = s

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

        # Assigns a list of status effects that helps in the use_item() method. All racers will begin with no status effects
        self.status = []

        # Racers_passed is used to stop the bullet bill after passing 5 karts. All racers will begin with 0 racers
        # passed
        self.racers_passed = 0


def update_position(racer1, racer2):
    if "mega" in racer1.status or "invulnerable" in racer1.status:
        racer2.status.append("stunned")
        racer2.speed = 0
        if racer1.item == "bullet_bill":
            racer1.racers_passed += 1
    racer1.position, racer2.position = racer2.position, racer1.position


def update_distance(racer, time):
    # Changes the distance the racer has traveled in a certain time (in this case I used 1 second, but we can change
    # it based on how the race looks and the processing power of our computers). This also assumes the racer speeds
    # are all in m/s
    distance = racer.distance_from_start + (racer.speed * time)
    racer.distance_from_start = distance


def update_speed(racer, time):
    # Adjusts the speed of the racer based on its acceleration. The method assumes 1 second has passed
    if racer.speed < racer.max_speed:
        speed = racer.speed + racer.acceleration * time
        racer.speed = speed

    # For decelerating back to initial speed after racer uses a mushroom or something
    if racer.speed > racer.max_speed:
        speed = racer.speed - racer.acceleration * time
        racer.speed = speed


def choose_item(choices, position):
    total = sum(weight[position] for _, weight in choices)
    r = random.uniform(0, total)
    subtotal = 0

    for item, weight in choices:
        subtotal += weight[position]
        if subtotal >= r:
            return item


# Gets all possible items a racer at a certain position can pull
def possible_items(position, probability_list):
    return [item[0] for item in probability_list if item[1][position] != 0]


# Updates the item probabilities based on what is currently unavailable
# This is so we can take into account the item limits and timing limits
def update_probabilities(items, probability_list, position):
    other_items = []
    sum_prob_items = 0
    for possible_item in probability_list:
        if possible_item[0] in items:
            sum_prob_items += possible_item[1][position]
        if possible_item[0] not in items and possible_item[1][position] != 0:
            other_items.append(possible_item[0])
    for possible_item in probability_list:
        if possible_item[0] in other_items:
            possible_item[1][position] += (sum_prob_items / len(other_items))
        if possible_item[0] in items:
            possible_item[1][position] = 0
    return probability_list


def get_item(racer, num_racers, Unavailable_items):
    if num_racers == 2:
        if not Unavailable_items or racer.position == 1 or not any(
                item in possible_items(racer.position, all_items_2) for item in Unavailable_items):
            item = choose_item(all_items_2, racer.position)
            racer.item = item
        else:
            item = choose_item(update_probabilities(Unavailable_items, all_items_2, racer.position), racer.position)
            racer.item = item
    if num_racers == 3:
        if not Unavailable_items or racer.position == 1 or not any(
                item in possible_items(racer.position, all_items_3) for item in Unavailable_items):
            item = choose_item(all_items_3, racer.position)
            racer.item = item
        else:
            item = choose_item(update_probabilities(Unavailable_items, all_items_3, racer.position), racer.position)
            racer.item = item
    if num_racers == 4:
        if not Unavailable_items or racer.position == 1 or not any(
                item in possible_items(racer.position, all_items_4) for item in Unavailable_items):
            item = choose_item(all_items_4, racer.position)
            racer.item = item
        else:
            item = choose_item(update_probabilities(Unavailable_items, all_items_4, racer.position), racer.position)
            racer.item = item
    if num_racers == 5:
        if not Unavailable_items or racer.position == 1 or not any(
                item in possible_items(racer.position, all_items_5) for item in Unavailable_items):
            item = choose_item(all_items_5, racer.position)
            racer.item = item
        else:
            item = choose_item(update_probabilities(Unavailable_items, all_items_5, racer.position), racer.position)
            racer.item = item
    if num_racers == 6:
        if not Unavailable_items or racer.position == 1 or not any(
                item in possible_items(racer.position, all_items_6) for item in Unavailable_items):
            item = choose_item(all_items_6, racer.position)
            racer.item = item
        else:
            item = choose_item(update_probabilities(Unavailable_items, all_items_6, racer.position), racer.position)
            racer.item = item
    if num_racers == 7:
        if not Unavailable_items or racer.position == 1 or not any(
                item in possible_items(racer.position, all_items_7) for item in Unavailable_items):
            item = choose_item(all_items_7, racer.position)
            racer.item = item
        else:
            item = choose_item(update_probabilities(Unavailable_items, all_items_7, racer.position), racer.position)
            racer.item = item
    if num_racers == 8:
        if not Unavailable_items or racer.position in [1, 2] or not any(
                item in possible_items(racer.position, all_items_8) for item in Unavailable_items):
            item = choose_item(all_items_8, racer.position)
            racer.item = item
        else:
            item = choose_item(update_probabilities(Unavailable_items, all_items_8, racer.position), racer.position)
            racer.item = item
    if num_racers == 9:
        if not Unavailable_items or racer.position in [1, 2] or not any(
                item in possible_items(racer.position, all_items_9) for item in Unavailable_items):
            item = choose_item(all_items_9, racer.position)
            racer.item = item
        else:
            item = choose_item(update_probabilities(Unavailable_items, all_items_9, racer.position), racer.position)
            racer.item = item
    if num_racers == 10:
        if not Unavailable_items or racer.position in [1, 2] or not any(
                item in possible_items(racer.position, all_items_10) for item in Unavailable_items):
            item = choose_item(all_items_10, racer.position)
            racer.item = item
        else:
            item = choose_item(update_probabilities(Unavailable_items, all_items_10, racer.position), racer.position)
            racer.item = item
    if num_racers == 11:
        if not Unavailable_items or racer.position in [1, 2] or not any(
                item in possible_items(racer.position, all_items_11) for item in Unavailable_items):
            item = choose_item(all_items_11, racer.position)
            racer.item = item
        else:
            item = choose_item(update_probabilities(Unavailable_items, all_items_11, racer.position), racer.position)
            racer.item = item
    if num_racers == 12:
        if not Unavailable_items or racer.position in [1, 2] or not any(
                item in possible_items(racer.position, all_items_12) for item in Unavailable_items):
            item = choose_item(all_items_12, racer.position)
            racer.item = item
        else:
            item = choose_item(update_probabilities(Unavailable_items, all_items_12, racer.position), racer.position)
            racer.item = item


# The racer using the item and the list of participants are the input arguments
def use_item(racer, participants):
    # THE LIGHTNING CLOUD IS USED IMMEDIATELY UPON OBTAINING IT, BE AWARE OF THIS IN main()
    # Also the racer won't lose the lightning cloud until it zaps them
    if racer.item == "lightning_cloud":
        if "mega" in racer.status or "invulnerable" in racer.status:
            racer.item = None
        else:
            time = 0
            speed = racer.speed  # Speed was defined before the while loop so the speed only decreases at the initial item usage and not throughout the while loop
            racer.status.append("TC")
            while time <= 9:
                if "shrunk" in racer.status or "inked" in racer.status:
                    if time < 5:
                        # Instantaneous acceleration for lightning clouds for the first few seconds
                        while racer.speed != 1.1 * speed and "stunned" not in racer.status and "sped up" not in racer.status:
                            racer.speed = 1.1 * speed

                    elif 5 <= time <= 6:
                        racer.speed = 0
                        racer.item = None
                    else:
                        time_accel1 = 1
                        while racer.speed != 0.35 * racer.initial_speed:
                            update_speed(racer, time_accel1)
                            time_accel1 += 1

                else:
                    if time < 5:
                        while racer.speed != 1.1 * speed and "stunned" not in racer.status and "sped up" not in racer.status:
                            racer.speed = 1.1 * racer.initial_speed
                    elif 5 <= time <= 6:
                        racer.speed = 0
                        racer.item = None
                    else:
                        time_accel2 = 1
                        while racer.speed != 0.35 * racer.initial_speed:
                            update_speed(racer, time_accel2)
                            time_accel2 += 1
                time += 1
            racer.status.remove("TC")

    if racer.item == "lightning_bolt":
        # Removes the item from the user's inventory the moment it gets used (that's how it works in the game)
        racer.item = None
        time = 0
        for other_racer in participants:
            if other_racer != racer:
                if "sped up" in other_racer.status:
                    other_racer.status.remove("sped up")
                if "mega" in other_racer.status and "invulnerable" not in other_racer.status:
                    other_racer.status.remove("mega")
                elif "invulnerable" in other_racer.status:
                    pass
                else:
                    other_racer.status.append("shrunk")
        while time <= 4:
            if time <= 1:
                for other_racer in participants:
                    if "shrunk" in other_racer.status:

                        # Cannot shock out a lightning cloud from another racer
                        if other_racer.item == "lightning_cloud":
                            other_racer.speed = 0
                        else:
                            other_racer.item = None
                            other_racer.speed = 0
            else:
                for kart in participants:
                    if "shrunk" in kart.status:
                        # Accelerates each racer to their reduced speed
                        time_accel2 = 1
                        while kart.speed != 0.35 * kart.initial_speed:
                            update_speed(kart, time_accel2)
                            time_accel2 += 1
            time += 1
        for other_racer in participants:
            if "shrunk" in other_racer.status:
                other_racer.status.remove("shrunk")

    if racer.item == "blooper":
        # Removes the item from the user's inventory the moment it gets used
        racer.item = None
        time = 0
        for other_racer in participants:
            if other_racer.position < racer.position:
                # Mushrooms override blooper effects
                if "invulnerable" not in other_racer.status and "mega" not in other_racer.status and "sped up" not in other_racer.status:
                    other_racer.status.append("inked")
        while time <= 5:
            for other_racer in participants:
                if "inked" in other_racer.status:
                    if "TC" in other_racer.status or "shrunk" in other_racer.status:
                        time_accel1 = 1
                        s = 0.9 * other_racer.speed
                        while other_racer.speed != s and "stunned" not in other_racer.status:
                            update_speed(other_racer, time_accel1)
                            time_accel1 += 1

                    else:
                        time_accel2 = 1
                        while other_racer.speed != 0.9 * other_racer.initial_speed and "stunned" not in other_racer.status:
                            update_speed(other_racer, time_accel2)
                            time_accel2 += 1
            time += 1
        for other_racer in participants:
            if "inked" in other_racer.status:
                other_racer.status.remove("inked")

    if racer.item == "POW":
        # Removes the item from the user's inventory the moment it gets used
        racer.item = None
        time = 0
        for other_racer in participants:
            if other_racer.position < racer.position:
                if "invulnerable" not in other_racer.status and "mega" not in other_racer.status:
                    other_racer.status.append("stunned")
                    other_racer.status.append("POW'd")
                if "sped up" in other_racer.status:
                    other_racer.status.remove("sped up")
        while time <= 2:
            for other_racer in participants:
                if "stunned" in other_racer.status and "POW'd" in other_racer.status:

                    # Cannot pow out a lightning cloud from a racer
                    if other_racer.item == "lightning_cloud":
                        other_racer.speed = 0
                    else:
                        other_racer.item = None
                        other_racer.speed = 0
            time += 1
        for other_racer in participants:
            # Having 2 statuses added to the list at first allows us to make sure that only the racers that get POW'd
            # get their stunned status removed after 2 seconds.
            if "stunned" in other_racer.status and "POW'd" in other_racer.status:
                other_racer.status.remove("stunned")
                other_racer.status.remove("POW'd")

    if racer.item == "mushroom":
        # Removes the item from the inventory the moment it gets used
        racer.item = None
        time = 0
        speed = racer.speed
        racer.status.append("sped up")

        # Mushrooms remove blooper effects
        if "inked" in racer.status:
            racer.status.remove("inked")
        while time <= 2 and "sped up" in racer.status:
            
            # To account for mushroom being used when small
            if "shrunk" in racer.status or "TC" in racer.status:
                racer.speed = 1.5 * speed
            else:
                racer.speed = 1.5 * racer.initial_speed
            time += 1
        if "sped up" in racer.status:
            racer.status.remove("sped up")
            racer.speed = racer.initial_speed

    if racer.item == "trip_mushroom":
        time = 0
        speed = racer.speed
        racer.status.append("sped up")
        if "inked" in racer.status:
            racer.status.remove("inked")
        while time <= 6 and "sped up" in racer.status:
            if "shrunk" in racer.status or "TC" in racer.status:
                racer.speed = 1.5 * speed
            else:
                racer.speed = 1.5 * racer.initial_speed
            time += 1
        if "sped up" in racer.status:
            racer.status.remove("sped up")
            racer.speed = racer.initial_speed
        # In the actual game, your item gets fully removed from your inventory when the 3rd mushroom is used,
        # but here, we'll keep it simple and assume that it gets fully removed after the effects of all 3 mushrooms
        # runs out
        racer.item = None

    if racer.item == "gold_mushroom":
        time = 0
        speed = racer.speed
        racer.status.append("sped up")
        if "inked" in racer.status:
            racer.status.remove("inked")
        while time <= 9 and "sped up" in racer.status:
            if "shrunk" in racer.status or "TC" in racer.status:
                racer.speed = 1.5 * speed
            else:
                racer.speed = 1.5 * racer.initial_speed
            time += 1
        if "sped up" in racer.status:
            racer.status.remove("sped up")
            racer.speed = racer.initial_speed
        # In the actual game, the item is fully removed from inventory after the effect runs out
        racer.item = None

    if racer.item == "star":
        # Remove item from inventory the moment it gets used
        racer.item = None
        time = 0
        racer.status.append("invulnerable")
        if "inked" in racer.status:
            racer.status.remove("inked")
        speed = racer.speed
        while time <= 10 and "bill" not in racer.status:
            if "shrunk" in racer.status or "TC" in racer.status:
                racer.speed = 1.3 * speed
            else:
                racer.speed = 1.3 * racer.initial_speed
            # Have to find out how to code in hitting other karts
            time += 1
        if "invulnerable" in racer.status and "bill" not in racer.status:
            racer.status.remove("invulnerable")
            
    if racer.item == "mega_mushroom":
        # Remove item from inventory the moment it gets used
        racer.item = None
        time = 0
        racer.status.append("mega")

        # The mega mushroom removes all these effects
        if "inked" in racer.status:
            racer.status.remove("inked")
        if "shrunk" in racer.status:
            racer.status.remove("shrunk")
        if "TC" in racer.status:
            racer.status.remove("TC")
        speed = racer.speed
        while time <= 10 and "mega" in racer.status:
            if "invulnerable" not in racer.status:
                racer.speed = 1.1 * racer.initial_speed
            else:
                racer.speed = 1.1 * speed
            time += 1
            # Have to find out how to code in hitting other karts
        if "mega" in racer.status:
            racer.status.remove("mega")
            racer.speed = racer.initial_speed

    if racer.item == "bullet_bill":
        
        time = 0
        if "inked" in racer.status:
            racer.status.remove("inked")
        if "mega" in racer.status:
            racer.status.remove("mega")
        if "shrunk" in racer.status:
            racer.status.remove("shrunk")
        if "TC" in racer.status:
            racer.status.remove("TC")

        # If the user is currently in a star when they use the bullet bill, remove the invulnerable status
        # and add it again to guarantee that nothing weird happens
        if "invulnerable" in racer.status:
            racer.status.remove("invulnerable")

        # The 'bill' status is required for a very specific situation in which the user activates the bill while in a star
        # Don't want the code to break because of this
        racer.status.append("invulnerable")
        racer.status.append("bill")
        

        if racer.position == 1:
            while time <= 2:
                racer.speed = 2 * racer.initial_speed
                time += 1
        else:
            while time <= 8 | racer.racers_passed < 5 | racer.position != 1:
                racer.speed = 2 * racer.initial_speed
                time += 1
        racer.speed = racer.initial_speed
        racer.racers_passed = 0
        racer.status.remove("invulnerable")
        racer.status.remove("bill")

        # Bullet bills don't disappear from inventory until they run out
        racer.item = None

    if racer.item == "green_shell":
        racer.item = None
        action = random.random()
        time = 0
        while time <= 1:
            if racer.position == 1:
                if 0 <= action <= 0.4:
                    for other_racer in participants:
                        if other_racer.position == racer.position + 1:
                            if other_racer.status != "invulnerable":
                                kart = other_racer
                                kart.status = "stunned"
                                kart.speed = 0

            elif racer.position == len(participants) + 1:
                if 0 <= action <= 0.4:
                    for other_racer in participants:
                        if other_racer.position == racer.position - 1:
                            if other_racer.status != "invulnerable":
                                kart = other_racer
                                kart.status = "stunned"
                                kart.speed = 0

            else:
                if 0 <= action <= 0.3:
                    for other_racer in participants:
                        if other_racer.position == racer.position + 1:
                            if other_racer.status != "invulnerable":
                                kart = other_racer
                                kart.status = "stunned"
                                kart.speed = 0
                elif 0.3 < action <= 0.6:
                    for other_racer in participants:
                        if other_racer.position == racer.position - 1:
                            if other_racer.status != "invulnerable":
                                kart = other_racer
                                kart.status = "stunned"
                                kart.speed = 0

            time += 1
        kart.status = None

    if racer.item == "trip_green_shell":
        racer.item = None
        action = random.random()
        time = 0

        while time <= 1:
            if racer.position == 1:
                if 0 <= action <= 0.5:
                    for other_racer in participants:
                        if other_racer.position == racer.position + 1:
                            if other_racer.status != "invulnerable":
                                kart = other_racer
                                kart.status = "stunned"
                                kart.speed = 0
                elif 0.5 < action < 0.9:
                    for other_racer in participants:
                        if other_racer.position == racer.position + 1:
                            kart1 = other_racer
                        everyone_else = [r for r in participants if r != kart1]
                        kart = random.choice(everyone_else)
                        if kart.status != "invulnerable":
                            kart.status = "stunned"
                            kart.speed = 0

            elif racer.position == len(participants) + 1:
                if 0 <= action <= 0.5:
                    for other_racer in participants:
                        if other_racer.position == racer.position - 1:
                            if other_racer.status != "invulnerable":
                                kart = other_racer
                                kart.status = "stunned"
                                kart.speed = 0
                elif 0.5 < action < 0.9:
                    for other_racer in participants:
                        if other_racer.position == racer.position - 1:
                            kart1 = other_racer
                        everyone_else = [r for r in participants if r != kart1]
                        kart = random.choice(everyone_else)
                        if kart.status != "invulnerable":
                            kart.status = "stunned"
                            kart.speed = 0

            else:
                if 0 <= action <= 0.35:
                    for other_racer in participants:
                        if other_racer.position == racer.position + 1:
                            if other_racer.status != "invulnerable":
                                kart = other_racer
                                kart.status = "stunned"
                                kart.speed = 0

                elif 0.35 < action <= 0.7:
                    for other_racer in participants:
                        if other_racer.position == racer.position - 1:
                            if other_racer.status != "invulnerable":
                                kart = other_racer
                                kart.status = "stunned"
                                kart.speed = 0

                elif 0.7 < action <= 0.9:
                    for other_racer in participants:
                        if other_racer.position == racer.position + 1:
                            kart1 = other_racer
                        if other_racer.position == racer.position - 1:
                            kart2 = other_racer
                        everyone_else = [r for r in participants if r != kart1 & r != kart2]
                        kart = random.choice(everyone_else)
                        if kart.status != "invulnerable":
                            kart.status = "stunned"
                            kart.speed = 0
            time += 1
        kart.status.remove("stunned")


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

    # a list of items that racers are currently unable to obtain due to item/timing limits
    # When a race starts, these 4 items will be unavailable until a certain period of time has passed (check item probability site)
    # WILL NEED TO BE UPDATED THROUGHOUT THE RACE
    # For simplicity, there will be 6 items that can become unavailable: the 4 already on the list and the bullet bill and lightning cloud
    unavailable_items = ["blooper", "blue_shell", "POW", "lightning_bolt"]

    # Select int(n) racers at random from the list of all racers
    participants = random.sample(all_racers, num_racers)
    initial_positions = [i for i in range(1, num_racers + 1)]

    # Assign each participant an initial position and initial distance from the starting line
    # Will probably need to change the -1 to something else depending on the size of the race track
    for j in range(len(participants)):
        participants[j].position = initial_positions[j]
        participants[j].distance_from_start = -1 * initial_positions[j]

    # Causes racers to accelerate or decelerate back to their initial speed
    # Not sure if this is how to do it though
    # INCLUDE THIS IN THE BIG WHILE LOOP ONCE WE MAKE THAT
    for racer in participants:
        time_accel = 1
        while (participants[racer].speed != participants[racer].initial_speed) and (not participants[racer].status):
                                                                                    
            update_speed(participants[racer], time_accel)
            time_accel += 1

        # Sets time_accel back to 1 so it's not stuck at the value it was after the while loop ended
        # Not sure if this line is needed though
        time_accel = 1

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
