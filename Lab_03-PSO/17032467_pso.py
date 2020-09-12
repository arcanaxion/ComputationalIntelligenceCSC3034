import random
import matplotlib.pyplot as plt

class Particle:
    def __init__(self, position = 0, velocity = 0):
        self.position = position
        self.velocity = velocity
        self.best_position = position
        self.position_list = [position]
        self.velocity_list = [velocity]
        self.best_position_list = []

    def update_personal_best(self):
        # 1. calculate the fitnesses of the best_position and the particle's current 
        # 2. compare the fitnesses and determine if the current position is better than the best_position
        # 3. update if necessary
        # 4. no return statement is required
        if fit_fcn(self.position) < fit_fcn(self.best_position):
            self.best_position = self.position
        self.best_position_list.append(self.best_position)

    def update_velocity(self, alpha, beta, glob_best_pos):
        # alpha is a list of two values. we will access alpha_1 and alpha_2 by alpha[0] 
        # and alpha[1] respectively. This also applies to beta.
        # the current position, current velocity, and personal best position of 
        # the particle can be accessed by self.position, self.velocity, and self.best_position
        # assign the particle's velocity with the updated velocity
        individual_factor = alpha[0] * beta[0] * (self.best_position - self.position)
        group_factor = alpha[1] * beta[1] * (glob_best_pos - self.position)
        self.velocity += (individual_factor + group_factor)
        self.velocity_list.append(self.velocity)

    def update_position(self, position_limits):
        self.position = self.position + self.velocity
        # how should you solve the problem of the position (x) going out of the limits
        if self.position < position_limits[0]:
            self.position = position_limits[0]
        elif self.position > position_limits[1]:
            self.position = position_limits[1]
        self.position_list.append(self.position)


def fit_fcn(position):
    fitness = (position + 100) * (position + 50) * position * (position - 20) \
        * (position - 60) * (position - 100)
    # fitness = fitness * -1
    return fitness

def initialise_particles(n_ptc, position_limits):
    # position_limits is a list of two values. The first value is the lower 
    # boundary and the second value is the upper boundary.
    particles = [Particle(random.randint(position_limits[0], position_limits[1])) for i in range(n_ptc)]
    return particles

def compareFitness(pos1, pos2):
    # 1. calculate the fitness of pos1 and pos2
    # 2. compare to determine the better position
    betterpos = pos1 if fit_fcn(pos1) < fit_fcn(pos2) else pos2
    return betterpos

def calc_avg_fit_diff(particles):
    # 1. calculate mean fitness of all particles
    fitness_list = [fit_fcn(ptc.position) for ptc in particles]
    mean_fitness = sum(fitness_list)/len(fitness_list)
    # 2. calculate the difference between the mean fitness and the fitness of each particle
    difference = [abs(fit - mean_fitness) for fit in fitness_list]
    # 3. calculate the average of the differences obtained from step 2
    avg_fit_diff = sum(difference)/len(difference)
    return avg_fit_diff 

def calc_avg_pos_diff(particles):
    # 1. calculate mean position of all particles
    position_list = [ptc.position for ptc in particles]
    mean_pos = sum(position_list)/len(position_list)
    # 2. calculate the difference between the mean position and the position of each particle
    difference = [abs(pos - mean_pos) for pos in position_list]
    # 3. calculate the average of the differences obtained from step 2
    avg_pos_diff = sum(difference)/len(difference)
    return avg_pos_diff

