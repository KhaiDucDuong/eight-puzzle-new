import pygame
import random
import time
import numpy as np
import tkinter as tk
from tkinter import filedialog
from sprite import *
from settings import *
from BFS import BFS
from DFS import DFS
from IDDFS import IDDFS
from A_star import A_star


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        self.board_setting = 1
        self.tile_size = board_setting_1.TILESIZE.value
        self.game_size = board_setting_1.GAME_SIZE.value
        self.shuffle_time = 13
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
        self.max_depth = 15
        self.saved_state = self.create_game()
        self.default_image_path = "resources/evening_sky.jpg"
        self.puzzle_image = Sprite(0, 0, self.default_image_path, self.tile_size * self.game_size, self.tile_size * self.game_size)
        self.puzzle_image_segments = [self.split_img_into_segments()]

    def select_img_file(self):
        origin_file_path = self.default_image_path
        file_path = filedialog.askopenfilename()
        try:
            if(file_path != ''):    
                self.load_puzzle_img(file_path)
        except:
            print("cannot load image!")
            self.default_image_path = origin_file_path

    def load_puzzle_img(self, img_path = None):
        if(img_path != None):
            self.default_image_path = img_path
        self.puzzle_image = Sprite(0, 0, self.default_image_path, self.tile_size * self.game_size, self.tile_size * self.game_size) 
        self.puzzle_image_segments = self.split_img_into_segments()
        
    def split_img_into_segments(self):
        img_segments = []
        for i in range(self.game_size):
            for j in range(self.game_size):
                rect = pygame.Rect(self.tile_size * j, self.tile_size * i, self.tile_size, self.tile_size)
                img_segments.append(self.puzzle_image.getSurface().subsurface(rect))
        return img_segments

    def get_high_scores(self):
        with open("high_score.txt", "r") as file:
            scores = file.read().splitlines()
        return scores

    def save_score(self):
        with open("high_score.txt", "w") as file:
            file.write(str("%.3f\n" % self.high_score))

    def create_game(self):
        grid = [[x + y * self.game_size for x in range(1, self.game_size + 1)] for y in range(self.game_size)]
        grid[-1][-1] = 0
        return grid

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
        self.draw(1)
        UIElement(725, 550, "Solving...").draw(self.screen)
        pygame.display.flip()

        self.no_solution = 0
        p = BFS(self.tiles_grid, self.tiles_grid_completed, self.game_size)
        p.solve()

        if p.is_solved:
            self.solution = p.moves
            self.num_explored = p.node_counter
        else:
            self.no_solution = 1
        self.is_solving = 0

    def DFS_solve(self):
        self.draw(1)
        UIElement(725, 550, "Solving...").draw(self.screen)
        pygame.display.flip()

        self.no_solution = 0

        p = DFS(self.tiles_grid, self.tiles_grid_completed, self.game_size, self.max_depth)
        p.solve()
        if p.is_solved:
            self.solution = p.moves
            self.num_explored = p.node_counter
        else:
            self.no_solution = 1

    def IDDFS_solve(self):
        self.draw(1)
        UIElement(725, 550, "Solving...").draw(self.screen)
        pygame.display.flip()

        self.no_solution = 0

        p = IDDFS(self.tiles_grid, self.tiles_grid_completed, self.game_size, self.max_depth)
        p.solve()
        if p.is_solved:
            self.solution = p.moves
            self.num_explored = p.node_counter
        else:
            self.no_solution = 1

    def A_star_solve(self):
        self.draw(1)
        UIElement(725, 550, "Solving...").draw(self.screen)
        pygame.display.flip()

        self.no_solution = 0

        p = A_star(self.tiles_grid, self.tiles_grid_completed, self.game_size)
        p.solve()
        if p.is_solved:
            self.solution = p.moves
            self.num_explored = p.node_counter
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
                    #self.tiles[row].append(Tile(self, col, row, str(tile)))
                    self.tiles[row].append(Tile(self, col, row, str(tile), self.tile_size, self.game_size, self.puzzle_image_segments[tile - 1]))
                else:
                    self.tiles[row].append(Tile(self, col, row, "empty", self.tile_size, self.game_size))

    def new(self):
        self.all_sprites = pygame.sprite.Group()
        self.tiles_grid = self.create_game()
        self.tiles_grid_completed = self.create_game()
        self.load_puzzle_img()
        self.elapsed_time = 0
        self.total_moves = 0
        self.start_timer = False
        self.start_game = False
        self.buttons_list = []
        self.buttons_list.append(Button(425, 100, 200, 50, "Shuffle", WHITE, BLACK))
        self.buttons_list.append(Button(700, 100, 75, 50, "<<", WHITE, BLACK))
        self.buttons_list.append(Button(825, 100, 75, 50, ">>", WHITE, BLACK))
        self.buttons_list.append(Button(975, 100, 75, 50, "<-", WHITE, BLACK))
        self.buttons_list.append(Button(1100, 100, 75, 50, "->", WHITE, BLACK))
        self.buttons_list.append(Button(425, 170, 200, 50, "Save State", WHITE, BLACK))
        self.buttons_list.append(Button(700, 170, 200, 50, "Load State", WHITE, BLACK))
        self.buttons_list.append(Button(975, 170, 200, 50, "Reset", WHITE, BLACK))
        self.buttons_list.append(Button(975, 240, 200, 50, "Change Size", WHITE, BLACK))
        self.buttons_list.append(Button(425, 240, 200, 50, "BFS Solve", WHITE, BLACK))
        self.buttons_list.append(Button(425, 310, 200, 50, "DFS Solve", WHITE, BLACK))
        self.buttons_list.append(Button(700, 310, 200, 50, "A* Solve", WHITE, BLACK))
        self.buttons_list.append(Button(975, 310, 200, 50, "Load IMG", WHITE, BLACK))
        self.buttons_list.append(Button(700, 240, 200, 50, "IDDFS Solve", WHITE, BLACK))
        self.draw_tiles()

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

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
            self.remaining_shuffle -= 1
            if self.remaining_shuffle == 0:
                self.start_shuffle = False
                self.start_game = True
                self.start_timer = True
        
        if len(self.solution) > 0:
            self.doAction(self.solution.pop(0))
            self.draw_tiles()
        
        self.all_sprites.update()

    def draw_grid(self):
        for row in range(-1, self.game_size * self.tile_size, self.tile_size):
            pygame.draw.line(self.screen, LIGHTGREY, (row, 0), (row, self.game_size * self.tile_size))
        for col in range(-1, self.game_size * self.tile_size, self.tile_size):
            pygame.draw.line(self.screen, LIGHTGREY, (0, col), (self.game_size * self.tile_size, col))

    def draw(self, is_solving = 0):
        self.screen.fill(BGCOLOUR)
        self.all_sprites.draw(self.screen)
        self.draw_grid()
        for button in self.buttons_list:
            button.draw(self.screen)
        UIElement(425, 35, "%.3f" % self.elapsed_time).draw(self.screen)
        UIElement(700, 35, "DFS Depth: " + str(self.max_depth)).draw(self.screen)
        UIElement(975, 35, "Shuffle: " + str(self.shuffle_time)).draw(self.screen)
        UIElement(630, 450, "High Score - %.3f" % (self.high_score if self.high_score > 0 else 0)).draw(self.screen)
        UIElement(685, 500, "Total moves: " + str(self.total_moves)).draw(self.screen)
        if(self.no_solution == 1 and is_solving == 0):
            UIElement(525, 550, "No solution for chosen algorithm").draw(self.screen)
        if(self.num_explored != 0 and is_solving == 0):
            UIElement(625, 550, "State explored: " + str(self.num_explored)).draw(self.screen)
        self.screen.blit(self.puzzle_image.getSurface(), (0, self.tile_size * self.game_size + 20))
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
                            self.remaining_shuffle = self.shuffle_time
                            self.total_moves = 0
                            self.start_shuffle = True
                        if button.text == "Save State":
                            self.saved_state = [row[:] for row in self.tiles_grid]
                        if button.text == "Load State":
                            self.new()
                            self.tiles_grid = [row[:] for row in self.saved_state]
                            self.draw_tiles()
                        if button.text == "Reset":
                            self.new()
                        if button.text == "Change Size":
                            if(self.board_setting == 1):
                                self.board_setting = 2
                                self.tile_size = board_setting_2.TILESIZE.value
                                self.game_size = board_setting_2.GAME_SIZE.value
                            elif(self.board_setting == 2):
                                self.board_setting = 3
                                self.tile_size = board_setting_3.TILESIZE.value
                                self.game_size = board_setting_3.GAME_SIZE.value
                            elif(self.board_setting == 3):
                                self.board_setting = 1
                                self.tile_size = board_setting_1.TILESIZE.value
                                self.game_size = board_setting_1.GAME_SIZE.value
                            self.new()
                            self.saved_state = self.create_game()
                        if button.text == "BFS Solve":
                            self.total_moves = 0
                            self.num_explored = 0
                            self.BFS_solve()
                        if button.text == "DFS Solve":
                            self.total_moves = 0
                            self.num_explored = 0
                            self.DFS_solve()
                        if button.text == "IDDFS Solve":
                            self.total_moves = 0
                            self.num_explored = 0
                            self.IDDFS_solve()
                        if button.text == "A* Solve":
                            self.total_moves = 0
                            self.num_explored = 0
                            self.A_star_solve()
                        if button.text == "<<":
                            if(self.max_depth > 1):
                                self.max_depth -= 1
                        if button.text == ">>":
                            if(self.max_depth < 100):
                                self.max_depth += 1
                        if button.text == "<-":
                            if(self.shuffle_time > 1):
                                self.shuffle_time -= 1
                        if button.text == "->":
                            self.shuffle_time += 1
                        if button.text == "Load IMG":
                            self.select_img_file()
                            self.draw_tiles()
                            


game = Game()
while True:
    game.new()
    game.run()
