# -*- coding: utf-8 -*-

import math,random
import networkx as nx
import sys
import copy

# Objective function that evaluates the cost
def basinFunction(vector):
    # original basin function from Clever Algorithms book
    #return sum([pow(item,2) for item in vector])
    a,h,k = 0.5,2,-5
    return sum([a * pow((item-h),2) + k for item in vector])

def getRandomWithinBounds(min, max):
    return min + (max - min) * random.random()

# Randomizing function that selects random  inputs for the objective function
def randomSolution(minMax, problemSize):
    inputValues =[]
    while problemSize>0:
        # generates a value between the minimum and maximum values of the search space
        inputValues.append(getRandomWithinBounds(minMax[0], minMax[1]))
        problemSize -=1
        
    return inputValues

# Function to take a step and return the objective function value
def takeStep(bounds, currentInput, stepSize):
    stepInput =[]
    for index in range(0,len(currentInput)):
        lBound = max([bounds[0], currentInput[index] - stepSize ])
        uBound = min([bounds[1], currentInput[index] + stepSize])
        stepInput.append(getRandomWithinBounds(lBound, uBound))
    
    return stepInput

# Function which calculates the euclidean distance between two points
def euclideanDistance(v1, v2):
    # use Zip to iterate over the two vectors
    sum =0.0
    for coord1,coord2 in zip(v1,v2):
        sum += pow((coord1-coord2), 2)
    
    return math.sqrt(sum)

# Целевая функция
def tourCost(T):
    return T.size(weight='weight')

# Function that deletes two edges and reverses the sequence in between the deleted edges
def stochasticTwoOpt(perm):
    result = perm[:] # make a copy
    size = len(result)
    # select indices of two random points in the tour
    p1, p2 = random.randrange(0,size), random.randrange(0,size)
    # do this so as not to overshoot tour boundaries
    exclude = set([p1])
    if p1 == 0:
        exclude.add(size-1)
    else:
        exclude.add(p1-1)
    
    if p1 == size-1:
        exclude.add(0)
    else:
        exclude.add(p1+1) 
                       
    while p2 in exclude:
        p2 = random.randrange(0,size)

    # to ensure we always have p1<p2        
    if p2<p1:
        p1, p2 = p2, p1
     
    # now reverse the tour segment between p1 and p2   
    result[p1:p2] = reversed(result[p1:p2])
    
    return result

# реализация мува для TSP
def stochasticTwoOptWithEdges(perm):
    result = perm[:] # сделаем копию решения
    size = len(result)
    
    # select indices of two random points in the tour
    p1, p2 = random.randrange(0,size), random.randrange(0,size) # 2 числа
    
    # do this so as not to overshoot tour boundaries    
    exclude = set([p1])

    if p1 == 0:
        exclude.add(size-1)
    else:
        exclude.add(p1-1)    
    if p1 == size-1:
        exclude.add(0)
    else:
        exclude.add(p1+1) 
                       
    while p2 in exclude:
        p2 = random.randrange(0,size)

    # to ensure we always have p1<p2        
    if p2<p1:
        p1, p2 = p2, p1
     
    # now reverse the tour segment between p1 and p2   
    result[p1:p2] = reversed(result[p1:p2])
    
    return result, [[perm[p1-1],perm[p1]],[perm[p2-1],perm[p2]]]


#####################################################

def isTree(G):

    if len(G) == 0:
        raise nx.exception.NetworkXPointlessConcept('G has no nodes.')

    print "\nG.edges()=",G.edges()
    print "G.nodes()=",G.nodes()
    print "number_of_edges=",G.number_of_edges()
    print "len(G)=",len(G)
    print "number_of_nodes=",G.number_of_nodes()

    # A connected graph with no cycles has n-1 edges.
    if G.number_of_edges() != len(G) - 1:
        print "isTree-0"
        return False

    if G.is_directed():
        print "isTree-1"
        is_connected = nx.is_weakly_connected
    else:
        print "isTree-2"
        is_connected = nx.is_connected

    return is_connected(G)

# реализация мува для k-Tree
def swapMoves(T, G):

    k = T.number_of_edges()

    bestSwapCandidates=[]
    # цикл по всем ребрам дерева
    for i in xrange(0, k):



        H = T.copy() # сделаем копию решения

        # Нам надо удалить ребро
        e = H.edges(data='weight')[i]

        extNode = -1
        # если одна из вершин ребра внешняя - запомним ее
        if H.degree(e[0]) == 1:
            extNode = e[0]
        elif H.degree(e[1]) == 1:
            extNode = e[1]

        drop = e[:2]
        H.remove_edge(*drop)  # удаляем ребро
        if extNode != -1: # если одна из вершин ребра внешняя
            H.remove_node(extNode) # удаляем ее



        # теперь нужно добавить одно ребро из G
        applicants4addList = []
        for node in H.nodes(): # цикл по нодам оставшегося графа
            nodeNeighbors = G.neighbors(node) # вершины смежные к node

            # ищем ребро с минимальными весом для всех смежных узлов
            applicant4add = getApplicantForAdd(G, nodeNeighbors, node, H, drop)
            if applicant4add == None:
                continue
            applicants4addList.append(applicant4add)

        if not applicants4addList:
            # список кандидатов на добавление пуст
            # т.к. потеряна древестность
            # то ребро нельзя удалять
            continue



        # получаем ребро для добавления в "дерево" из G
        add = min(applicants4addList, key = lambda x:x[2])
        # и добавляем его в дерево
        H.add_edge(add[0],add[1],weight=add[2])

        # хотя уже была такая проверка в getApplicantForAdd()
        # сделаем её еще разок на всякий случай
        if not nx.is_tree(H): # если оставшийся граф - не дерево
            continue # то ребро нельзя удалять



        bestSwapCandidate = (add,drop)
        bestSwapCandidates.append(tuple((bestSwapCandidate,tourCost(H))))

    bestSwapWithCost = min(bestSwapCandidates, key = lambda x:x[1])
    bestSwap = bestSwapWithCost[0]

    H = T.copy() # сделаем копию решения
    drop = bestSwap[1]
    H.remove_edge(*drop)  # удаляем ребро
    add = bestSwap[0]
    H.add_edge(add[0],add[1],weight=add[2]) # и добавляем

    return H, bestSwap

