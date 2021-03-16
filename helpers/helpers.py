import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

SAVE_PATH = 'pictures\\{}\\{}.png'
SAVE_DIR = 'pictures\\{}'

def plot_result(solution, plot_title, save_name):
    x_points = list(map(lambda el: el.x, solution.instance._point_dict.values()))
    y_points = list(map(lambda el: el.y, solution.instance._point_dict.values()))

    x_solution = np.array(x_points)[solution.solution]
    y_solution = np.array(y_points)[solution.solution]
    
    fig, ax = plt.subplots()

    ax.scatter(x_points, y_points, color = 'black')
    for i, txt in enumerate(solution.instance._point_dict.keys()):
        ax.annotate(txt, (x_points[i], y_points[i]))

    ax.plot(x_solution, y_solution, color = 'orange')

    plt.title(label = plot_title)
    Path(SAVE_DIR.format(solution.algorithm)).mkdir(parents=True, exist_ok=True)

    plt.savefig(SAVE_PATH.format(solution.algorithm, save_name))
    plt.clf()