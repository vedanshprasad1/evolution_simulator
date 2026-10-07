import heapq
from math import sqrt
from random import shuffle

class Pathfinding():
    def update_map_grid(self):
        # Reset the values in the grid to be 0
        self.map_grid = [[10 for x in range(26)] for y in range(15)]

        for creature in self.creatures:
            pos_x, pos_y = creature.rect.center
            pos_x //= 50
            pos_y //= 50

            self.map_grid[pos_y][pos_x] += creature.strength - creature.social
            if self.map_grid[pos_y][pos_x] < 1:
                self.map_grid[pos_y][pos_x] = 1

            for neighbour_x, neighbour_y in [(pos_x+1, pos_y), (pos_x-1, pos_y), (pos_x, pos_y+1), (pos_x, pos_y-1), (pos_x+1, pos_y+1), (pos_x-1, pos_y-1), (pos_x+1, pos_y-1), (pos_x-1, pos_y+1)]:
                if 0 <= neighbour_x < 26 and 0 <= neighbour_y < 15:
                    self.map_grid[neighbour_y][neighbour_x] += creature.strength - creature.social - 2
                    if self.map_grid[neighbour_y][neighbour_x] < 1:
                        self.map_grid[neighbour_y][neighbour_x] = 1
            
            for neighbour_x, neighbour_y in [(pos_x+2, pos_y), (pos_x-2, pos_y), (pos_x, pos_y+2), (pos_x, pos_y-2), (pos_x+2, pos_y+2), (pos_x-2, pos_y-2), (pos_x+2, pos_y-2), (pos_x-2, pos_y+2)]:
                if 0 <= neighbour_x < 26 and 0 <= neighbour_y < 15:
                    self.map_grid[neighbour_y][neighbour_x] += creature.strength - creature.social - 4
                    if self.map_grid[neighbour_y][neighbour_x] < 1:
                        self.map_grid[neighbour_y][neighbour_x] = 1

            for neighbour_x, neighbour_y in [(pos_x+1, pos_y-2), (pos_x+1, pos_y+2), (pos_x-1, pos_y+2), (pos_x-1, pos_y-2), (pos_x-2, pos_y-1), (pos_x-2, pos_y+1), (pos_x+2, pos_y+1), (pos_x+2, pos_y-1)]:
                if 0 <= neighbour_x < 26 and 0 <= neighbour_y < 15:
                    self.map_grid[neighbour_y][neighbour_x] += creature.strength - creature.social - 4
                    if self.map_grid[neighbour_y][neighbour_x] < 1:
                        self.map_grid[neighbour_y][neighbour_x] = 1

    def determine_creature_move(self, creature):
        map_grid = [row.copy() for row in self.map_grid]
        # Set the start and end points
        start_x = creature.rect.centerx // 50
        start_y = creature.rect.centery // 50
        end_x = creature.destination.x // 50
        end_y = creature.destination.y // 50

        # Decrease cost for cells next to creatures in the same team
        for team_member in creature.team:
            pos_x, pos_y = team_member.rect.center
            pos_x //= 50
            pos_y //= 50

            # Undo added cost to cells if the cost came from a team member
            map_grid[pos_y][pos_x] -= team_member.strength - team_member.social
            if map_grid[pos_y][pos_x] < 1:
                map_grid[pos_y][pos_x] = 1

            for neighbour_x, neighbour_y in [(pos_x+1, pos_y), (pos_x-1, pos_y), (pos_x, pos_y+1), (pos_x, pos_y-1), (pos_x+1, pos_y+1), (pos_x-1, pos_y-1), (pos_x+1, pos_y-1), (pos_x-1, pos_y+1)]:
                if 0 <= neighbour_x < 26 and 0 <= neighbour_y < 15:
                    map_grid[neighbour_y][neighbour_x] -= team_member.strength - team_member.social
                    if map_grid[neighbour_y][neighbour_x] < 1:
                        map_grid[neighbour_y][neighbour_x] = 1
            
            for neighbour_x, neighbour_y in [(pos_x+2, pos_y), (pos_x-2, pos_y), (pos_x, pos_y+2), (pos_x, pos_y-2), (pos_x+2, pos_y+2), (pos_x-2, pos_y-2), (pos_x+2, pos_y-2), (pos_x-2, pos_y+2)]:
                if 0 <= neighbour_x < 26 and 0 <= neighbour_y < 15:
                    map_grid[neighbour_y][neighbour_x] -= team_member.strength - team_member.social
                    if map_grid[neighbour_y][neighbour_x] < 1:
                        map_grid[neighbour_y][neighbour_x] = 1

            for neighbour_x, neighbour_y in [(pos_x+1, pos_y-2), (pos_x+1, pos_y+2), (pos_x-1, pos_y+2), (pos_x-1, pos_y-2), (pos_x-2, pos_y-1), (pos_x-2, pos_y+1), (pos_x+2, pos_y+1), (pos_x+2, pos_y-1)]:
                if 0 <= neighbour_x < 26 and 0 <= neighbour_y < 15:
                    map_grid[neighbour_y][neighbour_x] -= team_member.strength - team_member.social
                    if map_grid[neighbour_y][neighbour_x] < 1:
                        map_grid[neighbour_y][neighbour_x] = 1

                
        neighbours = [(1,0), (-1,0), (0,1), (0,-1), (1,1), (-1,-1), (1,-1), (-1,1)]

        open_list = []
        heapq.heapify(open_list)
        heapq.heappush(open_list, (0, (start_y, start_x)))

        came_from = {} 
        g_score = {(start_y, start_x): 0} # Stores node with total cost to get there

        while open_list:
            # Heappop returns smallest element in heap
            # current_f stores the cost associated with each cell + the heuristic
            # cy, cx becomes coordinates of the node the algorithm is looking at
            current_f, (cy, cx) = heapq.heappop(open_list)

            # Reached goal
            if (cy, cx) == (end_y, end_x):
                path = []
                # Use came_from to work backwards from the goal and get to the starting point
                while (cy, cx) in came_from:
                    path.append((cx, cy))
                    cy, cx = came_from[(cy, cx)]
                path.append((start_x, start_y))
                path.reverse()
                return path
            
            # Explore neighbours
            for dy, dx in neighbours:
                # The cell being explored becomes (nx, ny)
                nx = cx + dx
                ny = cy + dy
                # Check if neighbours are valid places on the grid
                if 0 <= ny < 15 and 0 <= nx < 26:
                    new_g = g_score[(cy, cx)] + map_grid[ny][nx]  # cumulative movement cost from start cell through previous cell + cell cost

                    if (ny, nx) not in g_score or new_g < g_score[(ny, nx)]: # If not visited node before or found shorter path to get to the node
                        g_score[(ny, nx)] = new_g
                        # Calculate octile distance
                        hx = abs(nx - end_x)
                        hy = abs(ny - end_y)
                        distance = (hx + hy) + (sqrt(2)-2)*(min(hx, hy))
                        f = new_g + distance
                        heapq.heappush(open_list, (f, (ny, nx)))
                        came_from[(ny, nx)] = (cy, cx)

        # Explored every node
        path = []
        while (cy, cx) in came_from:
            path.append((cx, cy))
            cy, cx = came_from[(cy, cx)]
        path.reverse()

        if len(path) != 0:
            return path
        else:
            # Backup when A* doesn't find a path
            # Avoid mostly choosing one direction over the others
            shuffle(neighbours)
            costs = []
            min_cost = 1000
            best_move = None

            for dx, dy in neighbours:
                neighbour_x = start_x + dx
                neighbour_y = start_y + dy
                if 0 <= neighbour_x < 26 and 0 <= neighbour_y < 15:
                    # Calculate octile distance
                    hx = abs(neighbour_x - end_x)
                    hy = abs(neighbour_y - end_y)
                    distance = (hx + hy) + (sqrt(2)-2)*(min(hx, hy))

                    if distance + map_grid[neighbour_y][neighbour_x] <= min_cost:
                        min_cost = distance + map_grid[neighbour_y][neighbour_x]
                        best_move = neighbour_x, neighbour_y
                        costs.append(best_move)

            # Choose the minimum cost when its a tie at random
            shuffle(costs)
            best_move = costs[0]

            return [best_move]