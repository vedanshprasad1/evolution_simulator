import pygame
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from io import BytesIO

class Info():
    def __init__(self, main):
        self.main = main
        self.rect = pygame.Rect((1300, 0), (500, self.main.WINDOW_HEIGHT))

        self.creature_selected = None
        self.bush_selected = None
        self.tree_selected = None
        self.shelter_selected = None
        self.trait_selected = None
        self.temp_selected = None
        self.force_team = False
        self.force_chase = False
        self.in_graphs = False

        self.cross_image = pygame.transform.scale(pygame.image.load("images/cross.png").convert_alpha(), (50, 50))
        self.cross_rect = pygame.Rect((0, 0), (50, 50))

        self.button_size = 40
        self.button_font = pygame.font.SysFont("arialblack", self.button_size)

        self.title_size = 60
        self.title_font = pygame.font.SysFont("arial", self.title_size)

        self.traits_size = 30
        self.traits_font = pygame.font.SysFont("arial", self.traits_size)

        self.title_text = (pygame.font.SysFont("arial", 30).render("Click a creature to see info about it", True, (0, 0, 0)))
        self.title_text_rect = self.title_text.get_rect()
        self.title_text_rect.centerx = 1550
        self.title_text_rect.top = 10

        self.creature_text = (self.title_font.render("Creature", True, (0, 0, 0)))
        self.creature_text_rect = self.creature_text.get_rect()
        self.creature_text_rect.centerx = 1550
        self.creature_text_rect.top = 10

        self.team_rect = pygame.Rect((1575, 610), (200, 50))
        self.team_text = (self.button_font.render("Team", True, (255, 255, 255)))
        self.team_text_rect = self.team_text.get_rect()
        self.team_text_rect.center = self.team_rect.center

        self.chase_rect = pygame.Rect((1575, 685), (200, 50))
        self.chase_text = (self.button_font.render("Chase", True, (255, 255, 255)))
        self.chase_text_rect = self.chase_text.get_rect()
        self.chase_text_rect.center = self.chase_rect.center

        self.bush_text = (self.title_font.render("Bush", True, (0, 0, 0)))
        self.bush_text_rect = self.bush_text.get_rect()
        self.bush_text_rect.centerx = 1550
        self.bush_text_rect.top = 10

        self.tree_text = (self.title_font.render("Tree", True, (0, 0, 0)))
        self.tree_text_rect = self.tree_text.get_rect()
        self.tree_text_rect.centerx = 1550
        self.tree_text_rect.top = 10

        self.shelter_text = (self.title_font.render("Shelter", True, (0, 0, 0)))
        self.shelter_text_rect = self.shelter_text.get_rect()
        self.shelter_text_rect.centerx = 1550
        self.shelter_text_rect.top = 10

        self.delete_rect = pygame.Rect((1350, 200), (200, 125))
        self.delete_text = (self.button_font.render("Delete", True, (255, 255, 255)))
        self.delete_text_rect = self.delete_text.get_rect()
        self.delete_text_rect.center = self.delete_rect.center

        self.increase_food_rect = pygame.Rect((1700, 200), (50, 50))
        self.increase_food_text = (self.button_font.render("+", True, (0,0,0)))
        self.increase_food_text_rect = self.increase_food_text.get_rect()
        self.increase_food_text_rect.center = (self.increase_food_rect.centerx, self.increase_food_rect.centery - 3)

        self.decrease_food_rect = pygame.Rect((1700, 275), (50, 50))
        self.decrease_food_text = (self.button_font.render("-", True, (0,0,0)))
        self.decrease_food_text_rect = self.decrease_food_text.get_rect()
        self.decrease_food_text_rect.center = (self.decrease_food_rect.centerx, self.decrease_food_rect.centery - 6)

        self.increase_wood_rect = pygame.Rect((1700, 200), (50, 50))
        self.increase_wood_text = (self.button_font.render("+", True, (0,0,0)))
        self.increase_wood_text_rect = self.increase_wood_text.get_rect()
        self.increase_wood_text_rect.center = (self.increase_wood_rect.centerx, self.increase_wood_rect.centery - 3)

        self.decrease_wood_rect = pygame.Rect((1700, 275), (50, 50))
        self.decrease_wood_text = (self.button_font.render("-", True, (0,0,0)))
        self.decrease_wood_text_rect = self.decrease_wood_text.get_rect()
        self.decrease_wood_text_rect.center = (self.decrease_wood_rect.centerx, self.decrease_wood_rect.centery - 6)

        self.increase_trait_rect = pygame.Rect((1450, 550), (50, 50))
        self.increase_trait_text = (self.button_font.render("+", True, (0,0,0)))
        self.increase_trait_text_rect = self.increase_trait_text.get_rect()
        self.increase_trait_text_rect.center = (self.increase_trait_rect.centerx, self.increase_trait_rect.centery - 3)

        self.decrease_trait_rect = pygame.Rect((1650, 550), (50, 50))
        self.decrease_trait_text = (self.button_font.render("-", True, (0,0,0)))
        self.decrease_trait_text_rect = self.decrease_trait_text.get_rect()
        self.decrease_trait_text_rect.center = (self.decrease_trait_rect.centerx, self.decrease_trait_rect.centery - 6)

        self.increase_temp_rect = pygame.Rect((1450, 550), (50, 50))
        self.increase_temp_text = (self.button_font.render("+", True, (0,0,0)))
        self.increase_temp_text_rect = self.increase_temp_text.get_rect()
        self.increase_temp_text_rect.center = (self.increase_temp_rect.centerx, self.increase_temp_rect.centery - 3)

        self.decrease_temp_rect = pygame.Rect((1650, 550), (50, 50))
        self.decrease_temp_text = (self.button_font.render("-", True, (0,0,0)))
        self.decrease_temp_text_rect = self.decrease_temp_text.get_rect()
        self.decrease_temp_text_rect.center = (self.decrease_temp_rect.centerx, self.decrease_temp_rect.centery - 3)

        self.pause_rect = pygame.Rect((1700, 658), (80, 80))
        self.pause_image = pygame.transform.scale(pygame.image.load("images/pause.png").convert_alpha(), (50, 70))
        self.play_image = pygame.transform.scale(pygame.image.load("images/play.png").convert_alpha(), (60, 60))

        self.graph_rect = pygame.Rect((1350, 658), (200, 80))

        self.stats_history = {
            "day": [],
            "number of creatures": [],
            "energy": [],
            "speed": [],
            "strength": [],
            "sight": [],
            "farming": [],
            "social": [],
            "temperature": []
        }

        self.stats_surface = None
        self.last_stats_day = -1

        self.average_energy = 0
        self.lowest_energy = 0
        self.highest_energy = 0

        self.num_of_days = main.num_of_days

        self.total_in_shelters = 0

    def display_text(self, text, value, y_pos):
        self.main.screen.blit((self.traits_font.render(text, True, (0, 0, 0))), (1310, y_pos))

        val = (self.traits_font.render(str(value), True, (0, 0, 0)))
        val_rect = val.get_rect()
        val_rect.right = self.main.WINDOW_WIDTH + 500 - 10
        val_rect.top = y_pos
        self.main.screen.blit(val, val_rect.topleft)

    def find_energies(self):
        self.energies = []
        for creature in self.main.creatures:
            self.energies.append(creature.energy)

        if self.energies:
            self.lowest_energy = min(self.energies)
            self.highest_energy = max(self.energies)
            self.average_energy = sum(self.energies) / len(self.energies)
        else:
            self.lowest_energy = 0
            self.highest_energy = 0
            self.average_energy = 0

    def time_days(self):
        if not self.main.paused:
            if self.main.day_timer <= 0:
                self.num_of_days += 1

    def record_stats(self):
        day = len(self.stats_history["day"]) + 1
        self.stats_history["day"].append(day)

        num_of_creatures = len(self.main.creatures)
        # No creatures
        if num_of_creatures == 0:
            for key in self.stats_history:
                if key != "day":
                    self.stats_history[key].append(0)
            return

        # Record average statistics
        for key in self.stats_history:
            if key == "number of creatures":
                self.stats_history[key].append(num_of_creatures)
            elif key != "day":
                average = sum(getattr(creature, key) for creature in self.main.creatures) / num_of_creatures
                self.stats_history[key].append(average)

    def build_stats_surface(self, width=500, height=750, dpi=100):
        fig, axes = plt.subplots(2, 1, figsize=(width / dpi, height / dpi), dpi=dpi, constrained_layout=True)

        axes[0].plot(self.stats_history["day"], self.stats_history["number of creatures"], label="Number of creatures")
        axes[0].plot(self.stats_history["day"], self.stats_history["energy"], label="Average energy")
        axes[0].set_xlabel("Day")
        axes[0].set_ylabel("Average value")
        axes[0].legend()
        axes[0].grid(True)

        trait_keys = [k for k in self.stats_history if k not in ("day", "number of creatures", "energy")]

        for key in trait_keys:
            axes[1].plot(
                self.stats_history["day"],
                self.stats_history[key],
                label=f"Average {key}"
            )

        axes[1].set_xlabel("Day")
        axes[1].set_ylabel("Average value")
        axes[1].set_ylim(0, 100)
        axes[1].legend(fontsize=8, ncol=2)
        axes[1].grid(True)

        buf = BytesIO()
        fig.canvas.print_png(buf)
        buf.seek(0)
        surface = pygame.image.load(buf).convert_alpha()
        buf.close()
        plt.close(fig)

        return pygame.transform.smoothscale(surface, (width, 650))

    def update(self):
        if self.creature_selected:
            # Update position of the delete rect
            self.delete_rect.topleft = (1350, 610)
            self.delete_text_rect.center = self.delete_rect.center
        
        elif self.bush_selected or self.tree_selected:
            # Update position of the delete rect
            self.delete_rect.topleft = (1350, 200)
            self.delete_text_rect.center = self.delete_rect.center

        elif self.shelter_selected:
            self.delete_rect.topleft = (1350, 250)
            self.delete_text_rect.center = self.delete_rect.center
            
        pygame.draw.rect(self.main.screen, "white", self.rect)

        self.time_days()

        if self.creature_selected:
            # Display text
            self.main.screen.blit(self.creature_text, self.creature_text_rect.topleft)

            self.display_text("Age:", self.creature_selected.age, 100)

            self.display_text("Energy:", int(self.creature_selected.energy), 150)
            self.display_text("Energy used per day:", int(self.creature_selected.energy_consumption), 200)

            self.display_text("Speed:", self.creature_selected.speed, 250)
            self.display_text("Strength:", self.creature_selected.strength, 300)
            self.display_text("Sight:", self.creature_selected.sight, 350)
            self.display_text("Farming:", self.creature_selected.farming, 400)
            self.display_text("Social:", self.creature_selected.social, 450)
            self.display_text("Ideal Temperature:", self.creature_selected.temperature, 500)
            self.display_text("Wood:", self.creature_selected.wood, 550)

            # Delete button
            pygame.draw.rect(self.main.screen, "red", self.delete_rect)
            self.main.screen.blit(self.delete_text, self.delete_text_rect)

            # Team button
            pygame.draw.rect(self.main.screen, pygame.Color(72, 154, 217), self.team_rect)
            self.main.screen.blit(self.team_text, self.team_text_rect)

            # Chase button
            pygame.draw.rect(self.main.screen, pygame.Color(72, 154, 217), self.chase_rect)
            self.main.screen.blit(self.chase_text, self.chase_text_rect)

            # Reset colours for creatures that are not of interest
            for creature in self.main.creatures:
                creature.colour = "light blue"

            # Highlight team
            if self.creature_selected.team:
                for creature in self.creature_selected.team:
                    creature.colour = "green"

            # Highlight creatures coming to socialise
            if self.creature_selected.team_member_coming[0]:
                self.creature_selected.team_member_coming[1].colour = "purple"

            # Highlight enemy that chasing
            if self.creature_selected.chasing_creature[0]:
                self.creature_selected.chasing_creature[1].colour = "yellow"

            # Display creature's destination
            self.cross_rect.center = (self.creature_selected.destination.x + 12, self.creature_selected.destination.y + 12)
            self.main.screen.blit(self.cross_image, self.cross_rect)

            # If simulation is paused
            if self.main.paused and self.trait_selected:
                pygame.draw.rect(self.main.screen, "light blue", self.increase_trait_rect)
                self.main.screen.blit(self.increase_trait_text, self.increase_trait_text_rect)
                pygame.draw.rect(self.main.screen, "light blue", self.decrease_trait_rect)
                self.main.screen.blit(self.decrease_trait_text, self.decrease_trait_text_rect)
        
        elif self.bush_selected:
            self.main.screen.blit(self.bush_text, self.bush_text_rect.topleft)

            self.display_text("Food:", self.bush_selected.resource, 100)
            pygame.draw.rect(self.main.screen, "red", self.delete_rect)
            self.main.screen.blit(self.delete_text, self.delete_text_rect)
            pygame.draw.rect(self.main.screen, "light blue", self.increase_food_rect)
            self.main.screen.blit(self.increase_food_text, self.increase_food_text_rect)
            pygame.draw.rect(self.main.screen, "light blue", self.decrease_food_rect)
            self.main.screen.blit(self.decrease_food_text, self.decrease_food_text_rect)
        
        elif self.tree_selected:
            self.main.screen.blit(self.tree_text, self.tree_text_rect.topleft)

            self.tree_selected.resource = self.tree_selected.resource if self.tree_selected.resource <= 100 else 100
            self.display_text("Wood:", self.tree_selected.resource * self.main.wood_yield, 100)
            pygame.draw.rect(self.main.screen, "red", self.delete_rect)
            self.main.screen.blit(self.delete_text, self.delete_text_rect)
            pygame.draw.rect(self.main.screen, "light blue", self.increase_wood_rect)
            self.main.screen.blit(self.increase_wood_text, self.increase_wood_text_rect)
            pygame.draw.rect(self.main.screen, "light blue", self.decrease_wood_rect)
            self.main.screen.blit(self.decrease_wood_text, self.decrease_wood_text_rect)
        
        elif self.shelter_selected:
            self.main.screen.blit(self.shelter_text, self.shelter_text_rect.topleft)

            self.display_text("Maximum capacity:", self.shelter_selected.max_creatures, 100)
            self.display_text("Number of creatures inside:", len(self.shelter_selected.current_creatures), 150)
            self.display_text("Internal temperature:", self.shelter_selected.internal_temp, 200)

            pygame.draw.rect(self.main.screen, "red", self.delete_rect)
            self.main.screen.blit(self.delete_text, self.delete_text_rect)

        else:
            self.main.screen.blit(self.title_text, self.title_text_rect.topleft)
            
            self.display_text("Number of creatures:", len(self.main.creatures), 100)
            self.find_energies()
            self.display_text("Lowest energy:", round(self.lowest_energy, 1), 150)
            self.display_text("Average energy:", round(self.average_energy, 1), 200)
            self.display_text("Highest energy:", round(self.highest_energy, 1), 250)
            self.display_text("Days passed:", self.num_of_days, 300)
            self.display_text("Number of creatures in shelters:", sum(len(shelter.current_creatures) for shelter in self.main.shelters), 350)
            self.display_text("Current temperature:", round(self.main.current_temp, 1), 400)
            self.display_text("Maximum temperature:", self.main.max_temperature, 450)
            self.display_text("Minimum temperature:", self.main.min_temperature, 500)

            if self.temp_selected:
                pygame.draw.rect(self.main.screen, "light blue", self.increase_temp_rect)
                self.main.screen.blit(self.increase_temp_text, self.increase_temp_text_rect)
                pygame.draw.rect(self.main.screen, "light blue", self.decrease_temp_rect)
                self.main.screen.blit(self.decrease_temp_text, self.decrease_temp_text_rect)

            pygame.draw.rect(self.main.screen, "light blue", self.pause_rect)
            if self.main.paused:
                self.main.screen.blit(self.pause_image, (1715, 663))     
            else:
                self.main.screen.blit(self.play_image, (1710, 668))  
        
        if not self.in_graphs and not self.creature_selected and not self.bush_selected and not self.tree_selected and not self.shelter_selected:
            self.graph_text = (self.button_font.render("Graphs", True, (0, 0, 0)))
            self.graph_text_rect = self.graph_text.get_rect()
            self.graph_text_rect.center = (self.graph_rect.centerx, self.graph_rect.centery)
            pygame.draw.rect(self.main.screen, "light blue", self.graph_rect)
            self.main.screen.blit(self.graph_text, self.graph_text_rect)
        
        elif not self.creature_selected and not self.bush_selected and not self.tree_selected and not self.shelter_selected:
            self.graph_text = (self.button_font.render("Back", True, (0, 0, 0)))
            self.graph_text_rect = self.graph_text.get_rect()
            self.graph_text_rect.center = (self.graph_rect.centerx, self.graph_rect.centery)
            pygame.draw.rect(self.main.screen, "light blue", self.graph_rect)
            self.main.screen.blit(self.graph_text, self.graph_text_rect)

    def creature_circle(self):
        if self.creature_selected:
            # Display circle around creature showing its sight
            pygame.draw.circle(self.main.screen, "light blue", self.creature_selected.rect.center, self.creature_selected.sight * 2 + 50)