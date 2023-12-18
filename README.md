# Mario Kart Wii Simulation in Python

This was done as a final project for a university-level programming class. It was created by Justin Lam (repo owner), Mourya Chimpiri, and Idrees Bedar from Stony Brook University.

It simulates a typical race between CPUs in Mario Kart Wii. Users are able to choose between 2-12 racers and visualize that number of CPUs racing along the track. Run this function by typing python mkw.py into the command line once you are in the same directory as mkw.py. After typing this command, type in an integer from 2 to 12 when the program prompts you to "Enter the number of racers."

Please note that this simulation contains bugs and is missing certain features regarding item functionality, such as the inability for the racers to hit other racers when in a star, a bullet bill, or mega mushroom. It also heavily simplifies the race track, and the way the racers are visualized involve nothing but tables and bar graphs. We are considering fixing those bugs and adding more features in the future, but we will hold off on that for the time being.

Racer- This class initializes Racer objects for each participant in the computer-simulated race. Each racer is initialized with a certain name and weight. The maximum speed of each racer is initialized as a scalar (light: 23, medium: 25, heavy: 27) multiplied by a random float from 1 to 1.5. The acceleration is the maximum speed divided by a scalar (light: 3, medium: 4, heavy: 5). Each racer also has attributes that assist in item functionality (position, item, recently_used_item, distance_from_start, status, racers_passed, time_item_got, time_item_used, time_delay, using_item, action, shocked, marker, user_marker, TC_initial, TC_final, and finished).

update_position- Swaps the positions of two racers. This function is called if the distance traveled of one racer is larger than the racer in the position ahead

update_distance- Changes the distance of a racer using the racer speed

update_speed- Changes the speed of a racer using the racer acceleration. The racer speed is updated if it is below the maximum speed, and the maximum speed is the upper bound of the racer speed

choose_item- Picks an item when a racer passes an item box from the possible items. The item probabilities are first summed and a random float from 0 to the total probability is found. Based on this random float, the corresponding item is acquired by the racer

possible_item- Gets all the possible items a racer can get based on their position, the number of racers in the race, and the item number and timing limits

update_probabilities- Updates the item probabilities based on unavailable items. This method ensures that if an item is unavailable, the racer will still always get an item from an item box, assuming that they do not currently possess an item

get_item- Gives a racer an item based on the possible items. The function cycles through the dictionary of item probabilities for each number of racers and chooses an item based on the racer position and if there are unavailable items

max_speed_slowdown- Adjusts the speed of the racer if they have different combinations of status effects at once. 

one_sec_stun- Stuns the racer and changes the racer speed to 0 for 1 second

three_sec_stun- Stuns the racer and changes the racer speed to 0 for 3 seconds

banana_slowdown- Reduces the racer speed by 1/2 if the racer is hit by a banana

use_item- Uses the item a racer is holding. The effect of using each item varies immensely for all 19 items

update_race_state- Runs the race for 1 second. The function updates the distance, speed, position, and items each racer has and places the data in a dataframe to be visualized in the terminal while the script is running. Racers are given an item when their distance surpasses an item box by at most 50 meters. Racers who acquire an item also receive a time delay for item use

run_race_simulation- Simulates the entirety of the race by calling update_race_state until all racers have finished the race. The function also compiles all the race data from each iteration into a single dataframe

main- Runs all the functions mentioned previously. This function initializes the participants in the race by picking a certain number of racers from the character roster of 24, depending on user input. The positions of each racer are also initialized to create a staggered start grid

update_position_movie- Creates a position leaderboard that changes with each iteration of the race. The resultant animation is saved as position_animation.gif

update_speed_movie- Displays the speeds of each racer in a dynamic bar graph that changes with each iteration of the race. The resultant animation is saved as speed_animation.gif

update_distance_movie- Displays the distances traveled of each racer in a dynamic bar graph that changes with each iteration of the race. The resultant animation is saved as distance_animation.gif
