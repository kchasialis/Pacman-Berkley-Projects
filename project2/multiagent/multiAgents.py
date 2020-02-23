# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        ghostPositions = successorGameState.getGhostPositions()

        for position in ghostPositions:
            if newPos == position:
                return -999999
        if action == 'Stop':
            return -999999
        
        min_dist = 999
        for food in newFood.asList():
            dist = manhattanDistance(food,newPos)
            if (dist < min_dist):
                min_dist = dist

        food_dist = 0
        if min_dist != 999:
            food_dist = 1.0 / min_dist

        return food_dist + successorGameState.getScore()

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """
    def MINIMAX(self,gameState,agentIndex,depth):
        if agentIndex >= gameState.getNumAgents():
            agentIndex = 0
            depth += 1
        #check if terminal state
        if (depth == self.depth or gameState.isWin() or gameState.isLose()):
            return self.evaluationFunction(gameState)
        if agentIndex == 0:
            return self.MAX_VALUE(gameState,agentIndex,depth)
        else:
            return self.MIN_VALUE(gameState,agentIndex,depth)

    def MIN_VALUE(self,gameState,agentIndex,depth):
        actions = gameState.getLegalActions(agentIndex)
        val = float("inf")
        for action in actions:
            val = min(val,self.MINIMAX(gameState.generateSuccessor(agentIndex,action),agentIndex + 1,depth))
        return val

    def MAX_VALUE(self,gameState,agentIndex,depth):
        pacman_actions = gameState.getLegalActions(agentIndex)
        val = float("-inf")
        for action in pacman_actions:
            val = max(val,self.MINIMAX(gameState.generateSuccessor(agentIndex,action),agentIndex + 1,depth))
        return val

    def getAction(self, gameState):
        depth = 0
        agentIndex = 0
        max_action = ""
        max_val = float("-inf")
        actions = gameState.getLegalActions(agentIndex)
        for action in actions:
            val = self.MINIMAX(gameState.generateSuccessor(agentIndex,action),agentIndex + 1,depth)
            if val > max_val:
              max_val = val
              max_action = action
        return max_action
      #util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def ALPHA_BETA(self,gameState,agentIndex,alpha,beta,depth):
        if agentIndex >= gameState.getNumAgents():
            agentIndex = 0
            depth += 1
        #check if terminal state
        if (depth == self.depth or gameState.isWin() or gameState.isLose()):
            return self.evaluationFunction(gameState)
        if agentIndex == 0:
            return self.MAX_VALUE(gameState,agentIndex,alpha,beta,depth)
        else:
            return self.MIN_VALUE(gameState,agentIndex,alpha,beta,depth)

    def MIN_VALUE(self,gameState,agentIndex,alpha,beta,depth):
        actions = gameState.getLegalActions(agentIndex)
        val = float("inf")
        for action in actions:
            val = min(val,self.ALPHA_BETA(gameState.generateSuccessor(agentIndex,action),agentIndex + 1,alpha,beta,depth))
            if val < alpha:
              return val
            beta = min(beta,val)
        return val

    def MAX_VALUE(self,gameState,agentIndex,alpha,beta,depth):
        pacman_actions = gameState.getLegalActions(agentIndex)
        val = float("-inf")
        for action in pacman_actions:
            val = max(val,self.ALPHA_BETA(gameState.generateSuccessor(agentIndex,action),agentIndex + 1,alpha,beta,depth))
            if val > beta:
              return val
            alpha = max(alpha,val)
        return val

    def getAction(self, gameState):
        depth = 0
        agentIndex = 0
        max_action = ""
        alpha = float("-inf")
        beta = float("inf")
        actions = gameState.getLegalActions(agentIndex)
        for action in actions:
            val = self.ALPHA_BETA(gameState.generateSuccessor(agentIndex,action),agentIndex + 1,alpha,beta,0)
            if val > alpha:
              alpha = val
              max_action = action
        return max_action
        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def EXPECTIMAX(self,gameState,agentIndex,depth):
        if agentIndex >= gameState.getNumAgents():
            agentIndex = 0
            depth += 1
        #check if terminal state
        if (depth == self.depth or gameState.isWin() or gameState.isLose()):
            return self.evaluationFunction(gameState)
        if agentIndex == 0:
            return self.MAX_VALUE(gameState,agentIndex,depth)
        else:
            return self.EXP_VALUE(gameState,agentIndex,depth)

    def EXP_VALUE(self,gameState,agentIndex,depth):
        actions = gameState.getLegalActions(agentIndex)
        val = 0
        probability = 1.0 / len(actions)
        for action in actions:
            val += self.EXPECTIMAX(gameState.generateSuccessor(agentIndex,action),agentIndex + 1,depth) * probability
        return val

    def MAX_VALUE(self,gameState,agentIndex,depth):
        pacman_actions = gameState.getLegalActions(agentIndex)
        val = float("-inf")
        for action in pacman_actions:
            val = max(val,self.EXPECTIMAX(gameState.generateSuccessor(agentIndex,action),agentIndex + 1,depth))
        return val

    def getAction(self, gameState):
        depth = 0
        agentIndex = 0
        max_action = ""
        max_val = float("-inf")
        actions = gameState.getLegalActions(agentIndex)
        for action in actions:
            val = self.EXPECTIMAX(gameState.generateSuccessor(agentIndex,action),agentIndex + 1,depth)
            if val > max_val:
              max_val = val
              max_action = action
        return max_action

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <This function gives more value to the distance of the food and the score that this gameState gives
      and less value to the number of foods and capsules>
    """ 
    currentPos = currentGameState.getPacmanPosition()
    currentFood = currentGameState.getFood()
    ghostPositions = currentGameState.getGhostPositions()

    min_dist = 999
    for food in currentFood.asList():
        dist = manhattanDistance(food,currentPos)
        if (dist < min_dist):
            min_dist = dist

    food_dist = 0
    if min_dist != 999:
        food_dist = 1.0 / min_dist

    #If ghosts are nearby avoid this action
    nearby = False
    for position in ghostPositions:
        dist = manhattanDistance(currentPos,position)
        if dist < 2:
            nearby = True

    if nearby == True:
        return -100000000
    else:
        return food_dist + 100*currentGameState.getScore() - 10*currentGameState.getNumFood() - 5*len(currentGameState.getCapsules())
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

