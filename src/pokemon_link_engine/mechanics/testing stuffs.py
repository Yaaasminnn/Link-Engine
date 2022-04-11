from utils.json_utils import load_json, update_json
from exp_formulas import *
import random
#from main import user, user_home, game_dir
from utils.directories import get_project_dir
get_project_dir()
user_home = "./users/loona"

def load_pokemon_database():
    return load_json("mechanics/pokedex.json")

class Pokemon:

    class Nature:
        def __init__(self, nature):
            """
            This class is used to generate a nature when a pokemon is created.

            Here, we store the nature's name and stat mods(atk, def, spatk, spdef, speed)
            """
            natures = load_json("mechanics/natures.json")
            nat_info = self.calc_nature_data(nature, natures)
            self.name = nat_info[0]
            self.attack = nat_info[1]
            self.defence = nat_info[2]
            self.sp_attack = nat_info[3]
            self.sp_defence = nat_info[4]
            self.speed = nat_info[5]

        def choose_nature(self, natures):
            """
            will randomly select a nature from the natures json. then it returns the name of the nature.

            we only choose the name because a nature can be manually inputted in the Pokemon class as the nature name.
            this is to keep parity.
            """
            chosen_nature = random.choice(list(natures))
            return chosen_nature

        def calc_nature_data(self, nature, natures):
            """
            Takes the nature name and determines all the data/stat mods for the nature.

            Includes all the base stats.

            Example:
                >>> Pokemon.Nature.calc_nature_data() #generates a random nature, in this case the serious nature
                ["Serious", 0,0,0,0,0]

                >>> Pokemon.Nature.calc_nature_data("Bashful") #a manually inserted nature
                ["Bashful", 0,0,0,0,0]
            """
            nat_info = []

            if nature is None: nature = self.choose_nature(natures)
            nat_info.append(nature)
            nature = natures[nature]

            stat_mods = nature["Stat Mods"]
            nat_atk_mod = stat_mods["Attack Mod"]; nat_info.append(nat_atk_mod)
            nat_def_mod = stat_mods["Defence Mod"]; nat_info.append(nat_def_mod)
            nat_spatk_mod = stat_mods["Special Attack Mod"]; nat_info.append(nat_spatk_mod)
            nat_spdef_mod = stat_mods["Special Defence Mod"]; nat_info.append(nat_spdef_mod)
            nat_speed_mod = stat_mods["Speed Mod"]; nat_info.append(nat_speed_mod)

            return nat_info

    class EV:
        def __init__(self, EV:list[int]):
            """
            This class is used to determine a pokemon's EV's
            """
            self.evs = self.gen_EV(EV)
            self.hp = self.evs[0]
            self.attack = self.evs[1]
            self.defence = self.evs[2]
            self.sp_attack = self.evs[3]
            self.sp_defence = self.evs[4]
            self.speed = self.evs[5]

        def gen_EV(self, EV:list[int]):
            """
            Generates Effort Values.

            First it validiates the manually given EV's, if any. to do so, it iterates through the list.
            if one of the values are negative or above 252, it is marked as invalid. we also keep track of the sum
            of EV's. if that sum is not within 0-510 or have a length of 6, it is marked as invalid.

            If it is invalid or None, we assign all of it's EV's as 0. otherwise, if EV's were given and they are valid,
            we use those

            Example:
                >>>Pokemon.EV.gen_EV([-5,0,0,0,0,0]) # invalid because one of the numbers were out of range
                [0,0,0,0,0,0]

                >>>Pokemon.EV.gen_EV([5]) # invalid because the length is not 6
                [0,0,0,0,0,0]

                >>>Pokemon.EV.gen_EV([4,0,252,0,252,0]) # valid
                [4,0,252,0,252,0]
            """

            if EV is not None:
                sum = 0
                for ev in EV:
                    if ev <0 or ev >252: return [0,0,0,0,0,0]
                    sum+=ev

                if sum <0 or sum > 510 or len(EV)!=6: return [0,0,0,0,0,0]
                return EV

            return [0,0,0,0,0,0]

    class IV:
        def __init__(self, IV:list[int]):
            """
            This class is used to determine a pokemon's EV's
            """
            self.ivs = self.gen_IV(IV)
            self.hp = self.ivs[0]
            self.attack = self.ivs[1]
            self.defence = self.ivs[2]
            self.sp_attack = self.ivs[3]
            self.sp_defence = self.ivs[4]
            self.speed = self.ivs[5]
            self.sum = self.find_sum(self.ivs)

        def gen_IV(self, IV:list[int]):
            """
            Generates Individual Values.

            This works similarly to EV's

            First it validiates the manually given IV's, if any. to do so, it iterates through the list.
            if one of the values are negative or above 31, it is marked as invalid.
            if the IV list does not have a length of 6, it is marked as invalid.

            If it is invalid or None, we randomly assign all IV's. otherwise, if IV's were given and they are valid,
            we use those

            Example:
                >>>Pokemon.IV.gen_IV([-5,0,0,0,0,0]) # invalid because one of the numbers were out of range
                [rand, rand, rand, rand, rand, rand]

                >>>Pokemon.IV.gen_IV([5]) # invalid because the length is not 6
                [rand, rand, rand, rand, rand, rand]

                >>>Pokemon.IV.gen_IV([13,5,27,30,31,8]) # valid
                [13,5,27,30,31,8]
            """

            valid = True
            if IV is not None:
                if len(IV) != 6: valid = False
                else:
                    for iv in IV:
                        if iv < 0 or iv > 31: valid = False; break

            if IV is None or not valid:
                IV = []
                for iv in range(0,6):
                    iv = random.randint(0,31)
                    IV.append(iv)
            return IV

        def find_sum(self, ivs):
            """
            Determines sum of all iv's added up.

            This can be helpful for determining if the IV's are maxed out.
            """
            sum = 0
            for iv in ivs:
                sum+=iv
            return sum

    class Moves:
        def __init__(self, moveset, moves, level):
            self.moves=[]
            self.determine_moves(moves, moveset, level)

        def determine_moves(self, moves, moveset, level):
            if moves is not None and len(moves) <= 4: self.moves = moves; return #if the given moves are valid, use them

            #otherwise, generate them based on moves by level
            for move in moveset:
                req_lvl = moveset[move]["Level"] # the required level

                # if you have reached the qualified level, then it adds it onto the moves array. max of 4 moves allowed
                if level < req_lvl: break
                name = moveset[move]["Name"]
                if len(self.moves) == 4:
                    self.moves.pop(0)
                self.moves.append(name)

        def add_new_move(self, move):
            """
            adds a new move on.

            todo:
                if the length is equal to 4, we ask the user if they want to remove a move
            """
            if len(self.moves)==4:
                removed = int(input(f"Pokemon would like to learn {move}! \n"
                                    f"What move would you like to remove? select 1-4 for move choice or 0 to not learn it\n"
                                    f"{self.moves}"))
                if removed ==0: return
                self.moves[removed-1] = move
                return

            self.moves.append(move)

    def __init__(self,
                 species:int, level:int, exp:int=None, nickname:str=None, gender:str=None, id:int=0,
                 EV:list[int]=None, IV:list[int]=None, nature=None, friendship:int=0, status_code:int=0,
                 current_hp:int=None, moves:list[str]=None, item:str=None,
                 og_trainer:str=None, date_caught:str=None, catch_location:str=None,
                 has_pokerus:bool=None, shiny:bool=None):
        """
        Creates an instance of a pokemon.
        this can be used to generate any pokemon, whether its wild, predetermined or an existing pokemon

        caught poke's have an id from 10k-99999
        wild pkmn have an id from 1000-9999     maybe determines shiny n stuff?
        foe teams may have an id from 100-999
        make an id generator method

        todo:
            natures, moves, ev's and iv's may need to be un-selfed or have a value it returns somehow. prob not
            work on shinies/pokerus
            variable that holds what form the pokemon is so we know what stats or sprites to use
        """

        pkmn_db = load_json("mechanics/pokedex.json") #loads in all the pokemon in the database
        self.species = pkmn_db[str(species)] #loads in all the data on the species

        # sets the basic info
        self.name = self.set_name(species=self.species["Name"], nickname=nickname)
        self.level = level
        self.set_exp(exp)
        self.nature = Pokemon.Nature(nature)
        self.EV = Pokemon.EV(EV)
        self.IV = Pokemon.IV(IV)
        self.gender = self.determine_gender(gender)
        self.status_code = status_code
        self.pokerus = self.has_pokerus(has_pokerus)
        self.shiny = self.is_shiny(shiny)
        self.stat_stages = [0,0,0,0,0]
        self.calc_current_hp(current_hp) # work on this
        self.Moves = Pokemon.Moves(self.species["Moveset"], moves, self.level) # maybe set moves to ID's as well
        self.item = item
        self.catch_location = catch_location
        self.form = None
        self.variety = None

        # id, friendship, og Trainer(OT) and the date caught. none are applicable to wild pokemon
        self.id = id
        self.OT = og_trainer
        self.date_caught = date_caught
        self.friendship = friendship

    def determine_gender(self, gender):
        """
        determines the gender of the pokemon.

        reads the "gender ratio" key in the species data. the value is the ratio of the pokemon being male.
        if it is 0 or 100, we set the gender accordingly. if not, we roll a random float and if it passes the ratio,
        it is a female, if not, it is male.
        """
        if gender == "male" or gender == "female": return gender
        male_ratio = self.species["gender ratio"]
        rand_float = random.uniform(0.0, 100.0)
        if rand_float <= male_ratio: return "male"
        else: return "female"

    def set_name(self, species, nickname):
        """
        sets the pokemon's name. if it has a nickname, we set that as its name, otherwise it is given its species name.

        could be reused as the change nickname function
        """
        if nickname is None: return species
        return nickname

    def is_shiny(self, shiny:bool):
        if shiny: return True
        #otherwise determine by chance

    def has_pokerus(self, pokerus:bool):
        if pokerus: return True
        #otherwise determine by chance

    @property
    def status_condition(self):
        """
        Determines the status condition based on the given status code ranged from [0,6] inclusively.

        we use codes to easily select a status condition opposed to typing out the wrong string accidentally.
        additionally, its easier, simpler and more intuitive to correct those codes than if they were strings.
        """
        if self.status_code >6 or self.status_code <0: self.status_code = 0

        if self.status_code == 0: return "Healthy"
        elif self.status_code == 1: return "Paralyzed"
        elif self.status_code == 2: return "Burned"
        elif self.status_code == 3: return "Frozen"
        elif self.status_code == 4: return "Poisoned"
        elif self.status_code == 5: return "Asleep"
        elif self.status_code == 6: return "Fainted"

    @property
    def types(self):
        """
        Determines the pokemon's types based on its species
        """
        types = self.species["Types"]
        return types

    @property
    def stat_mods(self):
        """
        Sets the stat modifications based on self.stat_stages

        Sets the statmods as stages ranging from [-6,6] inclusively. we then run a lookup table to determine the value
        of those stat mods

        todo:
            move statmods to battle
            have a checker when moves are used that checks if the stat mods are out of range
        """
        stat_mods =[]
        for stage in self.stat_stages:
            if stage >6: stage =6
            if stage <-6: stage =-6
            if stage >=0: stat_mods.append((0.5*abs(int(stage)))+1)
            elif stage <0: stat_mods.append(1/((0.5*abs(int(stage)))+1))
        return stat_mods

    @property
    def base_stats(self):
        """
        Determines the pokemon's base stats.

        retrieves the base stats from the pokemon's species index in pokedex.json.
        """
        base_stats = self.species["Base Stats"]

        return [base_stats["Hit Points"], base_stats["Attack"], base_stats["Defence"],
                base_stats["Special Attack"], base_stats["Special Defence"], base_stats["Speed"]]

    @base_stats.setter
    def base_stats(self, stats: list[int] = (None, None, None, None, None, None)):
        """
        Modifies the base stats individually.
        """
        for i, stat in enumerate(stats):
            if stat is None or stat < 1: continue
            self.base_stats[i] = stat

    @property
    def stats(self):
        """
        returns the stats of the pokemon.

        Calculates the stats of a pokemon based on its IV's, EV's, level and base stats.
        todo:
            allow for stat mods that are default 1 but can be modified and recalculated per turn?
        """
        hp = int(((((2*self.base_stats[0]) + self.IV.hp + (self.EV.hp/4)) * self.level)/100) + self.level + 10)
        attack = int(self.stat_mods[0]*((((((2*self.base_stats[1]) + self.IV.attack + (self.EV.attack/4)) * self.level)/100) + 5) * self.nature.attack))
        defence = int(self.stat_mods[1]*((((((2 * self.base_stats[2]) + self.IV.defence + (self.EV.defence / 4)) * self.level)/100) + 5) * self.nature.defence))
        sp_attack = int(self.stat_mods[2]*((((((2 * self.base_stats[3]) + self.IV.sp_attack + (self.EV.sp_attack / 4)) * self.level)/100) + 5) * self.nature.sp_attack))
        sp_defence = int(self.stat_mods[3]*((((((2 * self.base_stats[4]) + self.IV.sp_defence + (self.EV.sp_defence / 4)) * self.level)/100) + 5) * self.nature.sp_defence))
        speed = int(self.stat_mods[4]*((((((2 * self.base_stats[5]) + self.IV.speed + (self.EV.speed / 4)) * self.level)/100) + 5) * self.nature.speed))
        return [hp, attack, defence, sp_attack, sp_defence, speed]

    @stats.setter
    def stats(self, stats:list[int]=(None, None, None, None, None, None)):
        """
        Modifies the stats individually

        issue: since stats calculates the stats everytime it updates, this method wont work especially since each stat
        is not its own attribute.  fixable by making them attributes, but we dont need to manually change the stats
        """
        for i, stat in enumerate(stats):
            if stat is None or stat <1: continue
            self.stats[i] = stat

    def evolve(self, num=None):
        """
        Evolves a pokemon into another.

        By default it checks the pokemon's level and its species entry in the pokedex to see which pokemon
        to evolve into. only does so if you meet the level requirements. If a pokemon is given mnaually by num, it
        ignores the level requirement.
        Afterward it recalculates the stats.
        todo:
            check what moves we can learn after evolution

        Called whenever we level up.
        """
        pkmn_db = load_pokemon_database() # loads in the database

        if num is not None: self.species = pkmn_db[str(num)]

        elif num is None:
            for evolution in self.species["Evolutions"]:
                if self.level >= evolution["level"]:
                    self.species = pkmn_db[str(evolution["id"])]
                    print(f"Wow! {self.name} has evolved into a {self.species['Name']}")
                else: continue

        # Check if it can learn moves

    def calc_current_hp(self, current_hp):
        """
        recalculate current hp.

        used if a pokemon does not generate with a full health bar.

        todo:
            set the current hp to full after an evolution
        """
        if current_hp is None: current_hp = self.stats[0]
        if current_hp > self.stats[0]: current_hp = self.stats[0]
        if current_hp < 0: current_hp = 0; self.status_code = 0
        self.current_hp = round(current_hp)

    def save(self):
        """
        Saves a wild pokemon.

        Meant to be used when catching or recieving a pokemon. assigns a unique id,
        then determines if it will be added to the pc or the party. if the party is full, it will be added to the pc.

        todo:
            keep in mind, this should be saved to ram instead of to the json directly.
            make the max number of pokemon unlimited and create boxes if no more are left.
        """
        def save_data(self,new_mem):
            new_mem["ID"] = self.id
            new_mem["Nickname"] = self.name
            new_mem["Species"] = self.species["Name"]
            new_mem["Level"] = self.level
            new_mem["Nature"] = self.nature.name
            new_mem["Gender"] = self.gender
            new_mem["EV's"] = [self.EV.hp, self.EV.attack, self.EV.defence, self.EV.sp_attack, self.EV.sp_defence,
                               self.EV.speed]
            new_mem["IV's"] = [self.IV.hp, self.IV.attack, self.IV.defence, self.IV.sp_attack, self.IV.sp_defence,
                               self.IV.speed]
            new_mem["Friendship"] = self.friendship
            new_mem["Stats"] = self.stats
            new_mem["Item"] = self.item
            new_mem["OT"] = self.OT #this will be the player name
            new_mem["Shiny"] = self.shiny
            new_mem["Pokerus"] = self.pokerus
            new_mem["Catch Location"] = self.catch_location #current location
            new_mem["Date Caught"] = self.date_caught #datetime object
            new_mem["Moves"] = self.Moves.moves  # might have to be a dictionary?

        pc_pkmn = load_json(f"{user_home}/pokemon/pc pkmn.json")
        party_pkmn = load_json(f"{user_home}/pokemon/party pkmn.json")

        # assigns a unique id for each pokemon
        while True:
            if (len(pc_pkmn)+len(party_pkmn)) >= 906: return # maximum amount of pokemon is 906 for now

            self.id = random.randint(10000, 99999)
            if self.id not in pc_pkmn and self.id not in party_pkmn: break

        if len(party_pkmn) < 6: # if the party isnt full, we add it to the party
            new_mem = party_pkmn[self.id] = {}
            save_data(self,new_mem)
            update_json(f"{user_home}/pokemon/party pkmn.json", party_pkmn)

        else: # otherwise, we dump it into the pc
            new_mem = pc_pkmn[self.id] = {}
            save_data(self, new_mem)
            update_json(f"{user_home}/pokemon/pc pkmn.json", pc_pkmn)

        return

    def set_exp(self, exp:int):
        """
        Sets the amount of EXP a pokemon has.

        Meant for generated, usually wild, pokemon. we take the pokemon's level and its Levelling rate to determine its
        EXP.

        todo:
            this shouldnt even be a function wtf
        """
        if exp == None:
            rate = self.species["Levelling Rate"]
            exp = calc_exp(rate, self.level)
        self.exp = exp


    def gain_exp(self, exp_gained):
        """
        Gain EXP.

        Simply adds the given exp to the pokemon's exp. it also checks the pokemon's level and EXP levelling rate to see
        if the pokemon will level up or not. if so, we call the self.level_up() function.

        todo:
            change this to use a while loop instead of recursion?
        """

        self.exp+=exp_gained # add the given exp
        #print(self.exp)
        self.can_level_up() # checks if it can level up

    def can_level_up(self):
        """
        Checks if a pokemon can level up.

        Uses its levelling rate and then checks if its experience is greater than whats required to level up.
        if so, level it up.
        """
        rate = self.species["Levelling Rate"]
        while self.exp >= calc_exp(rate, self.level + 1) and self.level <100:
            self.level_up()

    def level_up(self):
        """
        Levels up a pokemon.

        Is triggered by EXP milestones. Increments the p.level by 1 and then runs a check to evolve or to learn a new
        move. if it can learn a new move, we make it the 4th move(index 3). if it can evolve, we move its stats and data
        and spawn its evolution pokemon.

        todo:
            research pokemon EXP requirements n stuff
                based on egg field group? then we list egg group in pokedex and determine the next level based on group

        """
        #get current level
        self.level+=1

        # check if it can learn a new move
        # we check for evolutions after a battle.
        moveset = self.species["Moveset"]
        for move in moveset:
            if self.level == moveset[move]["Level"]:
                print(f"LeveL: {self.level}")
                self.Moves.add_new_move(moveset[move]["Name"])

        # this will only be after battles
        self.evolve()


    def __str__(self):
        id = f" with ID: {self.id}"
        shiny = ""
        level = f"Level {self.level}, "
        name = f"{self.species['Name']} "
        nickname = ""
        current_hp = f"{self.current_hp}"
        total_hp = f"{self.stats[0]}"
        hp = f"at {current_hp}/{total_hp} hp"
        status_cond = f"{self.status_condition}, "
        nature = f"{self.nature.name}, "

        if self.name != self.species["Name"]: nickname = f"named '{self.name}' "
        if self.shiny: shiny = "shiny "
        if self.status_code is None: status_cond = ""

        return status_cond + nature + level + shiny + name + nickname + hp + id

