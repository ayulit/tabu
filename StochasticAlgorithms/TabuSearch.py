# -*- coding: utf-8 -*-

import sys

from Helpers.Utilities import constructInitialSolution, tourCost, stochasticTwoOptWithEdges, blackBox

# Function that returns a best candidate, sorting by cost
def locateBestCandidate(candidates):
    candidates.sort(key = lambda(c): c["candidate"]["cost"])
    best, edges = candidates[0]["candidate"], candidates[0]["edges"]
    return best, edges 

# есть ли решение в табу-списке        
def isTabu(T, tabuList):
    result = False
    size = len(T) # длина решения

    print "size=", size

    sys.exit("isTabu")

    # цикл по элементам решения
    for index, edge in enumerate(perm): 		
        if index == size-1: # если перебрали все элементы решения
            edge2 = perm[0] # ребро равно первому элементу 
        else:
            edge2 = perm[index+1] # ребро равно текущему элементу решения

        # проверка если данный набор ребер в табу-списке
        if [edge, edge2] in tabuList:
            result = True
            break
        
    return result    

# Move: формирует 1 решение в окрестности начального решения best
def generateCandidates(best, tabuList, G):
    move, edges, result = None, None, {}
    
    # собственно move
    while move == None or isTabu(best["move"], tabuList):
        # move, edges = stochasticTwoOptWithEdges(best["move"])
        move, edges = blackBox(best["move"],G)
        sys.exit("generateCandidates")
        
    candidate ={}    
    candidate["move"] = move
    candidate["cost"] = tourCost(candidate["move"])
    
    result["candidate"] = candidate
    result["edges"] = edges
    
    return result  # возвращает решение

# главная функция алгоритма
# G - граф
def search(G, maxIterations, maxTabu, maxCandidates, k):

	# 1. конструирование начального решения
    best ={}
    best["move"] = constructInitialSolution(G,k) # начальное решение
    best["cost"] = tourCost(best["move"])  # ц.ф.



	# 2. пустой табу-лист
    tabuList =[] 
    
    # 3. главный цикл алгоритма на убывание
    # StopCondition: maxIterations = 0, maxIterations = 100 в начале
    # таким образом имеем 100 итераций - 100 локальных оптимумов
    while maxIterations > 0:
        
        # 4. пустой список кандидатов              
        candidates = []
        
        # Generate candidates using stocahstic 2-opt near current best candidate
        # Use Tabu list to not revisit previous rewired edges
        
        # 5. Ищем кандидатов, используя табуирование (даелаем мувы)
        for index in range(0, maxCandidates):
        	# заполняем список длиной maxCandidates решениями
            candidates.append(generateCandidates(best, tabuList, G))
            sys.exit("search")
            
            
        # Locate the best candidate
        # sort the list of candidates by cost
        # since it is an  involved sort, we write a function for getting the least cost candidate
        bestCandidate, bestCandidateEdges = locateBestCandidate(candidates)
        # compare with current best and update if necessary
        if bestCandidate["cost"] < best["cost"]:
            # set current to the best, so thatwe can continue iteration
            best = bestCandidate
            # update tabu list
            for edge in bestCandidateEdges:
                if len(tabuList) < maxTabu:
                    tabuList.append(edge)
                    
        maxIterations -=1
        
    return best  # алгоритм tabu search возвращает результат
    


