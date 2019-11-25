from inspect import signature
import numpy as np

def ordonnerTriplet(triplet) -> tuple:
    """Permet d'ordonner un triplet (x1, x2, w) avec x1 < x2.
    Renvoi le triplet ordonné en tant que tuple.
    Cette méthode est utile au delà de la définition de self.edges

    args:
        triplet: un tuple
    """
    if len(triplet) == 2:
        triplet = [triplet[0], triplet[1], 1]

    else:
        triplet = list(triplet)

    if(triplet[0] > triplet[1]):
        temp = triplet[0]
        triplet[0] = triplet[1]
        triplet[1] = temp

    return tuple(triplet)

ordonnerTripletSignature = signature(ordonnerTriplet)

def defineVertices(edges) -> list:
    """Permet de définir l'ensemble des sommets du graphe sur la base d'un
    ensemble d'arrêtes.
    Renvoie une liste d'int.
    """
    #pour compter le nombre de sommets
    sommets = {}
    for edge in edges:
        if(edge[0] in sommets):
            sommets[edge[0]] += 1
        else:
            sommets[edge[0]] = 1

        if(edge[1] in sommets):
            sommets[edge[1]] += 1
        else:
            sommets[edge[1]] = 1

    return [node for node in sommets]

defineVerticesSignature = signature(defineVertices)



