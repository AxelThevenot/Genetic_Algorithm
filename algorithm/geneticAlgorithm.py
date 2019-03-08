import matplotlib.pyplot as plt
import matplotlib.animation as animation
from population import *


# region variables
SIZE_PLOT = 10
DISPLAY_GENERATION = 5  # Display the best individuals each DISPLAY_GENERATION
N_POINT = 30  # Number of point to link
SIZE_POPULATION = 150  # Size of each population
MAX_GENERATION = 500  # Stop running at MAX_GENERATION
# each new generation is composed by :
# --> RATIO_SELECTION of the best individuals in the previous generation
# --> RATIO_CROSSOVER of children of the best individuals children
# --> The rest is new random individuals to minimize the chance to be in a local minimum
RATIO_SELECTION = 0.3
RATIO_CROSSOVER = 0.65
# each new generation is subject to a RATIO_MUTATION
RATIO_MUTATION = 0.7

# Initialize the first randomized population
population = randomPopulation(SIZE_POPULATION, SIZE_PLOT, N_POINT)
generation_count = 0
# costs array to keep the best cost value of each generation
costs = []

# Initialize the two plot
figGen = plt.figure(1)  # display the best cost according to the generation number
fig = plt.figure(0)  # display the best cost for actual generation

ax = fig.add_subplot(1,1,1)  # plot for the post visualization
axGen = figGen.add_subplot(1,1,1)  # plot for the costs evolution

ani = None  # to animate (update) the two plots
started = False
# endregion


# region plot
def display():
    """
    Udpdates the two plots
    """
    # First, clear the plots
    ax.clear()
    axGen.clear()

    # actualize plot title and axes labels
    ax.set_title("Generation : {0}".format(generation_count))
    axGen.set_xlabel("Generation")
    axGen.set_ylabel("best cost")
    # Ask for the best cost in two vectors (X coord and Y coord)
    X, Y = population.best.toXY()

    # place the N_POINT point (except starting-ending point coord(0, 0))
    plt.scatter(X[1:-1], Y[1:-1], c='#474747')
    # then place the starting-ending point
    plt.scatter(0, 0, c='#8800FF')

    if started:
        # show how the N_POINT are linked in the best cost case found
        ax.plot(X, Y, c='#2F9599', )
        # actualize the plot of costs
        axGen.plot([i for i in range(len(costs))], costs, c='#2F9599')
    axGen.set_xlim([0, MAX_GENERATION])  # to keep the same abscissa
    # the show the plots
    fig.canvas.draw()
    figGen.canvas.draw()

def key_pressed(event):
    """
    To start/pause running the programme
    :param event: key_press_event
    """
    if event.key == 'enter':
        global started
        started = not started
# endregion


# region Generation
def nextGeneration(frame_number):
    """
    Update for new generation of the population
    :param frame_number:
    """
    if started:
        global generation_count
        while generation_count < MAX_GENERATION:
            population.nextGeneration(RATIO_SELECTION, RATIO_CROSSOVER, RATIO_MUTATION)
            generation_count += 1
            costs.append(population.best.cost)  # actualize the best costs array
            # then display the new update
            if generation_count % DISPLAY_GENERATION == 0:
                display()
        figGen.canvas.draw()
# endregion


if __name__ == "__main__":
    # to animate the plot and launch the population update
    ani = animation.FuncAnimation(fig, nextGeneration)
    # connect to the key press event to start/pause the programme
    fig.canvas.mpl_connect('key_press_event', key_pressed)
    display()
    plt.show()

