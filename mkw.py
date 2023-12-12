'''
This is the code for our Mario Kart Wii simulation.

When the program is ran, the user will be prompted to enter an integer from 2-12, representing the number of racers
in the race.

Then, that number of participants is randomly chosen from the list of all of the characters in the game. 
The function update_race_state() calls on the functions for simulating racer movement, updating their positions whenever
they pass another racer, and getting and using their items, all at appropriate times.

The function run_race_simulation() calls on update_race_state repeatedly until all of the racers have cross the finish line, 
which is set to be a predetermined distance.

The race state at every frame is printed in the terminal in the form of a table, and at the end of the race,
animtations of the racers' positions, speeds, and distances from the start throughout the race are created and shown to the user.

Note that this simulation is not perfect, as it contains bugs that sometimes occur, and many simplifications were made
regarding the race track and item functionality.
'''

import random
import sys
import pandas as pd
import matplotlib.pyplot as plt
import time
from matplotlib.animation import FuncAnimation
from tabulate import tabulate
from operator import attrgetter

# The number of seconds that have elapsed since the start of the race
Race_duration = 0

# Variables storing the times that the lightning bolt, the POW block, and the blooper were used
# These are for the item timing rules
Lightning_use_time = 0
Blooper_use_time = 0
POW_use_time = 0

# The list of all items that can be unavailable because of item limit and/or item timing rules
All_possible_unavailable_items = ["lightning_cloud", "lightning_bolt", "POW", "bullet_bill", "blue_shell", "blooper"]

# The current list of items that are unavailable
# The race starts with these 4 items in the list. They will be removed after a certain number of seconds have passed.
Unavailable_items = ["lightning_bolt", "POW", "blue_shell", "blooper"]


class Racer:
    '''
    A class representing a racer.

    Attributes:
    name (str): The name of the racer
    weight (str): The weight of the racer (either Light, Medium, or Heavy)
    position (int): The current position of the racer in the race
    item (str): The racer's current item in the race
    recently_used_item (str): The item that the racer just used.
                              This attribute is solely to help with the item functionality.
    distance_from_start(float): The racer's current distance from the starting line
    speed (float): The racer's current speed (in meters per second)
    max_speed (float): The speed that the racer should be going at when not affected by any items
                       The heavier the character, the greater their max_speed
    acceleration (float): How fast the racer can get back to their max_speed after being affected by an item
                          The lighter the character, the greater their acceleration
    status (list of strings): Any status effects that the racer currently has when affected by an item
    racers_passed (int): Stores the number of racers that a user has passed
                         This atttribute is solely used for the bullet bill item functionality.
    time_item_got (int): Keeps track of when exactly the racer got an item
    time_item_used (int): Keeps track of when exactly the racer used an item
                          This attribute is solely used for item functionality and item timing rules
    time_delay (int): The number of seconds that must elapse before a racer can use their item
                      Paired with time_item_got to simulate the time that elapses in the original game 
                      between when you touch an item box and when the item is actually in your inventory and available for use.
    using_item (bool): Keeps track of whether status effects should be applied to the racer or other racers
                       This attribute acts as a flag and is solely used for item functionality and item timing rules
    action (float): A random floating point value between 0 and 1 that determines who the racer will stun if using certain items
                    Initially set to 0 but will be updated accordingly
    shocked (bool): Keeps track of whether the racer is just zapped by the lightning bolt or lightning cloud
    marker (int): Keeps track of the other racer(s) that the racer just stunned
    user_marker (int): Keeps track of the racer that is doing the stunning
                       This attribute and marker are solely used for the functionality of certain items
    TC_initial (bool): Keeps track of whether the racer is in the initial phase of the lightning cloud item
    TC_final (bool): Keeps track of whether the racer is in the final phase of the lightning cloud item
    finished (bool): Keeps track of whether the racer has crossed the finish line

    Methods:
    None
    '''

    def __init__(self, name, weight):
        '''
        Constructs all the necessary attributes for the Racer class

        Parameters:
        name (str): The name of the racer (Mario, Peach, Funky Kong, etc)
        weight (str): The weight of the racer (Light, Medium, or Heavy)

        Returns:
        None
        '''

        self.name = name
        self.weight = weight

        # Initially set the position to 0
        # When the race starts, the racer will be assigned a random position between 1 and the number of participants
        self.position = 0

        # Initially, each racer will have no items
        self.item = None
        self.recently_used_item = None

        # Initially set the distance to 0
        # When the race starts, each racer will start behind the finish line
        # Their initial distance will be a negative int and will correspond with their initial positions
        self.distance_from_start = 0

        # Assigns random max_speed values based on weight
        # Initially, all racers will start with a speed of 0
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
        if weight == "Light":
            self.acceleration = self.max_speed / 3
        if weight == "Medium":
            self.acceleration = self.max_speed / 4
        if weight == "Heavy":
            self.acceleration = self.max_speed / 5

        # All racers begin with no status effects.
        self.status = []

        # This value only gets updated whenever the racer is using a bullet bill
        self.racers_passed = 0

        # These are initially set to 0 and will be changed when the racer gets and uses an item
        self.time_item_got = 0
        self.time_item_used = 0

        # Initially set to 0 but will be set to a random int between 3 and 5 inclusive when the racer gets an item
        self.time_delay = 0

        # Initially set to False because the racer is not using an item when the race starts
        self.using_item = False

        # Will be updated when the racer is using certain items
        self.action = None

        # Initially set to false, as the racer is not zapped by a lightning bolt or lightning cloud at the start of
        # the race
        self.shocked = False

        # Initially set to 0 but will be updated based on what specific item the racer is using
        self.marker = 0
        self.user_marker = 0

        # Initially set to False, as the racer is not using a lightning cloud at the beginning of the race
        self.TC_initial = False
        self.TC_final = False

        # WIll be set to True once the racer crosses the finish line
        self.finished = False


def update_position(racer1, racer2):
    """
    Swaps the positions of two racers if racer1 passes racer2
    Parameter:
    racer1 (object): the racer who is passing another racer
    racer2 (object): the racer who racer1 is passing

    Returns:
    racer2.position, racer1.position (int): returns the new positions of these racers
    racer1.racers_passed (int): if racer1 is in a bullet bill and passes racer2, the number of racers passed increases by 1 to
    monitor when to stop the bullet bill
    """
    racer1.position, racer2.position = racer2.position, racer1.position
    if "bill" in racer1.status:
        racer1.racers_passed += 1


def update_distance(racer, use_time):
    """
    Changes the distance the racer has traveled from the start
    Parameter:
    racer (obj): the racer whose distance from the start is changing
    use_time (int): the time over which the distance from the start is changing

    Returns:
    racer.distance_from_start: new distance attribute for the racer
    """

    # Distance traveled is adjusted using the formula final_distance = initial_distance + speed*time
    distance = racer.distance_from_start + (racer.speed * use_time)
    racer.distance_from_start = distance


def update_speed(racer, use_time):
    """
    Changes the speed of the racer based on the acceleration
    Parameter:
    racer (obj): the racer whose speed is changing
    use_time (int): the time over which the speed is changing

    Returns:
    racer.speed: new speed attribute for the racer
    """
    # Increases the racer speed up to the maximum speed based on the acceleration. Speed is updated first, then the
    # racer moves and then their distance is updated
    if racer.speed < racer.max_speed:
        speed = racer.speed + racer.acceleration * use_time
        racer.speed = speed
        # If the new racer speed exceeds the maximum speed, the racer speed is set to the maximum bound
        if racer.speed > racer.max_speed:
            racer.speed = racer.max_speed

    # For decelerating back to initial speed after racer uses a speed-ramping item
    if racer.speed > racer.max_speed:
        speed = racer.speed - racer.acceleration * use_time
        racer.speed = speed


def choose_item(choices, position):
    """
    Picks the item a racer gets from an item box
    Parameters:
    choices (dict): the potential items to choose from and the probabilities of acquiring each item
    position (int): the position of the racer is currently in

    Returns:
    item (str): the item the racer now possesses
    """
    total = sum(weight[position] for _, weight in choices)  # Finds all the possible items a racer can get
    r = random.uniform(0, total)  # Chooses a random float to choose the item
    subtotal = 0

    for item, weight in choices:
        subtotal += weight[position]
        if subtotal >= r:  # If r is within the probability range of the item, then that item is returned
            return item


