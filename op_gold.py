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

def n_pod_mov(e0, v0):
    friction = 0.85
    ef = e0 + friction*v0
    return round(ef)
def n_pod_v(v0,a):
    v = v0 + a
    return v

def step_correction(steps,error):
    return (steps[0]-error[0], steps[1]-error[1])    

def turns_to_point(ef:list, e:list, v:list, thrust_vec:list):
    for t in range(100):
        dist = math.dist(e,ef)
        if dist<=600:
            return t
        e = [n_pod_mov(e_,v_) for e_,v_ in zip(e,v)]
        v = [n_pod_v(v_, thrust_) for v_,thrust_ in zip(v,thrust_vec)]
    return 101

    
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
pod_orientation=[[0.0,0.0],[0.0,0.0]]

next_pod_pos=[[0,0],[0,0]]
thrust = 0
# game loop
while True:
    for i in range(2):
        # x: x position of your pod
        # y: y position of your pod
        # vx: x speed of your pod
        # vy: y speed of your pod
        # angle: angle of your pod
        # next_check_point_id: next check point id of your pod
        x, y, vx, vy, angle, next_check_point_id = [int(j) for j in input().split()]

        pod_pos[i] = [x,y]
        pod_speed[i] = [vx,vy]
        pod_orientation[i] = [1*math.cos(math.radians(angle)), 1*math.sin(math.radians(angle))]

        next_checkpoint = checkpoints[next_check_point_id]
        rel_next_check = [x-y for x,y in zip(next_checkpoint, pod_pos[i])]
        last_checkpoint = checkpoints[next_check_point_id-1]
        rel_last_check = [x-y for x,y in zip(last_checkpoint, pod_pos[i])]
        orientation_to_check = cosine_similarity([pod_orientation[i]], [rel_next_check]).item()
        
        try:
            future_checkpoint = checkpoints[checkpoints.index(next_checkpoint)+1]
        except:
            future_checkpoint = checkpoints[0]
        
        rel_fut_check = [x-y for x,y in zip(future_checkpoint, pod_pos[i])]
        orientation_to_future = cosine_similarity([pod_orientation[i]], [rel_fut_check]).item()

        if boost_flag:
            orders[i] = (str(next_checkpoint[0]) + " " + str(next_checkpoint[1]) + " "+ "BOOST")
            boost_flag = False
            continue

        thrust= 100
        thrust_x, thrust_y = [thrust*pod_orientation[i][0], thrust*pod_orientation[i][1]]
        next_pod_pos[i] = [n_pod_mov(x,vx), n_pod_mov(y,vy)]

        rem_turns = turns_to_point(next_checkpoint, pod_pos[i], pod_speed[i], [thrust_x, thrust_y])

        if rem_turns<=1:
            wp, wf = 0.0, 1.0
            thrust=round(50 + 50*orientation_to_future)
        elif orientation_to_future<=0.5 and rem_turns<=3: #0.5 4 #0.3, 3
            wp, wf = 0.0, 1.0
            thrust=0
        elif orientation_to_check<=0.8:
            wp, wf = 1.0, 0.0
            thrust=round(50 + 50*orientation_to_check)
        else:
            wp, wf = 0.95, 0.05
            thrust= 100
        
        step_x, step_y = step_correction(
                move_1step_ahead(
                    wp, wf,
                    next_checkpoint,
                    future_checkpoint),
                    [vx +thrust_x*0.5, vy+thrust_y*0.5])
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

            if (next_opponent_dist <= 810) and orientation_sim<=0.0:
                #Adjustment to opponent if hit
                step_x, step_y = step_correction(
                    [int(order_list[0]), int(order_list[1])], [vx_2, vy_2])
                orders[k]=(f"{step_x} {step_y} {'SHIELD'}")
            
            if math.dist(next_pod_pos[0], next_pod_pos[1])<810:
                step_x, step_y = step_correction(
                    [int(order_list[0]), int(order_list[1])], 
                    [pod_speed[k-1][0], pod_speed[k-1]][1])
                orders[k]=(f"{step_x} {step_y} {order_list[2]}")
                
    for order in orders:
        print(order)
    