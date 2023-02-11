import random
import math

from enum import Enum
from agents import Agent

# MinimaxAgent -> minimax algoritam 
# MinimaxABAgnet -> minimax sa alfa-beta odsecanjem
# MaxNAgent -> realizacija generalizacije minimax algoritma?
# ExpectAgent - EKSPEKTIMAKS? algoritma -> max i chance, svi protivnici igraju nasumicno cvorove

class StudentAgent(Agent):
    def __init__(self, position, file_name):
        super().__init__(position, file_name)
        self.id = 0
    
    @staticmethod
    def kind():
        return '0'

    def get_next_action(self, state, max_levels):
        actions = self.get_legal_actions(state)
        chosen_action = actions[random.randint(0, len(actions) - 1)]
        return chosen_action


class Player(Enum):
    MAX = 0
    MIN = 1

class MinimaxAgent(StudentAgent):
    def get_next_action(self, state, max_levels):
        action, score = self.minimax(state, max_levels, Player.MAX)
        return action

    def minimax(self, state, max_levels, player):
        agents = state.agents
        last_agent_played_id = len(agents) - 1 if state.last_agent_played_id is None else state.last_agent_played_id
        agent = agents[(last_agent_played_id + 1) % len(agents)]
        actions = state.get_legal_actions(agent.id)

        if len(actions) == 0:
            return None, 100 if player == Player.MIN else -100

        # if depth is 0 or node is a terminal node set evaluation for max player(score = -inf)
        if max_levels == 0:
            if player == Player.MAX:
                score = -math.inf
                best_action = None
                for action in actions:
                    new_state = state.apply_action(agent.id, action)
                    number_of_min_agent_actions = 8 - len(new_state.get_legal_actions(last_agent_played_id))
                    if score < number_of_min_agent_actions:
                        score = number_of_min_agent_actions
                        best_action = action
                return best_action, score
            # if depth is 0 set evaluation for min player(score = +inf)
            else:
                score = math.inf
                best_action = None
                for action in actions:
                    new_state = state.apply_action(agent.id, action)
                    number_of_max_agent_actions = len(new_state.get_legal_actions(last_agent_played_id)) - 8
                    if score > number_of_max_agent_actions:
                        score = number_of_max_agent_actions
                        best_action = action
                return best_action, score
        if player == Player.MAX:
            score = -math.inf
            best_action = None
            # for each child of node calculate evaluation and return max value  
            for action in actions:
                new_state = state.apply_action(agent.id, action)
                minimax_action, minimax_score = self.minimax(new_state, max_levels - 1, Player.MIN)
                if score < minimax_score:
                    score = minimax_score
                    best_action = action
            return best_action, score
        else:
            score = math.inf
            best_action = None
            # for each child of node calculate evaluation and return min value (best action for this player)
            for action in actions:
                new_state = state.apply_action(agent.id, action)
                minimax_action, minimax_score = self.minimax(new_state, max_levels - 1, Player.MAX)
                if score > minimax_score:
                    score = minimax_score
                    best_action = action
            return best_action, score

