import random
import sys
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

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
            s = int(23 * random.uniform(1.0, 1.5))
            self.max_speed = s
            self.speed = 0
        if weight == "Medium":
            s = int(25 * random.uniform(1.0, 1.5))
            self.max_speed = s
            self.speed = 0
        if weight == "Heavy":
            s = int(27 * random.uniform(1.0, 1.5))
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

all_racers = [
    Racer("Mario", "Medium"), Racer("Luigi", "Medium"), Racer("Peach", "Medium"), Racer("Daisy", "Medium"),
    Racer("Yoshi", "Medium"), Racer("Diddy Kong", "Medium"), Racer("Birdo", "Medium"), Racer("Bowser Jr.", "Medium"),
    Racer("Baby Mario", "Light"), Racer("Baby Luigi", "Light"), Racer("Baby Peach", "Light"), Racer("Baby Daisy", "Light"),
    Racer("Toad", "Light"), Racer("Toadette", "Light"), Racer("Koopa Troopa", "Light"), Racer("Dry Bones", "Light"),
    Racer("Bowser", "Heavy"), Racer("Rosalina", "Heavy"), Racer("Funky Kong", "Heavy"), Racer("Donkey Kong", "Heavy"),
    Racer("Wario", "Heavy"), Racer("Waluigi", "Heavy"), Racer("Dry Bowser", "Heavy"), Racer("King Boo", "Heavy")
]

def update_position(race_data_distance):
    # Sort the racers based on their distance_from_start
    sorted_racers = race_data_distance.iloc[:, 1:].mean().sort_values(ascending=False).index
    
    # Create a DataFrame for position
    race_data_position = {"time": [race_data_distance.iloc[0, 0]]}
    for distance, racer in enumerate(sorted_racers, start=1):
        race_data_position[racer] = [distance]

    return pd.DataFrame(race_data_position)

def update_distance(racer, time):
    # Changes the distance the racer has traveled in a certain time (in this case I used 1 second, but we can change
    # it based on how the race looks and the processing power of our computers). This also assumes the racer speeds
    # are all in m/s
    distance = racer.distance_from_start + (racer.speed * time)
    racer.distance_from_start = distance

    # Update the racer's position based on their distance from the start line
    racer.position = int(racer.distance_from_start)

def update_speed(racer, time):
    # Adjusts the speed of the racer based on its acceleration. The method assumes 1 second has passed
    if racer.speed < racer.max_speed:
        speed = racer.speed + racer.acceleration * time
        if speed >= racer.max_speed:
            racer.speed = racer.max_speed
        else:
            racer.speed = speed

def update_race_state(participants, time):
    race_data_distance = {"time": [time]}
    race_data_speed = {"time": [time]}
    
    for racer in participants:
        update_speed(racer, 1)
        update_distance(racer, 1)
        race_data_distance[racer.name] = [racer.distance_from_start]
        race_data_speed[racer.name] = [racer.speed]

    df_distance = pd.DataFrame(race_data_distance)
    df_speed = pd.DataFrame(race_data_speed)
    df_position = update_position(df_distance)
    return df_distance, df_speed, df_position

def run_race_simulation(participants):
    finish_line = 2000  # Adjust the finish line distance as needed

    time = 0

    df_speed = pd.DataFrame({"time": []})
    df_distance = pd.DataFrame({"time": []})
    df_position = pd.DataFrame({"time": []})
    while True:
        time += 1

        race_data_distance, race_data_speed, race_data_position = update_race_state(participants, time)

        df_distance = pd.concat([df_distance, race_data_distance], ignore_index=True)
        df_speed = pd.concat([df_speed, race_data_speed], ignore_index=True)
        df_position = pd.concat([df_position, race_data_position], ignore_index=True)
        if any(racer.distance_from_start >= finish_line for racer in participants):
            break
    print(df_distance)
    print(df_speed)
    print(df_position)
    return df_distance, df_speed, df_position

def main():
    # Checks if the user inputs an integer between 2 and 12
    # The error handling at the bottom will handle the cases where the user inputs a string
    n = input("Enter number of racers: ")
    if not (n.isdigit() and 2 <= int(n) <= 12):
        print("Must input an integer between 2 and 12, inclusive.")
        sys.exit()

    num_racers = int(n)
    participants = random.sample(all_racers, num_racers)
    initial_positions = [i for i in range(1, num_racers + 1)]

    for j in range(len(participants)):
        participants[j].position = initial_positions[j]
        participants[j].distance_from_start = -1 * initial_positions[j]

    df_distance, df_speed, df_position = run_race_simulation(participants)

    # Set up the figure and axis for the position movie
    fig, ax = plt.subplots()

    # Function to update the bar graph for each time instance
    def update_distance_movie(frame):
        ax.clear()
        ax.bar(df_distance.columns[1:], df_distance.iloc[frame, 1:])
        ax.set_ylim(0, df_distance.iloc[:, 1:].max().max())
        ax.set_title(f'Time: {df_distance.iloc[frame, 0]} seconds - Distance')

    # Create the position animation
    animation_distance = FuncAnimation(fig, update_distance_movie, frames=len(df_distance), repeat=False)

    # Set up the figure and axis for the speed movie
    fig2, ax2 = plt.subplots()

    # Function to update the bar graph for each time instance
    def update_speed_movie(frame):
        ax2.clear()
        ax2.bar(df_speed.columns[1:], df_speed.iloc[frame, 1:])
        ax2.set_ylim(0, df_speed.iloc[:, 1:].max().max())
        ax2.set_title(f'Time: {df_speed.iloc[frame, 0]} seconds - Speed')

    # Create the speed animation
    animation_speed = FuncAnimation(fig2, update_speed_movie, frames=len(df_speed), repeat=False)
    
    fig3, ax3 = plt.subplots()
    # Function to update the bar graph for each time instance
    def update_position_movie(frame):
        ax3.clear()
        ax3.set_title(f'Time: {df_position.iloc[frame, 0]} seconds - Position')
    
    # Create a horizontal bar plot for the position leaderboard with inverted y-axis
        ax3.barh(df_position.columns[1:], df_position.iloc[frame, 1:], color='skyblue')
    
    # Invert the y-axis
        ax3.invert_yaxis()
    
    # Add labels and annotations if needed
        for i, value in enumerate(df_position.iloc[frame, 1:]):
            ax.text(value + 0.1, i, str(value), va='center', fontsize=8)

# Create the position animation
    animation_position = FuncAnimation(fig3, update_position_movie, frames=len(df_position), repeat=False)


    # Display the animations
    plt.show()
    print(df_distance)
    print(df_speed)
    print(df_position)
    

if __name__ == "__main__":
    main()
    
    
