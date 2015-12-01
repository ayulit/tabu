# -*- coding: utf-8 -*-

import sys

import networkx as nx
import numpy as np

import unittest
from Helpers.Utilities import basinFunction
from ResultHelpers import TSPResult, BasinResult

# класс с юнит-тестом
class SearchTests(unittest.TestCase):
    
    def setUp(self):
        self.Vector = [1,2]
        # Problem Configuration
        # матрица смежности
        matrix = np.loadtxt("test0")
        G = nx.from_numpy_matrix(matrix) # Return a graph from numpy matrix.

        # данные
        self.TSPLIB = G

    def tearDown(self):
        self.Vector =[]
    

    #@unittest.skip("Don't run FOR NOW!")          
    def testTabuSearch(self): # тест
    
    	# импортим реализацию алгоритма
        from StochasticAlgorithms.TabuSearch import search
        
        # Problem Configuration
        # Use Berlin52 instance of TSPLIB

        # Algorithm Configuration
        maxIterations = 10 # итераций главного цикла (число лок. оптимумов)
        maxTabuCount = 15
        maxCandidates = 50 # итераций поиска лок. оптимума
        k = 4 # количество ребер в искомом дереве

        # Execute the algorithm
        result = search(self.TSPLIB, maxIterations, maxTabuCount, maxCandidates, k)
        
        # 7542 - результат для проверки
        tspResult = TSPResult(7542, "Tabu Search Results")
        
        print tspResult.FormattedOutput(result)
    

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testRandomSeaarch']
    unittest.main()