def possible_items(position, probability_list):
    """
    Gets all possible items that a racer at a certain position can pull

    Parameters:
    position (int): the position of the racer
    probability_list (list of tuples): The item probability list corresponding to the number of racers in the race

    Returns:
    list of items: All the item that a racer can pull given their position and how many racers are in the race
    """

    # Loops through the probability list to get all of the items that have a probability value greater than 0
    return [item[0] for item in probability_list if item[1][position] != 0]


def update_probabilities(items, probability_list, position):
    """
    Updates the probability list based on what items are currently unavailable due to item limit and item timing rules

    Parameters:
    items (list of strings): The list of items that are currently unavailable
    probability_list (list of tuples): The item probability list corresponding to the number of racers in the race
    position (int): The current position of the racer

    Returns probability_list (list of tuples): The updated probability list after taking into account the current unavailable items
    """

    # The list of items that are currently available
    other_items = []

    # The sum of the probabilities of all of the unavailable items
    sum_prob_items = 0

    # Loops through the default probability list
    for possible_item in probability_list:
        # Checks if any item is in the list of unavailable items
        # If they are, then add their probability to sum_prob_items
        if possible_item[0] in items:
            sum_prob_items += possible_item[1][position]
        # If they are not, then add them to the list of currently available items
        if possible_item[0] not in items and possible_item[1][position] != 0:
            other_items.append(possible_item[0])

    # Loops through the default probability list again
    for possible_item in probability_list:
        # Distributes the probabilities of the unavailable items equally among the available items
        if possible_item[0] in other_items:
            possible_item[1][position] += (sum_prob_items / len(other_items))
        # Sets the probability of the unavailable items to 0
        if possible_item[0] in items:
            possible_item[1][position] = 0
    return probability_list


def get_item(racer, num_racers):
    """
    Gives the racer an item

    Parameters:
    racer (obj): The racer the item is being given to
    num_racers (int): The number of racers in the race

    Returns:
    None
    """

    # Checks for how many racers are in the current race
    if num_racers == 2:
        # If there aren't any unavailable items, or if the racer is in a position where none of the items they can get
        # can become unavailable, or if none of the unavailable items are in the list of the racer's possible items
        if not Unavailable_items or racer.position == 1 or not any(
                item in possible_items(racer.position, all_items_2) for item in Unavailable_items):
            # Choose an item from the default item probability list
            item = choose_item(all_items_2, racer.position)
            racer.item = item
        else:
            # Otherwise, choose an item from the updated probabilities list
            item = choose_item(update_probabilities(Unavailable_items, all_items_2, racer.position), racer.position)
            racer.item = item
    # Does the same process for every other possible number of racers
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


# For very specific scenarios where a racer has at least one of these status and needs to accelerate
# to their max speed based on which ones they have
def max_speed_slowdown(racer):
    """
    Adjusts the speed of the racer if they have multiple status effects at once. Accounts for the combination of item
    effects

    Parameter:
    racer (object): the racer whose speed will decrease based on these effects

    Returns:
    speed (float) : new racer speed based on the possible cases
    """

    if ("shrunk" in racer.status and "inked" not in racer.status and "squished" not in racer.status) or ("squished" in
                                                                                                         racer.status and "shrunk" not in racer.status and "inked" not in racer.status):
        speed = 0.35 * racer.max_speed
    elif "inked" in racer.status and "shrunk" not in racer.status and "squished" not in racer.status:
        speed = 0.9 * racer.max_speed
    elif ("shrunk" in racer.status and "inked" in racer.status and "squished" not in racer.status) or ("squished" in
                                                                                                       racer.status and "inked" in racer.status and "shrunk" not in racer.status):
        speed = 0.35 * 0.9 * racer.max_speed
    elif "shrunk" in racer.status and "squished" in racer.status and "inked" not in racer.status:
        speed = 0.35 * 0.35 * racer.max_speed
    elif "shrunk" in racer.status and "inked" in racer.status and "squished" in racer.status:
        speed = 0.35 * 0.35 * 0.9 * racer.max_speed
    else:
        speed = racer.max_speed
    return speed


def one_sec_stun(original_racer, racer):
    """
    Stuns a racer for one second and updates several attributes appropriately

    Parameters:
    original_racer(obj): The racer doing the stunning
    racer (obj): The racer being stunned

    Returns:
    None
    """

    # Checks if the one second has elapsed since the original racer used their item
    if Race_duration <= original_racer.time_item_used + 1:
        # If so, add the appropriate status effects to the racer being affected if they are not already in their
        # status list and if the racer is not invincible Also sets the affected racer's speed to 0 if they are not
        # invincible
        if ("POW'd" not in racer.status) and ("stunned" not in
                                              racer.status) and (
                "1s_stun" not in racer.status) and "3s_stun" not in racer.status:
            if "invulnerable" not in racer.status and "mega" not in racer.status:
                racer.status.append("stunned")
                racer.status.append("1s_stun")
        if "invulnerable" not in racer.status and "mega" not in racer.status:
            racer.speed = 0
    # If it is past one second (meaning the stun time is over), remove the status effects
    # and set the attributes for both the affected racer and original racer back to their original values
    elif Race_duration > original_racer.time_item_used + 1:
        if "stunned" in racer.status and "1s_stun" in racer.status and racer.marker == 1:
            racer.status.remove("stunned")
            racer.status.remove("1s_stun")
            racer.marker = 0
        original_racer.user_marker = 0
        original_racer.using_item = False
        original_racer.action = None
        original_racer.recently_used_item = None


# Stuns the racer for 3 seconds (used in use_item)
def three_sec_stun(original_racer, racer):
    """
    Stuns a racer for 3 seconds, gets rid of their item, and updates several attributes appropriately

    Parameters:
    original_racer (obj): The racer doing the stunning
    racer (obj): The racer being stunned
    """

    # Checks if the three seconds has elapsed since the original racer used their item
    if Race_duration <= original_racer.time_item_used + 3:
        # If so, add the appropriate status effects to the racer being affected if they are not already in their
        # status list and if the racer is not invincible Also sets the affected racer's speed to 0 and removes their
        # items if they are not invincible
        if "stunned" and "3s_stun" not in racer.status:
            if "stunned" in racer.status and "1s_stun" in racer.status:
                racer.status.remove("stunned")
                racer.status.remove("1s_stun")
            if "stunned" in racer.status and "POW'd" in racer.status:
                racer.status.remove("stunned")
                racer.status.remove("POW'd")
            if "sped up" in racer.status and "invulnerable" not in racer.status and "mega" not in racer.status:
                racer.status.remove("sped up")
                racer.item = None
                racer.using_item = False
                racer.recently_used_item = None
            if "invulnerable" not in racer.status and "mega" not in racer.status:
                # The lightning cloud cannot be removed until it zaps the racer it's affected
                if racer.item != "lightning_cloud":
                    if racer.item in All_possible_unavailable_items and racer.item in Unavailable_items:
                        Unavailable_items.remove(racer.item)
                    racer.item = None
                racer.status.append("stunned")
                racer.status.append("3s_stun")
        if "invulnerable" not in racer.status and "mega" not in racer.status:
            racer.speed = 0

    # If it is past three seconds (meaning the stun time is over), remove the status effects
    # and set the attributes for both the affected racer and original racer back to their original values
    elif Race_duration > original_racer.time_item_used + 3:
        if "stunned" in racer.status and "3s_stun" in racer.status and racer.marker == 3:
            racer.status.remove("stunned")
            racer.status.remove("3s_stun")
            racer.marker = 0
        original_racer.user_marker = 0
        original_racer.using_item = False
        original_racer.action = None
        original_racer.recently_used_item = None


def banana_slowdown(racer):
    """
    Reduces a racer's speed by half when hit by a banana

    Parameters:
    racer (obj): The racer being affected

    Returns:
    None
    """

    speed = racer.speed
    # If a racer is currently being stunned by another item, this function should not have any effect
    if ("POW'd" not in racer.status) and ("stunned" not in
                                          racer.status) and (
            "1s_stun" not in racer.status) and "3s_stun" not in racer.status:
        if "sped up" in racer.status and "invulnerable" not in racer.status and "mega" not in racer.status:
            racer.status.remove("sped up")
        # Reduces speed by half if racer is not invincible
        if "invulnerable" not in racer.status and "mega" not in racer.status:
            racer.speed = 0.5 * speed