class MinimaxABAgent(StudentAgent):

    def get_next_action(self, state, max_levels):
        alpha = -math.inf
        beta = math.inf
        action, score = self.minimax(state, max_levels, Player.MAX, alpha, beta)
        return action

    def minimax(self, state, max_levels, player, alpha, beta):
        agents = state.agents
        last_agent_played_id = len(agents) - 1 if state.last_agent_played_id is None else state.last_agent_played_id
        agent = agents[(last_agent_played_id + 1) % len(agents)]
        actions = state.get_legal_actions(agent.id)

        if len(actions) == 0:
            return None, 100 if player == Player.MIN else -100

        if max_levels == 0:
            if player == Player.MAX:
                score = -math.inf
                best_action = None
                for action in actions:
                    new_state = state.apply_action(agent.id, action)
                    number_of_min_agent_actions = 8 - len(new_state.get_legal_actions(last_agent_played_id))
                    if score < number_of_min_agent_actions:
                        score = number_of_min_agent_actions
                        best_action = action
                    # set alpha to max value
                    alpha = max(alpha, score)
                    # check if alpha is more than beta than PRUNE
                    if alpha >= beta:
                        break
                return best_action, score
            else:
                score = math.inf
                best_action = None
                for action in actions:
                    new_state = state.apply_action(agent.id, action)
                    number_of_max_agent_actions = len(new_state.get_legal_actions(last_agent_played_id)) - 8
                    if score > number_of_max_agent_actions:
                        score = number_of_max_agent_actions
                        best_action = action
                    beta = min(beta, score)
                    if alpha >= beta:
                        break
                return best_action, score

        if player == Player.MAX:
            score = -math.inf
            best_action = None
            for action in actions:
                new_state = state.apply_action(agent.id, action)
                minimax_action, minimax_score = self.minimax(new_state, max_levels - 1, Player.MIN, alpha, beta)
                if score < minimax_score:
                    score = minimax_score
                    best_action = action
                alpha = max(alpha, score)
                if alpha >= beta:
                    break
            return best_action, score
        else:
            score = math.inf
            best_action = None
            for action in actions:
                new_state = state.apply_action(agent.id, action)
                minimax_action, minimax_score = self.minimax(new_state, max_levels - 1, Player.MAX, alpha, beta)
                if score > minimax_score:
                    score = minimax_score
                    best_action = action
                beta = min(beta, score)
                if alpha >= beta:
                    break
            return best_action, score

class MaxNAgent(StudentAgent):
    def get_next_action(self, state, max_levels):
        action, score = self.minimax(state, max_levels)
        return action

    def minimax(self, state, max_levels):
        agents = state.agents
        last_played_agent_id = len(agents) - 1 if state.last_agent_played_id is None else state.last_agent_played_id
        agent = agents[(last_played_agent_id + 1) % len(agents)]
        while not agent.is_active():
            agent = agents[(agent.id + 1) % len(agents)]
        actions = state.get_legal_actions(agent.id)

        if len(actions) == 0:
            return None, -100 if agent.id == self.id else 100

        if max_levels == 0:
            if agent.id == self.id:
                score = -math.inf
                best_action = None
                for action in actions:
                    new_state = state.apply_action(agent.id, action)
                    number_of_min_agents_actions = 16 - len(new_state.get_legal_actions(agents[(agent.id + 1) % len(agents)].id)) + len(new_state.get_legal_actions(agents[(agent.id + 2) % len(agents)].id))
                    if score < number_of_min_agents_actions:
                        score = number_of_min_agents_actions
                        best_action = action
                return best_action, score
            else:
                score = math.inf
                best_action = None
                for action in actions:
                    new_state = state.apply_action(agent.id, action)
                    number_of_max_agent_actions = len(new_state.get_legal_actions(agents[(agent.id + 1) % len(agents)].id)) + len(new_state.get_legal_actions(agents[(agent.id + 2) % len(agents)].id)) - 16
                    if score > number_of_max_agent_actions:
                        score = number_of_max_agent_actions
                        best_action = action
                return best_action, score

        if agent.id == self.id:
            score = -math.inf
            best_action = None
            for action in actions:
                new_state = state.apply_action(agent.id, action)
                minimax_action, minimax_score = self.minimax(new_state, max_levels - 1)
                if score < minimax_score:
                    score = minimax_score
                    best_action = action
            return best_action, score
        else:
            score = math.inf
            best_action = None
            for action in actions:
                new_state = state.apply_action(agent.id, action)
                minimax_action, minimax_score = self.minimax(new_state, max_levels - 1)
                if score > minimax_score:
                    score = minimax_score
                    best_action = action
            return best_action, score

class ExpectAgent(StudentAgent):
    pass