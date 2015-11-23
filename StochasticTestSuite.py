# -*- coding: utf-8 -*-

import unittest
from Helpers.Utilities import basinFunction
from ResultHelpers import TSPResult, BasinResult

# класс с юнит-тестом
class SearchTests(unittest.TestCase):
    
    def setUp(self):
        self.Vector = [1,2]
        # Problem Configuration
        # cписок координат точек
        berlin52 = [[565,575],[25,185],[345,750],[945,685],[845,655],
                    [880,660],[25,230],[525,1000],[580,1175],[650,1130],[1605,620],
                    [1220,580],[1465,200],[1530,5],[845,680],[725,370],[145,665],
                    [415,635],[510,875],[560,365],[300,465],[520,585],[480,415],
                    [835,625],[975,580],[1215,245],[1320,315],[1250,400],[660,180],
                    [410,250],[420,555],[575,665],[1150,1160],[700,580],[685,595],
                    [685,610],[770,610],[795,645],[720,635],[760,650],[475,960],
                    [95,260],[875,920],[700,500],[555,815],[830,485],[1170,65],
                    [830,610],[605,625],[595,360],[1340,725],[1740,245]
                   ]
        self.TSPLIB = berlin52
        
    def tearDown(self):
        self.Vector =[]
    

    #@unittest.skip("Don't run FOR NOW!")          
    def testTabuSearch(self): # тест
    
    	# импортим реализацию алгоритма
        from StochasticAlgorithms.TabuSearch import search
        
        # Problem Configuration
        # Use Berlin52 instance of TSPLIB

        # Algorithm Configuration
        maxIterations = 100 # итераций главного цикла (число лок. оптимумов)
        maxTabuCount = 15
        maxCandidates = 50 # итераций поиска лок. оптимума

        # Execute the algorithm
        result = search(self.TSPLIB,maxIterations, maxTabuCount, maxCandidates)
        
        # 7542 - результат для проверки
        tspResult = TSPResult(7542,"Tabu Search Results")
        
        print tspResult.FormattedOutput(result)
    

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testRandomSeaarch']
    unittest.main()
