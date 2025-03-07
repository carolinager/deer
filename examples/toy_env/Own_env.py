"""
The environment simulates the possibility of buying or selling a good. The agent can either have one unit or zero unit of that good. At each transaction with the market, the agent obtains a reward equivalent to the price of the good when selling it and the opposite when buying. In addition, a penalty of 0.5 (negative reward) is added for each transaction.
Two actions are possible for the agent:
- Action 0 corresponds to selling if the agent possesses one unit or idle if the agent possesses zero unit.
- Action 1 corresponds to buying if the agent possesses zero unit or idle if the agent already possesses one unit.
The state of the agent is made up of an history of two punctual observations:
- The price signal
- Either the agent possesses the good or not (1 or 0)
The price signal is build following the same rules for the training and the validation environment. That allows the agent to learn a strategy that exploits this successfully.

"""

import numpy as np
from mpl_toolkits.axes_grid1 import host_subplot
import mpl_toolkits.axisartist as AA
import matplotlib.pyplot as plt

from deer.base_classes import Environment

class MyEnv(Environment):

    def __init__(self, rng):
        """ Initialize environment.

        Parameters
        -----------
        rng : the numpy random number generator
        """
        # Defining the type of environment
        self._last_ponctual_observation = [-1] # last state

        # self._random_state = rng
        #
        # # Building a price signal with some patterns
        # self._price_signal=[]
        # for i in range (1000):
        #     price = np.array([0.,0.,0.,-1.,0.,1.,0., 0., 0.])
        #     price += self._random_state.uniform(0, 3)
        #     self._price_signal.extend(price.tolist())
        #
        # self._price_signal_train = self._price_signal[:len(self._price_signal)//2]
        # self._price_signal_valid = self._price_signal[len(self._price_signal)//2:]
        # self._prices = None
        # self._counter = 1

        self._statelist = []
        self._actionlist = []

    def reset(self, mode):
        """ Resets the environment for a new episode.

        Parameters
        -----------
        mode : int
            -1 is for the training phase, others are for validation/test.

        Returns
        -------
        list
            Initialization of the sequence of observations used for the pseudo-state; dimension must match self.inputDimensions().
            If only the current observation is used as a (pseudo-)state, then this list is equal to self._last_ponctual_observation.
        """
        # if mode == -1:
        #     self.prices = self._price_signal_train
        # else:
        #     self.prices = self._price_signal_valid


        self._last_ponctual_observation = [-1]
        self._statelist = []

        # self._counter = 1
        return [-1] # changed since inputDim = [(1,)] now

    def act(self, action):
        """ Performs one time-step within the environment and updates the current observation self._last_ponctual_observation

        Parameters
        -----------
        action : int
            Integer in [0, ..., N_A] where N_A is the number of actions given by self.nActions()

        Returns
        -------
        reward: float
        """
        reward = 0

        #old:
        # if (action == 0 and self._last_ponctual_observation[1] == 1):
        #     reward = self.prices[self._counter-1] - 0.5
        # if (action == 1 and self._last_ponctual_observation[1] == 0):
        #     reward = -self.prices[self._counter-1] - 0.5
        #
        # self._last_ponctual_observation[0] = self.prices[self._counter]
        # self._last_ponctual_observation[1] = action
        #
        # self._counter += 1

        #own:
        # action 0 = a - action 1 = b
        # obs = (price, action) and price == state?? - no, I determine it...?
        # how to encode states & where????
        # states : [-1, 1] where -1=1, -0.5=2, 0=3, 0.5=4, 5=1

        if (self._last_ponctual_observation[0] == -1 and action == 1):
            reward = 0.2
            new_state = -1
        else if (self._last_ponctual_observation[0] == 1 action == 0):
            reward = 1
            new_state = 1
        else if (action == 0): # from states 1,2,3,4 with action a to next state
            new_state = self._last_ponctual_observation[0] + 0.5
        else if (action == 1): #from states 5,4,3,2 with action b to state 1
            new_state = self._last_ponctual_observation[0] - 0.5

        self._last_ponctual_observation[0] = new_state
        #self._last_ponctual_observation[1] = action

        self._statelist.append(new_state)
        self._actionlist.append(action)

        return reward

    def summarizePerformance(self, test_data_set, *args, **kwargs):
        """
        This function is called at every PERIOD_BTW_SUMMARY_PERFS.
        Parameters
        -----------
            test_data_set
        """

        # TODO
        print ("Summary Perf")

        # observations = test_data_set.observations()
        # prices = observations[0][100:200]
        # invest = observations[1][100:200]
        #
        # steps=np.arange(len(prices))
        # steps_long=np.arange(len(prices)*10)/10.
        #
        #print steps,invest,prices
        # host = host_subplot(111, axes_class=AA.Axes)
        # plt.subplots_adjust(right=0.9, left=0.1)
        #
        # par1 = host.twinx()
        #
        # host.set_xlabel("Time")
        # host.set_ylabel("Price")
        # par1.set_ylabel("Investment")
        #
        # p1, = host.plot(steps_long, np.repeat(prices,10), lw=3, c = 'b', alpha=0.8, ls='-', label = 'Price')
        # p2, = par1.plot(steps, invest, marker='o', lw=3, c = 'g', alpha=0.5, ls='-', label = 'Investment')
        #
        # par1.set_ylim(-0.09, 1.09)
        #
        #
        # host.axis["left"].label.set_color(p1.get_color())
        # par1.axis["right"].label.set_color(p2.get_color())
        #
        # plt.savefig("plot.png")
        # print ("A plot of the policy obtained has been saved under the name plot.png")

        print(statelist)
        print(actionlist)

    def inputDimensions(self): # changed according to tips
        return [(1,)]            # without history


    def nActions(self):
        return 2                # The environment allows two different actions to be taken at each time step


    def inTerminalState(self):
        return False

    def observe(self):
        return np.array(self._last_ponctual_observation)    # encoded state representation




def main():
    # Can be used for debug purposes
    rng = np.random.RandomState(123456)
    myenv = MyEnv(rng)

    print (myenv.observe())

if __name__ == "__main__":
    main()
