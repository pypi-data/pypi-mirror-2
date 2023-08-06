# Maja Machine Learning Framework
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published
# by the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>.

"""
This module contains an implementation of the maze 2d dynamics which can be 
used in a world of the mmlf.framework.

2008-03-08, Jan Hendrik Metzen (jhm@informatik.uni-bremen.de)
"""

__author__ = "Jan Hendrik Metzen"
__copyright__ = "Copyright 2011, University Bremen, AG Robotics"
__credits__ = ['Mark Edgington']
__license__ = "GPLv3"
__version__ = "1.0"
__maintainer__ = "Jan Hendrik Metzen"
__email__ = "jhm@informatik.uni-bremen.de"

import random

from copy import deepcopy

from mmlf.framework.spaces import StateSpace, ActionSpace
from mmlf.framework.protocol import EnvironmentInfo
from mmlf.environments.single_agent_environment import SingleAgentEnvironment

class MazeCliffEnvironment(SingleAgentEnvironment):
    """ The two-dimensional maze cliff environment.
    
    In this maze, there are two alternative ways from the start to the goal 
    state: one short way which leads along a dangerous cliff and one long 
    but secure way. If the agent happens to step into the maze, it will
    get a huge negative reward (configurable via *cliffPenalty*) and is reset
    into the start state. Per default, the maze is deterministic, i.e. the agent 
    always moves in the direction it chooses. However, the parameter
    *stochasticity* allows to control the stochasticity of the environment.
    For instance, when stochasticity is set to 0.01, the the agent performs a
    random move instead of the chosen one with probability 0.01. 
    
    The maze structure is as follows where "S" is the start state, "G" the goal 
    state and "C" is a cliff field:
    **************
    *            *
    *            *
    *            *
    *SCCCCCCCCCCG*
    **************
    
    **CONFIG DICT**
        :cliffPenalty: : The reward an agent obtains when stepping into the cliff area
        :stochasticity: : The stochasticity of the state transition matrix. With probability *stochasticity* the desired transition is made, otherwise a random transition 
    
    """
    
    DEFAULT_CONFIG_DICT = {"cliffPenalty" : -100,
                           "stochasticity" : 0.0}
    
    def __init__(self, useGUI, *args, **kwargs):
        self.environmentInfo = EnvironmentInfo(versionNumber="0.3",
                                               environmentName="Maze Cliff",
                                               discreteActionSpace=True,
                                               episodic=True,
                                               continuousStateSpace=False,
                                               continuousActionSpace=False,
                                               stochastic=False)

        super(MazeCliffEnvironment, self).__init__(useGUI=useGUI, *args, **kwargs)
        
        # A string which describes the structure of the maze
        # A * indicates a wall, an S the start position of the agent
        # and a G the goal. A blank indicates a free cell.
        mazeDescriptionString =  """**************
                                    *            *
                                    *            *
                                    *            *
                                    *S          G*
                                    **************
                                    """                            
                                    
        #The maze object is created from the description
        self.maze = Maze.createMazeFromString(mazeDescriptionString,
                                              cliffPenalty=self.configDict["cliffPenalty"],
                                              stochasticity=self.configDict["stochasticity"])
        
        #The state space of the Maze2d Simulation
        oldStyleStateSpace =   {
                                "column": ("discrete", range(self.maze.getColumns())),
                                "row": ("discrete", range(self.maze.getRows())),
                            }
        
        self.stateSpace = StateSpace()
        self.stateSpace.addOldStyleSpace(oldStyleStateSpace, limitType="soft")
        
        #The action space of the Single Pole Balancing Simulation
        oldStyleActionSpace =  {
                                "action": ("discrete", ["north", "south", "west", "east"])
                            }
        
        self.actionSpace = ActionSpace()
        self.actionSpace.addOldStyleSpace(oldStyleActionSpace, limitType="soft")
        
        
        # dictionary which contains all configuration options specific to this environment
        # it is VERY important to put ALL configuration options which uniquely determine
        # the behavior of the environment in this dictionary.
        self.configDict =  {}
               
        #The current state of the simulation
        self.initialState =  { 
                     "row": self.maze.getStartPosition()[0],
                     "column": self.maze.getStartPosition()[1],
                  }
        #The current state is initially set to the initial state
        self.currentState = deepcopy(self.initialState)
        
        #A counter which stores the number of steps which have been perfomed in this episode
        self.stepCounter = 0
        self.episodeCounter = 0
        
        #The accumulated reward
        self.reward = 0.0
        
        #Action trace
        self.actionTrace = []
             
    
    ########################## Interface Functions #####################################
    def getInitialState(self):
        """
        Returns the initial state of the simulation
        """
        return self._createStateForAgent(self.initialState)
    
    def getStateSpace(self):
        """
        Returns the state space of this simulation.
        """
        return self.stateSpace
    
    def getActionSpace(self):
        """
        Return the action space of this simulation.
        """
        return self.actionSpace
    
    def evaluateAction(self, actionObject):
        """ Execute an agent's action in the environment.
        
        Take an actionObject containing the action of an agent, and evaluate 
        this action, calculating the next state, and the reward the agent 
        should receive for having taken this action.
        
        Additionally, decide whether the episode should continue,
        or end after the reward has been  issued to the agent.
        
        This method returns a dictionary with the following keys:
           :rewardValue: : An integer or float representing the agent's reward.
                           If rewardValue == None, then no reward is given to the agent.
           :startNewEpisode: : True if the agent's action has caused an episode
                               to get finished.
           :nextState: : A State object which contains the state the environment
                         takes on after executing the action. This might be the
                         initial state of the next episode if a new episode
                         has just started (startNewEpisode == True)
           :terminalState: : A State object which contains the terminal state 
                             of the environment in the last episode if a new 
                             episode has just started (startNewEpisode == True). 
                             Otherwise None.        
        """  
        action = actionObject['action']
        self.actionTrace.append(action)
        
        # Execute the action which was chosen by the agent
        reward = self._stateTransition(action)
        
        self.reward +=reward
           
        #Check if the episode is finished (i.e. the goal is reached)
        episodeFinished = self._checkEpisodeFinished()
        
        terminalState = self.currentState if episodeFinished else None
        
        if episodeFinished:
            self.episodeLengthObservable.addValue(self.episodeCounter,
                                                  self.stepCounter + 1)
            self.returnObservable.addValue(self.episodeCounter, self.reward)
            self.environmentLog.info("Episode %s. Length: %s steps, "
                                     "Accumulated reward: %s."
                                         % (self.episodeCounter, 
                                            self.stepCounter+1, self.reward))
            if len(self.actionTrace) < 20: 
                self.environmentLog.info("Action Trace is %s" % self.actionTrace)
            else:
                actionTrace = ["..."] + self.actionTrace[-20:]
                self.environmentLog.info("Action Trace is %s" % actionTrace)
            #Reset the simulation to the initial state (always the same)
            self.stepCounter = 0
            self.reward = 0.0
            self.actionTrace = []
            self.currentState = deepcopy(self.initialState)
            self.episodeCounter += 1
        else:
            self.stepCounter += 1

        resultsDict = {"reward" : reward,
                       "terminalState" : terminalState,
                       "nextState" : self._createStateForAgent(self.currentState),
                       "startNewEpisode" : episodeFinished}
        return resultsDict
    
    def _stateTransition(self, action):
        "Execute the specified action and store the resulting state"
        # If the action was move forward:
        currentPos = (self.currentState['row'],self.currentState['column'])
        nextPos, reward = self.maze.tryToMove(currentPos,action)
    
        self.currentState['row'] = nextPos[0]
        self.currentState['column'] = nextPos[1]
                
        return reward
        
    def _checkEpisodeFinished(self):
        "Checks whether the episode is finished, i. e. the goal is reached"        
        currentPos = (self.currentState['row'],self.currentState['column'])
        return self.maze.isGoalReached(currentPos)
    
    def _createStateForAgent(self, state):
        "Create a state description for the agent"
        return state
    
