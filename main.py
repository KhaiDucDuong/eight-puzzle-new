import pygame
import random
import time
import numpy as np
from sprite import *
from settings import *
from eight_puzzle import *
# import multiprocessing

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        self.shuffle_time = 0
        self.start_shuffle = False
        self.previous_choice = ""
        self.start_game = False
        self.start_timer = False
        self.elapsed_time = 0
        self.high_score = float(self.get_high_scores()[0])
        self.solution = []
        self.total_moves = 0
        self.num_explored = 0
        self.no_solution = 0
        self.max_depth = 10
        self.is_solving = False

    def get_high_scores(self):
        with open("high_score.txt", "r") as file:
            scores = file.read().splitlines()
        return scores

    def save_score(self):
        with open("high_score.txt", "w") as file:
            file.write(str("%.3f\n" % self.high_score))

    def create_game(self):
        grid = [[x + y * GAME_SIZE for x in range(1, GAME_SIZE + 1)] for y in range(GAME_SIZE)]
        grid[-1][-1] = 0
        return grid

    def get0Pos(self):
        for row, tiles in enumerate(self.tiles):
                    for col, tile in enumerate(tiles):
                        if self.tiles_grid[row][col] == 0:
                            return (row, col)

    def doAction(self, action):
        match action:
            case "left":
                tile = self.get0Pos()
                tile[1] -= 1
                self.swapTiles(tile)
                self.total_moves += 1
            case "right":
                tile = self.get0Pos()
                tile[1] += 1
                self.swapTiles(tile)
                self.total_moves += 1
            case "down":
                tile = self.get0Pos()
                tile[0] += 1
                self.swapTiles(tile)
                self.total_moves += 1
            case "up":
                tile = self.get0Pos()
                tile[0] -= 1
                self.swapTiles(tile)
                self.total_moves += 1

    def get0Pos(self):
        for row, tiles in enumerate(self.tiles):
                    for col, tile in enumerate(tiles):
                        if self.tiles_grid[row][col] == 0:
                            return [row, col]

    def BFS_solve(self):
        start = np.zeros((GAME_SIZE, GAME_SIZE))
        goal = np.zeros((GAME_SIZE, GAME_SIZE))
            
        for row, tiles in enumerate(self.tiles):
                    for col, tile in enumerate(tiles):
                        start[row][col] = self.tiles_grid[row][col]
        
        for row, tiles in enumerate(self.tiles):
                    for col, tile in enumerate(tiles):
                        goal[row][col] = self.tiles_grid_completed[row][col]

        startPos = self.get0Pos()
        startIndex = (startPos[0], startPos[1])
        goalIndex = self.get0Pos()

        self.no_solution = 0

        p = Puzzle(start, startIndex, goal, goalIndex, size=GAME_SIZE)
        p.BFSsolve()
        if(self.solution is not None):
            self.solution = p.solution[0]
            self.num_explored = p.num_explored
        else:
            self.no_solution = 1

    def DFS_solve(self, max_move):
        start = np.zeros((GAME_SIZE, GAME_SIZE))
        goal = np.zeros((GAME_SIZE, GAME_SIZE))
            
        for row, tiles in enumerate(self.tiles):
                    for col, tile in enumerate(tiles):
                        start[row][col] = self.tiles_grid[row][col]
        
        for row, tiles in enumerate(self.tiles):
                    for col, tile in enumerate(tiles):
                        goal[row][col] = self.tiles_grid_completed[row][col]

        startPos = self.get0Pos()
        startIndex = (startPos[0], startPos[1])
        goalIndex = self.get0Pos()
            
        self.no_solution = 0
        
        p = Puzzle(start, startIndex, goal, goalIndex, max_cost=max_move, size=GAME_SIZE)
        p.DFSsolve()
        
        if(p.solution is not None):
            self.solution = p.solution[0]
            self.num_explored = p.num_explored
        else:
            self.no_solution = 1

    def A_solve(self):
        start = np.zeros((GAME_SIZE, GAME_SIZE))
        goal = np.zeros((GAME_SIZE, GAME_SIZE))
            
        for row, tiles in enumerate(self.tiles):
                    for col, tile in enumerate(tiles):
                        start[row][col] = self.tiles_grid[row][col]
        
        for row, tiles in enumerate(self.tiles):
                    for col, tile in enumerate(tiles):
                        goal[row][col] = self.tiles_grid_completed[row][col]

        for row, tiles in enumerate(self.tiles):
                    for col, tile in enumerate(tiles):
                        start[row][col] = self.tiles_grid[row][col]
        
        for row, tiles in enumerate(self.tiles):
                    for col, tile in enumerate(tiles):
                        goal[row][col] = self.tiles_grid_completed[row][col]

        startPos = self.get0Pos()
        startIndex = (startPos[0], startPos[1])
        goalIndex = (2, 2)
        
        startPos = self.get0Pos()
        startIndex = (startPos[0], startPos[1])
        goalIndex = (2, 2)
        
        self.no_solution = 0
        
        p = Puzzle(start, startIndex, goal, goalIndex, size=GAME_SIZE)
        p.A_solve()
        
        if(p.solution is not None):
            self.solution = p.solution[0]
            self.num_explored = p.num_explored
        else:
            self.no_solution = 1


    def swapTiles(self, tile):
        blankTile = self.get0Pos()
        temp = self.tiles_grid[tile[0]][tile[1]]
        self.tiles_grid[tile[0]][tile[1]] = self.tiles_grid[blankTile[0]][blankTile[1]]
        self.tiles_grid[blankTile[0]][blankTile[1]] = temp

    def shuffle(self):
        possible_moves = []
        for row, tiles in enumerate(self.tiles):
            for col, tile in enumerate(tiles):
                if tile.text == "empty":
                    if tile.right():
                        possible_moves.append("right")
                    if tile.left():
                        possible_moves.append("left")
                    if tile.up():
                        possible_moves.append("up")
                    if tile.down():
                        possible_moves.append("down")
                    break
            if len(possible_moves) > 0:
                break

        if self.previous_choice == "right":
            possible_moves.remove("left") if "left" in possible_moves else possible_moves
        elif self.previous_choice == "left":
            possible_moves.remove("right") if "right" in possible_moves else possible_moves
        elif self.previous_choice == "up":
            possible_moves.remove("down") if "down" in possible_moves else possible_moves
        elif self.previous_choice == "down":
            possible_moves.remove("up") if "up" in possible_moves else possible_moves

        choice = random.choice(possible_moves)
        self.previous_choice = choice
        if choice == "right":
            self.tiles_grid[row][col], self.tiles_grid[row][col + 1] = self.tiles_grid[row][col + 1], \
                                                                       self.tiles_grid[row][col]
        elif choice == "left":
            self.tiles_grid[row][col], self.tiles_grid[row][col - 1] = self.tiles_grid[row][col - 1], \
                                                                       self.tiles_grid[row][col]
        elif choice == "up":
            self.tiles_grid[row][col], self.tiles_grid[row - 1][col] = self.tiles_grid[row - 1][col], \
                                                                       self.tiles_grid[row][col]
        elif choice == "down":
            self.tiles_grid[row][col], self.tiles_grid[row + 1][col] = self.tiles_grid[row + 1][col], \
                                                                       self.tiles_grid[row][col]

    def draw_tiles(self):
        self.tiles = []
        for row, x in enumerate(self.tiles_grid):
            self.tiles.append([])
            for col, tile in enumerate(x):
                if tile != 0:
                    self.tiles[row].append(Tile(self, col, row, str(tile)))
                else:
                    self.tiles[row].append(Tile(self, col, row, "empty"))

    def new(self):
        self.all_sprites = pygame.sprite.Group()
        self.tiles_grid = self.create_game()
        self.tiles_grid_completed = self.create_game()
        self.elapsed_time = 0
        self.total_moves = 0
        self.start_timer = False
        self.start_game = False
        self.buttons_list = []
        self.buttons_list.append(Button(425, 100, 200, 50, "Shuffle", WHITE, BLACK))
        self.buttons_list.append(Button(425, 170, 200, 50, "Reset", WHITE, BLACK))
        self.buttons_list.append(Button(425, 240, 200, 50, "BFS Solve", WHITE, BLACK))
        self.buttons_list.append(Button(712, 240, 200, 50, "A* Solve", WHITE, BLACK))
        self.buttons_list.append(Button(425, 310, 200, 50, "DFS Solve", WHITE, BLACK))
        self.buttons_list.append(Button(700, 100, 75, 50, "<<", WHITE, BLACK))
        self.buttons_list.append(Button(850, 100, 75, 50, ">>", WHITE, BLACK))
        self.draw_tiles()

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def run_timer(self):
        self.start_game = True
        self.start_timer = True

    def update(self):
        if self.start_game:
            if self.tiles_grid == self.tiles_grid_completed:
                self.start_game = False
                if self.high_score > 0:
                    self.high_score = self.elapsed_time if self.elapsed_time < self.high_score else self.high_score
                else:
                    self.high_score = self.elapsed_time
                self.save_score()

            if self.start_timer:
                self.timer = time.time()
                self.start_timer = False
            self.elapsed_time = time.time() - self.timer

        if self.start_shuffle:
            self.shuffle()
            self.draw_tiles()
            self.shuffle_time += 1
            if self.shuffle_time > 8:
                self.start_shuffle = False
                self.run_timer()
        
        if len(self.solution) > 0:
            self.doAction(self.solution.pop(0))
            self.draw_tiles()
        
        self.all_sprites.update()

    def draw_grid(self):
        for row in range(-1, GAME_SIZE * TILESIZE, TILESIZE):
            pygame.draw.line(self.screen, LIGHTGREY, (row, 0), (row, GAME_SIZE * TILESIZE))
        for col in range(-1, GAME_SIZE * TILESIZE, TILESIZE):
            pygame.draw.line(self.screen, LIGHTGREY, (0, col), (GAME_SIZE * TILESIZE, col))

    def draw(self):
        self.screen.fill(BGCOLOUR)
        self.all_sprites.draw(self.screen)
        self.draw_grid()
        for button in self.buttons_list:
            button.draw(self.screen)
        UIElement(425, 35, "%.3f" % self.elapsed_time).draw(self.screen)
        UIElement(700, 35, "DFS Depth: " + str(self.max_depth)).draw(self.screen)
        UIElement(430, 450, "High Score - %.3f" % (self.high_score if self.high_score > 0 else 0)).draw(self.screen)
        UIElement(485, 500, "Total moves: " + str(self.total_moves)).draw(self.screen)
        if(self.no_solution == 1):
            UIElement(125, 550, "No solution for chosen algorithm").draw(self.screen)
        if(self.num_explored != 0):
            UIElement(225, 550, "State explored: " + str(self.num_explored)).draw(self.screen)
        if(self.is_solving == True):
            UIElement(125, 550, "Solving...").draw(self.screen) 
        pygame.display.flip()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit(0)

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for row, tiles in enumerate(self.tiles):
                    for col, tile in enumerate(tiles):
                        if tile.click(mouse_x, mouse_y):
                            if tile.right() and self.tiles_grid[row][col + 1] == 0:
                                self.doAction("left")
                                # self.tiles_grid[row][col], self.tiles_grid[row][col + 1] = self.tiles_grid[row][col + 1], self.tiles_grid[row][col]

                            if tile.left() and self.tiles_grid[row][col - 1] == 0:
                                self.doAction("right")
                                # self.tiles_grid[row][col], self.tiles_grid[row][col - 1] = self.tiles_grid[row][col - 1], self.tiles_grid[row][col]

                            if tile.up() and self.tiles_grid[row - 1][col] == 0:
                                self.doAction("down")
                                # self.tiles_grid[row][col], self.tiles_grid[row - 1][col] = self.tiles_grid[row - 1][col], self.tiles_grid[row][col]

                            if tile.down() and self.tiles_grid[row + 1][col] == 0:
                                self.doAction("up")
                                # self.tiles_grid[row][col], self.tiles_grid[row + 1][col] = self.tiles_grid[row + 1][col], self.tiles_grid[row][col]

                            self.draw_tiles()

                for button in self.buttons_list:
                    if button.click(mouse_x, mouse_y):
                        if button.text == "Shuffle":
                            self.shuffle_time = 0
                            self.total_moves = 0
                            self.start_shuffle = True
                        if button.text == "Reset":
                            self.new()
                        if button.text == "BFS Solve":
                            self.total_moves = 0
                            self.num_explored = 0;
                            self.BFS_solve()
                        if button.text == "DFS Solve":
                            self.total_moves = 0
                            self.num_explored = 0;
                            self.DFS_solve(self.max_depth)
                        if button.text == "A* Solve":
                            self.total_moves = 0
                            self.num_explored = 0
                            self.A_solve()
                        if button.text == ">>":
                            if(self.max_depth < 100):
                                self.max_depth += 1
                        if button.text == "<<":
                            if(self.max_depth > 1):
                                self.max_depth -=1
    

game = Game()
while True:
    game.new()
    game.run()