def use_item(racer, participants):
    """
    Uses the item that the racer is holding

    Parameters:
    racer (obj): The racer using the item
    participants (list of objects): The list of all the racers in the race

    Returns:
    None
    """

    global Unavailable_items, Blooper_use_time, POW_use_time, Lightning_use_time

    # Checks for the racer's recently used item because some items disappear from the racers' inventory the moment
    # this function is called for the first time. The recently used item attribute stores the item that the racer
    # just used until any status effects completely wear off. The attribute is needed because we will call this
    # function over and over in update_race_state() until a certain period of time has passed, each time continuing
    # to apply certain status effects. Once time is up, the recently used item attribute will be set back to None,
    # to let the program know to stop calling this function
    if racer.recently_used_item == "lightning_cloud":
        if "mega" in racer.status or "invulnerable" in racer.status:
            if "lightning_cloud" in Unavailable_items:
                Unavailable_items.remove("lightning_cloud")
            racer.item = None
            racer.recently_used_item = None
        else:
            if Race_duration <= racer.time_item_used + 9 and "TC" not in racer.status:
                racer.status.append("TC")
                racer.TC_initial = True
            if Race_duration <= racer.time_item_used + 9 and "TC" in racer.status:  # Ensures if the item is used for 9
                # seconds
                if "shrunk" in racer.status or "inked" in racer.status or "squished" in racer.status:
                    if Race_duration < racer.time_item_used + 5:
                        if (racer.speed != 1.1 * max_speed_slowdown(racer) and "stunned" not in racer.status
                                and "sped up" not in racer.status and racer.shocked is False):
                            # Instantaneous acceleration for lightning clouds for the first few seconds
                            racer.speed = 1.1 * max_speed_slowdown(racer)

                    elif racer.time_item_used + 5 <= Race_duration <= racer.time_item_used + 6:
                        racer.speed = 0
                        racer.item = None
                        racer.TC_initial = False
                        racer.shocked = True
                        racer.using_item = False
                        if "lightning_cloud" in Unavailable_items:
                            Unavailable_items.remove("lightning_cloud")
                    else:
                        racer.TC_final = True
                        racer.shocked = False
                        if racer.speed != max_speed_slowdown(
                                racer) and "stunned" not in racer.status and racer.shocked is False:
                            update_speed(racer, 1)
                else:
                    if Race_duration < racer.time_item_used + 5:
                        if (racer.speed != 1.1 * racer.max_speed and "stunned" not in racer.status
                                and "sped up" not in racer.status and racer.shocked is False):
                            racer.speed = 1.1 * racer.max_speed
                    elif racer.time_item_used + 5 <= Race_duration <= racer.time_item_used + 6:
                        racer.speed = 0
                        racer.item = None
                        racer.TC_initial = False
                        racer.shocked = True
                        racer.using_item = False
                        if "lightning_cloud" in Unavailable_items:
                            Unavailable_items.remove("lightning_cloud")
                    else:
                        racer.TC_final = True
                        racer.shocked = False
                        if (racer.speed != 0.35 * racer.max_speed and "stunned" not in racer.status and racer.shocked is
                                False):
                            update_speed(racer, 1)
            elif Race_duration > racer.time_item_used + 9:
                if "TC" in racer.status:
                    racer.status.remove("TC")
                if racer.TC_initial is True:
                    racer.TC_initial = False
                if racer.TC_final is True:
                    racer.TC_final = False
                racer.recently_used_item = None

    if racer.recently_used_item == "lightning_bolt":
        # Removes the item from the user's inventory the moment it gets used (that's how it works in the game)
        racer.item = None
        Lightning_use_time = racer.time_item_used
        if Race_duration <= racer.time_item_used + 4:
            if Race_duration <= racer.time_item_used + 1:
                for other_racer in participants:
                    if other_racer != racer:
                        if "sped up" in other_racer.status:
                            other_racer.status.remove("sped up")

                        if "mega" in other_racer.status and "invulnerable" not in other_racer.status:
                            other_racer.status.remove("mega")
                        elif "invulnerable" in other_racer.status:  # Does not affect invulnerable racers
                            pass
                        elif "shrunk" not in other_racer.status:
                            other_racer.status.append("shrunk")

                for other_racer in participants:
                    if "shrunk" in other_racer.status:
                        # Cannot shock out a lightning cloud from another racer
                        if other_racer.item == "lightning_cloud":
                            other_racer.speed = 0
                            other_racer.shocked = True
                        else:
                            if (other_racer.item in All_possible_unavailable_items and other_racer.item in
                                    Unavailable_items):
                                Unavailable_items.remove(other_racer.item)
                            other_racer.item = None
                            other_racer.speed = 0
                            other_racer.shocked = True
                            other_racer.using_item = False
                            other_racer.recently_used_item = None

            else:
                for kart in participants:
                    if "shrunk" in kart.status:
                        kart.shocked = False
                        if kart.TC_initial is True and "inked" not in kart.status and "squished" not in kart.status:
                            if kart.speed != 0.35 * 1.1 * kart.max_speed and "stunned" not in kart.status:
                                kart.speed = 0.35 * 1.1 * kart.max_speed
                        elif kart.TC_initial is True and ("inked" in kart.status or "squished" in kart.status):
                            if kart.speed != 1.1 * max_speed_slowdown(kart) and "stunned" not in kart.status:
                                kart.speed = 1.1 * max_speed_slowdown(kart)
                        else:
                            # Accelerates each racer to their reduced speed
                            if (kart.speed != max_speed_slowdown(kart) and "stunned" not in kart.status
                                    and kart.shocked == False):
                                update_speed(kart, 1)
        else:
            for other_racer in participants:
                if "shrunk" in other_racer.status:
                    other_racer.status.remove("shrunk")
            racer.using_item = False
            racer.recently_used_item = None

    if racer.recently_used_item == "blooper":
        # Removes the item from the user's inventory the moment it gets used
        racer.item = None
        Blooper_use_time = racer.time_item_used
        if Race_duration <= racer.time_item_used + 5:
            if Race_duration <= racer.time_item_used + 1:
                for other_racer in participants:
                    if other_racer.position < racer.position:
                        # Mushrooms override blooper effects
                        if ("invulnerable" not in other_racer.status and
                                "mega" not in other_racer.status and "sped up" not in other_racer.status and "inked" not in other_racer.status):
                            other_racer.status.append("inked")

            for other_racer in participants:
                if "inked" in other_racer.status:
                    if (other_racer.TC_initial is True and "shrunk" not in other_racer.status and "squished" not in
                            other_racer.status):
                        if (other_racer.speed != 0.9 * 1.1 * other_racer.max_speed
                                and "stunned" not in other_racer.status and other_racer.shocked is False):
                            other_racer.speed = 0.9 * 1.1 * other_racer.max_speed
                    elif (other_racer.TC_final is True and "shrunk" not in other_racer.status and "squished" not in
                          other_racer.status):
                        if (other_racer.speed != 0.35 * 0.9 * other_racer.max_speed
                                and "stunned" not in other_racer.status and other_racer.shocked is False):
                            update_speed(other_racer, 1)

                    else:
                        if (other_racer.speed != max_speed_slowdown(other_racer)
                                and "stunned" not in other_racer.status and other_racer.shocked == False):
                            update_speed(other_racer, 1)
        else:
            for other_racer in participants:
                if "inked" in other_racer.status:
                    other_racer.status.remove("inked")
            racer.using_item = False
            racer.recently_used_item = None

    if racer.recently_used_item == "POW":
        # Removes the item from the user's inventory the moment it gets used
        racer.item = None
        POW_use_time = racer.time_item_used
        if Race_duration <= racer.time_item_used + 2:
            for other_racer in participants:
                if other_racer.position < racer.position and "3s_stun" not in other_racer.status:

                    # Remove "stunned" from the status list if racer is currently stunned from a shell or FIB
                    # and then readd it to ensure the code doesn't break
                    if "stunned" in other_racer.status and "1s_stun" in other_racer.status:
                        other_racer.status.remove("stunned")
                        other_racer.status.remove("1s_stun")
                    if "sped up" in other_racer.status and "invulnerable" not in other_racer.status and "mega" not in other_racer.status:
                        other_racer.status.remove("sped up")
                    if ("invulnerable" not in other_racer.status and "mega" not in other_racer.status and
                            "stunned" not in other_racer.status and "POW'd" not in other_racer.status):
                        other_racer.status.append("stunned")
                        other_racer.status.append("POW'd")

            for other_racer in participants:
                if "stunned" in other_racer.status and "POW'd" in other_racer.status:

                    # Cannot pow out a lightning cloud from a racer
                    if other_racer.item == "lightning_cloud":
                        other_racer.speed = 0
                    else:
                        if other_racer.item in All_possible_unavailable_items and other_racer.item in Unavailable_items:
                            Unavailable_items.remove(other_racer.item)
                        other_racer.item = None
                        other_racer.speed = 0
                        other_racer.using_item = False
                        other_racer.recently_used_item = None

        else:
            for other_racer in participants:
                # Having 2 statuses added to the list at first allows us to make sure that only the racers that get
                # POW'd get their stunned status removed after 2 seconds.
                if "stunned" in other_racer.status and "POW'd" in other_racer.status:
                    other_racer.status.remove("stunned")
                    other_racer.status.remove("POW'd")
            racer.using_item = False
            racer.recently_used_item = None

    if racer.recently_used_item == "mushroom":
        # Removes the item from the inventory the moment it gets used
        racer.item = None
        if Race_duration <= racer.time_item_used + 2 and "sped up" not in racer.status:
            racer.status.append("sped up")
            # Mushrooms remove blooper effects
            if "inked" in racer.status:
                racer.status.remove("inked")
        if Race_duration <= racer.time_item_used + 2 and "sped up" in racer.status:
            # To account for mushroom being used when small
            if racer.TC_final is True and "shrunk" not in racer.status and "squished" not in racer.status:
                racer.speed = 1.5 * 0.35 * racer.max_speed
            elif "shrunk" in racer.status or "squished" in racer.status:
                racer.speed = 1.5 * max_speed_slowdown(racer)
            elif "stunned" in racer.status:
                racer.speed = 0
            else:
                racer.speed = 1.5 * racer.max_speed
        elif Race_duration > racer.time_item_used + 2:
            if "sped up" in racer.status:
                racer.status.remove("sped up")
            racer.using_item = False
            racer.recently_used_item = None

    if racer.recently_used_item == "trip_mushroom":
        # Provides a speed boost for 6 seconds (3 times a normal mushroom)
        if Race_duration <= racer.time_item_used + 6 and "sped up" not in racer.status:
            racer.status.append("sped up")
            if "inked" in racer.status:
                racer.status.remove("inked")
        if Race_duration <= racer.time_item_used + 6 and "sped up" in racer.status:
            if racer.TC_final is True and "shrunk" not in racer.status and "squished" not in racer.status:
                racer.speed = 1.5 * 0.35 * racer.max_speed
            elif "shrunk" in racer.status or "TC" in racer.status or "squished" in racer.status:
                racer.speed = 1.5 * max_speed_slowdown(racer)
            elif "stunned" in racer.status:
                racer.speed = 0
            else:
                racer.speed = 1.5 * racer.max_speed
        elif Race_duration > racer.time_item_used + 6:
            if "sped up" in racer.status:
                racer.status.remove("sped up")
            racer.using_item = False
            # In the actual game, your item gets fully removed from your inventory when the 3rd mushroom is used,
            # but here, we'll keep it simple and assume that it gets fully removed after the effects of all 3 mushrooms
            # runs out
            racer.item = None
            racer.recently_used_item = None

    if racer.recently_used_item == "gold_mushroom":
        # Provides a mushroom speed boost for 9 seconds
        if Race_duration <= racer.time_item_used + 9 and "sped up" not in racer.status:
            racer.status.append("sped up")
            if "inked" in racer.status:
                racer.status.remove("inked")
        if Race_duration <= racer.time_item_used + 9 and "sped up" in racer.status:
            if racer.TC_final is True and "shrunk" not in racer.status and "squished" not in racer.status:
                racer.speed = 1.5 * 0.35 * racer.max_speed
            elif "shrunk" in racer.status or "TC" in racer.status or "squished" in racer.status:
                racer.speed = 1.5 * max_speed_slowdown(racer)
            elif "stunned" in racer.status:
                racer.speed = 0
            else:
                racer.speed = 1.5 * racer.max_speed
        elif Race_duration > racer.time_item_used + 9:
            if "sped up" in racer.status:
                racer.status.remove("sped up")
            racer.using_item = False
            # In the actual game, the item is fully removed from inventory after the effect runs out
            racer.item = None
            racer.recently_used_item = None

    if racer.recently_used_item == "star":
        # Provides a speed boost slightly smaller than the mushroom boost and makes the racer invulnerable for 10
        # seconds

        # Remove item from inventory the moment it gets used
        racer.item = None
        # In case a racer uses a star while already in a star
        if Race_duration <= racer.time_item_used + 10 and "invulnerable" not in racer.status:
            racer.status.append("invulnerable")
            if "inked" in racer.status:
                racer.status.remove("inked")  # Eliminates blooper effect
        if Race_duration <= racer.time_item_used + 10 and "bill" not in racer.status:
            if racer.TC_final is True and "shrunk" not in racer.status and "squished" not in racer.status:
                racer.speed = 1.3 * 0.35 * racer.max_speed
            elif "shrunk" in racer.status or "squished" in racer.status:
                racer.speed = 1.3 * max_speed_slowdown(racer)
            else:
                racer.speed = 1.3 * racer.max_speed
        elif Race_duration > racer.time_item_used + 10:
            if "invulnerable" in racer.status and "bill" not in racer.status:
                racer.status.remove("invulnerable")
            racer.using_item = False
            racer.recently_used_item = None

    if racer.recently_used_item == "mega_mushroom":
        # Gives the user a slight speed boost and provides a shield to prevent some item effects for 10 seconds

        # Remove item from inventory the moment it gets used
        racer.item = None
        if Race_duration <= racer.time_item_used + 10 and "mega" not in racer.status:
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
        if Race_duration <= racer.time_item_used + 10 and "mega" in racer.status:
            if "invulnerable" not in racer.status:
                racer.speed = 1.1 * racer.max_speed
            else:
                racer.speed = 1.1 * speed
        elif Race_duration > racer.time_item_used + 10:
            if "mega" in racer.status:
                racer.status.remove("mega")
            racer.using_item = False
            racer.recently_used_item = None

    if racer.recently_used_item == "bullet_bill":
        # Gives the racer a large speed boost and makes the racer invulnerable for either 8 seconds or until the racer
        # passes 5 others, whichever comes first
        if racer.position == 1:
            if Race_duration <= racer.time_item_used + 2 and "bill" not in racer.status:
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

                # The 'bill' status is required for a very specific situation in which the user activates the bill
                # while in a star. Don't want the code to break because of this
                if "invulnerable" not in racer.status:
                    racer.status.append("invulnerable")
                racer.status.append("bill")
        else:
            if (Race_duration <= racer.time_item_used + 8 and racer.racers_passed < 5 and racer.position != 1 and "bill"
                    not in racer.status):
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

                # The 'bill' status is required for a very specific situation in which the user activates the bill
                # while in a star Don't want the code to break because of this
                if "invulnerable" not in racer.status:
                    racer.status.append("invulnerable")
                racer.status.append("bill")

        if racer.position == 1:
            if Race_duration <= racer.time_item_used + 2:  # If in 1st place when activating the bullet bill, the effect
                # lasts only 2 seconds
                racer.speed = 2 * racer.max_speed
            else:
                racer.racers_passed = 0
                racer.status.remove("invulnerable")
                racer.status.remove("bill")
                Unavailable_items.remove("bullet_bill")
                racer.using_item = None
                racer.item = None
                racer.recently_used_item = None
        else:
            if Race_duration <= racer.time_item_used + 8 and racer.racers_passed < 5 and racer.position != 1:
                racer.speed = 2 * racer.max_speed
            else:
                racer.racers_passed = 0
                racer.status.remove("invulnerable")
                racer.status.remove("bill")
                Unavailable_items.remove("bullet_bill")
                racer.using_item = None
                racer.item = None
                racer.recently_used_item = None

    if racer.recently_used_item == "green_shell":
        # Can either stun the racer in front of the user, behind the user, or do nothing
        racer.item = None

        if racer.action is None:
            racer.action = random.random()
        if racer.position == 1 and racer.user_marker == 0:
            racer.user_marker = 4
        elif racer.position == len(participants) and racer.user_marker == 0:
            racer.user_marker = 5
        elif len(participants) > 2 and racer.position != 1 and racer.position != len(
                participants) and racer.user_marker == 0:
            racer.user_marker = 6

        if racer.user_marker == 4:
            if 0 <= racer.action <= 0.4:  # 40% chance of stunning 2nd place, 60% of doing nothing
                for other_racer in participants:
                    if Race_duration == racer.time_item_used:
                        if (other_racer.position == racer.position + 1) and other_racer.marker not in [1, 2, 3]:
                            other_racer.marker = 1
                    if other_racer.marker == 1:
                        one_sec_stun(racer, other_racer)

        elif racer.user_marker == 5:
            if 0 <= racer.action <= 0.4:  # 40% chance of stunning the racer ahead, 60% chance of doing nothing
                for other_racer in participants:
                    if Race_duration == racer.time_item_used:
                        if (other_racer.position == racer.position - 1) and other_racer.marker not in [1, 2, 3]:
                            other_racer.marker = 1
                    if other_racer.marker == 1:
                        one_sec_stun(racer, other_racer)

        else:
            if 0 <= racer.action <= 0.3:  # 30% chance of stunning the racer behind
                for other_racer in participants:
                    if Race_duration == racer.time_item_used:
                        if (other_racer.position == racer.position + 1) and other_racer.marker not in [1, 2, 3]:
                            other_racer.marker = 1
                    if other_racer.marker == 1:
                        one_sec_stun(racer, other_racer)

            elif 0.3 < racer.action <= 0.6:  # 30% chance of stunning the racer ahead
                for other_racer in participants:
                    if Race_duration == racer.time_item_used:
                        if (other_racer.position == racer.position - 1) and other_racer.marker not in [1, 2, 3]:
                            other_racer.marker = 1
                    if other_racer.marker == 1:
                        one_sec_stun(racer, other_racer)

    if racer.recently_used_item == "trip_green_shell":
        # Similar logic to green shells but a slightly lower chance of doing nothing and the ability to hit racers
        # other than the ones directly ahead or behind

        racer.item = None
        if racer.action is None:
            racer.action = random.random()
        if racer.position == 1 and racer.user_marker == 0:
            racer.user_marker = 4
        elif racer.position == len(participants) and racer.user_marker == 0:
            racer.user_marker = 5
        elif len(participants) > 2 and racer.position != 1 and racer.position != len(
                participants) and racer.user_marker == 0:
            racer.user_marker = 6

        if racer.user_marker == 4:
            if 0 <= racer.action <= 0.5:  # 50% chance of stunning 2nd place
                for other_racer in participants:
                    if Race_duration == racer.time_item_used:
                        if (other_racer.position == racer.position + 1) and other_racer.marker not in [1, 2, 3]:
                            other_racer.marker = 1
                    if other_racer.marker == 1:
                        one_sec_stun(racer, other_racer)
            elif 0.5 < racer.action <= 0.9:  # 40% of hitting any other racer
                for other_racer in participants:
                    if Race_duration == racer.time_item_used:
                        if other_racer.position == racer.position + 1:
                            kart1 = other_racer
                            everyone_else = [r for r in participants if r != kart1]
                            kart = random.choice(everyone_else)
                            if kart.marker not in [1, 2, 3]:
                                kart.marker = 1
                    if other_racer.marker == 1:
                        one_sec_stun(racer, other_racer)

        elif racer.user_marker == 5:
            if 0 <= racer.action <= 0.5:  # 50% chance of stunning 2nd to last place
                for other_racer in participants:
                    if Race_duration == racer.time_item_used:
                        if (other_racer.position == racer.position - 1) and other_racer.marker not in [1, 2, 3]:
                            other_racer.marker = 1
                    if other_racer.marker == 1:
                        one_sec_stun(racer, other_racer)

            elif 0.5 < racer.action <= 0.9:  # 40% chance of hitting anyone else
                for other_racer in participants:
                    if Race_duration == racer.time_item_used:
                        if other_racer.position == racer.position - 1:
                            kart1 = other_racer
                            everyone_else = [r for r in participants if r != kart1]
                            kart = random.choice(everyone_else)
                            if kart.marker not in [1, 2, 3]:
                                kart.marker = 1
                    if other_racer.marker == 1:
                        one_sec_stun(racer, other_racer)

        else:
            if 0 <= racer.action <= 0.35:  # 35% chance of hitting the racer behind
                for other_racer in participants:
                    if Race_duration == racer.time_item_used:
                        if (other_racer.position == racer.position + 1) and other_racer.marker not in [1, 2, 3]:
                            other_racer.marker = 1
                    if other_racer.marker == 1:
                        one_sec_stun(racer, other_racer)

            elif 0.35 < racer.action <= 0.7:  # 35% chance of hitting the racer ahead
                for other_racer in participants:
                    if Race_duration == racer.time_item_used:
                        if (other_racer.position == racer.position - 1) and other_racer.marker not in [1, 2, 3]:
                            other_racer.marker = 1
                    if other_racer.marker == 1:
                        one_sec_stun(racer, other_racer)

            elif 0.7 < racer.action <= 0.9:  # 20% chance of hitting any other racer
                for other_racer in participants:
                    if Race_duration == racer.time_item_used:
                        unaffected = []
                        if other_racer.position == racer.position + 1:
                            unaffected.append(other_racer)
                        if other_racer.position == racer.position - 1:
                            unaffected.append(other_racer)
                        everyone_else = [r for r in participants if r not in unaffected]
                        kart = random.choice(everyone_else)
                        if kart.marker not in [1, 2, 3]:
                            kart.marker = 1
                    if other_racer.marker == 1:
                        one_sec_stun(racer, other_racer)

    if racer.recently_used_item == "blue_shell":
        # When used, stuns the racer in 1st place for 3 seconds
        racer.item = None
        if "blue_shell" in Unavailable_items:
            Unavailable_items.remove("blue_shell")
        for other_racer in participants:
            if Race_duration == racer.time_item_used:
                if other_racer.position == 1 and other_racer.marker != 3:
                    other_racer.marker = 3
            if other_racer.marker == 3:
                three_sec_stun(racer, other_racer)

    if racer.recently_used_item == "red_shell":
        # Similar logic to green shells but slightly higher chance of hitting a racer
        racer.item = None
        if racer.action is None:
            racer.action = random.random()
        if racer.position == 1 and racer.user_marker == 0:
            racer.user_marker = 4
        elif racer.position == len(participants) and racer.user_marker == 0:
            racer.user_marker = 5
        elif len(participants) > 2 and racer.position != 1 and racer.position != len(
                participants) and racer.user_marker == 0:
            racer.user_marker = 6

        if racer.user_marker == 4:
            if 0 <= racer.action <= 0.3:
                for other_racer in participants:
                    if Race_duration == racer.time_item_used:
                        if (other_racer.position == racer.position + 1) and other_racer.marker not in [1, 2, 3]:
                            other_racer.marker = 1
                    if other_racer.marker == 1:
                        one_sec_stun(racer, other_racer)

        elif racer.user_marker == 5:
            if 0 <= racer.action <= 0.7:
                for other_racer in participants:
                    if Race_duration == racer.time_item_used:
                        if (other_racer.position == racer.position - 1) and other_racer.marker not in [1, 2, 3]:
                            other_racer.marker = 1
                    if other_racer.marker == 1:
                        one_sec_stun(racer, other_racer)

        else:
            if 0 <= racer.action <= 0.65:
                for other_racer in participants:
                    if Race_duration == racer.time_item_used:
                        if (other_racer.position == racer.position - 1) and other_racer.marker not in [1, 2, 3]:
                            other_racer.marker = 1
                    if other_racer.marker == 1:
                        one_sec_stun(racer, other_racer)

            elif 0.65 < racer.action <= 0.85:
                for other_racer in participants:
                    if Race_duration == racer.time_item_used:
                        if (other_racer.position == racer.position + 1) and other_racer.marker not in [1, 2, 3]:
                            other_racer.marker = 1
                    if other_racer.marker == 1:
                        one_sec_stun(racer, other_racer)

    if racer.recently_used_item == "trip_red_shell":
        # Similar logic to triple green shells but slightly higher chance of hitting a racer
        racer.item = None
        if racer.action == None:
            racer.action = random.random()
        if racer.position == 1 and racer.user_marker == 0:
            racer.user_marker = 4
        elif racer.position == len(participants) and racer.user_marker == 0:
            racer.user_marker = 5
        elif len(participants) > 2 and racer.position == 2 and racer.user_marker == 0:
            racer.user_marker = 2
        elif len(participants) > 3 and racer.position != 1 and racer.position != 2 and racer.position != len(
                participants) and racer.user_marker == 0:
            racer.user_marker = 6

        if len(participants) >= 3:
            if racer.user_marker == 4:
                if 0 <= racer.action <= 0.4:
                    for other_racer in participants:
                        if Race_duration == racer.time_item_used:
                            if (other_racer.position == racer.position + 1) and other_racer.marker not in [1, 2, 3]:
                                other_racer.marker = 1
                        if other_racer.marker == 1:
                            one_sec_stun(racer, other_racer)

                elif 0.4 < racer.action <= 0.65:
                    for other_racer in participants:
                        if Race_duration == racer.time_item_used:
                            if other_racer.position == racer.position + 1:
                                kart1 = other_racer
                                everyone_else = [r for r in participants if r != kart1]
                                kart = random.choice(everyone_else)
                                if kart.marker not in [1, 2, 3]:
                                    kart.marker = 1
                        if other_racer.marker == 1:
                            one_sec_stun(racer, other_racer)

            elif racer.user_marker == 5:
                if 0 <= racer.action <= 0.6:
                    for other_racer in participants:
                        if Race_duration == racer.time_item_used:
                            if (other_racer.position == racer.position - 1) and other_racer.marker not in [1, 2, 3]:
                                other_racer.marker = 1
                            if (other_racer.position == racer.position - 2) and other_racer.marker not in [1, 2, 3]:
                                other_racer.marker = 1
                        if other_racer.marker == 1:
                            one_sec_stun(racer, other_racer)

                elif 0.6 < racer.action < 0.95:
                    for other_racer in participants:
                        if Race_duration == racer.time_item_used:
                            if (other_racer.position == racer.position - 1) and other_racer.marker not in [1, 2, 3]:
                                other_racer.marker = 1
                        if other_racer.marker == 1:
                            one_sec_stun(racer, other_racer)

            elif racer.user_marker == 2:
                if 0 <= racer.action <= 0.75:
                    for other_racer in participants:
                        if Race_duration == racer.time_item_used:
                            if (other_racer.position == racer.position - 1) and other_racer.marker not in [1, 2, 3]:
                                other_racer.marker = 1
                        if other_racer.marker == 1:
                            one_sec_stun(racer, other_racer)

                elif 0.75 < racer.action <= 0.95:
                    for other_racer in participants:
                        if Race_duration == racer.time_item_used:
                            if (other_racer.position == racer.position + 1) and other_racer.marker not in [1, 2, 3]:
                                other_racer.marker = 1
                        if other_racer.marker == 1:
                            one_sec_stun(racer, other_racer)
            else:
                if 0 <= racer.action <= 0.6:
                    for other_racer in participants:
                        if Race_duration == racer.time_item_used:
                            if (other_racer.position == racer.position - 1) and other_racer.marker not in [1, 2, 3]:
                                other_racer.marker = 1
                            if (other_racer.position == racer.position - 2) and other_racer.marker not in [1, 2, 3]:
                                other_racer.marker = 1
                        if other_racer.marker == 1:
                            one_sec_stun(racer, other_racer)

                elif 0.6 < racer.action <= 0.85:
                    for other_racer in participants:
                        if Race_duration == racer.time_item_used:
                            if (other_racer.position == racer.position - 1) and other_racer.marker not in [1, 2, 3]:
                                other_racer.marker = 1
                        if other_racer.marker == 1:
                            one_sec_stun(racer, other_racer)

                elif 0.85 < racer.action <= 0.95:
                    for other_racer in participants:
                        if Race_duration == racer.time_item_used:
                            if (other_racer.position == racer.position + 1) and other_racer.marker not in [1, 2, 3]:
                                other_racer.marker = 1
                        if other_racer.marker == 1:
                            one_sec_stun(racer, other_racer)

        else:
            if racer.user_marker == 4:
                if 0 <= racer.action <= 0.4:
                    for other_racer in participants:
                        if Race_duration == racer.time_item_used:
                            if (other_racer.position == racer.position + 1) and other_racer.marker not in [1, 2, 3]:
                                other_racer.marker = 1
                        if other_racer.marker == 1:
                            one_sec_stun(racer, other_racer)
            else:
                if 0 <= racer.action <= 0.8:
                    for other_racer in participants:
                        if Race_duration == racer.time_item_used:
                            if (other_racer.position == racer.position - 1) and other_racer.marker not in [1, 2, 3]:
                                other_racer.marker = 1
                        if other_racer.marker == 1:
                            one_sec_stun(racer, other_racer)

    if racer.recently_used_item == "FIB":
        # Works very similarly to shells but a higher chance of missing a racer
        racer.item = None
        if racer.action is None:
            racer.action = random.random()
        if racer.position == 1 and racer.user_marker == 0:
            racer.user_marker = 4
        elif racer.position == len(participants) and racer.user_marker == 0:
            racer.user_marker = 5
        elif len(participants) > 2 and racer.position != 1 and racer.position != len(
                participants) and racer.user_marker == 0:
            racer.user_marker = 6
        if racer.user_marker == 4:
            if 0 <= racer.action <= 0.35:
                for other_racer in participants:
                    if Race_duration == racer.time_item_used:
                        if (other_racer.position == racer.position + 1) and other_racer.marker not in [1, 2, 3]:
                            other_racer.marker = 1
                    if other_racer.marker == 1:
                        one_sec_stun(racer, other_racer)

        elif racer.user_marker == 5:
            if 0 <= racer.action <= 0.35:
                for other_racer in participants:
                    if Race_duration == racer.time_item_used:
                        if (other_racer.position == racer.position - 1) and other_racer.marker not in [1, 2, 3]:
                            other_racer.marker = 1
                    if other_racer.marker == 1:
                        one_sec_stun(racer, other_racer)

        else:
            if 0 <= racer.action <= 0.25:
                for other_racer in participants:
                    if Race_duration == racer.time_item_used:
                        if (other_racer.position == racer.position + 1) and other_racer.marker not in [1, 2, 3]:
                            other_racer.marker = 1
                    if other_racer.marker == 1:
                        one_sec_stun(racer, other_racer)

            elif 0.25 < racer.action <= 0.5:
                for other_racer in participants:
                    if Race_duration == racer.time_item_used:
                        if (other_racer.position == racer.position - 1) and other_racer.marker not in [1, 2, 3]:
                            other_racer.marker = 1
                    if other_racer.marker == 1:
                        one_sec_stun(racer, other_racer)

    if racer.recently_used_item == "banana":
        # Same logic as a green shell and FIB but slightly higher chance of doing nothing
        racer.item = None
        if racer.action is None:
            racer.action = random.random()
        if racer.position == 1:
            if 0 <= racer.action <= 0.3:
                for other_racer in participants:
                    if other_racer.position == racer.position + 1:
                        banana_slowdown(other_racer)

        elif racer.position == len(participants):
            if 0 <= racer.action <= 0.3:
                for other_racer in participants:
                    if other_racer.position == racer.position - 1:
                        banana_slowdown(other_racer)

        else:
            if 0 <= racer.action <= 0.2:
                for other_racer in participants:
                    if other_racer.position == racer.position + 1:
                        banana_slowdown(other_racer)

            elif 0.2 < racer.action <= 0.4:
                for other_racer in participants:
                    if other_racer.position == racer.position - 1:
                        banana_slowdown(other_racer)
        racer.using_item = False
        racer.action = None
        racer.recently_used_item = None

    if racer.recently_used_item == "trip_bananas":
        # Similar to triple green/red shells, but the racer can only hit racers up to 3 positions away
        racer.item = None
        if racer.action is None:
            racer.action = random.random()
        if racer.position == 1:
            if 0 <= racer.action <= 0.4:
                for other_racer in participants:
                    if other_racer.position == racer.position + 1:
                        banana_slowdown(other_racer)

            elif 0.4 < racer.action <= 0.7:
                back_three = []
                for other_racer in participants:
                    if (other_racer.position == racer.position + 1 or
                            other_racer.position == racer.position + 2 or other_racer.position == racer.position + 3):
                        back_three.append(other_racer)
                kart = random.choice(back_three)
                banana_slowdown(kart)

        elif racer.position == len(participants):
            if 0 <= racer.action <= 0.4:
                for other_racer in participants:
                    if other_racer.position == racer.position - 1:
                        banana_slowdown(other_racer)

            elif 0.4 < racer.action <= 0.7:
                front_three = []
                for other_racer in participants:
                    if (other_racer.position == racer.position - 1 or
                            other_racer.position == racer.position - 2 or other_racer.position == racer.position - 3):
                        front_three.append(other_racer)
                kart = random.choice(front_three)
                banana_slowdown(kart)

        else:
            if 0 <= racer.action <= 0.25:
                for other_racer in participants:
                    if other_racer.position == racer.position + 1:
                        banana_slowdown(other_racer)

            elif 0.25 < racer.action <= 0.5:
                for other_racer in participants:
                    if other_racer.position == racer.position - 1:
                        banana_slowdown(other_racer)

            elif 0.5 < racer.action <= 0.7:
                within_three = []
                for other_racer in participants:
                    if (other_racer.position == racer.position + 1 or other_racer.position == racer.position + 2 or
                            other_racer.position == racer.position + 3 or other_racer.position == racer.position - 1 or
                            other_racer.position == racer.position - 2 or other_racer.position == racer.position - 3):
                        within_three.append(other_racer)
                kart = random.choice(within_three)
                banana_slowdown(kart)
        racer.using_item = False
        racer.action = None
        racer.recently_used_item = None

    if racer.recently_used_item == "bob_omb":
        # Similar to triple bananas but a lower chance of doing nothing
        racer.item = None
        if racer.action is None:
            racer.action = random.random()

        if racer.position == 1 and racer.user_marker == 0:
            racer.user_marker = 4
        elif racer.position == len(participants) and racer.user_marker == 0:
            racer.user_marker = 5
        elif len(participants) > 3 and racer.position != 1 and racer.position != 2 and racer.position != len(
                participants) and racer.user_marker == 0:
            racer.user_marker = 6
        if racer.user_marker == 4:
            if 0 <= racer.action <= 0.5:
                for other_racer in participants:
                    if Race_duration == racer.time_item_used:
                        if (other_racer.position == racer.position + 1) and other_racer.marker != 3:
                            other_racer.marker = 3
                    if other_racer.marker == 3:
                        three_sec_stun(racer, other_racer)

            elif 0.5 < racer.action <= 0.8:
                for other_racer in participants:
                    if Race_duration == racer.time_item_used:
                        if (
                                other_racer.position == racer.position + 1 or other_racer.position == racer.position + 2) and other_racer.marker != 3:
                            other_racer.marker = 3
                    if other_racer.marker == 3:
                        three_sec_stun(racer, other_racer)

            elif 0.8 < racer.action <= 0.9:
                for other_racer in participants:
                    if Race_duration == racer.time_item_used:
                        if ((other_racer.position == racer.position + 1 or
                             other_racer.position == racer.position + 2 or other_racer.position == racer.position + 3)
                                and other_racer.marker != 3):
                            other_racer.marker = 3
                    if other_racer.marker == 3:
                        three_sec_stun(racer, other_racer)

        elif racer.user_marker == 5:
            if 0 <= racer.action <= 0.5:
                for other_racer in participants:
                    if Race_duration == racer.time_item_used:
                        if (other_racer.position == racer.position - 1) and other_racer.marker != 3:
                            other_racer.marker = 3
                    if other_racer.marker == 3:
                        three_sec_stun(racer, other_racer)

            elif 0.5 < racer.action <= 0.8:
                for other_racer in participants:
                    if Race_duration == racer.time_item_used:
                        if ((other_racer.position == racer.position - 1 or other_racer.position == racer.position - 2)
                                and other_racer.marker != 3):
                            other_racer.marker = 3
                    if other_racer.marker == 3:
                        three_sec_stun(racer, other_racer)

            elif 0.8 < racer.action <= 0.9:
                for other_racer in participants:
                    if Race_duration == racer.time_item_used:
                        if ((other_racer.position == racer.position - 1 or
                             other_racer.position == racer.position - 2 or other_racer.position == racer.position - 3)
                                and other_racer.marker != 3):
                            other_racer.marker = 3
                    if other_racer.marker == 3:
                        three_sec_stun(racer, other_racer)

        else:
            if 0 <= racer.action <= 0.2:
                for other_racer in participants:
                    if Race_duration == racer.time_item_used:
                        if (other_racer.position == racer.position - 1) and other_racer.marker != 3:
                            other_racer.marker = 3
                    if other_racer.marker == 3:
                        three_sec_stun(racer, other_racer)

            elif 0.2 < racer.action <= 0.35:
                for other_racer in participants:
                    if Race_duration == racer.time_item_used:
                        if ((other_racer.position == racer.position - 1 or other_racer.position == racer.position - 2)
                                and other_racer.marker != 3):
                            other_racer.marker = 3
                    if other_racer.marker == 3:
                        three_sec_stun(racer, other_racer)

            elif 0.35 < racer.action <= 0.45:
                for other_racer in participants:
                    if Race_duration == racer.time_item_used:
                        if ((other_racer.position == racer.position - 1 or
                             other_racer.position == racer.position - 2 or other_racer.position == racer.position - 3)
                                and other_racer.marker != 3):
                            other_racer.marker = 3
                    if other_racer.marker == 3:
                        three_sec_stun(racer, other_racer)

            elif 0.45 < racer.action <= 0.65:
                for other_racer in participants:
                    if Race_duration == racer.time_item_used:
                        if (other_racer.position == racer.position + 1) and other_racer.marker != 3:
                            other_racer.marker = 3
                    if other_racer.marker == 3:
                        three_sec_stun(racer, other_racer)

            elif 0.65 < racer.action <= 0.8:
                for other_racer in participants:
                    if Race_duration == racer.time_item_used:
                        if ((other_racer.position == racer.position + 1 or other_racer.position == racer.position + 2)
                                and other_racer.marker != 3):
                            other_racer.marker = 3
                    if other_racer.marker == 3:
                        three_sec_stun(racer, other_racer)

            elif 0.8 < racer.action <= 0.9:
                for other_racer in participants:
                    if Race_duration == racer.time_item_used:
                        if ((other_racer.position == racer.position + 1 or
                             other_racer.position == racer.position + 2 or other_racer.position == racer.position + 3)
                                and other_racer.marker != 3):
                            other_racer.marker = 3
                    if other_racer.marker == 3:
                        three_sec_stun(racer, other_racer)