class Reseau():

    def reset(self):
        """initialise ou réinitialise toutes les variables internes de la
        classe"""

        self.edges = []
        self.Vertices = []
        self.NbEdges = 0
        self.nbVertices = 0
        self.weight = 0
        self.dmin = 0
        self.dmax = 0
    #-----------------------------------------------------
    def check(self):
        """print l'ensemble des attributs de l'instance Reseau. Ne renvoie rien
        """
        print(f"self.Vertices = {self.Vertices}")
        print(f"self.edges = {self.edges}")
        print(f"self.NbEdges = {self.NbEdges}")
        print(f"self.nbVertices = {self.nbVertices}")
        print(f"self.weight = {self.weight}")
        print(f"self.dmin = {self.dmin}")
        print(f"self.dmax = {self.dmax}")

    #-----------------------------------------------------
    def updateDegre(self) -> None:
        """permet de mettre à jour les degrés maximums et minimums du graphe"""

        listeDegres = [self.degre(sommet) for sommet in self.Vertices]
        self.dmin = np.min(listeDegres)
        self.dmax = np.max(listeDegres)

    #-----------------------------------------------------
    def __init__(self,triplets=[]):

        self.reset()

        #on jette les triplets mal construits et on modifient ceux avec mauvais w
        for triplet in triplets:
            if (len(triplet) != 3):
                triplets.remove(triplet)
            elif (-10 > triplet[2] or triplet[2] > 10):
                weight = 1

        #pour compter le nombre de sommets
        sommets = {}
        for triplet in triplets:
            if(triplet[0] in sommets):
                sommets[triplet[0]] += 1
            else:
                sommets[triplet[0]] = 1

            if(triplet[1] in sommets):
                sommets[triplet[1]] += 1
            else:
                sommets[triplet[1]] = 1
        self.nbVertices = len(self.Vertices)

        self.nbEdges = len(triplets)

        sommeArretes = 0
        for triplet in triplets:
            sommeArretes += triplet[2]
        self.weight = sommeArretes

        #on détermine le degré max et min
        degreMin = 0
        degreMax = 0
        for singleSommet in sommets:
            if(degreMin > singleSommet):
                degreMin = singleSommet
            if(degreMax < singleSommet):
                degreMax = singleSommet
        self.dmin = degreMin
        self.dmax = degreMax

        #création de l'attribut edges avec les sommets x1 < x2
        self.edges = []
        for triplet in triplets:
            self.edges.append(ordonnerTriplet(triplet))

        #création attribut qui liste l'ensemble des sommets
        self.Vertices = [node for node in sommets]
    #-----------------------------------------------------
    def add_node(self, node):
        """renvoie True et ajoute le sommet passé en argument s'il n'est pas
        présent dans la liste self.Vertices, renvoie False sinon
        """
        if(type(node) != int):
            return False

        elif (not node in self.Vertices):
            self.Vertices.append(node)
            self.nbVertices += 1
            self.Vertices.sort()
            return True

        else:
            return False
    #-----------------------------------------------------
    def add_edge(self , node1, node2 , weight=1):
        """ajoute l'arrête à la liste des arrêtes déjà existante. Si les sommets
        n'existent pas, les ajoute à la liste des sommets self.Vertices
        """
        if weight > 10 or weight < -10:
            weight = 1

        condition = ordonnerTriplet((node1, node2, weight)) not in self.edges

        if node1 not in self.Vertices and condition:
            self.Vertices.append(node1)
            self.nbVertices += 1
        if node2 not in self.Vertices and condition:
            self.Vertices.append(node2)
            self.nbVertices += 1



        tripletToAdd = ordonnerTriplet((node1, node2, weight))

        for triplet in self.edges:
            if triplet == tripletToAdd:
                return False

        self.edges.append(tripletToAdd)
        self.nbEdges += 1
        self.weight += tripletToAdd[2]
        self.updateDegre()
        return True

    #-----------------------------------------------------
    def del_nodes(self):
        """supprime toutes les arrêtes et sommets du graphe"""

        self.edges.clear()
        self.Vertices.clear()
        self.NbEdges = 0
        self.nbVertices = 0
        self.weight = 0
        self.dmin = 0
        self.dmax = 0

    #-----------------------------------------------------
    def del_node(self, node):
        """supprime un sommet et toutes les arrêtes qui lui sont associées"""

        if node in self.Vertices:
            self.Vertices.remove(node)
            self.nbVertices -= 1

            for triplet in self.edges:
                if node in triplet:
                    self.edges.remove(triplet)
                    self.nbEdges -= 1
                    self.weight -= triplet[2]
                    self.updateDegre()
            return True

        else:
            return False

    #-----------------------------------------------------
    def del_edges(self):
        """efface toutes les arrêtes du graphe"""
        self.edges.clear()
        self.nbEdges = 0
        self.weight = 0
        self.updateDegre()

    #-----------------------------------------------------
    def del_edge(self, node1, node2, weight=1):
        """supprime l'arrête correspondante donnée en entrée"""

        if ordonnerTriplet((node1, node2, weight)) in self.edges:
            self.edges.remove(ordonnerTriplet((node1, node2, weight)))
            self.weight -= weight
            self.updateDegre()
            self.nbEdges -= 1
            return True

        else:
            return False

    #-----------------------------------------------------
    def erase_edge(self, node1, node2):
        """efface toutes les arrêtes entre les deux sommets donnés en arguments
        """
        deleted = False

        if node1 < node2:
            nodeMin = node1
            nodeMax = node2
        else:
            nodeMin = node2
            nodeMax = node1

        for triplet in self.edges:
            if triplet[0] == nodeMin and triplet[1] == nodeMax:
                self.edges.remove(triplet)
                self.nbEdges -= 1
                self.weight -= triplet[2]
                deleted = True

        return deleted

    #-----------------------------------------------------
    def adj(self, node):
        """renvoie les sommets adjacent au sommet donné en argument"""
        adjList = []
        for triplet in self.edges:
            if node in triplet:
                indexNode = triplet.index(node)
                indexOtherNode = 1 - indexNode

                if (triplet[indexOtherNode] not in adjlist and triplet[indexOtherNode]!=triplet[indexNode]):
                    adjlist.append(triplet[indexOtherNode])
        adjlist.sort()
        return adjlist

    #-----------------------------------------------------
    def degre(self, node):
        """ retourn -1 si le sommet n'appartient pas au graphe, i.e il n'a aucune
        arrête associée, retourne son degré sinon"""

        if node in self.Vertices:
            check = 0
            for triplet in self.edges:
                if node in triplet:
                    check += 1

            if check == 0:
                return  -1
            else:
                return check

    #-----------------------------------------------------
    def composante(self, node):
        """renvoie la liste triée des sommets faisant partie de la même
        composante connexe, i.e reliés entre eux"""

        connectedNodes = [node]

        #à chaque fois qu'on rajoute un sommet dans le liste de connection
        #on scan à nouveau pour voir si on n'a pas encore des sommets à rajouter
        toAdd = True
        while toAdd:
            toAdd = False
            for sommet in connectedNodes:
                for triplet in self.edges:
                    if sommet in triplet:
                        indexSommet = triplet.index(sommet)
                        indexOtherSommet = 1 - indexSommet
                        sommetToAdd = triplet[indexOtherSommet]

                        if sommetToAdd not in connectedNodes:
                            connectedNodes.append(sommetToAdd)
                            toAdd = True

        connectedNodes.sort()
        return connectedNodes

    #-----------------------------------------------------
    def estSimple(self):
        """verifie si le graphe ne comporte ni arrête multiple ni boucle"""

        checkBoucle = True
        checkMultiple = True
        for triplet in self.edges:
            if triplet[0] == triplet[1]:
                checkBoucle = False

            for checkTripletMultiple in self.edges:
                if (
                    triplet[0]==checkTripletMultiple[0] and
                    triplet[1]==checkTripletMultiple[1] and
                    triplet != checkTripletMultiple
                    ):
                    checkMultiple = False

        if checkBoucle and checkMultiple:
            return True
        else:
            return False

    #-----------------------------------------------------
    def estConnexe(self):
        """renvoie True si il n'y a qu'une composante connexe"""
        connexeList = []
        for node in self.Vertices:
            comp = self.composante(node)
            if comp not in connexeList:
                connexeList.append(comp)

        if len(connexeList) == 1:
            return True
        else:
            return False
    #-----------------------------------------------------
    def estComplet(self):
        """renvoie True si le graphe est complet"""
        countCheck = 0

        #on vérifie que chaque sommet est relié 2à2 à tous les autres sommets
        for node in self.Vertices:
            checkConnection = [node]
            for triplet in self.edges:
                if node in triplet:

                    indexNode = triplet.index(node)
                    indexOtherNode = 1 - indexNode
                    nodeToAdd = triplet[indexOtherNode]

                    if nodeToAdd not in checkConnection:
                        checkConnection.append(nodeToAdd)

            checkConnection.sort()
            if checkConnection == self.Vertices:
                countCheck += 1

        if countCheck == self.nbVertices:
            return True
        else:
            return False

    #-----------------------------------------------------
    def estEulerien(self):
        """renvoie True si le graphe est Eulérien, i.e chaque sommet est relié
        à un nombre paire d'arrêtes distinctes"""

        checkNode = 0
        for node in self.Vertices:
            listeSommets = [node]
            checkEdges = 0

            for triplet in self.edges:
                if node in triplet:
                    indexNode = triplet.index(node)
                    indexOtherNode = 1 - indexNode
                    otherNode = triplet[indexOtherNode]

                    if otherNode not in listeSommets:
                        listeSommets.append(otherNode)
                        checkEdges += 1

            if checkEdges % 2 == 0:
                checkNode += 1

        if checkNode == len(self.Vertices):
            return True

        else:
            return False

    #-----------------------------------------------------
    def estArbre(self):
        """renvoie True si le graphe est un arbre, i.e si le nombre de sommet est
        supérieur au nombre d'arrêtes d'au moins un"""

        uniqueEdge = []
        for triplet in self.edges:
            duoSommets = [triplet[i] for i in [0,1]]
            if duoSommets not in uniqueEdge and duoSommets[0] != duoSommets[1]:
                uniqueEdge.append(duoSommets)

        if len(uniqueEdge) < self.nbVertices:
            return True
        else:
            return False
    #-----------------------------------------------------
    def cconnexe(self):
        """renvoie un dictionnaire contenant comme clé les numéros de sommets,
        et en valeur le numéro de sommet le plus petit appartenant à la même
        entité connexe"""

        dic = {}

        for sommet in self.Vertices:
            listeSommetsConnexes = self.composante(sommet)
            if len(listeSommetsConnexes) != 0:
                dic[sommet] = np.min(listeSommetsConnexes)


        return dic

    #-----------------------------------------------------
    def minimisation(self):
        """renvoie un sous-graphe simple et avec des weight minimales"""

        #on enlève les boucles
        for triplet in self.edges:
            if triplet[0] == triplet[1]:
                self.edges.remove(triplet)

        #on enlève les arrêtes multiples de poids maximal
        edgesCopy = []
        for triplet in self.edges:
            tripletsConcurrents = [triplet]
            duo1 = [triplet[0], triplet[1]]
            for test in self.edges:
                duo2 = [test[0], test[1]]

                if duo1 == duo2 and triplet[2] != test[2]:
                    tripletsConcurrents.append(test)

            differentWeights = [edge[2] for edge in tripletsConcurrents]
            minWeight = np.min(differentWeights)
            tripletToAdd = tripletsConcurrents[differentWeights.index(minWeight)]

            if tripletToAdd not in edgesCopy:
                edgesCopy.append(tripletToAdd)

        return edgesCopy
    #-----------------------------------------------------
    def maximisation(self):
        """renvoie un sous-graphe simple et avec des weight maximales"""

        #on enlève les boucles
        for triplet in self.edges:
            if triplet[0] == triplet[1]:
                self.edges.remove(triplet)

        #on enlève les arrêtes multiples de poids maximal
        edgesCopy = []
        for triplet in self.edges:
            tripletsConcurrents = [triplet]
            duo1 = [triplet[0], triplet[1]]
            for test in self.edges:
                duo2 = [test[0], test[1]]

                if duo1 == duo2 and triplet[2] != test[2]:
                    tripletsConcurrents.append(test)

            differentWeights = [edge[2] for edge in tripletsConcurrents]
            maxWeight = np.max(differentWeights)
            tripletToAdd = tripletsConcurrents[differentWeights.index(maxWeight)]

            if tripletToAdd not in edgesCopy:
                edgesCopy.append(tripletToAdd)

        return edgesCopy
    #-----------------------------------------------------
    def write_to(self):
        """écrit le réseau dans un fichier texte"""

        file = open("reseau_Jodie.txt", "w+")
        file.write(f"{self.nbVertices},{self.nbEdges},{self.dmin},{self.dmax}\n")

        for edge in self.edges:
            toWrite = [val for val in edge]
            if toWrite[2] == 1:
                toWrite = toWrite[0:2]

            if len(toWrite) == 2:
                file.write(f"{toWrite[0]},{toWrite[1]}\n")
            elif len(toWrite) == 3:
                file.write(f"{toWrite[0]},{toWrite[1]},{toWrite[2]}\n")

        file.close()
    #-----------------------------------------------------
    def read_from(self):
        """permet d'importer un réseau déjà encodé dans un fichier texte.
        Si les données ne sont pas cohérentes entre elles, renvoie un réseau
        vide"""

        with open("reseau_Jodie.txt", "r") as file:

            listeEdges = []
            lineIndicator = 0

            for line in file:
                #on extrait la première ligne
                if lineIndicator == 0:
                    firstLine = line.split(sep=",")
                    self.nbVertices = firstLine[0]
                    self.nbEdges = firstLine[1]

                    tempDmin = firstLine[2]
                    tempDmax = firstLine[3]

                else:
                    #extraction des arrêtes du fichier
                    splitedLine = line.split(sep=",")
                    triplet = [int(val) for val in splitedLine]
                    goodTriplet = ordonnerTriplet(triplet)

                    if goodTriplet not in listeEdges:
                        listeEdges.append(goodTriplet)

                lineIndicator += 1


            self.edges = listeEdges
            self.nbEdges = len(self.edges)
            self.Vertices = defineVertices(self.edges)
            self.updateDegre()

            #pour compter le nombre de sommets
            sommets = {}
            for edge in listeEdges:
                if(edge[0] in sommets):
                    sommets[edge[0]] += 1
                else:
                    sommets[edge[0]] = 1

                if(edge[1] in sommets):
                    sommets[edge[1]] += 1
                else:
                    sommets[edge[1]] = 1

            #tableau stockant les conditions à tester pour la cohérence des données
            tab = [0,0,0,0]
            tab[0] = self.nbEdges == len(listeEdges)
            tab[1] = int(self.nbVertices) == int(len(sommets))
            tab[2] = int(tempDmax) == int(self.dmax)
            tab[3] = int(tempDmin) == int(self.dmin)

            #np.all renvoie True si tous les éléments sont True
            if not np.all(tab):
                self.reset()

            else:
                for triplet in self.edges:
                    self.weight += triplet[2]

    #-----------------------------------------------------
if __name__ =='__main__':
    g=Reseau([(2,5,2), (4,3,1), (8,8,8)])
    g.add_edge(1, 2, 3)
    g.add_edge(3, 2 ,1)
    g.add_edge(4, 2, 1)
    g.add_edge(2, 1, 3)
    g.nbVertices
