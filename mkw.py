import random
import sys

race_duration = 0

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

        # Stores when a racer gets an item from an item box
        self.time_item_got = 0

        # The time that must pass before a racer uses an item after getting one
        # is an integer from 3-5
        self.time_delay = 0

        # To account for a very specific scenario in this a racer gets zapped by lightning bolt or lightning cloud when they're
        # already shrunk or squished. Since self.status is a list, we can't simply append "stunned" to the list since everything is in a while
        # loop and multiple "stunned" will be appended, which we don't want.
        self.shocked = False

        # Stores whether a racer with a lightning cloud is currently in the initial phase where they speed up
        # or in the final phase where they are shocked and slowed down
        # Mainly used to account for very specific scenarios that have potential to break the code
        self.TC_initial = False
        self.TC_final = False

        # For very specifc scnearios where a racer has at least one of these status and needs to accelerate
        # to their max speed based on which ones they have
        def max_speed_slowdown(self):
            if ("shrunk" in self.status and "inked" not in self.status and "squished" not in self.status) or ("squished" in 
                            self.status and "shrunk" not in self.status and "inked" not in self.status):
                speed = 0.35 * self.max_speed
            elif "inked" in self.status and "shrunk" not in self.status and "squished" not in self.status:
                speed = 0.9 * self.max_speed
            elif ("shrunk" in self.status and "inked" in self.status and "squished" not in self.status) or ("squished" in
                            self.status and "inked" in self.status and "shrunk" not in self.status):
                speed = 0.35 * 0.9 * self.max_speed
            elif "shrunk" in self.status and "squished" in self.status and "inked" not in self.status:
                speed = 0.35 * 0.35 * self.max_speed
            elif "shrunk" in self.status and "inked" in self.status and "squished" in self.status:
                speed = 0.35 * 0.35 * 0.9 * self.max_speed
            else: 
                speed = self.max_speed
            return speed

def update_position(racer1, racer2):
    racer1.position, racer2.position = racer2.position, racer1.position

    # 50% chance of racers in stars and bullet bills hitting the racers they pass
    action = random.random()
    time = race_duration.copy()
    if "invulnerable" in racer1.status and "bill" not in racer1.status:
        if 0 <= action <= 0.5:
            if ("POW'd" not in racer2.status) and ("stunned" not in racer2.status) and ("1s_stun" 
                                                    not in racer2.status) and "3s_stun" not in racer2.status:
                if "sped up" in racer2.status and "invulnerable" not in racer2.status:
                    racer2.status.remove("sped up")
                
                # Normally the star wouldn't take away the mega effect, but let's make things easier for ourselves
                if "mega" in racer2.status and "invulnerable" not in racer2.status:
                    racer2.status.remove("mega")
                if "invulnerable" not in racer2.status:
                    racer2.status.append("stunned")
                    racer2.status.append("1s_stun")
                while race_duration <= time + 1 and "stunned" in racer2.status and "1s_stun" in racer2.status:
                    if racer2.item == "lightning_cloud":
                        racer2.speed = 0
                    else:
                        racer2.speed = 0
                        racer2.item = None
                if "stunned" in racer2.status and "1s_stun" in racer2.status:
                    racer2.status.remove("stunned")
                    racer2.status.remove("1s_stun")

    if "bill" in racer1.status:
        racer1.racers_passed += 1
        if 0 <= action <= 0.5:
            if "3s_stun" not in racer2.status:
                if "mega" in racer2.status and "invulnerable" not in racer2.status:
                    racer2.status.remove("mega")
                if "stunned" in racer2.status:
                    racer2.status.remove("stunned")
                if "1s_stun" in racer2.status:
                    racer2.status.remove("1s_stun")
                if "POW'd" in racer2.status:
                    racer2.status.remove("POW'd")
                if "sped up" in racer2.status and "invulnerable" not in racer2.status:
                    racer2.status.remove("sped up")
                if "invulnerable" not in racer2.status:
                    racer2.status.append("stunned")
                    racer2.status.append("3s_stun")
                while race_duration <= time + 3 and "stunned" in racer2.status and "3s_stun" in racer2.status:
                    if racer2.item == "lightning_cloud":
                        racer2.speed = 0
                    else:
                        racer2.speed = 0
                        racer2.item = None
                    time += 1
                racer2.status.remove("stunned")
                racer2.status.remove("3s_stun")

    if "mega" in racer1.status and "invulnerable" not in racer1.status:
        if 0 <= action <= 0.5:
        
            if "sped up" in racer2.status:
                racer2.status.remove("sped up")
            if "invulnerable" not in racer2.status and "mega" not in racer2.status:
                racer2.status.append("squished")
            while race_duration <= time + 4 and "squished" in racer2.status:
                if race_duration <= time + 1:
                    if racer2.item == "lightning_cloud":
                        racer2.speed = 0
                        racer2.shocked = True
                    else:
                        racer2.shocked = True
                        racer2.item = None
                        racer2.speed = 0
                else:
                    racer2.shocked = False
                    if "squished" in racer2.status:
                        if racer2.TC_initial == True and "shrunk" not in racer2.status and "inked" not in racer2.status:
                            if (racer2.speed != 0.35 * 1.1 * racer2.max_speed 
                                   and "stunned" not in racer2.status and racer2.shocked == False):
                                racer2.speed = 0.35 * 1.1 * racer2.max_speed
                        elif racer2.TC_initial == True and ("shrunk" in racer2.status or "inked" in racer2.status):
                            if (racer2.speed != 1.1 * racer2.max_speed_slowdown() 
                                   and "stunned" not in racer2.status and racer2.shocked == False):
                                racer2.speed = 1.1 * racer2.max_speed_slowdown()
                        elif racer2.TC_final == True and "shrunk" not in racer2.status:    
                            if racer2.speed != 0.35 * racer2.max_speed_slowdown() and "stunned" not in racer2.status and racer2.shocked == False:
                                update_speed(racer2, 1)     
                        else:
                            if racer2.speed != racer2.max_speed_slowdown() and "stunned" not in racer2.status and racer2.shocked == False:
                                update_speed(racer2, 1)  
            if "squished" in racer2.status:
                racer2.status.remove("squished")

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

