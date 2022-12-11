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

#Using game physics
def n_pod_mov(e0: float, v0:float) -> int:
    """Calculates the next pod's position"""
    friction = 0.85
    ef = e0 + friction*v0
    return round(ef)
def n_pod_v(v0:float, a:float)-> float:
    """Calculates the next pod's speed"""
    v = v0 + a
    return v

def step_correction(steps:list,error:list)->tuple:
    """Substracts an error amount from the calculated step"""
    return (steps[0]-error[0], steps[1]-error[1])    


def turns_to_point(ef:list, e:list, v:list, thrust_vec:list) -> int:
    """Using the game physics, calculates in how many t's the pod will reach the checkpoint"""
    #starting at t = 0 (this turn)
    for t in range(100):
        dist = math.dist(e,ef)
        #If checkpoint is reached
        if dist<=600:
            return t
        #if not, we calculate the next pod position, and speed, then check again
        e = [n_pod_mov(e_,v_) for e_,v_ in zip(e,v)]
        v = [n_pod_v(v_, thrust_) for v_,thrust_ in zip(v,thrust_vec)]
    return 101

def get_first_op_id(pods_next_check:list)->int:
    """Returns the Id of the first opponent's Pod"""
    if pods_next_check[2][0] < pods_next_check[3][0]:
        id= 3
    elif pods_next_check[2][0] > pods_next_check[3][0]:
        id= 2
    else:
        if pods_next_check[2][1] < pods_next_check[3][1]:
            id= 3
        elif pods_next_check[2][1] > pods_next_check[3][1]:
            id= 2
        else:
            if pods_next_check[2][2] < pods_next_check[3][2]:
                id= 2
            elif pods_next_check[2][2] > pods_next_check[3][2]:
                id= 3
            else: id = 2
    return id

def get_my_last_id(pods_next_check:list):
    """Returns the Id of my last Pod"""
    if pods_next_check[0][0] < pods_next_check[1][0]:
        id= 0
    elif pods_next_check[0][0] > pods_next_check[1][0]:
        id= 1
    else:
        if pods_next_check[0][1] < pods_next_check[1][1]:
            id= 0
        elif pods_next_check[0][1] > pods_next_check[1][1]:
            id= 1
        else:
            if pods_next_check[0][2] < pods_next_check[1][2]:
                id= 1
            elif pods_next_check[0][2] > pods_next_check[1][2]:
                id= 0 
            else: id = 0
    return id

#We'll save the Checkpoints on a List to anticipate them
checkpoints = []

laps = int(input())
checkpoint_count = int(input())
for i in range(checkpoint_count):
    checkpoint_x, checkpoint_y = [int(j) for j in input().split()]
    checkpoints += [(checkpoint_x, checkpoint_y)]

#We define the game lists: [x, y]
boost_flag = True
orders=["", ""]
pod_pos=[[0,0],[0,0]]
pod_speed=[[0,0],[0,0]]
op_speed=[[0,0],[0,0]]
pod_orientation=[[0.0,0.0],[0.0,0.0]]
#each list represents: [lap, checkpoint_id, check_dist]
pods_next_check=[[0,0,0], [0,0,0], [0,0,0], [0,0,0]]

