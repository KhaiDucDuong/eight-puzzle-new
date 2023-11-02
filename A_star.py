from queue import PriorityQueue
import numpy as np

class Node:
        def __init__(self, state, parent, move, depth, h_cost):
            self.state = state
            self.parent = parent
            self.move = move
            self.depth = depth
            self.cost = self.depth + h_cost

        def __lt__(self, other):
            if(self.cost < other.cost):
                return True
            return False
        def __gt__(self, other):
            if(self.cost > other.cost):
                return True
            return False
        def __eq__(self, other):
            if(self.cost == other.cost):
                return True
            return False

class A_star:
    #heuristic determines the which heuristic function is used for calculation
    #Misplaced tiles for Number of misplaced tiles 
    #Manhattan distance for Sum of Manhattan distances of the tiles from their goal positions
    def __init__(self, start_state, goal_state, size, heuristic = 'Misplaced tiles'):
        self.size = size
        self.moves = []
        self.start_state = start_state
        self.goal_state = goal_state
        self.node_counter = 0
        self.is_solved = False
        self.heuristic_type = heuristic

    def get_blank_pos(self, state):
        for r in range (self.size):
            for c in range (self.size):
                if(state[r][c] == 0):
                    return r, c
                   
    def is_valid(self, r, c):
        return 0 <= r < self.size and 0 <= c < self.size
    
    def is_goal_state(self, state):
        for r in range (self.size):
            for c in range (self.size):
                if(state[r][c] != self.goal_state[r][c]):
                    return False
        return True
    
    def trace_back_moves(self, node):
        if node is None:
            return
        self.trace_back_moves(node.parent)
        if node.move is not None:
            self.moves.append(node.move)

    def heuristic_misplaced_tiles(self, state):
        h = 0
        for r in range (self.size):
            for c in range (self.size):
                if(state[r][c] != 0 and state[r][c] != self.goal_state[r][c]):
                    h +=1
        return h
    
    def heuristic_manhattan_distance(self, state):
        h = 0
        for r in range (self.size):
            for c in range (self.size):
                tile_value = state[r][c]
                if(tile_value != 0):
                    correct_tile_r = int()
                    correct_tile_c = int()
                    if(int(tile_value / self.size) > 0):
                        correct_tile_r = int(tile_value / self.size)
                    else:
                        correct_tile_r = 0
                    if(tile_value % self.size == 0):
                        correct_tile_r -=1
                        correct_tile_c = self.size - 1
                    else:
                        correct_tile_c = tile_value % self.size - 1
                    h += abs(correct_tile_r - r) + abs(correct_tile_c - c)
        return h
    
    def solve(self):
        #set the selected heuristic function
        get_heuristic = None
        if(self.heuristic_type == 'Misplaced tiles'):
            get_heuristic = self.heuristic_misplaced_tiles
        elif(self.heuristic_type == 'Manhattan distance'):
            get_heuristic = self.heuristic_manhattan_distance
        
        possible_moves = [(0, -1, 'left'), (0, 1, 'right'), (-1, 0, 'up'), (1, 0, 'down')]
        initial_node = Node(self.start_state, None, None, 0, 0)

        queue = PriorityQueue()
        queue.put((0, initial_node))
        #explored_states store visited states and depth of the states
        explored_states = set()

        while queue:
            current_node = queue.get()[1]
            self.node_counter += 1

            if self.is_goal_state(current_node.state):
                self.is_solved = True
                self.trace_back_moves(current_node)
                return
            
            r, c = self.get_blank_pos(current_node.state)

            for dr, dc, move in possible_moves:
                new_r, new_c = r + dr, c + dc
                if self.is_valid(new_r, new_c):
                    new_state = [row[:] for row in current_node.state]
                    new_state[r][c], new_state[new_r][new_c] = new_state[new_r][new_c], new_state[r][c]
                    new_depth = current_node.depth + 1
                    new_h_cost = get_heuristic(new_state)
                    new_node = Node(new_state, current_node, move, new_depth, new_h_cost)

                    state_key = tuple(tuple(row) for row in new_state)
                    if (state_key, new_depth) not in explored_states:
                        queue.put((new_depth + new_h_cost, new_node))
                        explored_states.add((state_key, new_depth))


                    
                