class Party:
    """
    Class that creates an instance of a party of pokemon.(each are an instance of the pokemon class)

    on init, it will take info of the user's pokemon(from ram or a json) and for each pokemon,
    it initializes the pokemon class.

    todo:
        maybe make a seperate memebers property based on each pokemon in the party
    """

    def __init__(self, *pokemon):
        self.party = []
        for p in pokemon:
            team_mem = p
            team_mem.active = False
            self.party.append(team_mem)
        self.size = len(self.party)

    def __str__(self):
        message = "Party containing:{\n"
        for pokemon in self.party:
            message+= f"[{str(pokemon)}],\n"
        return message+"}"

    def switch_members(self, poke1, poke2):
        """
        Takes 2 pokemon, or indexes?, and switches their indexes.

        think about how this is called
        """
        pass

    def list_party(self):
        for p in self.party:
            print(p)

class Battle:
    def __init__(self, team1, team2, team3=None, max_active:int=1, wild=True):
        """
        creates a battle instance. each team will be an array consisting of several pokemon instances.
        maybe support up to 3 teams?

        Example:
            team1 = [lucario, charizard, dialga]
            team2 = [arceus, weavile]

            moves are really simple. focus on basic ones for now.
            find active, choose an action
            find moves. choose their prioritu
            choose priority
            execute. looks for move in database and executes based on its properties.(could do this when we choose priority.)
        """

        self.wild = wild # determines if this is a wild battle or not
        self.max_active = max_active #how many pokemon per team can be active at once
        self.team1 = team1
        self.team2 = team2

        self.teams = [self.team1, self.team2] #contains the teams and their actives. used to determine team-active specifics
        if team3 is not None: #if we have a 3rd team in a ffa, add em in
            self.team3 = team3
            self.teams.append(self.team3)

        self.assign_teams()
        self.actives = [] #all the active pokemon. grouped by team but cannot identify which team
        self.turn = 0 #what turn we are on
        self.gen_actives()
        self.get_actions()

        """for p in self.team1.party: # prints all pokemon in a party
            print(p)"""

        """for p in self.team1.actives:
            print(p)

        print("\n")
        self.team1.actives[0].active = False; self.team1.actives.pop(0)

        for p in self.team1.actives:
            print(p)

        print("\n")

        self.turn+=1; self.gen_actives()

        for p in self.team1.actives:
            print(p)"""

    def __str__(self):
        """
        lists the parties and prints em as:
        party1:
        party2:
        """
        message = f"Battle instance with {len(self.teams)} teams:\n"
        for team in self.teams:
            message += f"{str(team)}\n"

        return message

    def assign_teams(self):
        for index, team in enumerate(self.teams):
            for p in team.party:
                p.team = index

    def check_alive(self, team, return_sum=False):
        sum = 0
        alive = []
        for pokemon in team.party:
            if pokemon.status_code != "fainted" or pokemon.current_hp >0:
                if return_sum: sum +=1
                alive.append(pokemon)

        if return_sum: return sum
        return alive

    def fainted(self):
        """
        Procedure when a pokemon has fainted.

        Removes them from both actives
        how to determine which team their on?
        """

    def add_actives(self, team):
        """
        adds a pokemon to team.actives.

        make it only add 1 pokemon per call.
        """
        for p in team.party:
            if p.active == False:
                p.active = True
                team.actives.append(p)
                self.actives.append(p)
                return

    def gen_actives(self):
        """
        Make all active pokemon.

        This checks through all active pokemon and if there arent enough active pokemon in battle, it places them in.
        Executes between rounds. including at the start of a battle. if it is the start of the battle, it automatically
        adds the first :num_active: pokemon in each party. otherwise, it will prompt the user to choose what pokemon
        to send in.
        """

        #on the first turn, this looks through all teams, and adds the first pokemon as active and appends it to the team actives and battle actives
        if self.turn == 0: # runs on initialization
            for team in self.teams:
                team.actives = []
                for i in range(self.max_active):
                    try:
                        team.party[i].active = True
                        team.actives.append(team.party[i]) #adds them to the team actives
                        self.actives.append(team.party[i])  # adds this team to total actives
                    except IndexError: pass #teams might have less pokemon than required
            return

        # otherwise, this is run at the end of a round to see if the maximum number of pokemon are active
        for team in self.teams:
            num_active = len(team.actives) #number of currently active pokemon
            max_active = self.max_active # number of pokemon that are supposed to be active
            num_alive = self.check_alive(team, return_sum=True) #number of pokemon in the team that are alive
            if num_active < max_active:
                availiable = num_alive - num_active
                needed = max_active-num_active
                for i in range(min(needed, availiable)):
                    self.add_actives(team)

            """if len(team.actives) < self.max_active:
                num_alive = self.check_alive(team, return_sum=True)

                if num_alive == len(team.actives): print("These are the only ones alive. cant add another") #if there are no other availiable pokemon

                elif num_alive > len(team.actives): #if they have more availiable pokemon left
                    print("We need a new one")
                    pkmn_needed = num_alive-len(team.actives)
                    for i in range(pkmn_needed):
                        self.add_actives(team) # adds as many pokemon to actives as possible
                    #add a function that gets the next pokemon that isnt active

            else:print("we clear")"""

    def clear_actives(self):
        """
        Clears all active pokemon.

        To be called at the end of the battle. this clears self.actives and it also clears every team.active
        """

    def list_actives(self, team):
        """
        prints the active pokemon
        """
        for p in team.actives:
            print(p)

    def get_actions(self):
        """
        For every active pokemon, gets their actions.

        looks through all pokemon in self.actives and assigns an attribute of self.action
        Recursion?
        """
        for pokemon in self.actives: pokemon.action = self.choose_action(pokemon)

    def choose_action(self, pokemon):
        """
        Gets the action of a pokemon.

        Can choose between 1 of 4 choices: fight, switch pokemon, use an item or run.
        Each choice prompts another function asking for another choice, except for run.
        If fight, we execute choose_move()
        If pokemon, we execute view_pokemon();  they will also be able to view the info on each pokemon as well
        If item, we exec choose_item()
        If run, we exec try_run()

        Returns an array [action, action_priority]
        """
        selection = int(input(f"What will {pokemon.name} do?"))

        if selection==1: # they choose to battle
            return self.choose_move(pokemon)
        elif selection==2: # they choose to switch/view pokemon
            return self.switch_pokemon(pokemon)
        elif selection==3: # they choose to use an item
            pass
        elif selection>=4: # they attempt to run
            return self.try_run(pokemon)

    def choose_move(self, pokemon):
        """
        Chooses a move for the pokemon.

        :return [{"fight":move}, priority]:

        todo:
            when we add in moves to the database, we search for the move in the database and use that for priority
            should this be part of the pokemon class?
        """
        move = int(input(f"Enter 1-4 to choose the respective move. {pokemon.Moves.moves}"))
        priority = 1
        try: selected = pokemon.Moves.moves[move]
        except: selected = pokemon.Moves.moves[0]
        return [{"fight":selected}, priority]

    def order_actions(self):
        """
        orders the actions based on action priority and each pokemon's speed.

        Takes in self.actives and from there we look at pokemon.action to view the priority of the move, we sort it from
        there and make it a temporary list. after, we check for any pokemon who's priorities are tied.(both have 2 priority)
        and then order based on each individual pokemon's speed. assign each pokemon another property called order
        """
        #sort the entire array
        self.actives.sort(key=lambda x: x.action[1], reverse=False)

        #find indexes where priority is 2, 1 or -1, and sort pokemon into their respective list
        top, mid, bot = [],[],[]
        for active in self.actives:
            if active.action[1] == 2: top.append(active)
            if active.action[1] == 1: mid.append(active)
            if active.action[1] == -1: bot.append(active)

        for priority_list in [top, mid, bot]:  # sort em by speed
            priority_list.sort(key=lambda x: x.speed, reverse=True)

        self.actives = top+mid+bot # merge em
        for p in self.actives:
            print(f"poke: {p}, speed: {p.speed}, priority: {p.action[1]}")


    def switch_pokemon(self, pokemon):
        """
        Displays all party members and allows the option to switch pokemon.

        We find the pokemon's party using the self.team attribute all pokemon are given on initialization.
        Using that, we list all pokemon in the respective team using Party.list_party().

        From here, we allow the user to select which pokemon they would like to switch with. so long as the selected
        pokemon hasnt fainted or isnt the currently active pokemon.
        """
        priority = 2
        team = self.teams[pokemon.team]
        while True:
            try:
                team.list_party()
                selected = int(input(f"Choose a pokemon to switch to\nCurrently active is {pokemon}"))
                if (pokemon != team.party[selected]) and (team.party[selected].status_code != "fainted"): print(f"you chose {team.party[selected]}"); break #lets you switch to a pokemon so long as it in healthy and a different one
            except IndexError: pass

        return [{"switch":selected},priority]

    def try_run(self, pokemon):
        """
        Attemps to run.

        Checks all pokemon that are not on the same team(different self.team values) and checks if any of them are faster.
        """
        if self.wild==False: return #figure this out. ideally they can return back to selecting an action
        faster = False
        for index, team in enumerate(self.teams):
            if index==pokemon.team: continue
            for p in team.actives:
                if p.speed >= pokemon.speed: faster = True;break
        if not faster:
            pass # exit the battle. call the ending func
        if faster:
            pass #roll the random function

a = Pokemon(species=1, level=5, nickname="test", status_code=2) #loads in a charmander
#b = Pokemon(species=1, level=5, nickname="Bulby", shiny=True, moves=["Flare Blitz"])
#c = Pokemon(species=4, level=5, nickname="flamethrowmer")
#d = Pokemon(species=4, level=1, nickname="sdf")
#e=Pokemon(species=4, level=15, nickname="1")
a.save()


"""
print(a)
print(a.types)
print(f"Base stats: {a.base_stats}")
print(f"Stats: {a.stats}")
#a.stats = (0,0,0,12,0,2)
#print(f"Stats: {a.stats}")

print("Evolving!")
a.evolve()
print(a)
print(f"Base stats: {a.base_stats}")
print(f"Stats: {a.stats}")
party = Party(a,b)
party2 = Party(c,d)
#party3 = Party(e)
print(party)
battle = Battle(party, party2, max_active=1)
print(battle)"""

#battle.order_actions()

"""
print("\n\n\n\n\n")
for team in battle.teams:
    battle.list_actives(team)
    print("\n")
    for p in team.party:
        print(p)#; break
    print("\n")
for p in battle.actives:
    print(p.action)#"""

