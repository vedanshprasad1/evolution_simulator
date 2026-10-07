import pygame
import sys
from json import loads, dump
from info import Info
from pathfinding import Pathfinding
from shrubs import Bush, Tree
from shelter import Shelter
from creature import Creature
from image_loader import Image_loader

pygame.init()

class Main(Pathfinding):
    def __init__(self):
        self.WINDOW_WIDTH, self.WINDOW_HEIGHT = (1300, 750) # 26 x 15 grid
        # +500 is to accomodate the extra info screen
        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH + 500, self.WINDOW_HEIGHT))
        pygame.display.set_caption("Simulation")
        self.running = True
        self.total = 0

        # Load the JSON file
        self.json_file = sys.argv[1]

        with open(f"sims/{self.json_file}", "r") as file:
            data = file.read()
            data = loads(data)

        # Grid
        self.map_grid = [[10 for x in range(26)] for y in range(15)]

        self.all_sprites = pygame.sprite.Group()
        self.creature_sprites = pygame.sprite.Group()

        self.dying_age = data["Dying age"]
        self.energy_from_food = data["Energy from food"]
        self.wood_yield = data["Wood yield"]
        self.min_temperature = data["Min temperature"]
        self.max_temperature = data["Max temperature"]
        self.season_length = data["Season length"]

        self.image_loader = Image_loader()

        # Spawn Bushes
        self.data_bushes = data["Bushes"]
        self.bushes = []
        for bush in self.data_bushes:
            self.bushes.append(Bush((bush[1], bush[2]), bush[3], bush[4], bush[5], (self.all_sprites), self))

        # Spawn Trees
        self.data_trees = data["Trees"]
        self.trees = []
        for tree in self.data_trees:
            self.trees.append(Tree((tree[1], tree[2]), tree[3], tree[4], tree[5], (self.all_sprites), self))

        # Spawn shelters
        self.data_shelters = data["Shelters"]
        self.shelters = []
        for shelter in self.data_shelters:
            self.shelters.append(Shelter((shelter[1], shelter[2]), shelter[3], shelter[4], shelter[5], self.all_sprites, self))

         # Spawn creatures
        self.data_creatures = data["Creatures"]
        self.creatures = []
        for creature in self.data_creatures:
            self.creatures.append(Creature(creature[1], creature[2], creature[3], creature[4], creature[5], creature[6], creature[7], creature[8], creature[9], creature[10], creature[11], creature[12], creature[13], creature[14], creature[15], creature[16], creature[17], creature[18], creature[19], (self.creature_sprites), self))

        for creature in self.creatures:
            creature.assign_team()
            creature.assign_state()

        for shelter in self.shelters:
            shelter.add_past_creatures()

        self.temperature_range = self.max_temperature - self.min_temperature
        self.current_temp = data["Current temperature"]
        self.moving_to_season = data["Season"]

        self.clock = pygame.time.Clock()
        self.day_timer = 6

        self.num_of_days = data["Days passed"]

        self.info = Info(self)
        self.info.build_stats_surface()

        self.paused = False

    def save_sim(self):
        data = {}

        data["Creatures"] = []
        for count, creature in enumerate(self.creatures):
            team = []
            for member in creature.team:
                if member in self.creatures:
                    team.append(self.creatures.index(member))
            
            getting_food = [False, None]
            getting_wood = [False, None]
            chasing_creature = [False, None]
            socialising = [False, None]
            going_to_shelter = [False, None]
            reproducing = [False, None]
            in_shelter = [False, None]

            if creature.getting_food[0]:
                if creature.getting_food[1] in self.bushes:
                    index = self.bushes.index(creature.getting_food[1])
                    getting_food = [creature.getting_food[0], index, "bush"]
                elif creature.getting_food[1] in self.creatures:
                    index = self.creatures.index(creature.getting_food[1])
                    getting_food = [creature.getting_food[0], index, "creature"]
                else:
                    getting_food = [False, None]
            
            if creature.getting_wood[0]:
                index = self.trees.index(creature.getting_wood[1])
                getting_wood = [creature.getting_wood[0], index]

            if creature.chasing_creature[0]:
                index = self.creatures.index(creature.chasing_creature[1])
                chasing_creature = [creature.chasing_creature[0], index]

            if creature.socialising[0]:
                index = self.creatures.index(creature.socialising[1])
                socialising = [creature.socialising[0], index]

            if creature.going_to_shelter[0]:
                index = self.shelters.index(creature.going_to_shelter[1])
                going_to_shelter = [creature.going_to_shelter[0], index]

            if creature.reproducing[0]:
                index = self.creatures.index(creature.reproducing[1])
                reproducing = [creature.reproducing[0], index]
            
            if creature.in_shelter[0]:
                index = self.shelters.index(creature.in_shelter[1])
                in_shelter = [creature.in_shelter[0], index]

            data["Creatures"].append([f"Creature{count}", 
                                      creature.energy,
                                      creature.age,
                                      creature.speed,
                                      creature.strength,
                                      creature.sight,
                                      creature.farming,
                                      creature.social,
                                      creature.temperature,
                                      creature.wood,
                                      creature.rect.left,
                                      creature.rect.top,
                                      team,
                                      getting_food,
                                      getting_wood,
                                      chasing_creature,
                                      socialising,
                                      going_to_shelter,
                                      reproducing,
                                      in_shelter])
        
        data["Bushes"] = []
        for count, bush in enumerate(self.bushes):
            data["Bushes"].append([f"Bush{count}",
                                   bush.rect.left,
                                   bush.rect.top,
                                   bush.growth_rate,
                                   bush.dying_probability,
                                   bush.resource])
            
        data["Trees"] = []
        for count, tree in enumerate(self.trees):
            data["Trees"].append([f"Tree{count}",
                                   tree.rect.left,
                                   tree.rect.top,
                                   tree.growth_rate,
                                   tree.dying_probability,
                                   tree.resource])
            
        data["Shelters"] = []
        for count, shelter in enumerate(self.shelters):
            current_creatures = []
            if shelter.current_creatures:
                for member in shelter.current_creatures:
                    if member in self.creatures:
                        current_creatures.append(self.creatures.index(member))
            data["Shelters"].append([f"Shelter{count}",
                                     shelter.rect.left,
                                     shelter.rect.top,
                                     shelter.internal_temp,
                                     shelter.max_creatures,
                                     current_creatures])
            
        data["Dying age"] = self.dying_age
        data["Energy from food"] = self.energy_from_food
        data["Wood yield"] = self.wood_yield
        data["Min temperature"] = self.min_temperature
        data["Max temperature"] = self.max_temperature
        data["Current temperature"] = self.current_temp
        data["Season"] = self.moving_to_season
        data["Season length"] = self.season_length

        data["Days passed"] = self.info.num_of_days

        # Store to JSON file
        with open(f"sims/{self.json_file}", "w") as file:
            dump(data, file)

    def kill_creature(self, creature):
        for creature_in_sim in self.creatures:
            if creature in creature_in_sim.team:
                creature_in_sim.team.discard(creature)
        try:
            creature.team.clear()
            self.creatures.remove(creature)
            self.creature_sprites.remove(creature)
            creature.kill()
        except:
            creature.kill()

    def grow_bush(self, quality, pos):
        if quality <= 20:
            growth_rate = 1
            dying_prob = 0.2
        elif quality <= 40:
            growth_rate = 2
            dying_prob = 0.18
        elif quality <= 60:
            growth_rate = 3
            dying_prob = 0.16
        elif quality <= 80:
            growth_rate = 4
            dying_prob = 0.14
        else:
            growth_rate = 5
            dying_prob = 0.12

        bush = Bush(pos, growth_rate, dying_prob, 0, (self.all_sprites), self)
        self.bushes.append(bush)
        bush.resource = 2

    def grow_tree(self, quality, pos):
        if quality <= 20:
            growth_rate = 1
            dying_prob = 0.2
        elif quality <= 40:
            growth_rate = 2
            dying_prob = 0.18
        elif quality <= 60:
            growth_rate = 3
            dying_prob = 0.16
        elif quality <= 80:
            growth_rate = 4
            dying_prob = 0.14
        else:
            growth_rate = 5
            dying_prob = 0.12

        tree = Tree(pos, growth_rate, dying_prob, 0, (self.all_sprites), self)
        self.trees.append(tree)
        tree.resource = 0

    def kill_bush(self, bush):
        self.bushes.remove(bush)
        self.all_sprites.remove(bush)
        bush.kill()

    def kill_tree(self, tree):
        self.trees.remove(tree)
        self.all_sprites.remove(tree)
        tree.kill()

    def kill_shelter(self, shelter):
        for creature in shelter.current_creatures:
            creature.leave_shelter()
        self.shelters.remove(shelter)
        self.all_sprites.remove(shelter)
        shelter.kill()

    def create_creature(self, creature1, creature2, energy):
        creature = Creature(energy,
                            0,
                            (creature1.speed + creature2.speed) // 2,
                            (creature1.strength + creature2.strength) // 2,
                            (creature1.sight + creature2.sight) // 2,
                            (creature1.farming + creature2.farming) // 2,
                            (creature1.social + creature2.social) // 2,
                            (creature1.temperature + creature2.temperature) // 2,
                            0,
                            creature1.rect.centerx,
                            creature1.rect.centery,
                            [],
                            [False, None],
                            [False, None],
                            [False, None],
                            [False, None],
                            [False, None],
                            [False, None],
                            [False, None],
                            self.creature_sprites,
                            self)
        self.creatures.append(creature)
        creature1.team.add(creature)
        creature2.team.add(creature)
        creature.team.add(creature1)
        creature.team.add(creature2)

    def create_shelter(self, owner, wood_used, internal_temp):
        self.shelters.append(Shelter(owner.rect.topleft, internal_temp, wood_used // 50, None, (self.all_sprites), self))

    def set_temperature(self):
        self.temperature_range = self.max_temperature - self.min_temperature
        if self.moving_to_season == "summer":
            self.current_temp += self.temperature_range / self.season_length
        elif self.moving_to_season == "winter":
            self.current_temp -= self.temperature_range / self.season_length

        if self.current_temp >= self.max_temperature:
            self.current_temp = self.max_temperature
            self.moving_to_season = "winter"
        elif self.current_temp <= self.min_temperature:
            self.current_temp = self.min_temperature
            self.moving_to_season = "summer"

    def event_loop(self, event):
        if event.type == pygame.QUIT:
            self.save_sim()
            self.running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()

            if self.paused:
                # Check if the mouse has clicked any trait
                if 1300 < pos[0] < 1800 and 100 <= pos[1] < 600 and self.info.creature_selected and not ((pos[0] >= 1450 and pos[0] <= 1500) or (pos[0] >= 1650 and pos[0] <= 1700)):
                    if pos[1] < 150:
                        self.info.trait_selected = "age"
                    elif pos[1] < 200:
                        self.info.trait_selected = "energy"
                    elif pos[1] < 300 and pos[1] >= 250:
                        self.info.trait_selected = "speed"
                    elif pos[1] < 350:
                        self.info.trait_selected = "strength"
                    elif pos[1] < 400:
                        self.info.trait_selected = "sight"
                    elif pos[1] < 450:
                        self.info.trait_selected = "farming"
                    elif pos[1] < 500:
                        self.info.trait_selected = "social"
                    elif pos[1] < 550:
                        self.info.trait_selected = "temperature"
                    elif pos[1] < 600:
                        self.info.trait_selected = "wood"
                    self.info.temp_selected = False
                    return
                
                elif pos[0] < 1300 and self.info.temp_selected:
                    self.info.temp_selected = None
                
                if not self.info.creature_selected and not self.info.bush_selected and not self.info.tree_selected and not self.info.shelter_selected and pos[0] > 1300:
                    if 400 <= pos[1] <= 450:
                        self.info.trait_selected = None
                        self.info.temp_selected = "current"
                        return
                    elif 450 <= pos[1] <= 500:
                        self.info.trait_selected = None
                        self.info.temp_selected = "max"
                        return
                    elif 500 <= pos[1] <= 550:
                        self.info.trait_selected = None
                        self.info.temp_selected = "min"
                        return

                if self.info.temp_selected:
                    if self.info.increase_temp_rect.collidepoint(pos):
                        if self.info.temp_selected == "current":
                            if self.current_temp != self.max_temperature:
                                self.current_temp += 1.0
                                if self.current_temp > self.max_temperature:
                                    self.current_temp = self.max_temperature

                        elif self.info.temp_selected == "max":
                            self.max_temperature += 1

                        elif self.info.temp_selected == "min":
                            if self.min_temperature != self.max_temperature:
                                self.min_temperature += 1
                            if self.current_temp < self.min_temperature:
                                self.current_temp += 1
                        return
                    if self.info.decrease_temp_rect.collidepoint(pos):
                        if self.info.temp_selected == "current":
                            if self.current_temp != self.min_temperature:
                                self.current_temp -= 1.0
                                if self.current_temp < self.min_temperature:
                                    self.current_temp = self.min_temperature

                        elif self.info.temp_selected == "max":
                            if self.min_temperature != self.max_temperature:
                                self.max_temperature -= 1
                            if self.current_temp > self.max_temperature:
                                self.current_temp -= 1

                        elif self.info.temp_selected == "min":
                            self.min_temperature -= 1
                        return

                if self.info.trait_selected and self.info.trait_selected != "energy" and self.info.trait_selected != "wood":
                    if self.info.increase_trait_rect.collidepoint(pos):
                        setattr(self.info.creature_selected, self.info.trait_selected, getattr(self.info.creature_selected, self.info.trait_selected) + 1)
                        if getattr(self.info.creature_selected, self.info.trait_selected) > 100:
                            setattr(self.info.creature_selected, self.info.trait_selected, 100)
                        return
                    if self.info.decrease_trait_rect.collidepoint(pos):
                        setattr(self.info.creature_selected, self.info.trait_selected, getattr(self.info.creature_selected, self.info.trait_selected) - 1)
                        if getattr(self.info.creature_selected, self.info.trait_selected) < 0:
                            setattr(self.info.creature_selected, self.info.trait_selected, 0)
                        return
                elif self.info.trait_selected:
                    if self.info.increase_trait_rect.collidepoint(pos):
                        setattr(self.info.creature_selected, self.info.trait_selected, getattr(self.info.creature_selected, self.info.trait_selected) + 1)
                        return
                    if self.info.decrease_trait_rect.collidepoint(pos):
                        setattr(self.info.creature_selected, self.info.trait_selected, getattr(self.info.creature_selected, self.info.trait_selected) - 1)
                        if getattr(self.info.creature_selected, self.info.trait_selected) < 0:
                                setattr(self.info.creature_selected, self.info.trait_selected, 0)
                        return
            else:
                self.info.trait_selected = None
                self.info.temp_selected = False

            if self.info.pause_rect.collidepoint(pos):
                self.paused = False if self.paused else True
                self.info.trait_selected = None
                self.info.temp_selected = False
                return
            
            if self.info.graph_rect.collidepoint(pos) and not self.info.creature_selected and not self.info.bush_selected and not self.info.tree_selected and not self.info.shelter_selected:
                self.info.in_graphs = False if self.info.in_graphs else True
                if self.info.in_graphs:
                    self.stats_surface = self.info.build_stats_surface(width=500, height=self.WINDOW_HEIGHT)
                else:
                    self.stats_surface = None
                return

            if self.info.creature_selected:
                if self.info.team_rect.collidepoint(pos):
                    self.info.force_team = False if self.info.force_team else True
                    self.info.force_chase = False
                    return
                
                if self.info.chase_rect.collidepoint(pos):
                    self.info.force_chase = False if self.info.force_chase else True
                    self.info.force_team = False
                    return
                
                if self.info.delete_rect.collidepoint(pos):
                    self.kill_creature(self.info.creature_selected)
                    self.info.creature_selected = None
                    for creature in self.creatures:
                        creature.colour = "light blue"
                    return

                
            if self.info.shelter_selected and self.info.delete_rect.collidepoint(pos):
                self.kill_shelter(self.info.shelter_selected)
                self.info.shelter_selected = None
                return
                
            if self.info.force_team:
                for creature in self.creatures:
                    if creature.rect.scale_by(3).collidepoint(pos) and not creature.in_shelter[0]:
                        self.info.creature_selected.team.add(creature)
                        creature.team.add(self.info.creature_selected)

                        self.info.force_team = False
                        return
                    
            if self.info.force_chase:
                for creature in self.creatures:
                    if creature.rect.scale_by(3).collidepoint(pos) and not creature.in_shelter[0]:
                        self.info.creature_selected.destination = pygame.Vector2(creature.rect.center)
                        self.info.creature_selected.chasing_creature = [True, creature]
                        self.getting_food = [False, None]
                        self.getting_wood = [False, None]
                        self.socialising = [False, None]
                        self.going_to_shelter = [False, None]
                        self.reproducing = [False, None]
                        self.info.creature_selected.idle = False

                        if self.info.creature_selected.chasing_creature[1] in self.info.creature_selected.team:
                            for team_creature in self.info.creature_selected.team:
                                if self.info.creature_selected in team_creature.team:
                                    team_creature.team.discard(self.info.creature_selected)
                            self.info.creature_selected.team = set()

                        self.info.force_chase = False
                        return

            if self.info.bush_selected:
                if self.info.delete_rect.collidepoint(pos):
                    self.kill_bush(self.info.bush_selected)
                    self.info.bush_selected = None
                    return

                if self.info.increase_food_rect.collidepoint(pos):
                    self.info.bush_selected.resource += 1
                    return
                
                if self.info.decrease_food_rect.collidepoint(pos):
                    self.info.bush_selected.resource -= 1
                    if self.info.bush_selected.resource < 0:
                        self.info.bush_selected.resource = 0
                    return
            
            if self.info.tree_selected:
                if self.info.delete_rect.collidepoint(pos):
                    self.kill_tree(self.info.tree_selected)
                    self.info.tree_selected = None
                    return

                if self.info.increase_wood_rect.collidepoint(pos):
                    self.info.tree_selected.resource += 1
                    return
                
                if self.info.decrease_wood_rect.collidepoint(pos):
                    self.info.tree_selected.resource -= 1
                    if self.info.tree_selected.resource < 0:
                        self.info.tree_selected.resource = 0
                    return

            for bush in self.bushes:
                if bush.rect.scale_by(3).collidepoint(pos):
                    self.info.creature_selected = None
                    self.info.tree_selected = None
                    self.info.shelter_selected = None
                    self.info.bush_selected = bush
                    return

                else:
                    self.info.bush_selected = None
                
            for shelter in self.shelters:
                if shelter.rect.scale_by(3).collidepoint(pos):
                    self.info.creature_selected = None
                    self.info.bush_selected = None
                    self.info.tree_selected = None
                    self.info.shelter_selected = shelter
                    return
                
                else:
                    self.info.shelter_selected = None

            for tree in self.trees:
                if tree.rect.scale_by(3).collidepoint(pos):
                    self.info.creature_selected = None
                    self.info.bush_selected = None
                    self.info.shelter_selected = None
                    self.info.tree_selected = tree
                    return
                    
                else:
                    self.info.tree_selected = None
            
            for creature in self.creatures:
                if creature.rect.scale_by(3).collidepoint(pos) and not creature.in_shelter[0]:
                    self.info.bush_selected = None
                    self.info.tree_selected = None
                    self.info.shelter_selected = None
                    self.info.creature_selected = creature
                    # Reset the screen
                    for creature in self.creatures:
                        creature.colour = "light blue"
                    return

            # Reset the screen
            for creature in self.creatures:
                creature.colour = "light blue"
            self.info.creature_selected = None
            self.info.tree_selected = None
            self.info.bush_selected = None
            self.info.shelter_selected = None
            self.info.force_chase = False
            self.info.force_team = False
            self.info.trait_selected = None
            self.info.temp_selected = None

    def main_loop(self):
        frame_counter = 0
        while self.running:
            for event in pygame.event.get():
                self.event_loop(event)

            self.screen.fill(pygame.Color(220, 207, 163))

            self.dt = self.clock.tick(60) / 1000

            if not self.paused:
                frame_counter += 1
                if frame_counter > 3:
                    frame_counter = 0

                if not frame_counter % 2:
                    self.update_map_grid()

                # Determine creatures' next move
                for creature in self.creatures:
                    if not creature.idle and not creature.in_shelter[0]:
                        if creature.reached_tile:
                            creature.reached_tile = False
                            creature.path = self.determine_creature_move(creature)
                            creature.set_intermediate_tile(creature.path[0])
                        else:
                            creature.movement()
                    else:
                        creature.decide_action()

                self.day_timer -= self.dt

            self.info.creature_circle()
            self.all_sprites.update()
            self.creature_sprites.update()
            self.info.update()

            if self.day_timer <= 0:
                self.set_temperature()
                self.info.record_stats()
                self.day_timer = 6
                
                if self.info.in_graphs:
                    self.info.stats_surface = self.info.build_stats_surface(width=500, height=self.WINDOW_HEIGHT)
                else:
                    self.info.stats_surface = None

            if self.info.in_graphs and not self.info.stats_surface:
                self.info.stats_surface = self.info.build_stats_surface(width=500, height=self.WINDOW_HEIGHT)
            elif not self.info.in_graphs:
                self.info.stats_surface = None

            if self.info.stats_surface:
                stats_x = self.WINDOW_WIDTH
                stats_y = 0
                self.screen.blit(self.info.stats_surface, (stats_x, stats_y))
                for creature in self.creatures:
                    creature.colour = "light blue"
                self.info.creature_selected = None
                self.info.tree_selected = None
                self.info.bush_selected = None
                self.info.shelter_selected = None
                self.info.force_chase = False
                self.info.force_team = False

            pygame.display.update()

        pygame.quit()

if __name__ == "__main__":
    main = Main()
    main.main_loop()