next_pod_pos=[[0,0],[0,0]]
op_pos=[[0,0],[0,0]]
next_opponent_pos = [[0,0],[0,0]]
next_checkpoint_2 = [[0,0],[0,0]]
future_checkpoint_2 = [[0,0],[0,0]]
thrust = 0
# game loop
while True:
    #My pod's status
    for i in range(2):
        x, y, vx, vy, angle, next_check_point_id = [int(j) for j in input().split()]

        pod_pos[i] = [x,y]
        #save positions to then verify who is first and who is last >:)
        if next_check_point_id!=pods_next_check[i][1]:
            pods_next_check[i][1] = next_check_point_id
            if pods_next_check[i][1] == 0:
                pods_next_check[i][0] += 1 #laps

        pod_speed[i] = [vx,vy]
        pod_orientation[i] = [1*math.cos(math.radians(angle)), 1*math.sin(math.radians(angle))]

        next_checkpoint = checkpoints[next_check_point_id]
        #We calculate the position of the next checkpoint relative to the Pod
        rel_next_check = [x-y for x,y in zip(next_checkpoint, pod_pos[i])]
        #save dist to check
        pods_next_check[i][2] = round(math.dist(pod_pos[i], next_checkpoint))
        
        last_checkpoint = checkpoints[next_check_point_id-1]
        rel_last_check = [x-y for x,y in zip(last_checkpoint, pod_pos[i])]
        orientation_to_check = cosine_similarity([pod_orientation[i]], [rel_next_check]).item()
        
        try:
            future_checkpoint = checkpoints[checkpoints.index(next_checkpoint)+1]
        except:
            future_checkpoint = checkpoints[0]
        
        rel_fut_check = [x-y for x,y in zip(future_checkpoint, pod_pos[i])]
        orientation_to_future = cosine_similarity([pod_orientation[i]], [rel_fut_check]).item()          

        thrust= 100
        thrust_x, thrust_y = [thrust*pod_orientation[i][0], thrust*pod_orientation[i][1]]
        next_pod_pos[i] = [n_pod_mov(x,vx), n_pod_mov(y,vy)]

        #We calculate the number of remaining turns to make decisions
        rem_turns = turns_to_point(next_checkpoint, pod_pos[i], pod_speed[i], [thrust_x, thrust_y])

        if rem_turns<=1:
            wp, wf = 0.1, 0.9
            thrust=round(50 + 50*orientation_to_future)
        elif orientation_to_future<=0.5 and rem_turns<=3: #0.5 4 #0.3, 3
            wp, wf = 0.2, 0.8
            thrust=round(50 + 50*orientation_to_future)
        elif orientation_to_future<=0.8 and rem_turns<=3: #0.5 4 #0.3, 3
            wp, wf = 0.5, 0.5
            thrust=round(50 + 50*orientation_to_future)
        elif orientation_to_check<=0.8:
            wp, wf = 1.0, 0.0
            thrust=round(50 + 50*orientation_to_check)
        else:
            wp, wf = 1.0, 0.0
            thrust= 'BOOST'
        
        #We correct of direction depending on the thrust, remaining turns, and velocity (Should be improved)
        step_x, step_y = step_correction(
                move_1step_ahead(
                    wp, wf,
                    next_checkpoint,
                    future_checkpoint),
                    [0.05*rem_turns*vx +thrust_x*0.5, 0.05*rem_turns*vy+thrust_y*0.5])
        
        #We save the orders on a list before printing it, so we could modify them after looking at the opponets 
        orders[i]=(f"{round(step_x)} {round(step_y)} {thrust}")
    
    #Opponents Status
    for i in range(2):
        x_2, y_2, vx_2, vy_2, angle_2, next_check_point_id_2 = [int(j) for j in input().split()]
        op_pos[i] = [x_2, y_2]
        next_opponent_pos[i] = [x_2+vx_2, y_2+vy_2]
        next_checkpoint_2[i] = checkpoints[next_check_point_id_2]
        op_speed[i] = [vx_2, vy_2]
        
        try:
            future_checkpoint_2[i] = checkpoints[checkpoints.index(next_checkpoint_2[i])+1]
        except:
            future_checkpoint_2[i] = checkpoints[0]

        #save positions
        if next_check_point_id_2!=pods_next_check[i+2][1]:
            pods_next_check[i+2][1] = next_check_point_id_2
            if pods_next_check[i+2][1] == 0:
                pods_next_check[i+2][0] += 1 #laps

        #save dist to check
        pods_next_check[i+2][2] = round(math.dist(op_pos[i], next_checkpoint_2[i]))

        #Defense against opponents Pods
        for k, pos in enumerate(pod_pos):
            next_opponent_dist = math.dist(next_opponent_pos[i], next_pod_pos[k])
            orientation_sim = cosine_similarity(
                [pod_speed[k]],
                [[vx_2, vy_2]]).item()
            order_list = orders[k].split(" ")

            #My last pod attacts first opponent's Pod
            #Dirty ship offense
            if k == get_my_last_id(pods_next_check):
                #What is his first Pod's Id?
                f_op_id = get_first_op_id(pods_next_check)-2
                f_opponent_dist = math.dist(next_opponent_pos[f_op_id], next_pod_pos[k])
                f_op_orientation_sim = cosine_similarity(
                    [pod_speed[k]],
                    [op_speed[i]]).item()
                op_dist_to_check = math.dist(next_checkpoint_2[f_op_id],op_pos[f_op_id])
                my_dist_to_op_check = math.dist(next_checkpoint_2[f_op_id], next_pod_pos[k])
                
                #if opponent is near:
                if (f_opponent_dist <= 1500): #1500
                    step_x, step_y = step_correction(
                        [round(
                            0.0*op_pos[f_op_id][0] + 0.9*next_opponent_pos[f_op_id][0] + 0.1*next_checkpoint_2[f_op_id][0]+ 0.0*future_checkpoint_2[f_op_id][0]), 
                        round(
                            0.0*op_pos[f_op_id][1] + 0.9*next_opponent_pos[f_op_id][1] + 0.1*next_checkpoint_2[f_op_id][1]+ 0.0*future_checkpoint_2[f_op_id][1])],
                        [pod_speed[k][0]-op_speed[f_op_id][0], pod_speed[k][1]-op_speed[f_op_id][1]])
                    thrust =100
                elif (f_opponent_dist <= 3000): #1500
                    step_x, step_y = step_correction(
                        [round(
                            0.0*op_pos[f_op_id][0] + 0.5*next_opponent_pos[f_op_id][0] + 0.4*next_checkpoint_2[f_op_id][0]+ 0.1*future_checkpoint_2[f_op_id][0]), 
                        round(
                            0.0*op_pos[f_op_id][1] + 0.5*next_opponent_pos[f_op_id][1] + 0.4*next_checkpoint_2[f_op_id][1]+ 0.1*future_checkpoint_2[f_op_id][1])],
                        [pod_speed[k][0]-op_speed[f_op_id][0], pod_speed[k][1]-op_speed[f_op_id][1]])
                    thrust =95
                else:
                    step_x, step_y = step_correction(
                        [round(
                            0.4*next_opponent_pos[f_op_id][0] + 0.3*next_checkpoint_2[f_op_id][0]+ 0.3*future_checkpoint_2[f_op_id][0]), 
                        round(
                            0.4*next_opponent_pos[f_op_id][1] + 0.3*next_checkpoint_2[f_op_id][1]+ 0.3*future_checkpoint_2[f_op_id][1])],
                        [pod_speed[k][0]-op_speed[f_op_id][0], pod_speed[k][1]-op_speed[f_op_id][1]])
                    thrust = 90
                
                #thrust = round(90 + 10*(1-orientation_sim)) #90 10 orient
                if (thrust > 95) and (f_opponent_dist <= 1000) and orientation_sim<0.0:
                    orders[k]=(f"{op_pos[f_op_id][0]} {op_pos[f_op_id][1]} {'BOOST'}")
                else:
                    orders[k]=(f"{step_x} {step_y} {thrust}")
                
                #If future opponent will hit us
                if (f_opponent_dist <= 810):
                    #Adjustment to opponent if hit
                    order_list = orders[k].split(" ")
                    step_x, step_y = step_correction(
                        [int(order_list[0]), int(order_list[1])], 
                        [op_speed[f_op_id][0], op_speed[f_op_id][1]])
                    orders[k]=(f"{step_x} {step_y} {'SHIELD'}")

                #If our dirty ship encounters our clean ship 
                if math.dist(next_pod_pos[0], next_pod_pos[1])<810:
                    order_list = orders[k].split(" ")
                    step_x, step_y = step_correction(
                        [int(order_list[0]), int(order_list[1])], 
                        [pod_speed[k-1][0], pod_speed[k-1]][1])
                    orders[k]=(f"{step_x} {step_y} {0}")
            
            #Clean ship defense
            else:
                #If the'll collide at a very different angle
                if (next_opponent_dist <= 810) and orientation_sim<=0.5:
                    #Adjustment to opponent if hit
                    order_list = orders[k].split(" ")
                    step_x, step_y = step_correction(
                        [int(order_list[0]), int(order_list[1])], [vx_2, vy_2])
                    orders[k]=(f"{step_x} {step_y} {'SHIELD'}")
                
                #adjust to oponent's collisions
                if (next_opponent_dist <= 1000):
                    order_list = orders[k].split(" ")
                    step_x, step_y = step_correction(
                        [int(order_list[0]), int(order_list[1])], 
                        [op_speed[i][0], op_speed[i][1]])
                    orders[k]=(f"{step_x} {step_y} {order_list[2]}")

                if math.dist(next_pod_pos[0], next_pod_pos[1])<810:
                    order_list = orders[k].split(" ")
                    step_x, step_y = step_correction(
                        [int(order_list[0]), int(order_list[1])], 
                        [pod_speed[k-1][0], pod_speed[k-1]][1])
                    orders[k]=(f"{step_x} {step_y} {order_list[2]}")

    for order in orders:
        print(order)
    