if __name__ == '__main__':
    # parameter initialisation
    alpha = [0.1, 0.1]
    n_particle = 10
    global_best_position = None
    position_limits = [-100, 100]
    global_best_position_list = []
    # termination threshold
    iteration = 0
    max_iter = 200
    min_avg_fit_diff = 0.1
    min_avg_pos_diff = 0.1
    # initialise particles
    particles = initialise_particles(n_particle, position_limits)

    space_ax = plt.axes()
    space_ax.plot(list(range(*position_limits)),[fit_fcn(x) for x in range(*position_limits)])
    space_ax.set_title("Position of particles in iteration {}".format(iteration))
    space_ax.set_xlabel("Position")
    space_ax.set_ylabel("Fitness")

    while ((iteration < 200) and (calc_avg_fit_diff(particles) > min_avg_fit_diff) and \
    (calc_avg_pos_diff(particles) > min_avg_pos_diff)): 
    # how should you define the termination criteria here?

        if len(space_ax.lines) > 1:
            del space_ax.lines[1]
        space_ax.plot([x.position for x in particles], [fit_fcn(x.position) for x in particles], 'go')
        space_ax.set_title("Position of particles in iteration {}".format(iteration))
        plt.pause(0.1) # pause the program for 0.5 second; if graph changes too quickly, 
        # increase this value; you can also speed up the process by decreasing this value

        print(iteration, [round(x.position,2) for x in particles])
        for particle in particles:
            # update personal best
            particle.update_personal_best()
            # update global best
            if global_best_position == None:
                global_best_position = particle.position
            else:
                global_best_position = compareFitness(global_best_position, particle.position)
        global_best_position_list.append(global_best_position)
        # generate beta randomly for current iteration
        beta = [random.random(), random.random()]
        for particle in particles:
            # update velocity
            particle.update_velocity(alpha, beta, global_best_position)
            # update position
            particle.update_position(position_limits)
        iteration += 1
    # display results
    print(iteration, [round(x.position,2) for x in particles])

    if len(space_ax.lines) > 1:
        del space_ax.lines[1]
    space_ax.plot([x.position for x in particles], [fit_fcn(x.position) for x in particles], 'go')
    space_ax.set_title("Position of particles in iteration {}".format(iteration))
    plt.pause(0.5) # pause the program for 0.5 second; if graph changes too quickly, 
    # increase this value; you can also speed up the process by decreasing this value

    [pos_fig, position_axes] = plt.subplots(4,1,sharex=True)
    position_axes[0].set_title("Position of each particle")
    position_axes[1].set_title("Fitness of each particle")
    position_axes[2].set_title("Boxplot of position at each iteration")
    position_axes[3].set_title("Boxplot of fitness at each iteration")
    position_axes[3].set_xlabel("Iteration")
    [vel_fig, velocity_axes] = plt.subplots(2,1,sharex=True)
    velocity_axes[0].set_title("Velocity of each particle")
    velocity_axes[1].set_title("Boxplot for velocity at each iteration")
    velocity_axes[1].set_xlabel("Iteration")
    [p_best_fig, personal_best_axes] = plt.subplots(4,1,sharex=True)
    personal_best_axes[0].set_title("Personal best position of each particle")
    personal_best_axes[1].set_title("Personal best fitness of each particle")
    personal_best_axes[2].set_title("Boxplot of personal best position at each iteration")
    personal_best_axes[3].set_title("Boxplot of personal best fitness at each iteration")
    personal_best_axes[3].set_xlabel("Iteration")
    [g_best_fig, global_best_axes] = plt.subplots(2,1,sharex=True)
    global_best_axes[0].set_title("Global best position")
    global_best_axes[1].set_title("Boxplot for global best position")
    global_best_axes[1].set_xlabel("Iteration")
    for particle in particles:
        iteration_list = list(range(len(particle.position_list)))
        position_axes[0].plot(iteration_list, particle.position_list, '-o')
        position_axes[1].plot(iteration_list, [fit_fcn(x) for x in particle.position_list], '-o')

        velocity_axes[0].plot(iteration_list, particle.velocity_list, '-o')

        personal_best_axes[0].plot(iteration_list[:-1], particle.best_position_list, '-o')
        personal_best_axes[1].plot(iteration_list[:-1], [fit_fcn(x) for x in particle.best_position_list], '-o')

    position_axes[2].boxplot([[p.position_list[i] for p in particles] for i in iteration_list], positions=iteration_list)
    position_axes[3].boxplot([[fit_fcn(p.position_list[i]) for p in particles] for i in iteration_list], positions=iteration_list)

    velocity_axes[1].boxplot([[p.velocity_list[i] for p in particles] for i in iteration_list], positions=iteration_list)

    personal_best_axes[2].boxplot([[p.best_position_list[i] for p in particles] for i in iteration_list[:-1]], positions=iteration_list[:-1])
    personal_best_axes[3].boxplot([[fit_fcn(p.best_position_list[i]) for p in particles] for i in iteration_list[:-1]], positions=iteration_list[:-1])

    global_best_axes[0].plot(iteration_list[:-1], global_best_position_list, '-o')
    global_best_axes[1].plot(iteration_list[:-1], [fit_fcn(x) for x in global_best_position_list], '-o')
    # plt.show()