import tkinter as tk
from glob import glob
from subprocess import Popen
from json import dump
from tkinter import messagebox
from random import normalvariate, randint

class MainMenu():
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Main Menu")
        self.root.geometry("1200x800")
        self.root.configure(background="light blue")
        self.frame = tk.Frame(self.root, bg="light blue")
        self.frame.pack(fill="both", expand=True)

        self.start_menu()

    def start_menu(self):
        for item in self.frame.winfo_children():
            item.destroy()

        label = tk.Label(self.frame, text="Main Menu", font=("Arial", 40), bg="light blue")
        label.pack()

        button = tk.Button(self.frame, text="Start Simulation", font=("Arial", 35), command=self.configure_settings)
        button.pack(pady=30)
        button.config(width=20, height=1)
        button.configure(background="#2a9aab")

        button = tk.Button(self.frame, text="Load Simulation", font=("Arial", 35), command=self.load_sim)
        button.pack(pady=30)
        button.config(width=20, height=1)
        button.configure(background="#2a9aab")

        button = tk.Button(self.frame, text="Info", font=("Arial", 35), command=self.info)
        button.pack(pady=30)
        button.config(width=20, height=1)
        button.configure(background="#2a9aab")

        button = tk.Button(self.frame, text="Quit", font=("Arial", 35), command=self.quit)
        button.pack(pady=30)
        button.config(width=20, height=1)
        button.configure(background="#2a9aab")

    def configure_settings(self):
        for item in self.frame.winfo_children():
            item.destroy()

        def go_back():
            for item in self.frame.winfo_children():
                item.destroy()
            self.start_menu()

        def store_to_json():
            # Check minimum and maximum temperatures are the right way round
            min_temp = self.min_temperature.get()
            max_temp = self.max_temperature.get()

            if min_temp > max_temp:
                messagebox.showerror("Error", "Minimum temperature is greater than the maximum temperature")
                return
            if max_temp < min_temp:
                messagebox.showerror("Error", "Maximum temperature is less than the minimum temperature")
                return

            # The first part of the creatures' array will be [energy, age, speed, strength, sight, farming, social, temperature, wood, posx, posy]

            num_of_creatures = self.num_of_creatures.get()
            starting_energy = self.amount_of_energy.get()
            energy_variation = self.energy_variation.get()
            speed = self.speed.get()
            speed_variation = self.speed_variation.get()
            strength = self.strength.get()
            strength_variation = self.strength_variation.get()
            sight = self.sight.get()
            sight_variation = self.sight_variation.get()
            farming = self.farming.get()
            farming_variation = self.farming_variation.get()
            social = self.social.get()
            social_variation = self.social_variation.get()
            temperature = self.temperature.get()
            temperature_variation = self.temperature_variation.get()
            wood = 0

            data = {}

            data["Creatures"] = []

            for creature in range(0, num_of_creatures):
                data["Creatures"].append([f"Creature{creature}", 
                                          max(min(max(round(normalvariate(starting_energy, energy_variation/2)), starting_energy - energy_variation), starting_energy + energy_variation), 0), 
                                          0, 
                                          max(min(max(min(round(normalvariate(speed, speed_variation/2)), speed + speed_variation), speed - speed_variation), 100), 0), 
                                          max(min(max(min(round(normalvariate(strength, strength_variation/2)), strength + strength_variation), strength - strength_variation), 100), 0), 
                                          max(min(max(min(round(normalvariate(sight, sight_variation/2)), sight + sight_variation), sight - sight_variation), 100), 0), 
                                          max(min(max(min(round(normalvariate(farming, farming_variation/2)), farming + farming_variation), farming - farming_variation), 100), 0), 
                                          max(min(max(min(round(normalvariate(social, social_variation/2)), social + social_variation), social - social_variation), 100), 0), 
                                          max(min(max(min(round(normalvariate(temperature, temperature_variation/2)), temperature + temperature_variation), temperature - temperature_variation), 100), 0), 
                                          wood,
                                          randint(0, 1299) // 50 * 50,
                                          randint(0, 749) // 50 * 50,
                                          [],
                                          [False, None],
                                          [False, None],
                                          [False, None],
                                          [False, None],
                                          [False, None],
                                          [False, None],
                                          [False, None]])
                
            # Bush array will be [pos, growth_rate, dying_probability, resource]
            data["Bushes"] = []
            for bush in range(0, self.amount_of_bushes.get()):
                data["Bushes"].append([f"Bush{bush}",
                                       randint(0, 1299) // 50 * 50,
                                       randint(0, 749) // 50 * 50,
                                       self.food_growth_rate.get(),
                                       0.02,
                                       0])

            # Tree array will be [pos, growth_rate, dying_probability, resource]
            data["Trees"] = []
            for tree in range(0, self.amount_of_trees.get()):
                data["Trees"].append([f"Tree{tree}",
                                      randint(0, 1299) // 50 * 50,
                                      randint(0, 749) // 50 * 50,
                                      self.trees_growth_rate.get(),
                                      0.02,
                                      0])
                
            # Shelters, initially none
            data["Shelters"] = []

            # Simulation settings
            data["Dying age"] = self.dying_age.get()
            data["Energy from food"] = self.energy_from_food.get()
            data["Wood yield"] = self.wood_yield.get()
            data["Min temperature"] = min_temp
            data["Max temperature"] = max_temp
            data["Current temperature"] = (min_temp + max_temp) / 2
            data["Season"] = "summer"
            data["Season length"] = self.season_length.get()
            data["Days passed"] = 0

            # Store to JSON file
            try:
                with open(f"sims/{self.name_of_sim.get()}.json", "w") as file:
                    dump(data, file)
                Popen(["python", "main.py", f"{self.name_of_sim.get()}.json"])
                self.root.destroy()
            except:
                messagebox.showerror("Error", "Invalid name for Simulation. Enter a name without special characters")
        
        # Setup for Scrollbar on side

        container = tk.Frame(self.frame, bg="light blue")
        container.pack(fill="both", expand=True)

        canvas = tk.Canvas(container, bg="light blue", highlightthickness=0)
        scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        self.scrollable_frame = tk.Frame(canvas, bg="light blue")
        window_id = canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        def _on_canvas_configure(event):
            canvas.itemconfig(window_id, width=event.width)
        canvas.bind("<Configure>", _on_canvas_configure)

        def _on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        self.scrollable_frame.bind("<Configure>", _on_frame_configure)

        def create_label(frame, text, font_size, side):
            label = tk.Label(frame, text=text, font=("Arial", font_size), bg="light blue")
            if side != None:
                return label.pack(side=side)
            else:
                return label.pack()
            
        def create_horizontal_frame():
            horizontal_frame = tk.Frame(self.scrollable_frame, bg="light blue")
            horizontal_frame.pack()
            return horizontal_frame

        # Visual elements

        label = tk.Label(self.scrollable_frame, text="Configure Simulation", font=("Arial", 40))
        label.pack(pady=10)
        label.configure(background="light blue")

        # Frame for number of creatures
        horizontal_frame_creatures = create_horizontal_frame()

        # Number of Creatures label and slider
        create_label(horizontal_frame_creatures, "Number of Creatures", 30, "left")

        self.num_of_creatures = tk.Scale(horizontal_frame_creatures, from_=1, to=100, length=300, orient="horizontal", background="#2a9aab", font=("Arial", 30), sliderlength=50)
        self.num_of_creatures.pack(pady=15, padx=10)
        self.num_of_creatures.set(50)

        # Frame for starting energy
        horizontal_frame = create_horizontal_frame()
        horizontal_frame.pack(pady=10)

        # Starting Energy label and slider
        create_label(horizontal_frame, "Starting energy", 30, "left")

        self.amount_of_energy = tk.Scale(horizontal_frame, from_=50, to=500, length=600, orient="horizontal", background="#2a9aab", font=("Arial", 30), sliderlength=40)
        self.amount_of_energy.pack(padx=30, pady=15, side="left")
        self.amount_of_energy.set(250)

        # Starting energy variation
        horizontal_frame = create_horizontal_frame()
        horizontal_frame.pack(pady=10)

        create_label(horizontal_frame, "±", 30, "left")

        self.energy_variation = tk.Scale(horizontal_frame, from_=0, to=500, length=600, orient="horizontal", background="#2a9aab", font=("Arial", 30), sliderlength=40)
        self.energy_variation.pack(padx=30, pady=15, side="left")
        self.energy_variation.set(0)

        # Dying Age
        horizontal_frame = create_horizontal_frame()
        horizontal_frame.pack(pady=10)

        create_label(horizontal_frame, "Dying age", 30, "left")

        self.dying_age = tk.Scale(horizontal_frame, from_=1, to=50, length=300, orient="horizontal", background="#2a9aab", font=("Arial", 30), sliderlength=40)
        self.dying_age.pack(pady=20, padx=30, side="left")
        self.dying_age.set(25)

        # Traits (Speed, Strength, Sight, Farming, Social, Temperature)
        create_label(self.scrollable_frame, "Starting Traits", 22, None)

        horizontal_frame = create_horizontal_frame()
        create_label(horizontal_frame, "Speed", 20, "left")
        self.speed = tk.Scale(horizontal_frame, from_=1, to=100, length=400, orient="horizontal", background="#2a9aab", font=("Arial", 30), sliderlength=40)
        self.speed.pack(pady=20, padx=30, side="left")
        self.speed.set(50)

        # Starting speed variation
        horizontal_frame = create_horizontal_frame()
        horizontal_frame.pack(pady=10)

        create_label(horizontal_frame, "±", 30, "left")

        self.speed_variation = tk.Scale(horizontal_frame, from_=0, to=50, length=400, orient="horizontal", background="#2a9aab", font=("Arial", 30), sliderlength=40)
        self.speed_variation.pack(padx=30, pady=20, side="left")
        self.speed_variation.set(0)

        horizontal_frame = create_horizontal_frame()
        create_label(horizontal_frame, "Strength", 20, "left")
        self.strength = tk.Scale(horizontal_frame, from_=1, to=100, length=400, orient="horizontal", background="#2a9aab", font=("Arial", 30), sliderlength=40)
        self.strength.pack(pady=20, padx=30, side="left")
        self.strength.set(50)

        # Starting strength variation
        horizontal_frame = create_horizontal_frame()
        horizontal_frame.pack(pady=10)

        create_label(horizontal_frame, "±", 30, "left")

        self.strength_variation = tk.Scale(horizontal_frame, from_=0, to=50, length=400, orient="horizontal", background="#2a9aab", font=("Arial", 30), sliderlength=40)
        self.strength_variation.pack(padx=30, pady=20, side="left")
        self.strength_variation.set(0)

        horizontal_frame = create_horizontal_frame()
        create_label(horizontal_frame, "Sight", 20, "left")
        self.sight = tk.Scale(horizontal_frame, from_=1, to=100, length=400, orient="horizontal", background="#2a9aab", font=("Arial", 30), sliderlength=40)
        self.sight.pack(pady=20, padx=30, side="left")
        self.sight.set(50)

        # Starting sight variation
        horizontal_frame = create_horizontal_frame()
        horizontal_frame.pack(pady=10)

        create_label(horizontal_frame, "±", 30, "left")

        self.sight_variation = tk.Scale(horizontal_frame, from_=0, to=50, length=400, orient="horizontal", background="#2a9aab", font=("Arial", 30), sliderlength=40)
        self.sight_variation.pack(padx=30, pady=20, side="left")
        self.sight_variation.set(0)

        horizontal_frame = create_horizontal_frame()
        create_label(horizontal_frame, "Farming", 20, "left")
        self.farming = tk.Scale(horizontal_frame, from_=1, to=100, length=400, orient="horizontal", background="#2a9aab", font=("Arial", 30), sliderlength=40)
        self.farming.pack(pady=20, padx=30, side="left")
        self.farming.set(50)

        # Starting farming variation
        horizontal_frame = create_horizontal_frame()
        horizontal_frame.pack(pady=10)

        create_label(horizontal_frame, "±", 30, "left")

        self.farming_variation = tk.Scale(horizontal_frame, from_=0, to=50, length=400, orient="horizontal", background="#2a9aab", font=("Arial", 30), sliderlength=40)
        self.farming_variation.pack(padx=30, pady=20, side="left")
        self.farming_variation.set(0)

        horizontal_frame = create_horizontal_frame()
        create_label(horizontal_frame, "Social", 20, "left")
        self.social = tk.Scale(horizontal_frame, from_=1, to=100, length=400, orient="horizontal", background="#2a9aab", font=("Arial", 30), sliderlength=40)
        self.social.pack(pady=20, padx=30, side="left")
        self.social.set(50)

        # Starting social variation
        horizontal_frame = create_horizontal_frame()
        horizontal_frame.pack(pady=10)

        create_label(horizontal_frame, "±", 30, "left")

        self.social_variation = tk.Scale(horizontal_frame, from_=0, to=50, length=400, orient="horizontal", background="#2a9aab", font=("Arial", 30), sliderlength=40)
        self.social_variation.pack(padx=30, pady=20, side="left")
        self.social_variation.set(0)

        horizontal_frame = create_horizontal_frame()
        create_label(horizontal_frame, "Ideal Temperature", 20, "left")
        self.temperature = tk.Scale(horizontal_frame, from_=1, to=100, length=400, orient="horizontal", background="#2a9aab", font=("Arial", 30), sliderlength=40)
        self.temperature.pack(pady=20, padx=30, side="left")
        self.temperature.set(50)

        # Starting temperature variation
        horizontal_frame = create_horizontal_frame()
        horizontal_frame.pack(pady=10)

        create_label(horizontal_frame, "±", 30, "left")

        self.temperature_variation = tk.Scale(horizontal_frame, from_=0, to=50, length=400, orient="horizontal", background="#2a9aab", font=("Arial", 30), sliderlength=40)
        self.temperature_variation.pack(padx=30, pady=20, side="left")
        self.temperature_variation.set(0)

        # Amount of Bushes
        horizontal_frame = create_horizontal_frame()
        create_label(horizontal_frame, "Amount of Bushes", 20, "left")
        self.amount_of_bushes = tk.Scale(horizontal_frame, from_=1, to=50, length=300, orient="horizontal", background="#2a9aab", font=("Arial", 30), sliderlength=50)
        self.amount_of_bushes.pack(pady=15, padx=10)
        self.amount_of_bushes.set(25)

        # Rate of food growth
        horizontal_frame = create_horizontal_frame()
        create_label(horizontal_frame, "Amount of food grown per day", 20, "left")
        self.food_growth_rate = tk.Scale(horizontal_frame, from_=0, to=5, length = 300, orient="horizontal", background="#2a9aab", font=("Arial", 30), sliderlength=50, resolution=0.1)
        self.food_growth_rate.pack(pady=15, padx=10)
        self.food_growth_rate.set(5)

        # Amount of energy restored by food
        horizontal_frame = create_horizontal_frame()
        create_label(horizontal_frame, "Energy restored from food", 20, "left")
        self.energy_from_food = tk.Scale(horizontal_frame, from_=1, to=100, length=600, orient="horizontal", background="#2a9aab", font=("Arial", 30), sliderlength=50)
        self.energy_from_food.pack(pady=15, padx=10)
        self.energy_from_food.set(500)

        # Trees (wood yield, growth rate, amount)
        horizontal_frame = create_horizontal_frame()
        create_label(horizontal_frame, "Amount of trees", 20, "left")
        self.amount_of_trees = tk.Scale(horizontal_frame, from_=0, to=50, length=300, orient="horizontal", background="#2a9aab", font=("Arial", 30), sliderlength=50)
        self.amount_of_trees.pack(pady=15, padx=10)
        self.amount_of_trees.set(25)

        horizontal_frame = create_horizontal_frame()
        create_label(horizontal_frame, "Growth rate of trees", 20, "left")
        self.trees_growth_rate = tk.Scale(horizontal_frame, from_=0, to=1, length=300, orient="horizontal", background="#2a9aab", font=("Arial", 30), sliderlength=50, resolution=0.1)
        self.trees_growth_rate.pack(pady=15, padx=10)
        self.trees_growth_rate.set(25)

        horizontal_frame = create_horizontal_frame()
        create_label(horizontal_frame, "Wood yield", 20, "left")
        self.wood_yield = tk.Scale(horizontal_frame, from_=0, to=1, length=300, orient="horizontal", background="#2a9aab", font=("Arial", 30), sliderlength=50, resolution=0.1)
        self.wood_yield.pack(pady=15, padx=10)
        self.wood_yield.set(25)

        # Temperature range
        horizontal_frame = create_horizontal_frame()
        create_label(horizontal_frame, "Minimum Temperature", 20, "left")
        self.min_temperature = tk.Scale(horizontal_frame, from_=0, to=100, length=300, orient="horizontal", background="#2a9aab", font=("Arial", 30), sliderlength=50)
        self.min_temperature.pack(pady=15, padx=10)
        self.min_temperature.set(50)

        horizontal_frame = create_horizontal_frame()
        create_label(horizontal_frame, "Maximum Temperature", 20, "left")
        self.max_temperature = tk.Scale(horizontal_frame, from_=0, to=100, length=300, orient="horizontal", background="#2a9aab", font=("Arial", 30), sliderlength=50)
        self.max_temperature.pack(pady=15, padx=10)
        self.max_temperature.set(50)

        # Length of seasons
        horizontal_frame = create_horizontal_frame()
        create_label(horizontal_frame, "Length of seasons", 20, "left")
        self.season_length = tk.Scale(horizontal_frame, from_=0, to=50, length=300, orient="horizontal", background="#2a9aab", font=("Arial", 30), sliderlength=50)
        self.season_length.pack(pady=15, padx=10)
        self.season_length.set(10)

        # Name of the file of the simulation
        horizontal_frame = create_horizontal_frame()
        create_label(horizontal_frame, "Name of Simulation", 20, "left")
        self.name_of_sim = tk.Entry(horizontal_frame, bg="white", width=15, borderwidth=2, font=("Arial", 20))
        self.name_of_sim.pack(pady=10)

        horizontal_frame = tk.Frame(self.frame, bg="light blue")
        horizontal_frame.pack()

        # Button to start the simulation
        button = tk.Button(horizontal_frame, text="Save and Start Simulation", font=("Arial", 20), command=store_to_json)
        button.pack(side="left", padx=20, pady=20)
        button.config(width=20, height=1)
        button.configure(background="#2a9aab")

        # Button to go back to start menu
        button = tk.Button(horizontal_frame, text="Back", font=("Arial", 20), command=go_back)
        button.pack(side="left", padx=60, pady=20)
        button.config(width=10, height=1)
        button.configure(background="#2a9aab")
    
    def load_sim(self):
        def go_back():
            for item in self.frame.winfo_children():
                item.destroy()
            self.start_menu()

        for item in self.frame.winfo_children():
            item.destroy()

        # Load the JSON file
        def load_sim():
            try:
                Popen(["python", "main.py", f"{selected_value.get()}.json"])
                self.root.destroy()
            except:
                messagebox.showerror("Error", "Cannot find file")

        # Get all the JSON files
        directory = "sims"
        json_files = glob(f"{directory}/*.json") + glob(f"{directory}/.json")

        # Display the names of the simulations as an OptionMenu
        file_names = []
        for file in json_files:
            file_names.append(file[5:-5])

        if file_names:
        
            label = tk.Label(self.frame, text="Select Simulation", font=("Arial", 40), bg="light blue")
            label.pack(pady=10)

            selected_value = tk.StringVar(value=file_names[0])

            dropdown = tk.OptionMenu(self.frame, selected_value, *file_names)
            dropdown.config(width=15, height=2, font=("Arial", 25))
            dropdown.pack(pady=30)

            options = dropdown["menu"]
            options.config(font=["Arial", 20])

            # Start simulation button
            button = tk.Button(self.frame, text="Continue Simulation", font=("Arial", 20), command=load_sim)
            button.pack()
            button.config(width=20, height=1)
            button.configure(background="#2a9aab")

            # Button to go back to start menu
            button = tk.Button(self.frame, text="Back", font=("Arial", 20), command=go_back)
            button.pack(pady=50)
            button.config(width=10, height=1)
            button.configure(background="#2a9aab")
        
        else:
            label = tk.Label(self.frame, text="No Simulation found", font=("Arial", 40), bg="light blue")
            label.pack(pady=10)

            # Button to go back to start menu
            button = tk.Button(self.frame, text="Back", font=("Arial", 40), command=go_back)
            button.pack(pady=20)
            button.config(width=15, height=2)
            button.configure(background="#2a9aab")

    def info(self):
        def go_back():
            for item in self.frame.winfo_children():
                item.destroy()
            self.start_menu()

        for item in self.frame.winfo_children():
            item.destroy()

        # Setup for Scrollbar on side

        container = tk.Frame(self.frame, bg="light blue")
        container.pack(fill="both", expand=True)

        canvas = tk.Canvas(container, bg="light blue", highlightthickness=0)
        scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        self.scrollable_frame = tk.Frame(canvas, bg="light blue")
        window_id = canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        def _on_canvas_configure(event):
            canvas.itemconfig(window_id, width=event.width)
        canvas.bind("<Configure>", _on_canvas_configure)

        def _on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        self.scrollable_frame.bind("<Configure>", _on_frame_configure)

        def create_label(text, font_size, padding):
            label = tk.Label(self.scrollable_frame, text=text, font=("Arial", font_size), bg="light blue", wraplength=1000)
            label.pack(pady=padding)

        create_label("Key Info", 40, 10)
        create_label("Natural Selection - the idea relating to evolution where organisms better adapted to their environment tend to survive and reproduce", 20, 10)
        create_label("Evolution - the process by which organisms are transformed to different forms by changes over successive generations", 20, 10)
        create_label("Traits - distinguishing characteristics of an organism genetically determined", 20, 10)
        create_label("Mutation - the action or process of changing in form or nature", 20, 10)
        create_label("How the simulation works", 40, 10)
        create_label("Creatures in the simulation move around and decide what actions to carry out. At the end of everyday, they use up energy depending on their traits", 20, 10)
        create_label("In the simulation, click a creature to see all their traits", 20, 10)
        create_label("Clicking a creature reveals their sight range as a circle, and changes the colour of other creatures depending on how they're interacting", 20, 10)
        create_label("Green - in a team", 20, 5)
        create_label("Yellow - chasing that creature", 20, 5)
        create_label("Purple - coming to either get food or reproduce", 20, 5)
        create_label("While the simulation is paused, clicking a creature's trait will reveal the option of increasing or decreasing its value", 20, 10)
        create_label("Clicking a bush or a tree will also allow you to increase the amount of food/wood it has", 20, 10)
        create_label("Creatures are also able to get wood to build shelters, the more wood they use the bigger the shelter", 20, 10)
        create_label("Shelters provide a place where the creatures can stay at to be at a good temperature, as the bigger the difference between the environment temperature and the creature's ideal temperature, the more energy they will use", 20, 10)
        create_label("Creatures have the choice to socialise with other creatures, this could be making friends or getting food from them. Their social trait will determine how frequently this happens", 20, 10)
        create_label("They are also able to attack other creatures and kill them, gaining all their energy. Creatures will only go after other ones with a lower strength trait", 20, 10)
        create_label("Clicking the graphs button will bring up 2 graphs showing over time the average energy, number of creatures, and the average of all the traits", 20, 10)
        create_label('"Pixel Art Bush" by ManicPixelDreamGirl, available at https://manicpixeldreamgirl.itch.io/pixelartbush, is licensed under CC BY-ND 4.0.', 20, 10)

        # Button to go back to start menu
        button = tk.Button(self.frame, text="Back", font=("Arial", 40), command=go_back)
        button.pack(pady=20)
        button.config(width=10, height=1)
        button.configure(background="#2a9aab")

    def quit(self):
        self.root.destroy()

menu = MainMenu()
menu.root.mainloop()