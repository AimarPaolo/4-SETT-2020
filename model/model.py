import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo = nx.Graph()
        self._nodi = DAO.getNodi()
        self._grafo.add_nodes_from(self._nodi)
        self._idMap = dict()
        for f in self._grafo.nodes:
            self._idMap[f.id] = f
        self.nodoGradoMax = []
        self.bestPath = []
        self.peso = 0

    def buildGraph(self, rank):
        self._grafo.clear_edges()
        archi = DAO.getPesoArchi(rank)
        for n1, n2, peso in archi:
            if self._grafo.has_edge(self._idMap[n1], self._idMap[n2]) is False:
                self._grafo.add_edge(self._idMap[n1], self._idMap[n2], weight=peso)

    def getGradoMax(self):
        self.nodoGradoMax = []
        for n in self._grafo.nodes:
            peso = 0
            for s in self._grafo.neighbors(n):
                peso += self._grafo[n][s]['weight']
            self.nodoGradoMax.append((n, peso))
        ordinata = sorted(self.nodoGradoMax, key=lambda x: x[1], reverse=True)
        return ordinata[0][0], ordinata[0][1]

    def getBestPath(self, film):
        self.bestPath = []
        self.peso = 0
        parziale = [film]
        self.ricorsione(parziale)
        print(self.bestPath, self.peso)
        return self.bestPath, self.peso

    def getPeso(self, parziale):
        peso = 0
        for p in range(len(parziale)-1):
            peso += self._grafo[parziale[p]][parziale[p+1]]['weight']
        return peso

    def isIncrementale(self, parziale):
        peso = 0
        for p in range(len(parziale)-1):
            if peso < self._grafo[parziale[p]][parziale[p+1]]['weight']:
                peso = self._grafo[parziale[p]][parziale[p+1]]['weight']
            else:
                return False
        return True

    def ricorsione(self, parziale):
        if len(self.bestPath) < len(parziale):
            self.bestPath = copy.deepcopy(parziale)
            self.peso = self.getPeso(parziale)
        for n in self._grafo.neighbors(parziale[-1]):
            parziale.append(n)
            if self.isIncrementale(parziale):
                self.ricorsione(parziale)
            parziale.pop()

    def getCaratteristiche(self):
        return len(self._grafo.nodes), len(self._grafo.edges)
