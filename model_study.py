from src.Parameters import Parameters
from src.Scene import Scene
from src.Wind import Wind

import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt

# TODO : ajouter docstring, autoflake, isort
# TODO : lancer les simulations pour différentes densités, puis prendre les pires cas pour tester le firebreak

CELL_SIZE = 10
SCREEN_SIZE = (600, 600)  # (900,900) (1280,1280)
GRID_DIM = tuple(map(lambda x: int(x / CELL_SIZE), SCREEN_SIZE))
REFRESH_TIME = 10000
COLORS = [(255, 255, 255), (26, 174, 70), (7, 70, 22), (194, 46, 28), (107, 30, 30)]


parameters = Parameters(
    density1=0.4,  # The sum of densities must be included between 0 and 1
    density2=0.1,
    nbInitialFires=3,
    wind=Wind.West,  # South, West, North, East
    firebreak=True,
    resistanceTree1=1,
    resistanceTree2=1.3,
    transmissibilityFire3=0.3,
    transmissibilityFire4=0.5,
)


def one_simulation(parameters: Parameters):
    scene = Scene(
        SCREEN_SIZE, CELL_SIZE, COLORS, GRID_DIM, parameters, random=True, display=False
    )
    scene.initiate_fire()
    done = False
    while not done:
        scene.update()
        done = scene.repartition[3] == 0 and scene.repartition[4] == 0
    return sum(scene.repartition[1:3]) / sum(scene.repartition)


def many_simulation(t: int):
    densities1 = np.linspace(0.0, 0.6, t)
    densities2 = np.linspace(0.0, 0.4, t)

    # Run simulations
    resultats = [
        [
            one_simulation(
                Parameters(
                    density1=densities1[i1],
                    density2=densities2[i2],
                    nbInitialFires=3,
                    wind=Wind.West,
                    firebreak=False,
                    resistanceTree1=1,
                    resistanceTree2=1.3,
                    transmissibilityFire3=0.3,
                    transmissibilityFire4=0.5,
                )
            )
            for i1 in tqdm(range(len(densities1)))
        ]
        for i2 in tqdm(range(len(densities2)))
    ]

    # Display results
    print(resultats)
    plt.figure()
    for i in range(t):
        plt.plot(
            densities1,
            resultats[i],
            label=f"density2 = {densities2[i]}",
        )
    plt.title(f"Final density of trees for different initial values of densities")
    plt.xlabel("density1")
    plt.ylabel("final density of all trees")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    # print(one_simulation(parameters))
    many_simulation(5)