# Creating the objects for all of the racers
# Their names and weights are faithful to the original game
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


def update_race_state(participants, num_racers):
    '''
    Runs the race for 1 second
    Args:
        participants (list): the racers present in the race
        num_racers (int): the number of racers in the race

    Returns:
        None
    '''
    global Unavailable_items, Blooper_use_time, POW_use_time, Lightning_use_time
    # Adds the distance, speed, and position at a specific time point to a dataframe that can be visualized in future
    # graphs
    race_data_distance = {"Time Elapsed": [Race_duration]}
    race_data_speed = {"Time Elapsed": [Race_duration]}
    race_data_position = {"Time Elapsed": [Race_duration]}

    rd_list = []
    for i in range(len(participants)):
        rd_list.append(Race_duration)

    # The data from this dataframe is printed in the terminal with each iteration
    race_data = pd.DataFrame({'Racer #': [number for number in range(1, num_racers + 1)], 'Duration': rd_list,
                              'Racer': [character.name for character in participants],
                              'Position': [character.position for character in participants],
                              'Speed': [character.speed for character in participants],
                              'Item': [character.item for character in participants],
                              'Distance': [character.distance_from_start for character in participants]}).set_index(
        "Racer #")
    # Accounts for timing rules for items
    if Race_duration == Lightning_use_time + 30:
        Unavailable_items.remove("lightning_bolt")

    if Race_duration == POW_use_time + 20:
        Unavailable_items.remove("POW")

    if Race_duration == Blooper_use_time + 15:
        Unavailable_items.remove("blooper")

    if Race_duration == 30:
        Unavailable_items.remove("blue_shell")

    sorted_racers = sorted(participants, key=attrgetter('position'), reverse=True)
    for i in range(len(sorted_racers) - 1):
        if sorted_racers[i].distance_from_start > sorted_racers[i + 1].distance_from_start:  # If the racer has traveled
            # a longer distance than the racer in front of it, the first racer has passed the second racer and thus
            # switch positions
            update_position(sorted_racers[i], sorted_racers[i + 1])

    for racer in participants:
        update_distance(racer, 1)

        if (racer.speed != racer.max_speed) and (not racer.status):
            update_speed(racer, 1)

        distance_traveled = racer.distance_from_start
        remainder = distance_traveled % 250
        if (distance_traveled >= 250) and (distance_traveled < finish_line) and (0 <= remainder <= 50) and (
                racer.item is None):  # Item boxes are placed every 250 meters up until 1750 meters. Since some racers
            # may not land exactly on the item box, items are given to racers if they pass up to 50 meters of the item
            # box
            get_item(racer, num_racers)
            racer.time_item_got = Race_duration
            racer.time_delay = random.randint(3, 5)  # Random integer item usage delay to account for the item wheel
            # spinning and landing on the item in the real game
            if racer.item in All_possible_unavailable_items and racer.item not in Unavailable_items:
                Unavailable_items.append(racer.item)

        if racer.item == "lightning_cloud":
            if Race_duration == racer.time_item_got + 1 and racer.item is not None and racer.using_item is False:  # Use
                # the lightning cloud item after 1 second
                # This is faithful to the original game
                racer.recently_used_item = racer.item
                racer.time_item_used = Race_duration
                racer.using_item = True
        else:
            if ((Race_duration == racer.time_item_got + racer.time_delay) or (
                    Race_duration == racer.time_item_got + 2 * racer.time_delay) and racer.item is not None and
                    racer.using_item is False):  # Use an item after the time delay or up until 2x the time delay if
                # they are prevented from using an item
                racer.recently_used_item = racer.item
                racer.time_item_used = Race_duration
                racer.using_item = True

        if racer.recently_used_item is not None:
            use_item(racer, participants)

        # Accounts for multiple status effects combined with each other
        if "stunned" in racer.status and ("1s_stun" in racer.status and "3s_stun" in racer.status):
            racer.status.remove("stunned")
            racer.status.remove("1s_stun")
            racer.status.remove("3s_stun")

        if "stunned" in racer.status and "3s_stun" in racer.status and "invulnerable" in racer.status:
            racer.status.remove("stunned")
            racer.status.remove("3s_stun")
            racer.status.remove("invulnerable")

        if "stunned" in racer.status and "1s_stun" in racer.status and "invulnerable" in racer.status:
            racer.status.remove("stunned")
            racer.status.remove("1s_stun")
            racer.status.remove("invulnerable")

        # Populates the dataframes with the distance, speed, position, and other parameters for each racer
        race_data_distance[racer.name] = [racer.distance_from_start]
        race_data_speed[racer.name] = [racer.speed]
        race_data_position[racer.name] = [racer.position]
        index = race_data.Racer[race_data.Racer == racer.name].index.tolist()
        race_data.loc[index, 'Duration'] = Race_duration
        race_data.loc[index, 'Position'] = racer.position
        race_data.loc[index, 'Speed'] = racer.speed
        race_data.loc[index, 'Item'] = racer.item
        race_data.loc[index, 'Distance'] = racer.distance_from_start

    df_distance = pd.DataFrame(race_data_distance)
    df_speed = pd.DataFrame(race_data_speed)
    df_position = pd.DataFrame(race_data_position)

    # Update positions based on distance
    df_position.iloc[:, 1:] = df_distance.iloc[:, 1:].rank(axis=1, ascending=False, method='min')

    return df_position, df_speed, df_distance, race_data


