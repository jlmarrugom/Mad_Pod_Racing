import sys
import math
from sklearn.metrics.pairwise import cosine_similarity
# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

# 1 steps in the future aprox
def move_1step_ahead(
    wp:float,wf:float, present_goal: tuple, future_goal: tuple
    ) -> tuple:
    """
    Assigns weigths to the next two checkpoints so that the Pod starts to turn to the
    second checkpoint before reaching the first.
    """
    step_x = round(wf*future_goal[0] + wp*present_goal[0])
    step_y = round(wf*future_goal[1] + wp*present_goal[1])
    return step_x, step_y

def speed_correction(steps,speed):
    return (steps[0]-speed[0], steps[1]-speed[1])    
    
checkpoints = []

laps = int(input())
checkpoint_count = int(input())
for i in range(checkpoint_count):
    checkpoint_x, checkpoint_y = [int(j) for j in input().split()]
    checkpoints += [(checkpoint_x, checkpoint_y)]

boost_flag = True
orders=["", ""]
pod_pos=[[0,0],[0,0]]
pod_speed=[[0,0],[0,0]]

next_pod_pos=[[0,0],[0,0]]
thrust, angle_to_check=0,0
# game loop
while True:
    for i in range(2):
        # x: x position of your pod
        # y: y position of your pod
        # vx: x speed of your pod
        # vy: y speed of your pod
        # angle: angle of your pod
        # next_check_point_id: next check point id of your pod
        x, y, vx, vy, _, next_check_point_id = [int(j) for j in input().split()]

        pod_pos[i] = [x,y]
        pod_speed[i] = [vx,vy]
        next_pod_pos[i] = [(x+vx), (y+vy)]

        next_checkpoint = checkpoints[next_check_point_id]
        next_checkpoint_dist = math.dist(next_pod_pos[i],next_checkpoint)
        speed = math.hypot(vx,vy)
        next_turn_dist = math.dist(pod_pos[i],next_pod_pos[i])

        try:
            future_next_checkpoint = checkpoints[checkpoints.index(next_checkpoint)+1]
        except:
            future_next_checkpoint = checkpoints[0]

        if boost_flag:
            orders[i] = (str(next_checkpoint[0]) + " " + str(next_checkpoint[1]) + " "+ "BOOST")
            boost_flag = False
            continue
    
        wp, wf = 0.95, 0.05
        step_x, step_y = speed_correction(
            move_1step_ahead(
                wp, wf,
                next_checkpoint,
                future_next_checkpoint),
                [pod_speed[i][0], pod_speed[i][1]])

        orientation_to_step = cosine_similarity(
                [pod_speed[i]],
                [[step_x-pod_pos[i][0], step_y-pod_pos[i][1]]]).item()

        thrust=round(80+20*orientation_to_step)

        if next_checkpoint_dist<=1200:
            wp, wf = 0.6, 0.4
            step_x, step_y = speed_correction(
            move_1step_ahead(
                wp, wf,
                next_checkpoint,
                future_next_checkpoint),
                [pod_speed[i][0], pod_speed[i][1]])
            orientation_to_step = cosine_similarity(
                [pod_speed[i]],
                [[step_x-pod_pos[i][0], step_y-pod_pos[i][1]]]).item()

            thrust=round(50+ 50*orientation_to_step)
        
        orders[i]=(f"{round(step_x)} {round(step_y)} {thrust}")
        
    for i in range(2):
        # x_2: x position of the opponent's pod
        # y_2: y position of the opponent's pod
        # vx_2: x speed of the opponent's pod
        # vy_2: y speed of the opponent's pod
        # angle_2: angle of the opponent's pod
        # next_check_point_id_2: next check point id of the opponent's pod
        x_2, y_2, vx_2, vy_2, angle_2, next_check_point_id_2 = [int(j) for j in input().split()]
        next_opponent_pos = [x_2+vx_2, y_2+vy_2]

        for k, pos in enumerate(pod_pos):
            next_opponent_dist = math.dist(next_opponent_pos, next_pod_pos[k])
            orientation_sim = cosine_similarity(
                [pod_speed[k]],
                [[vx_2, vy_2]]).item()
            order_list = orders[k].split(" ")

            if (next_opponent_dist <= 810) and orientation_sim<=0.5:
                #Adjustment to opponent if hit
                step_x, step_y = speed_correction(
                    [int(order_list[0]), int(order_list[1])], [-vx_2, -vy_2])
                orders[k]=(f"{step_x} {step_y} {'SHIELD'}")
            
            if math.dist(next_pod_pos[0], next_pod_pos[1])<810:
                step_x, step_y = speed_correction(
                    [int(order_list[0]), int(order_list[1])], 
                    [pod_speed[k-1][0], pod_speed[k-1]][1])
                orders[k]=(f"{step_x} {step_y} {order_list[2]}")
                
    for order in orders:
        print(order)
    