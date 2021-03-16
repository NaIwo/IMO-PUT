import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

SAVE_PATH = 'pictures\\{}\\{}.png'
SAVE_DIR = 'pictures\\{}'

def plot_result(solution, plot_title, save_name):
    x_points = list(map(lambda el: el.x, solution.instance._point_dict.values()))
    y_points = list(map(lambda el: el.y, solution.instance._point_dict.values()))

    x_first_solution = np.array(x_points)[solution.first_solution]
    y_first_solution = np.array(y_points)[solution.first_solution]

    x_second_solution = np.array(x_points)[solution.second_solution]
    y_second_solution = np.array(y_points)[solution.second_solution]
    
    fig, ax = plt.subplots()

    ax.scatter(x_points, y_points, color = 'black')
    for i, txt in enumerate(solution.instance._point_dict.keys()):
        ax.annotate(txt, (x_points[i], y_points[i]))

    ax.plot(x_first_solution, y_first_solution, color = 'green')
    ax.plot(x_second_solution, y_second_solution, color = 'red')

    plt.title(label = plot_title)
    Path(SAVE_DIR.format(solution.algorithm)).mkdir(parents=True, exist_ok=True)

    plt.savefig(SAVE_PATH.format(solution.algorithm, save_name))
    plt.clf()