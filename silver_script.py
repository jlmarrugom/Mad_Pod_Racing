import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.
# 1 steps in the future aprox
def move_1step_ahead(wf:float,wp:float, present_goal, future_goal)->tuple:
    step_x = round(wf*future_goal[0] + wp*present_goal[0])
    step_y = round(wf*future_goal[1] + wp*present_goal[1])
    return step_x, step_y
checkpoints = []

# game loop
while True:
    # next_checkpoint_x: x position of the next check point
    # next_checkpoint_y: y position of the next check point
    # next_checkpoint_dist: distance to the next checkpoint
    # next_checkpoint_angle: angle between your pod orientation and the direction of the next checkpoint
    x, y, next_checkpoint_x, next_checkpoint_y, next_checkpoint_dist, next_checkpoint_angle = [int(i) for i in input().split()]
    opponent_x, opponent_y = [int(i) for i in input().split()]

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr, flush=True)
    next_tuple = (next_checkpoint_x,next_checkpoint_y)
    if next_tuple not in checkpoints:
        checkpoints +=[next_tuple]
        future_next_checkpoint = next_tuple
    else:
        try:
            future_next_checkpoint = checkpoints[checkpoints.index(next_tuple)+1]
        except:
            future_next_checkpoint = checkpoints[0]
    
    if abs(next_checkpoint_angle)<20:
        thrust=100
    elif abs(next_checkpoint_angle)<45:
        thrust=90
    else:
        thrust=85

    #1800 rank2
    if abs(next_checkpoint_angle)<5 and next_checkpoint_dist>5000:
        print(str(next_checkpoint_x) + " " + str(next_checkpoint_y) + " "+ "BOOST")
    elif abs(next_checkpoint_angle)<5 and next_checkpoint_dist<1200:
        step_x, step_y = move_1step_ahead(
            0.4, 0.6, 
            (next_checkpoint_x,next_checkpoint_y),
            future_next_checkpoint)
        print(str(step_x) + " " + str(step_y) + " "+ str(thrust-80))
    else:
        step_x, step_y = move_1step_ahead(
            0.1, 0.9, 
            (next_checkpoint_x,next_checkpoint_y),
            future_next_checkpoint)
        print(str(step_x) + " " + str(step_y) + " "+ str(thrust))

#programming #madmax