import random

from .Wind import Wind


class Parameters:
    def __init__(
        self,
        density1,
        density2,
        nbInitialFires,
        wind,
        firebreak,
        resistanceTree1,
        resistanceTree2,
        transmissibilityFire3,
        transmissibilityFire4,
    ):
        self.density1 = density1
        self.density2 = density2
        self.nb_initial_fires = nbInitialFires
        self.wind = wind
        self.firebreak = firebreak
        self.resistance_tree1 = resistanceTree1
        self.resistance_tree2 = resistanceTree2
        self.transmissibility_fire3 = transmissibilityFire3
        self.transmissibility_fire4 = transmissibilityFire4

    def randomize(self):
        rnd = random.Random()
        self.wind = Wind(rnd.randint(0, 3))
        self.nb_initial_fires = rnd.randint(1, 10)
        self.density1 = rnd.uniform(0.3, 0.8)
        self.density2 = rnd.uniform(0, 0.2)
        self.firebreak = rnd.choice([True, False])