class Maze(object):
    """ A class which represents the two-dimensional maze with cliff. """
    def __init__(self, rows, columns, cliffPenalty, stochasticity):
        "Create an empty maze with the specified number of rows and columns"
        self.structure = [[[] for i in range(columns)] for j in range(rows)]
        self.startPos = None
        self.goalPos = None
        self.cliffPenalty = cliffPenalty
        self.stochasticity = stochasticity
    
    @staticmethod
    def createMazeFromString(string, cliffPenalty, stochasticity):
        """
        Factory method which creates a maze based on the string which is passed.
        """
        structure = []
        for row in map(lambda s: s.strip(),string.split('\n')):
            if row == '': continue
            structure.append(list(row))    
            
        maze = Maze(len(structure), len(structure[0]), cliffPenalty, 
                    stochasticity)
        for row_index, row in enumerate(structure):
            for col_index, col in enumerate(row):
                maze.structure[row_index][col_index] = 1 if col == '*' else 0
                if col == 'S':
                    maze.startPos = (row_index,col_index)
                if col == 'G':
                    maze.goalPos = (row_index,col_index)
        return maze

    def tryToMove(self, pos, action):
        """
        The method executes a forward movement starting from the given pos
        in the given direction. If no wall is blocking the movement, the new position
        is returned, otherwise the old position.
        
        In stochastic environments, the chosen action is only executed
        with probability 1 - self.stochasticity. Otherwise, one action is
        chosen randomly
        """
        # In stochastic environments, the chosen action is only executed
        # with probability 1 - self.stochasticity. Otherwise, one action is
        # chosen randomly
        if random.random() < self.stochasticity:
            action = random.choice(["north", "south", "west", "east"])
        
        row = pos[0]
        col = pos[1]
        if action == 'west':
            newPos = (row,col - 1)
        elif action == 'east':
            newPos = (row,col + 1)
        elif action == 'north':
            newPos = (row-1,col)
        elif action == 'south':
            newPos = (row+1,col)
            
        if self.structure[newPos[0]][newPos[1]] == 1:
            return pos, -1
        else:
            if newPos[0] == 4 and newPos[1] in range(2,12):
                return self.startPos, self.cliffPenalty
            else:
                return newPos, -1

    
    def getColumns(self):
        "Returns the number of columns of the maze"
        return len(self.structure[0])
        
    def getRows(self):
        "Returns the number of rows of the maze"
        return len(self.structure)
    
    def getStartPosition(self):
        "Returns the start position of the maze"
        return self.startPos
        
    def isGoalReached(self, pos):
        "Checks if the given position is the goal position"
        return pos == self.goalPos
        
   
EnvironmentClass = MazeCliffEnvironment
EnvironmentName = "Maze Cliff"
