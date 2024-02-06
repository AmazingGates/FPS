# This is where we will create a pathfinding attribute for our npc
from collections import deque


class Pathfinding: # This is where we will create our Pathfinding class in which we need to define the ways of 
    #moving to neighboring tiles for the enemy
    def __init__(self, game):
        self.game = game
        self.map = game.map.mini_map
        self.ways = [-1, 0], [0, -1], [1, 0], [0, 1], [-1, -1], [1, -1], [1, 1], [-1, 1]
        self.graph = {}
        self.get_graph()

    def get_path(self, start, goal):
        self.visted = self.bfs(start, goal, self.graph)
        path = [goal]
        step = self.visted.get(goal, start)

        while step and step != start:
            path.append(step)
            step = self.visted[step]
        return path[-1]

    def bfs(self, start, goal, graph): # This is where we will write a cassic BFS algorithn
        queue = deque([start])
        visited = {start: None}

        while queue:
            cur_node = queue.popleft()
            if cur_node == goal:
                break
            next_nodes = graph[cur_node]

            for next_node in next_nodes:
                if next_node not in visited and next_node not in self.game.object_handler.npc_positions:
                    queue.append(next_node)
                    visited[next_node] = cur_node
        return visited

    def get_next_nodes(self, x, y):
        return [(x + dx, y + dy) for dx, dy in self.ways if (x + dx, y + dy ) not in self.game.map.world_map]

    # This is where we will build our graph of adjacent tiles. It will be a dictionary in which the coordinates
    #of each tile will coordinate to a list of adjacent tiles we can get to from the original one
    def get_graph(self):
        for y, row in enumerate(self.map):
            for x, col in enumerate(row):
                if not col:
                    self.graph[(x, y)] = self.graph.get((x, y), []) + self.get_next_nodes(x, y)