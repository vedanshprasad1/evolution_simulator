import pygame
from random import randint

class Creature(pygame.sprite.Sprite):
    def __init__(self, energy, age, speed, strength, sight, farming, social, temperature, wood, posx, posy, team, getting_food, getting_wood, chasing_creature, socialising, going_to_shelter, reproducing, in_shelter, groups, main):
        super().__init__(groups)
        self.pos = pygame.Vector2(posx, posy)

        # Setting traits
        self.energy = int(energy)
        self.age = int(age)
        self.speed = int(speed)
        self.strength = int(strength)
        self.sight = int(sight)
        self.farming = int(farming)
        self.social = int(social)
        self.temperature = int(temperature)
        self.wood = int(wood)

        # Energy consumption decided by speed, strength, and sight stats
        self.energy_consumption = (4 * self.speed + 2 * self.strength + self.sight) / 10

        self.main = main

        self.rect = pygame.Rect((int(self.pos.x), int(self.pos.y)), (25, 25))

        self.direction = pygame.Vector2(0, 0)
        self.destination = pygame.Vector2(self.pos.x, self.pos.y)
        self.idle = True
        
        self.team = set()
        self.past_team = team
        self.team_member_coming = [False, None]

        # Holds boolean of whether they're doing the action, and the object of interest
        self.getting_food = getting_food
        self.getting_wood = getting_wood
        self.chasing_creature = chasing_creature
        self.socialising = socialising
        self.going_to_shelter = going_to_shelter
        self.reproducing = reproducing
        self.in_shelter = in_shelter

        self.reached_tile = True
        self.tile_to_move_to = None
        self.path = []

        self.colour = "light blue"

        self.last_reproduced = 0

        self.grow_bush_timer = 10
        self.grow_tree_timer = 10
    
    def assign_team(self):
        for index in self.past_team:
            self.team.add(self.main.creatures[index])
    
    def assign_state(self):
        if self.getting_food[0]:
            if self.getting_food[2] in self.main.bushes:
                self.getting_food = [True, self.main.bushes[self.getting_food[1]]]
                self.idle = False
            elif self.getting_food[2] in self.main.creatures:
                self.getting_food = [True, self.main.creatures[self.getting_food[1]]]
                self.idle = False
            else:
                self.getting_food = [False, None]

        if self.getting_wood[0]:
            self.getting_wood[1] = self.main.trees[self.getting_wood[1]]
            self.idle = False

        if self.chasing_creature[0]:
            self.chasing_creature[1] = self.main.creatures[self.chasing_creature[1]]
            self.idle = False

        if self.socialising[0]:
            self.socialising[1] = self.main.creatures[self.socialising[1]]
            self.idle = False

        if self.going_to_shelter[0]:
            self.going_to_shelter[1] = self.main.shelters[self.going_to_shelter[1]]
            self.idle = False
        
        if self.reproducing[0]:
            self.reproducing[1] = self.main.creatures[self.reproducing[1]]
            self.idle = False

        if self.in_shelter[0]:
            self.in_shelter[1] = self.main.shelters[self.in_shelter[1]]
            self.idle = False

    def get_food(self, bush):
        food_collected = bush.give_resource()

        # Limit amount of food they can get
        if food_collected > 10:
            food_collected = 10

        # Increase energy based on food
        self.energy += food_collected * self.main.energy_from_food

    def get_wood(self, tree):
        wood_collected = tree.give_resource()

        # Limit amount of wood they can get
        if wood_collected > 100:
            wood_collected = 100

        # Increase amount of wood they can get
        self.wood += int(wood_collected * self.main.wood_yield)

    def grow(self):
        if self.main.day_timer <= 0:
            self.age += 1
            self.energy -= self.energy_consumption

            if self.grow_bush_timer > 0:
                self.grow_bush_timer -= 1

            if self.grow_tree_timer > 0:
                self.grow_tree_timer -= 1

        if self.age >= self.main.dying_age:
            self.main.kill_creature(self)

    def leave_shelter(self):
        if self.in_shelter[0]:
            self.in_shelter[1].current_creatures.remove(self)
            self.in_shelter = [False, None] 

    def set_intermediate_tile(self, new_pos):
        # if no value in new_pos
        if new_pos is None:
            self.tile_to_move_to = None
            self.reached_tile = True
            return
        # set tile value to move to
        self.tile_to_move_to = pygame.Vector2(new_pos[0] * 50, new_pos[1] * 50)
        self.reached_tile = False

    def movement(self):
        # Don't move if a team member needs help
        if self.team_member_coming[0]:
            # Make sure creature isn't stuck forever when they get low on energy
            if self.energy < 3 * self.energy_consumption:
                self.team_member_coming = [False, None]
            return

        # vector from current float pos to target tile
        target_direction = self.tile_to_move_to - self.pos
        distance = target_direction.length_squared()

        move_speed = float(self.speed * 2 + 50)

        # movement step this frame
        step = move_speed * self.main.dt

        # value for which if the creature is either less than 1 or less then one step away from target, the creature will just be counted as arrived
        snap_distance = max(1.0, step)

        # see if creature is chasing a creature
        if self.chasing_creature[0]:
            # creature reached prey
            if self.rect.colliderect(self.chasing_creature[1].rect):
                self.energy += int(self.chasing_creature[1].energy)
                self.main.kill_creature(self.chasing_creature[1])
                self.chasing_creature = [False, None]
                self.idle = True
                return

            # check if creature has lost sight of prey
            prey_distance = pygame.Vector2(self.rect.center).distance_to(pygame.Vector2(self.chasing_creature[1].rect.center))

            if prey_distance > self.sight * 2 + 50:
                self.chasing_creature = [False, None]
                self.idle = True
                return

        # at destination
        if distance <= snap_distance ** 2:
            self.pos = self.tile_to_move_to.copy()
            self.rect.topleft = (int(self.pos.x), int(self.pos.y))
            self.reached_tile = True
            # if at overall destination, perform relevant actions
            dest_tile = pygame.Vector2((self.destination.x // 50) * 50, (self.destination.y // 50) * 50)
            if self.tile_to_move_to == dest_tile:
                if self.getting_food[0]:
                    # Check if food is coming from a team creature
                    if self.socialising[0]:
                        creature = self.socialising[1]
                        if creature.energy > 3 * creature.energy_consumption:
                            energy_diff = int(creature.energy - 3 * creature.energy_consumption)
                            creature.energy -= energy_diff
                            self.energy += energy_diff
                            if self.energy > 3 * self.energy_consumption:
                                energy_diff = int(self.energy - 3 * self.energy_consumption)
                                self.energy -= energy_diff
                                creature.energy += energy_diff

                        creature.team_member_coming = [False, None]
                        self.socialising = [False, None]
                        self.getting_food = [False, None]
                    else:
                        # Get food from bush
                        self.get_food(self.getting_food[1])
                        self.getting_food = [False, None]
                elif self.getting_wood[0]:
                    self.get_wood(self.getting_wood[1])
                    self.getting_wood = [False, None]
                elif self.chasing_creature[0]:
                    # Keep chasing creature
                    if self.chasing_creature[1] in self.main.creatures:
                        self.destination = pygame.Vector2(self.chasing_creature[1].rect.center)
                    else:
                        self.chasing_creature = [False, None]
                        self.idle = True
                    self.clamp_destination()
                elif self.socialising[0]:
                    creature = self.socialising[1]
                    if randint(0, 100) <= creature.social:
                        if creature not in self.team:
                            self.team.add(creature)
                        for creature in creature.team:
                            if creature not in self.team and creature != self:
                                self.team.add(creature) 
                    
                        creature.team.add(self)
                        for creature in self.team:
                            if creature not in creature.team and creature != creature:
                                creature.team.add(creature)
                    
                    creature.team_member_coming = [False, None]

                    self.socialising = [False, None]
                
                elif self.reproducing[0]:
                    creature = self.reproducing[1]
                    excess_energy = ((self.energy - 3 * self.energy_consumption) + (creature.energy - 3 * creature.energy_consumption)) // 2
                    self.energy = 2 * self.energy_consumption
                    creature.energy = 2 * creature.energy_consumption
                    self.main.create_creature(self, creature, excess_energy)

                    self.last_reproduced = self.age
                    creature.last_reproduced = creature.age
                    self.reproducing = [False, None]
                    creature.reproducing = [False, None]
                    creature.team_member_coming = [False, None]

                elif self.going_to_shelter[0]:
                    if not self.going_to_shelter[1].full:
                        self.going_to_shelter[1].current_creatures.append(self)
                        self.in_shelter[0] = True
                        self.in_shelter[1] = self.going_to_shelter[1]
                        self.going_to_shelter = [False, None]
                    else:
                        self.going_to_shelter = [False, None]

                self.idle = True if not self.chasing_creature[0] else False
            # Otherwise find which tile the creature needs to move to next
            else:
                if len(self.path) >= 2:
                    self.set_intermediate_tile(self.path[1])
                    self.path.pop(0)
                else:
                    self.path = []

            return

        # still need to move - calculate normalized direction and move by step
        self.direction = target_direction.normalize()
        
        if step >= target_direction.length():
            self.pos = self.tile_to_move_to.copy()
        else:
            self.pos += self.direction * step

        # write integer rect position from float pos
        self.rect.topleft = (int(self.pos.x), int(self.pos.y))

    def snap_to_tile(self, value):
        return round(value / 50) * 50
        
    def decide_action(self):
        # No need to decide action
        if not self.idle:
            return
        
        # Get nearby bushes
        self.near_bushes = []
        for bush in self.main.bushes:
            distance = pygame.Vector2(bush.pos).distance_to(pygame.Vector2(self.rect.center))
            if distance <= self.sight * 2 + 50 and bush.resource >= 1:
                self.near_bushes.append([bush, distance])
        
        # Get nearby creatures that aren't doing anything important
        near_creatures = []
        for creature in self.main.creatures:
            if creature != self and not creature.getting_food[0] and not creature.socialising[0] and not creature.reproducing[0] and not creature.in_shelter[0]:
                distance_to_creature = pygame.Vector2(self.rect.center).distance_to(pygame.Vector2(creature.rect.center))
                if distance_to_creature <= self.sight * 2 + 50:
                    near_creatures.append(creature)

        # Get nearby trees
        self.near_trees = []
        for tree in self.main.trees:
            distance = pygame.Vector2(tree.pos).distance_to(pygame.Vector2(self.rect.center))
            if distance <= self.sight * 2 + 50 and tree.resource >= 1:
                self.near_trees.append([tree, distance])

        # Check if low on energy, then find the nearest bush and go towards it
        if self.energy < 3 * self.energy_consumption:
            shortest_distance = self.sight * 2 + 50
            nearest_bush = None
            for bush in range(len(self.near_bushes)):
                if self.near_bushes[bush][1] < shortest_distance:
                    shortest_distance = self.near_bushes[bush][1]
                    nearest_bush = self.near_bushes[bush][0]

            if nearest_bush:
                self.destination = pygame.Vector2(nearest_bush.rect.center)
                self.clamp_destination()
                self.getting_food = [True, nearest_bush]
                self.idle = False

                self.leave_shelter()
                return
            
            # No bushes nearby, plant a bush
            elif not self.near_bushes and self.grow_bush_timer <= 0 and not self.in_shelter[0]:
                self.main.grow_bush(self.farming, self.rect.topleft)
                self.energy -= self.energy_consumption
                self.grow_bush_timer = 10
                return

            # Not found a bush, check if the creature can see a team member or a weaker creature for energy
            # Order depends on social stat
            if self.social < 50:
                for creature in near_creatures:
                    if creature.strength < self.strength and randint(0, 100) < self.social and creature not in self.team:
                        self.destination = pygame.Vector2(creature.rect.center)
                        self.clamp_destination()
                        self.chasing_creature = [True, creature]
                        self.idle = False
                        self.leave_shelter()
                        return

                for creature in near_creatures:
                    if creature in self.team:
                        self.destination = pygame.Vector2(creature.rect.center)
                        self.clamp_destination()
                        self.socialising = [True, creature]
                        self.getting_food = [True, creature]
                        creature.team_member_coming = [True, self]
                        self.idle = False
                        self.leave_shelter()
                        return

            else:
                for creature in near_creatures:
                    if creature in self.team:
                        self.destination = pygame.Vector2(creature.rect.center)
                        self.clamp_destination()
                        self.socialising = [True, creature]
                        self.getting_food = [True, creature]
                        creature.team_member_coming = [True, self]
                        self.idle = False
                        self.leave_shelter()
                        return
                    
                for creature in near_creatures:
                    if creature.strength < self.strength and randint(0, 100) < self.social and creature not in self.team:
                        self.destination = pygame.Vector2(creature.rect.center)
                        self.clamp_destination()
                        self.chasing_creature = [True, creature]
                        self.idle = False
                        self.leave_shelter()
                        return
        
        # Find a shelter and go to it
        elif self.idle and (self.main.current_temp < self.temperature - 5 or self.main.current_temp > self.temperature + 5) and not self.in_shelter[0]:
            # Make sure they're not desparately low on energy, as they need to prioritise finding food
            if self.energy > 2 * self.energy_consumption:
                self.near_shelters = []
                for shelter in self.main.shelters:
                    if not shelter.full:
                        distance = pygame.Vector2(shelter.pos).distance_to(pygame.Vector2(self.rect.center))
                        if distance <= self.sight * 2 + 50:
                            self.near_shelters.append([shelter, abs(shelter.internal_temp - self.temperature)])

                best_temp = 100
                best_shelter = None
                for shelter in range(len(self.near_shelters)):
                    if self.near_shelters[shelter][1] < best_temp:
                        best_temp = self.near_shelters[shelter][1]
                        best_shelter = self.near_shelters[shelter][0]

                if best_shelter:

                    self.destination = pygame.Vector2(best_shelter.pos)
                    self.clamp_destination()
                    self.going_to_shelter = [True, best_shelter]
                    self.idle = False

                    return
            
                # Create a shelter
                else:
                    if self.energy > 3 * self.energy_consumption and self.wood > 50:
                        wood_used = self.wood // 50 * 50
                        self.wood -= wood_used
                        self.main.create_shelter(self, wood_used, self.temperature)
                        self.energy -= 2 * self.energy_consumption
                    else:
                        # Check if they don't have a lot of wood then go get wood
                        if self.idle and self.wood < 150 and not self.getting_wood[0] and not self.getting_food[0]:
                            shortest_distance = self.sight * 2 + 50
                            nearest_tree = None
                            for tree in range(len(self.near_trees)):
                                if self.near_trees[tree][1] < shortest_distance:
                                    shortest_distance = self.near_trees[tree][1]
                                    nearest_tree = self.near_trees[tree][0]

                            if nearest_tree:
                                self.destination = pygame.Vector2(nearest_tree.pos)
                                self.clamp_destination()
                                self.getting_wood = [True, nearest_tree]
                                self.idle = False
                                self.leave_shelter()
                                return

        # Check if the creature can see a weaker or highly sociable creature nearby
        elif near_creatures:
            for creature in near_creatures:
                # Check for a mate to reproduce with
                if self.energy > self.energy_consumption * 10 and creature.energy > creature.energy_consumption * 10 and creature in self.team and len(self.main.creatures) < 150:
                    if self.age > self.last_reproduced and creature.age > creature.last_reproduced:
                        self.destination = pygame.Vector2(creature.rect.center)
                        self.reproducing = [True, creature]
                        creature.team_member_coming = [True, self]
                        self.idle = False
                        self.leave_shelter()
                        return

                # Find someone to eat
                if creature.strength < self.strength and randint(0, 100) > self.social and creature not in self.team:
                    # Not in team
                    self.destination = pygame.Vector2(creature.rect.center)
                    self._creature = [True, creature]
                    self.idle = False
                    self.leave_shelter()
                    return
                
                elif creature.strength * 1.2 < self.strength and randint(0, 100) > self.social * 2.2 and creature in self.team:
                    # Betraying team
                    for team_creature in self.team:
                        if self in team_creature.team:
                            team_creature.team.discard(self)
                    self.team = set()
                    self.destination = pygame.Vector2(creature.rect.center)
                    self.chasing_creature = [True, creature]
                    self.idle = False
                    self.leave_shelter()
                    return
                
                # Find someone to socialise with
                elif creature.strength < self.strength + 10 and randint(0, 200) < self.social and creature not in self.team:
                    self.destination = pygame.Vector2(creature.rect.center)
                    self.socialising = [True, creature]
                    self.idle = False
                    self.leave_shelter()
                    return
        
        # Check if there are no trees nearby and the creatures have energy and not a lot of wood, then grow a tree
        elif not self.near_trees and self.grow_tree_timer <= 0 and self.energy >= 5 * self.energy_consumption and self.wood < 50:
            self.main.grow_tree(self.farming, self.rect.center)
            self.energy -= self.energy_consumption * 5
            self.grow_tree_timer = 10
            return

        # Set a random destination
        self.destination = pygame.Vector2(self.snap_to_tile(randint(self.rect.centerx-(self.sight*2+50), self.rect.centerx+(self.sight*2+50))), self.snap_to_tile(randint(self.rect.centery-(self.sight*2+50), self.rect.centery+(self.sight*2+50))))
        self.clamp_destination()

        # Check creature isn't already at the random destination selected
        if self.destination.distance_to(self.rect.center) < 50:
            self.decide_action()

        self.idle = False
    
    def clamp_destination(self):
        # snap to tile
        self.destination.x = self.snap_to_tile(self.destination.x)
        self.destination.y = self.snap_to_tile(self.destination.y)

        # clamp inside world
        if self.destination.x < 0:
            self.destination.x = 0
        elif self.destination.x > self.main.WINDOW_WIDTH - 50:
            self.destination.x = self.main.WINDOW_WIDTH - 50

        if self.destination.y < 0:
            self.destination.y = 0
        elif self.destination.y > self.main.WINDOW_HEIGHT - 50:
            self.destination.y = self.main.WINDOW_HEIGHT - 50

    def update(self):
        if self.in_shelter[0]:
            self.energy_consumption = (4 * self.speed + 2 * self.strength + self.sight) / 10 + (5 * abs(self.temperature - self.in_shelter[1].internal_temp))
        else:
            self.energy_consumption = (4 * self.speed + 2 * self.strength + self.sight) / 10 + (5 * abs(self.temperature - self.main.current_temp))

        if not self.main.paused:
            self.grow()

            if self.energy < 1:
                self.main.kill_creature(self)

        # Leave a shelter if they're in one if they're really low on energy or the environment temperature is fine
        if self.in_shelter[0] and (self.energy <= 2 * self.energy_consumption or self.temperature - 5 <= self.main.current_temp <= self.temperature + 5):
            self.leave_shelter()
        
        # Draw
        if not self.in_shelter[0]:
            pygame.draw.circle(self.main.screen, self.colour, (self.rect.center), 13)
            pygame.draw.circle(self.main.screen, "black", self.rect.center, 13, 2)