# возвращает смежное ребро с минимальным весом
# neighbors - список соседних вершин
# node - текущая вершина
def neighbourEdgeWithMinWeight(G,neighbors,node):

    minWeight = G[node][neighbors[0]]['weight'] # минимальный вес
    minNeighbourNode = neighbors[0] # первая соседняя вершина

    if len(neighbors) > 1: # если соседних вершин больше одной
        # запускаем процедуру поиска минимума
        for i in xrange(1,len(neighbors)):
            if G[node][neighbors[i]]['weight'] < minWeight:
                minWeight = G[node][neighbors[i]]['weight']
                # соседняя врешина, образующая ребро минимального веса
                minNeighbourNode = neighbors[i]

    if node < minNeighbourNode:
        minNeighbourEdgeW = (node, minNeighbourNode, minWeight)
    else:
        minNeighbourEdgeW = (minNeighbourNode, node, minWeight)

    return minNeighbourEdgeW


# возвращает смежное ребро с минимальным весом
# neighbors - список соседних вершин
# node - текущая вершина
# учитывает, что ребро не дропаное и не принадлежит дереву
def getApplicantForAdd(G, neighbors, node, H, drop):

    minWeight = 9999 # минимальный вес
    minNeighbourNode = -1 # первая соседняя вершина


    # запускаем процедуру поиска минимального ребра
    for i in xrange(0,len(neighbors)):

        a = copy.deepcopy(node)
        b = copy.deepcopy(neighbors[i])
        if b < a:
            a,b = b,a

        e = (a,b) # конструируем ребро
        # Если ребро есть в дереве или дропаное, пропускаем
        if H.has_edge(*e) or (a==drop[0] and b==drop[1]):
            continue

        # Если добавить такое ребро в "дерево" то проверим на древесность
        HH = H.copy() # сделаем копию "дерева"
        w = G[a][b]['weight']
        HH.add_edge(a,b,weight=w)
        if not nx.is_tree(HH):
            continue

        if G[a][b]['weight'] < minWeight:
            minWeight = G[a][b]['weight']
            # соседняя врешина, образующая ребро минимального веса
            minNeighbourNode = neighbors[i]

    if minWeight > 9000:
        return None


    if node < minNeighbourNode:
        minNeighbourEdgeW = (node, minNeighbourNode, minWeight)
    else:
        minNeighbourEdgeW = (minNeighbourNode, node, minWeight)

    return minNeighbourEdgeW


#####################################################


# Конструируем начальное решение
def constructInitialSolution(G,k):

    T = nx.Graph() # начальное дерево

    # 1. ШАГ 0

    candidates = G.edges(data='weight')  # список ребер графа с весами

    # 1.1 Global selection
    selection = min(candidates, key = lambda x:x[2]) # ребро с минимальным весом в графе
    T.add_edge(selection[0],selection[1],weight=selection[2]) # добавялем минимальное ребро в дерево

    nodeA = selection[0] # его вершина A (условимся что A < B)
    nodeB = selection[1] # его вершина B

    neighborsA = G.neighbors(nodeA) # вершины смежные к A
    neighborsB = G.neighbors(nodeB) # вершины смежные к B
    neighborsA.remove(nodeB) # вершины смежные к A исключая B
    neighborsB.remove(nodeA) # вершины смежные к B исключая A

    # ищем ребра с минимальными весам для всех смежных узлов
    minNeighbourEdgeA = neighbourEdgeWithMinWeight(G,neighborsA,nodeA) # for node A
    minNeighbourEdgeB = neighbourEdgeWithMinWeight(G,neighborsB,nodeB) # for node B

    # 1.2 Candidates
    candidates = [] # список кандидатов в дерево
    # добавляем ребра в список кандидатов
    candidates.append(minNeighbourEdgeA)
    candidates.append(minNeighbourEdgeB)

    # 2. ITERATION

    for i in xrange(1,k):

        # 2.1. Selection
        selection = min(candidates, key = lambda x:x[2]) # минимальное ребро из кандидатов
        T.add_edge(selection[0],selection[1],weight=selection[2]) # добавялем минимальное ребро в дерево
        candidates.remove(selection)# удаляем из списка кандидатов

        # 2.2. Choice - идентификация внешнего и внутреннего узлов
        if selection[0] in T:
            internalNode = selection[0]
            externalNode = selection[1]
        else:
            externalNode = selection[0]
            internalNode = selection[1]


        neighborsExt = G.neighbors(externalNode) # вершины смежные к externalNode
        neighborsExt.remove(internalNode) # вершины смежные к externalNode исключая internalNode

        minNeighbourEdgeExt = neighbourEdgeWithMinWeight(G,neighborsExt,externalNode)

        candidates.append(minNeighbourEdgeExt)

    return T

