import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

# 1 steps in the future aprox
def move_1step_ahead(
    wf:float,wp:float, present_goal: tuple, future_goal: tuple
    ) -> tuple:
    """
    Assigns weigths to the next two checkpoints so that the Pod starts to turn to the
    second checkpoint before reaching the first.
    """
    step_x = round(wf*future_goal[0] + wp*present_goal[0])
    step_y = round(wf*future_goal[1] + wp*present_goal[1])
    return step_x, step_y

def speed_correction(steps:tuple,vx,vy):
    return (steps[0]-vx, steps[1]-vy)

def calculate_relative_angle(current_pos, next_pos, check_pos)->float:
    #change reference - Transform coordinates
    check_dif = [x1-x for x1,x in zip(check_pos,current_pos)]
    angle_to_check = math.degrees(math.atan(check_dif[1]/(check_dif[0]+0.01)))

    next_dif = [x1-x for x1,x in zip(next_pos,current_pos)]
    angle_to_next_pos = math.degrees(math.atan(next_dif[1]/(next_dif[0]+0.01)))
    return angle_to_check+angle_to_next_pos

def calculate_distance(point1, point2):
    return ((point1[0]-point2[0])**2+(point1[1]-point2[1])**2)**0.5
    
checkpoints = []

laps = int(input())
checkpoint_count = int(input())
for i in range(checkpoint_count):
    checkpoint_x, checkpoint_y = [int(j) for j in input().split()]
    checkpoints += [(checkpoint_x, checkpoint_y)]

boost_flag = True
orders=["", ""]
pod_pos=[[0,0],[0,0]]
next_pod_pos=[[0,0],[0,0]]
# game loop
while True:
    for i in range(2):
        # x: x position of your pod
        # y: y position of your pod
        # vx: x speed of your pod
        # vy: y speed of your pod
        # angle: angle of your pod
        # next_check_point_id: next check point id of your pod
        x, y, vx, vy, angle_abs, next_check_point_id = [int(j) for j in input().split()]

        pod_pos[i] = [x,y]
        next_pod_pos[i] = [(x+vx/1), (y+vy/1)]
        next_checkpoint = checkpoints[next_check_point_id]
        next_checkpoint_dist = calculate_distance(pod_pos[i],next_checkpoint)
        next_turn_dist = calculate_distance(pod_pos[i],next_pod_pos[i])
        angle_to_check = calculate_relative_angle(pod_pos[i],next_pod_pos[i],next_checkpoint)

        try:
            future_next_checkpoint = checkpoints[checkpoints.index(next_checkpoint)+1]
        except:
            future_next_checkpoint = checkpoints[0]

        if boost_flag:
            orders[i] = (str(next_checkpoint[0]) + " " + str(next_checkpoint[1]) + " "+ "BOOST")
            boost_flag = False
            continue

        if next_checkpoint_dist<3*next_turn_dist:
            step_x, step_y = speed_correction(move_1step_ahead(
                0.2, 0.8,
                next_checkpoint,
                future_next_checkpoint),vx,vy)
            thrust=round(90+ 5*math.cos(angle_to_check))
            orders[i]=(str(step_x) + " " + str(step_y) + " "+ str(thrust))
        else:
            step_x, step_y = speed_correction(
                move_1step_ahead(
                0.00, 1.00,
                next_checkpoint,
                future_next_checkpoint), vx, vy)
            thrust=round(95+ 5*math.cos(angle_to_check))
            orders[i]=(str(step_x) + " " + str(step_y) + " "+ str(thrust))
        
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
            next_opponent_dist = calculate_distance(next_opponent_pos, next_pod_pos[k])

            if next_opponent_dist <= 810:
                order_list = orders[k].split(" ")
                orders[k]=(order_list[0] + " " + order_list[1] + " SHIELD")
    for order in orders:
        print(order)
    