# Stuns the racer for 1 second (used in use_item)
def one_sec_stun(racer, time):
    
    if ("POW'd" not in racer.status) and ("stunned" not in 
                            racer.status) and ("1s_stun" not in racer.status) and "3s_stun" not in racer.status:
        if "sped up" in racer.status and "invulnerable" not in racer.status and "mega" not in racer.status:
            racer.status.remove("sped up")
        if "invulnerable" not in racer.status and "mega" not in racer.status:
            racer.status.append("stunned")
            racer.status.append("1s_stun")
        while race_duration <= time + 1 and "stunned" in racer.status and "1s_stun" in racer.status:
            racer.speed = 0
        if "stunned" in racer.status and "1s_stun" in racer.status:
            racer.status.remove("stunned")
            racer.status.remove("1s_stun")

# Stuns the racer for 3 seconds (used in use_item)
def three_sec_stun(racer, time):
    
    if "3s_stun" not in racer.status:
        if "stunned" in racer.status:
            racer.status.remove("stunned")
        if "1s_stun" in racer.status:
            racer.status.remove("1s_stun")
        if "POW'd" in racer.status:
            racer.status.remove("POW'd")
        if "sped up" in racer.status and "invulnerable" not in racer.status and "mega" not in racer.status:
            racer.status.remove("sped up")
        if "invulnerable" not in racer.status and "mega" not in racer.status:
            racer.status.append("stunned")
            racer.status.append("3s_stun")
            if racer.item != "lightning_cloud":
                racer.item = None
        while race_duration <= time + 3 and "stunned" in racer.status and "3s_stun" in racer.status:
            racer.speed = 0
        racer.status.remove("stunned")
        racer.status.remove("3s_stun")

def banana_slowdown(racer):
    speed = racer.speed
    if ("POW'd" not in racer.status) and ("stunned" not in 
                            racer.status) and ("1s_stun" not in racer.status) and "3s_stun" not in racer.status:
        if "sped up" in racer.status and "invulnerable" not in racer.status and "mega" not in racer.status:
            racer.status.remove("sped up")
        if "invulnerable" not in racer.status and "mega" not in racer.status:
            racer.speed = 0.5 * speed
                

