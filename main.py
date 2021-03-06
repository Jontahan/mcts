import mcts
import nimsim
import numpy as np

# MCTS is always player 0, starting player is defined in nimsim (0 or 1)
class GameAgent:
    def __init__(self, env, model=None):
        self.env = env
        self.model = model
    
    def pick_action(self, state, viz=False):
        if self.model:
            return self.model.pick_action(state, viz)
        return np.random.choice(self.env.action_space)

N, K, M = 4, 2, 50
player_id, evil_id = 0, 1
starting_player = player_id
ns = nimsim.NimSim(N, K, starting_player=starting_player)

player_agent = GameAgent(ns, model=mcts.MCTS(ns, M, player_id))
evil_agent = GameAgent(ns, model=mcts.MCTS(ns, M, evil_id))

n_games = 100
wins = 0

for i in range(n_games): # for each game
    print('game', i)
    ns.reset(starting_player) 
    done = False
    state = ns.state
    
    while not done: # for each turn
        
        if state[0] == player_id: # shitty loop, but readable
            action = player_agent.pick_action(ns.state)#, viz=(state[1]==N))
        else: # opponent move
            action = evil_agent.pick_action(ns.state)
        
        state, done = ns.step(action)
        
    if state[0] != player_id:
        wins += 1

print('wins: {}/{}'.format(wins, n_games))