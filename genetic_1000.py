#1063 1078
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

# genetic algorithm search for continuous function optimization
from numpy.random import randint, rand
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

 
# decode bitstring to numbers
def decode(bounds, n_bits, bitstring:list):
    decoded = list()
    largest = 2**n_bits
    for i in range(len(bounds)):
        # extract the substring for the i bound (variable)
        start, end = i * n_bits, (i * n_bits)+n_bits
        substring = bitstring[start:end]
        # convert bitstring to a string of chars
        chars = ''.join([str(s) for s in substring])
        # convert string to integer
        integer = int(chars, 2)
        # scale integer to desired range
        value = bounds[i][0] + (integer/largest) * (bounds[i][1] - bounds[i][0])
        # store
        decoded.append(value)
    return decoded
 
# tournament selection
def selection(pop, scores, k=3):
    # first random selection
    selection_ix = randint(len(pop))
    for ix in randint(0, len(pop), k-1):
        # check if better (e.g. perform a tournament)
        if scores[ix] < scores[selection_ix]:
            selection_ix = ix

    return pop[selection_ix]
 
# crossover two parents to create two children
def crossover(p1, p2, r_cross):
    # children are copies of parents by default
    c1, c2 = p1.copy(), p2.copy()
    # check for recombination
    if rand() < r_cross:
        # select crossover point that is not on the end of the string
        pt = randint(1, len(p1)-2)
        # perform crossover
        c1 = np.append(p1[:pt], p2[pt:])
        c2 = np.append(p2[:pt], p1[pt:])
    return [c1, c2]
 
# mutation operator
def mutation(bitstring, r_mut):
    for i in range(len(bitstring)):
        # check for a mutation
        if rand() < r_mut:
            # flip the bit
            bitstring[i] = 1 - bitstring[i]
    return bitstring
 
# genetic algorithm
def genetic_algorithm(objective, bounds, n_bits, n_iter, n_pop, r_cross, r_mut, pbest):
    # initial population of random bitstring
    
    if pbest is None:
        pop = [randint(0, 2, n_bits*len(bounds)) for _ in range(n_pop)]
        # keep track of best solution
        best, best_eval = pop[0], objective(decode(bounds, n_bits, pop[0]))
    #start from the previous best
    else:
        pop = [pbest if i==0 else randint(0, 2, n_bits*len(bounds)) for i in range(n_pop)]
        best, best_eval = pop[0], objective(decode(bounds, n_bits, pop[0]))
    # enumerate generations
    for gen in range(n_iter):
        # decode population
        decoded = [decode(bounds, n_bits, p) for p in pop]
        # evaluate all candidates in the population
        scores = [objective(d) for d in decoded]
        # check for new best solution
        for i in range(n_pop):
            if scores[i] < best_eval:
                best, best_eval = pop[i], scores[i]
                #print(">%d, new best f(%s) = %f" % (gen,  decoded[i], scores[i]))

        # select parents
        selected = [selection(pop, scores) for _ in range(n_pop)]
        # create the next generation
        children = list()
        for i in range(0, n_pop, 2):
            # get selected parents in pairs
            p1, p2 = selected[i], selected[i+1]
            # crossover and mutation
            for c in crossover(p1, p2, r_cross):
                # mutation
                mut_child = mutation(c, r_mut)
                # store for next generation
                children.append(mut_child)
                # replace population
                pop = children
    return [best, best_eval]

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

#We'll save the Checkpoints on a List to anticipate them
checkpoints = []

laps = int(input())
checkpoint_count = int(input())
for i in range(checkpoint_count):
    checkpoint_x, checkpoint_y = [int(j) for j in input().split()]
    checkpoints += [(checkpoint_x, checkpoint_y)]

orders=["", ""]
pod_orientation=[[0.0,0.0],[0.0,0.0]]
pbest = [None, None]
pscore=[None, None]
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
        pod_orientation[i] = [1*math.cos(math.radians(angle)), 1*math.sin(math.radians(angle))]

        check_pos = checkpoints[next_check_point_id]
        try:
            future_check_pos = checkpoints[checkpoints.index(check_pos)+1]
        except:
            future_check_pos = checkpoints[0]

        # define the total iterations 100 #18 #10
        n_iter = 18
        # bits per variable 16def
        n_bits = 16
        # define the population size 100 #4
        n_pop = 4
        # crossover rate
        r_cross = 0.9

        # define range for input
        bounds = [
            [math.radians(angle)- math.radians(18), math.radians(angle)+ math.radians(18)],
            [0, 200]]

        # mutation rate
        r_mut = 1.0 / (float(n_bits) * len(bounds))

        # objective function
        def objective(w):
            """w0:angle, x1:ny, x2: thrust"""
            #desired_pos = [x+2000*math.cos(w[0]), y+2000*math.sin(w[0])]
            npos = [x+0.85*vx, y+0.85*vy] #desired_pos
            fpos = [
                npos[0] + 0.85*(vx + w[1]*math.cos(w[0])), #npos, podorientation[i] / #desired_pos
                npos[1] + 0.85*(vy + w[1]*math.sin(w[0]))
                ]

            fdist_to_check = math.dist(fpos, check_pos)
            
            rem_turns = turns_to_point(
                ef=check_pos, e=[x,y], v=[vx, vy], #x,y
                thrust_vec= [w[1]*math.cos(w[0]), w[1]*math.sin(w[0])]) #pod orientation
            frem_turns = turns_to_point(
                ef=future_check_pos, e=[x,y], v=[vx, vy], 
                thrust_vec= [w[1]*math.cos(w[0]), w[1]*math.sin(w[0])])
            return (
                10*rem_turns
                + 0.1*frem_turns
                + 0.1*fdist_to_check
                - 0.1*w[1]
                )

        # perform the genetic algorithm search
        best, score = genetic_algorithm(
            objective, bounds, 
            n_bits, n_iter, n_pop, r_cross, r_mut,
            pbest[i])
        decoded = decode(bounds, n_bits, best)
        orders[i]=(
            f"{round(x+2000*math.cos(decoded[0]))} {round(y+2000*math.sin(decoded[0]))} {round(decoded[1])}")
        pbest[i] = best

    for i in range(2):
        # x_2: x position of the opponent's pod
        # y_2: y position of the opponent's pod
        # vx_2: x speed of the opponent's pod
        # vy_2: y speed of the opponent's pod
        # angle_2: angle of the opponent's pod
        # next_check_point_id_2: next check point id of the opponent's pod
        x_2, y_2, vx_2, vy_2, angle_2, next_check_point_id_2 = [int(j) for j in input().split()]

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr, flush=True)


    #Give orders to the Pods
    for order in orders:
        print(order)