def run_race_simulation(participants, num_racers):
    '''
    Simulates the entire race by running update_race_state until the race is completed
    Args:
        participants (list): the racers participating in the race
        num_racers (int): the number of racers in the race

    Returns:
        None
    '''
    global df_position, df_speed, df_distance, Race_duration, finish_line, race_data

    finish_line = 2000  # Race length can be changed freely
    df_distance = pd.DataFrame({"Race duration": [Race_duration]})
    df_speed = pd.DataFrame({"Race Duration": [Race_duration]})
    df_position = pd.DataFrame({"Race Duration": [Race_duration]})

    while not all(kart.finished for kart in participants):  # Runs the race until all racers are finished
        Race_duration += 1

        race_data_position, race_data_speed, race_data_distance, race_data = update_race_state(participants, num_racers)

        # Adds the race data from 1 iteration to a larger dataframe for visualization
        df_distance = pd.concat([df_distance, race_data_distance], ignore_index=True)
        df_speed = pd.concat([df_speed, race_data_speed], ignore_index=True)
        df_position = pd.concat([df_position, race_data_position], ignore_index=True)

        # Prints the current state of the race
        print(tabulate(race_data, headers='keys', tablefmt='psql'))

        # Delays the execution of the while loop to view the current race state with each iteration
        time.sleep(1)

        for racer in participants:
            if racer.distance_from_start >= finish_line and racer.finished is False:
                racer.finished = True
    return df_distance, df_position, df_speed


