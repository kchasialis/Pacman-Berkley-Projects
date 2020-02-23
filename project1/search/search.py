# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util
import heapq

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:     
    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """

    "*** YOUR CODE HERE ***"
    startPos = problem.getStartState()
    stackOfPositions = util.Stack()
    stackOfPositions.push(startPos)
    stackOfActions = util.Stack()
    stackOfActions.push([])
    visitedNodes = []

    while not stackOfPositions.isEmpty():
        currentPos = stackOfPositions.pop()
        actions = stackOfActions.pop()
        if problem.isGoalState(currentPos):
            return actions
        visitedNodes.append(currentPos)
        successorsOfCurrent = problem.getSuccessors(currentPos)
        for successor in successorsOfCurrent:
            if successor[0] not in visitedNodes:
                stackOfPositions.push(successor[0])
                stackOfActions.push(actions + [successor[1]])

    return []
    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    startPos = problem.getStartState()
    queueOfPositions = util.Queue()
    queueOfPositions.push(startPos)
    queueOfActions = util.Queue()
    queueOfActions.push([])
    visitedNodes = [startPos]

    while not queueOfPositions.isEmpty():
        currentPos = queueOfPositions.pop()
        actions = queueOfActions.pop()
        if problem.isGoalState(currentPos):
            return actions
        successorsOfCurrent = problem.getSuccessors(currentPos)
        for successor in successorsOfCurrent:
            if successor[0] not in visitedNodes:
                visitedNodes.append(successor[0])
                queueOfPositions.push(successor[0])
                queueOfActions.push(actions + [successor[1]])

    return []
    util.raiseNotDefined()

"""Different update from the one provided because I want to check if only the first element of the tuple is the same"""
def myupdate(frontier, item, priority):
    for index, (p, c, i) in enumerate(frontier.heap):
        if i[0] == item[0]:
            if p <= priority:
                break
            del frontier.heap[index]
            frontier.heap.append((priority, c, item))
            heapq.heapify(frontier.heap)
            break
    else:
        frontier.push(item, priority)

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    
    startPos = problem.getStartState()
    frontier = util.PriorityQueue()
    frontier.push((startPos,[]),0)
    visitedNodes = []

    while not frontier.isEmpty():
        currentPos , actions = frontier.pop()
        if problem.isGoalState(currentPos):
            return actions
        visitedNodes.append(currentPos)
        successorsOfCurrent = problem.getSuccessors(currentPos)
        for successor in successorsOfCurrent:
            if successor[0] not in visitedNodes and successor[0] not in [k[2][0] for k in frontier.heap]:
                frontier.push((successor[0] , actions + [successor[1]]),problem.getCostOfActions(actions + [successor[1]]))
            elif successor[0] in [k[2][0] for k in frontier.heap]:
                myupdate(frontier,(successor[0], actions + [successor[1]]),problem.getCostOfActions(actions + [successor[1]]))

    return []
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    startPos = problem.getStartState()
    frontier = util.PriorityQueue()
    frontier.push((startPos,[]),0)
    visitedNodes = []

    while not frontier.isEmpty():
        currentPos , actions = frontier.pop()
        if problem.isGoalState(currentPos):
            return actions
        visitedNodes.append(currentPos)
        successorsOfCurrent = problem.getSuccessors(currentPos)
        for successor in successorsOfCurrent:
            if successor[0] not in visitedNodes and successor[0] not in [k[2][0] for k in frontier.heap]:
                frontier.push((successor[0] , actions + [successor[1]]),problem.getCostOfActions(actions + [successor[1]]) + heuristic(successor[0],problem))
            elif successor[0] in [k[2][0] for k in frontier.heap]:
                myupdate(frontier,(successor[0], actions + [successor[1]]),problem.getCostOfActions(actions + [successor[1]]) + heuristic(successor[0],problem))

    return []
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
