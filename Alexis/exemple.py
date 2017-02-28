

class Zoo(object):

    def __init__(self, nb_cage):
        self.nb_cage = nb_cage
        self.gardien = "Robert"

    def ajouter_cage(self, nb_de_cage):
        self.nb_cage += nb_de_cage


zoo = Zoo(5)
print(zoo.nb_cage)

zoo.ajouter_cage(6)
print(zoo.nb_cage)