# Where all the other functions will get called and where we will create the animation
def main():
    '''
    Runs all the functions described above
    Returns:
        None
    '''
    # Checks if the user inputs an integer between 2 and 12
    # The error handling at the bottom will handle the cases where the user inputs a string
    n = input("Enter number of racers: ")

    if (int(float(n)) != float(n)) or (float(n) < 2.0) or (float(n) > 12.0):
        print("Must input an integer between 2 and 12, inclusive.")
        sys.exit()
    num_racers = int(float(n))

    # Select int(n) racers at random from the list of all racers
    participants = random.sample(all_racers, num_racers)
    initial_positions = [i for i in range(1, num_racers + 1)]

    # Assign each participant an initial position and initial distance from the starting line. Simulates a staggered
    # start in a race

    for j in range(len(participants)):
        participants[j].position = initial_positions[j]
        participants[j].distance_from_start = -1 * initial_positions[j]

    df_distance, df_position, df_speed = run_race_simulation(participants, num_racers)

    fig, ax = plt.subplots()
    fig2, ax2 = plt.subplots()
    fig2.set_size_inches(8, 5)
    fig3, ax3 = plt.subplots()
    fig3.set_size_inches(8, 5)

    def update_position_movie(frame):
        """
        Creates the position leaderboard for each iteration of the race
        Args:
            frame (int): the current race duration

        Returns:
            None
        """
        ax.clear()
        ax.axis('off')

        # Gets the data for the current frame and sorts the position values in ascending order
        data = df_position.iloc[frame].sort_values(ascending=True, na_position='last')

        # Update the positions of racers based on the current frame
        for i, (index, value) in enumerate(data.items(), start=1):
            for racer in participants:
                if racer.name == index:
                    racer.position = i  # Gives the racers a position to sort for visualization

        # Sort the racers based on their positions
        sorted_racers = sorted(participants, key=lambda x: x.position)

        # Update the positions again to ensure they start from 1 instead of 0 indexing
        for i, racer in enumerate(sorted_racers, start=1):
            racer.position = i

        # Writes the information of the racers in the form of " [position]. [racer_name]"
        racer_info = [f"{racer.position}. {racer.name}" for racer in sorted_racers]

        for i, info in enumerate(racer_info):
            ax.text(0.5, 0.9 - i * 0.1, info, ha='center', va='center', fontsize=8)

        ax.set_title(f'Position Table - Frame {frame + 1}')

    # Creates the position animation
    animation_position = FuncAnimation(fig, update_position_movie, frames=len(df_position), repeat=False)
    animation_position.save('position_animation.gif', writer='pillow', fps=1)

    def update_speed_movie(frame):
        """
        Presents the speeds of the racers throughout the race as a dynamic bar graph
        Args:
            frame (int) : the current race duration

        Returns:

        """
        ax2.clear()
        ax2.bar(df_speed.columns[1:], df_speed.iloc[frame, 1:])  # Bars denote the speed of the racer
        ax2.set_ylim(0, df_speed.iloc[:, 1:].max().max())
        ax2.set_title(f'Speed')
        fig2.autofmt_xdate(rotation=45, ha='right')  # Racer names are rotated to prevent overlapping text

    # Runs the speed bar graph animation
    animation_speed = FuncAnimation(fig2, update_speed_movie, frames=len(df_speed), repeat=False)
    animation_speed.save('speed_animation.gif', writer='pillow', fps=1)

    def update_distance_movie(frame):
        """
        Presents the distance the racers are from the start as a dynamic bar graph
        Args:
            frame (int): current race duration

        Returns:

        """
        ax3.clear()
        ax3.bar(df_distance.columns[1:], df_distance.iloc[frame, 1:])  # Bars denote the distance each racer is from the
        # start
        ax3.set_ylim(0, df_distance.iloc[:, 1:].max().max())
        ax3.set_title(f'Distance')
        fig3.autofmt_xdate(rotation=45, ha='right')  # Racer names are rotated to prevent overlapping text

    animation_distance = FuncAnimation(fig3, update_distance_movie, frames=len(df_distance), repeat=False)
    animation_distance.save('distance_animation.gif', writer='pillow', fps=1)

    plt.show()

    if len(df_distance) < finish_line:
        for racer in participants:
            if racer.finished:
                print(f"{racer.name} has crossed the finish line in Position {racer.position}!")


# Error handling
# First checks if user inputs more than one command line argument
if len(sys.argv) != 1:
    print("Invalid number of inputs")
    sys.exit()
else:
    try:
        main()
    # Prints out a message if user ends a race early
    except KeyboardInterrupt:
        print("The race did not finish!")
    # Prints out a message if user does not enter an integer between 2 and 12
    except ValueError:
        print("Unexpected error occurred. Make sure you input an integer between 2 and 12, inclusive.")