# The racer using the item and the list of participants are the input arguments
'''
Additional notes on items: If a racer is currently stunned by a green or red shell, other red or green shells that hit them will
have no effect. Pow blocks will override the green or red shell hit, and bombs and blue shells will override the POW block stun
and thus will also override green or red shell stun.

The "1s_stun" status is the status used when a racer gets stunned by one of the items that only stuns for 1 second.
The "3s_stun" status is the status used when a racer gets stunned by one of the items that stuns for 3 seconds.
'''
def use_item(racer, participants):
    time = race_duration.copy()
    # THE LIGHTNING CLOUD IS USED IMMEDIATELY UPON OBTAINING IT, BE AWARE OF THIS IN main()
    # Also the racer won't lose the lightning cloud until it zaps them
    if racer.item == "lightning_cloud":
        if "mega" in racer.status or "invulnerable" in racer.status:
            racer.item = None
        else:
            speed = racer.speed  # Speed was defined before the while loop so the speed only decreases at the initial item usage and not throughout the while loop
            racer.status.append("TC")
            racer.TC_initial = True
            while race_duration <= time + 9 and "TC" in racer.status:
                if "shrunk" in racer.status or "inked" in racer.status or "squished" in racer.status:
                    if race_duration < time + 5: 
                        if (racer.speed != 1.1 * racer.max_speed_slowdown() and "stunned" not in racer.status 
                                and "sped up" not in racer.status and racer.shocked == False):
                            # Instantaneous acceleration for lightning clouds for the first few seconds
                            racer.speed = 1.1 * racer.max_speed_slowdown()

                    elif (time + 5) <= race_duration <= (time + 6):
                        racer.speed = 0
                        racer.item = None
                        racer.TC_initial = False
                        racer.shocked = True
                    else:
                        racer.TC_final = True
                        racer.shocked = False
                        if racer.speed != racer.max_speed_slowdown() and "stunned" not in racer.status and racer.shocked == False:
                            update_speed(racer, 1)
                else:
                    if race_duration < time + 5: 
                        if (racer.speed != 1.1 * racer.max_speed and "stunned" not in racer.status 
                               and "sped up" not in racer.status and racer.shocked == False):
                            racer.speed = 1.1 * racer.max_speed
                    elif (time + 5) <= race_duration <= (time + 6):
                        racer.speed = 0
                        racer.item = None
                        racer.TC_initial = False
                        racer.shocked = True                
                    else:
                        racer.TC_final = True
                        racer.shocked = False
                        if racer.speed != 0.35 * racer.max_speed and "stunned" not in racer.status and racer.shocked == False:
                            update_speed(racer, 1)
            if "TC" in racer.status:
                racer.status.remove("TC")
            if racer.TC_initial == True:
                racer.TC_initial = False
            if racer.TC_final == True:
                racer.TC_final = False

    if racer.item == "lightning_bolt":
        # Removes the item from the user's inventory the moment it gets used (that's how it works in the game)
        racer.item = None
        time_accel2 = 1
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
        while race_duration <= time + 4:
            if race_duration <= time + 1:
                for other_racer in participants:
                    if "shrunk" in other_racer.status:

                        # Cannot shock out a lightning cloud from another racer
                        if other_racer.item == "lightning_cloud":
                            other_racer.speed = 0
                            other_racer.shocked = True
                        else:
                            other_racer.item = None
                            other_racer.speed = 0
                            other_racer.shocked = True
            else:
                for kart in participants:
                    if "shrunk" in kart.status:
                        kart.shocked = False
                        if kart.TC_initial == True and "inked" not in kart.status and "squished" not in kart.status:
                            if (kart.speed != 0.35 * 1.1 * kart.max_speed and "stunned" not in kart.status):
                                kart.speed = 0.35 * 1.1 * kart.max_speed
                        elif kart.TC_initial == True and ("inked" in kart.status or "squished" in kart.status):
                            if (kart.speed != 1.1 * kart.max_speed_slowdown() and "stunned" not in kart.status):
                                kart.speed = 1.1 * kart.max_speed_slowdown()
                        else:
                            # Accelerates each racer to their reduced speed
                            if (kart.speed != kart.max_speed_slowdown() and "stunned" not in kart.status
                                and kart.shocked == False):
                                update_speed(kart, 1)
                                
        for other_racer in participants:
            if "shrunk" in other_racer.status:
                other_racer.status.remove("shrunk")

    if racer.item == "blooper":
        # Removes the item from the user's inventory the moment it gets used
        racer.item = None
        for other_racer in participants:
            if other_racer.position < racer.position:
                # Mushrooms override blooper effects
                if "invulnerable" not in other_racer.status and "mega" not in other_racer.status and "sped up" not in other_racer.status:
                    other_racer.status.append("inked")
        while race_duration <= time + 5:
            for other_racer in participants:
                if "inked" in other_racer.status:
                    if other_racer.TC_initial == True and "shrunk" not in other_racer.status and "squished" not in other_racer.status:
                        if (other_racer.speed != 0.9 * 1.1 * other_racer.max_speed 
                               and "stunned" not in other_racer.status and other_racer.shocked == False):
                            other_racer.speed = 0.9 * 1.1 * other_racer.max_speed
                    elif other_racer.TC_final == True and "shrunk" not in other_racer.status and "squished" not in other_racer.status:
                        if (other_racer.speed != 0.35 * 0.9 * other_racer.max_speed 
                               and "stunned" not in other_racer.status and other_racer.shocked == False):
                            update_speed(other_racer, 1)

                    else:
                        if (other_racer.speed != other_racer.max_speed_slowdown() 
                               and "stunned" not in other_racer.status and other_racer.shocked == False):
                            update_speed(other_racer, time_accel2)

        for other_racer in participants:
            if "inked" in other_racer.status:
                other_racer.status.remove("inked")

    if racer.item == "POW":
        # Removes the item from the user's inventory the moment it gets used
        racer.item = None
        for other_racer in participants:
            if other_racer.position < racer.position and "3s_stun" not in other_racer.status:

                # Remove "stunned" from the status list if racer is currently stunned from a shell or FIB
                # and then readd it to ensure the code doesn't break
                if "stunned" in other_racer.status:
                    other_racer.status.remove("stunned")
                if "1s_stun" in other_racer.status:
                    other_racer.status.remove("1s_stun")
                if "sped up" in other_racer.status and "invulnerable" not in other_racer.status and "mega" not in other_racer.status:
                    other_racer.status.remove("sped up")
                if "invulnerable" not in other_racer.status and "mega" not in other_racer.status:
                    other_racer.status.append("stunned")
                    other_racer.status.append("POW'd")
                
        while race_duration <= time + 2:
            for other_racer in participants:
                if "stunned" in other_racer.status and "POW'd" in other_racer.status:

                    # Cannot pow out a lightning cloud from a racer
                    if other_racer.item == "lightning_cloud":
                        other_racer.speed = 0
                    else:
                        other_racer.item = None
                        other_racer.speed = 0
            
        for other_racer in participants:
            # Having 2 statuses added to the list at first allows us to make sure that only the racers that get POW'd
            # get their stunned status removed after 2 seconds.
            if "stunned" in other_racer.status and "POW'd" in other_racer.status:
                other_racer.status.remove("stunned")
                other_racer.status.remove("POW'd")

    if racer.item == "mushroom":
        # Removes the item from the inventory the moment it gets used
        racer.item = None
        
        racer.status.append("sped up")

        # Mushrooms remove blooper effects
        if "inked" in racer.status:
            racer.status.remove("inked")
        while race_duration <= time + 2 and "sped up" in racer.status:
            
            # To account for mushroom being used when small
            if racer.TC_final == True and "shrunk" not in racer.status and "squished" not in racer.status:
                racer.speed = 1.5 * 0.35 * racer.max_speed
            elif "shrunk" in racer.status or "squished" in racer.status:
                racer.speed = 1.5 * racer.max_speed_slowdown()
            else:
                racer.speed = 1.5 * racer.max_speed
            
        if "sped up" in racer.status:
            racer.status.remove("sped up")

    if racer.item == "trip_mushroom":
        racer.status.append("sped up")
        if "inked" in racer.status:
            racer.status.remove("inked")
        while race_duration <= time + 6 and "sped up" in racer.status:
            if racer.TC_final == True and "shrunk" not in racer.status and "squished" not in racer.status:
                racer.speed = 1.5 * 0.35 * racer.max_speed
            elif "shrunk" in racer.status or "TC" in racer.status or "squished" in racer.status:
                racer.speed = 1.5 * racer.max_speed_slowdown()
            else:
                racer.speed = 1.5 * racer.max_speed
            
        if "sped up" in racer.status:
            racer.status.remove("sped up")
            
        # In the actual game, your item gets fully removed from your inventory when the 3rd mushroom is used,
        # but here, we'll keep it simple and assume that it gets fully removed after the effects of all 3 mushrooms
        # runs out
        racer.item = None

    if racer.item == "gold_mushroom":
        racer.status.append("sped up")
        if "inked" in racer.status:
            racer.status.remove("inked")
        while race_duration <= time + 9 and "sped up" in racer.status:
            if racer.TC_final == True and "shrunk" not in racer.status and "squished" not in racer.status:
                racer.speed = 1.5 * 0.35 * racer.max_speed
            elif "shrunk" in racer.status or "TC" in racer.status or "squished" in racer.status:
                racer.speed = 1.5 * racer.max_speed_slowdown()
            else:
                racer.speed = 1.5 * racer.max_speed
            
        if "sped up" in racer.status:
            racer.status.remove("sped up")
    
        # In the actual game, the item is fully removed from inventory after the effect runs out
        racer.item = None

    if racer.item == "star":
        # Remove item from inventory the moment it gets used
        racer.item = None
        # In case a racer uses a star while already in a star
        if "invulnerable" in racer.status:
            racer.status.remove("invulnerable")
        racer.status.append("invulnerable")
        if "inked" in racer.status:
            racer.status.remove("inked")
        while race_duration <= time + 10 and "bill" not in racer.status:
            if racer.TC_final == True and "shrunk" not in racer.status and "squished" not in racer.status:
                racer.speed = 1.3 * 0.35 * racer.max_speed
            elif "shrunk" in racer.status or "squished" in racer.status:
                racer.speed = 1.3 * racer.max_speed_slowdown()
            else:
                racer.speed = 1.3 * racer.max_speed
        if "invulnerable" in racer.status and "bill" not in racer.status:
            racer.status.remove("invulnerable")
            
    if racer.item == "mega_mushroom":
        # Remove item from inventory the moment it gets used
        racer.item = None
        if "mega" in racer.status:
            racer.status.remove("mega")
        racer.status.append("mega")

        # The mega mushroom removes all these effects
        if "inked" in racer.status:
            racer.status.remove("inked")
        if "shrunk" in racer.status:
            racer.status.remove("shrunk")
        if "TC" in racer.status:
            racer.status.remove("TC")
            racer.TC_final = False
        if "squished" in racer.status:
            racer.status.remove("squished")
        speed = racer.speed
        while race_duration <= time + 10 and "mega" in racer.status:
            if "invulnerable" not in racer.status:
                racer.speed = 1.1 * racer.max_speed
            else:
                racer.speed = 1.1 * speed
            
        if "mega" in racer.status:
            racer.status.remove("mega")

    if racer.item == "bullet_bill":
        if "inked" in racer.status:
            racer.status.remove("inked")
        if "mega" in racer.status:
            racer.status.remove("mega")
        if "shrunk" in racer.status:
            racer.status.remove("shrunk")
        if "TC" in racer.status:
            racer.status.remove("TC")
        if "squished" in racer.status:
            racer.status.remove("squished")
            
        # If the user is currently in a star when they use the bullet bill, remove the invulnerable status
        # and add it again to guarantee that nothing weird happens
        if "invulnerable" in racer.status:
            racer.status.remove("invulnerable")

        # The 'bill' status is required for a very specific situation in which the user activates the bill while in a star
        # Don't want the code to break because of this
        racer.status.append("invulnerable")
        racer.status.append("bill")
        
        if racer.position == 1:
            while race_duration <= time + 2:
                racer.speed = 2 * racer.max_speed
        else:
            while race_duration <= time + 8 | racer.racers_passed < 5 | racer.position != 1:
                racer.speed = 2 * racer.max_speed

        racer.racers_passed = 0
        racer.status.remove("invulnerable")
        racer.status.remove("bill")

        # Bullet bills don't disappear from inventory until they run out
        racer.item = None

    '''
    Code for the rest of the items on this list might not fully work because I'm not sure if
    it will track the correct racer if, for example, the person in first place switches positions
    with the person in 2nd while that person who was in 1st is still stunned from a blue shell. Or maybe
    I'm just overthinking it idk. For now, let's just hope everything works out.
    '''
    if racer.item == "green_shell":
        racer.item = None
        action = random.random()
        if racer.position == 1:
            if 0 <= action <= 0.4:
                for other_racer in participants:
                    
                    if (other_racer.position == racer.position + 1):
                        one_sec_stun(other_racer, time)

        elif racer.position == len(participants):
            if 0 <= action <= 0.4:
                for other_racer in participants:
                    if (other_racer.position == racer.position - 1):
                        one_sec_stun(other_racer, time)

        else:
            if 0 <= action <= 0.3:
                for other_racer in participants:
                    if (other_racer.position == racer.position + 1):
                        one_sec_stun(other_racer, time)

            elif 0.3 < action <= 0.6:
                for other_racer in participants:
                    if (other_racer.position == racer.position - 1):
                        one_sec_stun(other_racer, time)


    if racer.item == "trip_green_shell":
        racer.item = None
        action = random.random()
        if racer.position == 1:
            if 0 <= action <= 0.5:
                for other_racer in participants:
                    if (other_racer.position == racer.position + 1):
                        one_sec_stun(other_racer, time)

            elif 0.5 < action <= 0.9:
                for other_racer in participants:
                    if other_racer.position == racer.position + 1:
                        kart1 = other_racer
                everyone_else = [r for r in participants if r != kart1]
                kart = random.choice(everyone_else)
                one_sec_stun(kart, time)

        elif racer.position == len(participants):
            if 0 <= action <= 0.5:
                for other_racer in participants:
                    if (other_racer.position == racer.position - 1):
                        one_sec_stun(other_racer, time)

            elif 0.5 < action <= 0.9:
                for other_racer in participants:
                    if other_racer.position == racer.position - 1:
                        kart1 = other_racer
                everyone_else = [r for r in participants if (r != kart1)]
                kart = random.choice(everyone_else)
                one_sec_stun(kart, time)

        else:
            if 0 <= action <= 0.35:
                for other_racer in participants:
                    if (other_racer.position == racer.position + 1):
                        one_sec_stun(other_racer, time)

            elif 0.35 < action <= 0.7:
                for other_racer in participants:
                    if (other_racer.position == racer.position - 1):
                        one_sec_stun(other_racer, time)

            elif 0.7 < action <= 0.9:
                for other_racer in participants:
                    if other_racer.position == racer.position + 1:
                        kart1 = other_racer
                    if other_racer.position == racer.position - 1:
                        kart2 = other_racer
                everyone_else = [r for r in participants if (r != kart1 and r != kart2)]
                kart = random.choice(everyone_else)
                one_sec_stun(kart, time)

    if racer.item == "blue_shell":
        racer.item = None
        for other_racer in participants:
            if other_racer.position == 1:
                three_sec_stun(racer, time)

    if racer.item == "red_shell":
        racer.item = None
        action = random.random()
        if racer.position == 1:
            if 0 <= action <= 0.3:
                for other_racer in participants:
                    if (other_racer.position == racer.position + 1):
                        one_sec_stun(other_racer, time)

        elif racer.position == len(participants):
            if 0 <= action <= 0.7:
                for other_racer in participants:
                    if (other_racer.position == racer.position - 1):
                        one_sec_stun(other_racer, time)

        else:
            if 0 <= action <= 0.65:
                for other_racer in participants:
                    if (other_racer.position == racer.position - 1):
                        one_sec_stun(other_racer, time)

            elif 0.65 < action <= 0.85:
                for other_racer in participants:
                    if (other_racer.position == racer.position + 1):
                        one_sec_stun(other_racer, time)

    if racer.item == "trip_red_shell":
        racer.item = None
        action = random.random()
        if len(participants) >= 3:
            if racer.position == 1:
                if 0 <= action <= 0.4:
                    for other_racer in participants:
                        if (other_racer.position == racer.position + 1):
                            one_sec_stun(other_racer, time)

                elif 0.4 < action <= 0.65:
                    for other_racer in participants:
                        if other_racer.position == racer.position + 1:
                            kart1 = other_racer
                    everyone_else = [r for r in participants if r != kart1 and r != racer]
                    kart = random.choice(everyone_else)
                    one_sec_stun(kart, time)

            elif racer.position == len(participants):
                if 0 <= action <= 0.6:
                    for other_racer in participants:
                        if (other_racer.position == racer.position - 1):
                            one_sec_stun(other_racer, time)
                        if (other_racer.position == racer.position - 2):
                            one_sec_stun(other_racer, time)

                elif 0.6 < action < 0.95:
                    for other_racer in participants:
                        if (other_racer.position == racer.position - 1):
                            one_sec_stun(other_racer, time)

            elif racer.position == 2:
                if 0 <= action <= 0.75:
                    for other_racer in participants:
                        if (other_racer.position == racer.position - 1):
                            one_sec_stun(other_racer, time)

                elif 0.75 < action <= 0.95:
                    for other_racer in participants:
                        if (other_racer.position == racer.position + 1):
                            one_sec_stun(other_racer, time)
            else:
                if 0 <= action <= 0.6:
                    for other_racer in participants:
                        if (other_racer.position == racer.position - 1):
                            one_sec_stun(other_racer, time)

                        if (other_racer.position == racer.position - 2):
                            one_sec_stun(other_racer, time)
                            
                elif 0.6 < action <= 0.85:
                    if (other_racer.position == racer.position - 1):
                        one_sec_stun(other_racer, time)

                elif 0.85 < action <= 0.95:
                    for other_racer in participants:
                        if (other_racer.position == racer.position + 1):
                            one_sec_stun(other_racer, time)

        else:
            if racer.position == 1:
                if 0 <= action <= 0.4:
                    for other_racer in participants:
                        if (other_racer.position == racer.position + 1):
                            one_sec_stun(other_racer, time)
            else:
                if 0 <= action <= 0.8:
                    for other_racer in participants:
                        if (other_racer.position == racer.position - 1):
                            one_sec_stun(other_racer, time)

    if racer.item == "FIB":
        racer.item = None
        action = random.random()
        if racer.position == 1:
            if 0 <= action <= 0.35:
                for other_racer in participants:
                    if (other_racer.position == racer.position + 1):
                        one_sec_stun(other_racer, time)

        elif racer.position == len(participants):
            if 0 <= action <= 0.35:
                for other_racer in participants:
                    if (other_racer.position == racer.position - 1):
                        one_sec_stun(other_racer, time)

        else:
            if 0 <= action <= 0.25:
                for other_racer in participants:
                    if (other_racer.position == racer.position + 1):
                        one_sec_stun(other_racer, time)

            elif 0.25 < action <= 0.5:
                for other_racer in participants:
                    if (other_racer.position == racer.position - 1):
                        one_sec_stun(other_racer, time)      

    if racer.item == "banana":
        racer.item = None
        action = random.random()
        if racer.position == 1:
            if 0 <= action <= 0.3:
                for other_racer in participants:
                    if (other_racer.position == racer.position + 1):
                        banana_slowdown(other_racer)

        elif racer.position == len(participants):
            if 0 <= action <= 0.3:
                for other_racer in participants:
                    if (other_racer.position == racer.position - 1):
                        banana_slowdown(other_racer)

        else:
            if 0 <= action <= 0.2:
                for other_racer in participants:
                    if (other_racer.position == racer.position + 1):
                        banana_slowdown(other_racer)

            elif 0.2 < action <= 0.4:
                for other_racer in participants:
                    if (other_racer.position == racer.position - 1):
                        banana_slowdown(other_racer)

    if racer.item == "trip_bananas":
        racer.item = None
        action = random.random()
        if racer.position == 1:
            if 0 <= action <= 0.4:
                for other_racer in participants:
                    if (other_racer.position == racer.position + 1):
                        banana_slowdown(other_racer)

            elif 0.4 < action <= 0.7:
                back_three = []
                for other_racer in participants:
                    if (other_racer.position == racer.position + 1 or 
                            other_racer.position == racer.position + 2 or other_racer.position == racer.position + 3):
                        back_three.append(other_racer)
                kart = random.choice(back_three)
                banana_slowdown(kart)

        elif racer.position == len(participants):
            if 0 <= action <= 0.4:
                for other_racer in participants:
                    if (other_racer.position == racer.position - 1):
                        banana_slowdown(other_racer)

            elif 0.4 < action <= 0.7:
                front_three = []
                for other_racer in participants:
                    if (other_racer.position == racer.position - 1 or 
                            other_racer.position == racer.position - 2 or other_racer.position == racer.position - 3):
                        front_three.append(other_racer)
                kart = random.choice(front_three)
                banana_slowdown(kart)

        else:
            if 0 <= action <= 0.25:
                for other_racer in participants:
                    if (other_racer.position == racer.position + 1):
                        banana_slowdown(other_racer)

            elif 0.25 < action <= 0.5:
                for other_racer in participants:
                    if (other_racer.position == racer.position - 1):
                        banana_slowdown(other_racer)

            elif 0.5 < action <= 0.7:
                within_three = []
                for other_racer in participants:
                    if (other_racer.position == racer.position + 1 or other_racer.position == racer.position + 2 or
                            other_racer.position == racer.position + 3 or other_racer.position == racer.position - 1 or 
                            other_racer.position == racer.position - 2 or other_racer.position == racer.position - 3):
                        within_three.append(other_racer)
                kart = random.choice(within_three)
                banana_slowdown(kart)
    
    if racer.item == "bob_omb":
        racer.item = None
        action = random.random()
        if racer.position == 1:
            if 0 <= action <= 0.5:
                for other_racer in participants:
                    if (other_racer.position == racer.position + 1):
                        three_sec_stun(other_racer, time)
            
            elif 0.5 < action <= 0.8:
                back_two = []
                for other_racer in participants:
                    if (other_racer.position == racer.position + 1 or other_racer.position == racer.position + 2):
                        back_two.append(other_racer)
                for kart in back_two:
                    three_sec_stun(kart, time)
            
            elif 0.8 < action <= 0.9:
                back_three = []
                for other_racer in participants:
                    if (other_racer.position == racer.position + 1 or 
                            other_racer.position == racer.position + 2 or other_racer.position == racer.position + 3):
                        back_three.append(other_racer)
                for kart in back_three:
                    three_sec_stun(kart, time)

        elif racer.position == len(participants):
            if 0 <= action <= 0.5:
                for other_racer in participants:
                    if (other_racer.position == racer.position - 1):
                        three_sec_stun(other_racer, time)

            elif 0.5 < action <= 0.8:
                front_two = []
                for other_racer in participants:
                    if (other_racer.position == racer.position - 1 or other_racer.position == racer.position - 2):
                        front_two.append(other_racer)
                for kart in front_two:
                    three_sec_stun(kart, time)
            
            elif 0.8 < action <= 0.9:
                front_three = []
                for other_racer in participants:
                    if (other_racer.position == racer.position - 1 or 
                            other_racer.position == racer.position - 2 or other_racer.position == racer.position - 3):
                        front_three.append(other_racer)
                for kart in front_three:
                    three_sec_stun(kart, time)

        else:
            if 0 <= action <= 0.2:
                for other_racer in participants:
                    if (other_racer.position == racer.position - 1):
                        three_sec_stun(other_racer, time)
            
            elif 0.2 < action <= 0.35:
                front_two = []
                for other_racer in participants:
                    if (other_racer.position == racer.position - 1 or other_racer.position == racer.position - 2):
                        front_two.append(other_racer)
                for kart in front_two:
                    three_sec_stun(kart, time)

            elif 0.35 < action <= 0.45:
                front_three = []
                for other_racer in participants:
                    if (other_racer.position == racer.position - 1 or 
                            other_racer.position == racer.position - 2 or other_racer.position == racer.position - 3):
                        front_three.append(other_racer)
                for kart in front_three:
                    three_sec_stun(kart, time)

            elif 0.45 < action <= 0.65:
                for other_racer in participants:
                    if (other_racer.position == racer.position + 1):
                        three_sec_stun(other_racer, time)

            elif 0.65 < action <= 0.8:
                back_two = []
                for other_racer in participants:
                    if (other_racer.position == racer.position + 1 or other_racer.position == racer.position + 2):
                        back_two.append(other_racer)
                for kart in back_two:
                    three_sec_stun(kart, time)

            elif 0.8 < action <= 0.9:
                back_three = []
                for other_racer in participants:
                    if (other_racer.position == racer.position + 1 or 
                            other_racer.position == racer.position + 2 or other_racer.position == racer.position + 3):
                        back_three.append(other_racer)
                for kart in back_three:
                    three_sec_stun(kart, time)

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

# A list of all possible racers, which the program will pick from at random before every race
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

def update_race_state(participants, unavailable_items):
    race_data_distance = {"race_duration": [race_duration]}
    race_data_speed = {"race_duration": [race_duration]}
    race_data_position = {"race_duration": [race_duration]}

    for racer in participants:
        update_distance(racer, 1)
        
        if (racer.speed != racer.max_speed) and (not racer.status):
            update_speed(racer, 1)

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
