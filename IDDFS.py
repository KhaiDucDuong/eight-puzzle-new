from collections import deque
import numpy as np

class Node:
        def __init__(self, state, parent, move, depth):
            self.state = state
            self.parent = parent
            self.move = move
            self.depth = depth

class IDDFS:
    def __init__(self, start_state, goal_state, size, max_depth = 10):
        self.size = size
        self.moves = []
        self.leaf_nodes = []
        self.start_state = start_state
        self.goal_state = goal_state
        self.node_counter = 0
        self.max_depth = max_depth
        self.n_jump_depth = 5
        self.is_solved = False
    
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

    def solveDFS(self, max_depth):
        possible_moves = [(0, -1, 'left'), (0, 1, 'right'), (-1, 0, 'up'), (1, 0, 'down')]
        queue = deque()
        n_leafs = len(self.leaf_nodes)
        for i in range(n_leafs):
            queue.append(self.leaf_nodes.pop())
        #explored_states store visited states and depth of the states
        explored_states = set()

        while queue:
            current_node = queue.pop()
            self.node_counter += 1

            if self.is_goal_state(current_node.state):
                self.trace_back_moves(current_node)
                return True
            
            #check the depth of the current node
            #if it is larger than max depth then we stop extending its childs
            if(current_node.depth <= max_depth):
                #if it is less than the max_depth, we extend its childs
                if(current_node.depth < max_depth):
                    r, c = self.get_blank_pos(current_node.state)

                    for dr, dc, move in possible_moves:
                        new_r, new_c = r + dr, c + dc
                        if self.is_valid(new_r, new_c):
                            new_state = [row[:] for row in current_node.state]
                            new_state[r][c], new_state[new_r][new_c] = new_state[new_r][new_c], new_state[r][c]
                            new_depth = current_node.depth + 1
                            new_node = Node(new_state, current_node, move, new_depth)

                            state_key = tuple(tuple(row) for row in new_state)
                            if (state_key, new_depth) not in explored_states:
                                queue.append(new_node)
                                explored_states.add((state_key, new_depth))
                #if it is equal to the max_depth, we add it to the leaf_nodes
                else:
                    self.leaf_nodes.append(current_node)
        
        return False
    
    def solve(self):
        allowed_depth = 5
        if(self.max_depth < 5):
            allowed_depth = self.max_depth
        
        initial_node = Node(self.start_state, None, None, 0)
        self.leaf_nodes.append(initial_node)
        if self.solveDFS(allowed_depth):
            self.is_solved = True
        else:
            while (allowed_depth < self.max_depth):
                if(allowed_depth + self.n_jump_depth < self.max_depth):
                    allowed_depth += self.n_jump_depth
                    if self.solveDFS(allowed_depth):
                        self.is_solved = True
                        break
                else:
                    allowed_depth = self.max_depth
                    if self.solveDFS(allowed_depth):
                        self.is_solved = True
