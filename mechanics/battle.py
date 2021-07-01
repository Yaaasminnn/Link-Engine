"""
Pokemon Game Link Engine Alpha

Head Developer: Mon-Emperor
Creators: Mon-Emperor, DarkClaw
Contributors:
Start Date: April 28 2021 4:49am
Release Date:
"""
import json
import random
from moves import Moves

class Pokemon:
    def __init__(self,name, level, nickname = None):

        """
        Loads the json file and methods.

        Calls the function to load the jsons containing:
        pokemon, nature, and then loads the EV and IV methods
        """
        pkmn_data = Pokemon.load_pkmn_data()
        nature = Pokemon.load_nature_data()
        EV = Pokemon.create_EV()
        IV = Pokemon.create_IV()

        self.pkmn = pkmn_data[str(name)]
        self.name = self.pkmn["Name"]
        self.level = level
        self.id = 0
        self.base_stats = self.pkmn["Base Stats"]
        self.EVs = EV
        self.IVs = IV

        self.nature_name = nature[0] #Nature name
        self.nature = [] #Nature data
        for stat in nature[1]:
            self.nature.append(stat)

        self.stats = []
        self.hp = int(((((2*(self.base_stats["Hit Points"]))+self.IVs[0]+(self.EVs[0]/4)) * self.level) / 100) + self.level + 10)
        self.stats.append(self.hp)
        self.atk = int((((((2*(self.base_stats["Physical Attack"]))+self.IVs[1]+(self.EVs[1]/4)) * self.level) / 100) + 5) * self.nature[0])
        self.stats.append(self.atk)
        self.def_ = int((((((2*(self.base_stats["Physical Defence"]))+self.IVs[2]+(self.EVs[2]/4)) * self.level) / 100) + 5) * self.nature[1])
        self.stats.append(self.def_)
        self.sp_atk = int((((((2*(self.base_stats["Special Attack"]))+self.IVs[3]+(self.EVs[3]/4)) * self.level) / 100) + 5) * self.nature[2])
        self.stats.append(self.sp_atk)
        self.sp_def = int((((((2*(self.base_stats["Special Defence"]))+self.IVs[4]+(self.EVs[4]/4))*(self.level))/100)+5)*self.nature[3])
        self.stats.append(self.sp_def)
        self.speed = int((((((2*(self.base_stats["Speed"]))+self.IVs[5]+(self.EVs[5]/4))*self.level)/100)+5)*self.nature[4])
        self.stats.append(self.speed)

        """
        Moves.
        
        This creates an array that will contain up to 4 moves. It then reads the moveset data in the pokemondata.json
        upon reading it, it will read the move's level as well and if the pokemon's level is >= the move level, it will
        append it to the move array created. however, if there is already 4 moves, it will delete the first one and
        append the new move to the array. this way, as it levels up it learns new moves
        """
        self.moves = []
        move = 1
        self.moveset = self.pkmn["Movesets"]

        for moves in self.moveset:
            self.moveset_level = self.moveset[f"Move {str(move)}"]["Level"]
            self.moveset_name = self.moveset[f"Move {str(move)}"]["Name"]

            if self.level >= self.moveset_level: #if you are high enough level, append the move to the array
                if len(self.moves) == 4: #max of 4 moves: deletes the first move in the list and adds the new one
                    self.moves.pop(0)
                    self.moves.append(self.moveset_name)
                elif len(self.moves) < 4:
                    self.moves.append(self.moveset_name)
            else:
                pass
            move += 1

        self.pkmn_type = pkmn_data[str(name)]["Types"] #shows the pokemon's type

        if nickname is None: #if the pokemon has a nickname, refer to it by the nickname
            self.nickname = self.name
        else:
            self.nickname = str(nickname)

    @staticmethod #loads the pokemon database for the given wild pokemon
    def load_pkmn_data():
        """
        Loads the pokemon database for given wild pokemon
        """
        with open("pokemondata.json", "r") as pkmn:
            data = json.load(pkmn)
        return data

    @staticmethod #loads the natures database for a random nature for the generated pokemon
    def load_nature_data():
        """
        Reads the nature data from the natures.json file. it then assigns the mods to an array that is returned.
        """
        with open("natures.json", "r") as n:
            data = json.load(n)
            natures = [
                "Hardy",
                "Lonely",
                "Brave",
                "Adamant",
                "Naughty",
                "Bold",
                "Docile",
                "Relaxed",
                "Impish",
                "Lax",
                "Timid",
                "Hasty",
                "Serious",
                "Jolly",
                "Naive",
                "Modest",
                "Mild",
                "Quiet",
                "Bashful",
                "Rash",
                "Calm",
                "Gentle",
                "Sassy",
                "Careful",
                "Quirky"
            ]
            random_index = random.choice(natures)

            nature_data = []
            nature_name = data[random_index]["Name"]
            nature_data.append(nature_name)

            nature_stats = []
            nature_atk_mod = data[random_index]["Stat Mods"]["Attack Mod"]
            nature_stats.append(nature_atk_mod) #index 0

            nature_def_mod = data[random_index]["Stat Mods"]["Defence Mod"]
            nature_stats.append(nature_def_mod) #index 1

            nature_sp_atk_mod = data[random_index]["Stat Mods"]["Special Attack Mod"]
            nature_stats.append(nature_sp_atk_mod) #index 2

            nature_sp_def_mod = data[random_index]["Stat Mods"]["Special Defence Mod"]
            nature_stats.append(nature_sp_def_mod) #index 3

            nature_speed_mod = data[random_index]["Stat Mods"]["Speed Mod"]
            nature_stats.append(nature_speed_mod) #index 4

            nature_data.append(nature_stats)
        return nature_data

    @staticmethod #Creates a list of EV's for the generated pokemon which are all set to 0  by default
    def create_EV():
        """
        Creates base EV's for a generated pokemon that default to 0.

        This will only affect when pokemon are generated for the first time. when loading existing pokemon,
        they will be retrieved from a json containing all their stats
        """
        EV =[]

        EV_hp = 0 #index 0
        EV.append(EV_hp)
        EV_atk = 0 #index 1
        EV.append(EV_atk)
        EV_def = 0 #index 2
        EV.append(EV_def)
        EV_sp_atk = 0 #index 3
        EV.append(EV_sp_atk)
        EV_sp_def = 0 #index 4
        EV.append(EV_sp_def)
        EV_speed = 0 #index 5
        EV.append(EV_speed)

        return EV

    @staticmethod #Creates a list of IV's for the generated pokemon
    def create_IV():
        """
        Creates base IV's for a generated pokemon.

        rolls a random number from 0-31.
        """
        IV = []

        IV_hp = random.randint(0,31)
        IV.append(IV_hp)
        IV_atk = random.randint(0, 31)
        IV.append(IV_atk)
        IV_def = random.randint(0, 31)
        IV.append(IV_def)
        IV_sp_atk = random.randint(0, 31)
        IV.append(IV_sp_atk)
        IV_sp_def = random.randint(0, 31)
        IV.append(IV_sp_def)
        IV_speed = random.randint(0, 31)
        IV.append(IV_speed)

        return IV

    #saves a pokemon to the party or pc depending on the size of the user's party
    def save_pkmn(self):
        """
        Saves a pokemon.

        assigns the pokemon a unique id, then determines if it will be added to the party. if the party is already full,
        it will place it in the pc json file.
        """
        pc_pkmn = Load_Pokemon.load_pc()
        party_pkmn = Load_Pokemon.load_party()

        #assigns the pokemon a unique id name for identification. currently maxes out at 900, but thats plenty
        while True:
            if (len(pc_pkmn)+len(party_pkmn)) >= 906: return #make the limit 900 pc pokemon, 6

            self.id = random.randint(10000, 99999)
            if self.id not in pc_pkmn and self.id not in party_pkmn:
                break

        if len(party_pkmn) < 6:
            new_party_member = party_pkmn[f"{self.id}"] = {}
            new_party_member["ID"] = self.id
            new_party_member["Nickname"] = self.nickname
            new_party_member["Species"] = self.name
            new_party_member["Level"] = self.level
            new_party_member["Nature"] = self.nature_name
            new_party_member["EV's"] = self.EVs
            new_party_member["IV's"] = self.IVs
            new_party_member["Stats"] = self.stats

            new_party_member["Moves"] = {}
            position = 1
            for move in self.moves:
                new_party_member["Moves"][f"Move {position}"] = self.moves[position-1]
                position+=1

            Load_Pokemon.update_pkmn(party_pkmn, True)

        elif len(party_pkmn) == 6:

            box_num = 1
            for box in pc_pkmn:
                if len(pc_pkmn) == 900: return #if all boxes are maxed out, it returns
                if len(pc_pkmn[f"Box {box_num}"]) == 30: pass #if the box is full, move on to the next one
                elif len((pc_pkmn[f"Box {box_num}"])) < 30: break #if the box aint full, store the pokemon here
                box_num +=1

            pc_box = pc_pkmn[f"Box {box_num}"]
            new_pc_member = pc_box[f"{str(self.id)}"] = {}
            new_pc_member["ID"] = self.id
            new_pc_member["Nickname"] = self.nickname
            new_pc_member["Species"] = self.name
            new_pc_member["Level"] = self.level
            new_pc_member["Nature"] = self.nature_name
            new_pc_member["EV's"] = self.EVs
            new_pc_member["IV's"] = self.IVs
            new_pc_member["Stats"] = self.stats

            new_pc_member["Moves"] = {}
            position = 1
            for move in self.moves:
                new_pc_member["Moves"][f"Move {position}"] = self.moves[position - 1]
                position += 1

            Load_Pokemon.update_pkmn(pc_pkmn, False)

class Load_Pokemon:
    def __init__(self, box_or_party,box = None):
        """
        Loads either the party or the pc based on the input

        This class will also be used to load specific pokemon
        """
        self.party_is_loaded = False
        if box_or_party == "PC":
            self.load_pokemon_details(box)

        elif box_or_party == "Party":
            self.party_is_loaded = True
            self.load_pokemon_details()

    @staticmethod #loads the party pokemon from a json
    def load_party():
        with open("party pkmn.json", "r") as party:
            party_pkmn = json.load(party)
        return party_pkmn

    @staticmethod #loads the pc pokemon from a json
    def load_pc(): #loads the pc pokemon
        with open("pc pkmn.json", "r") as pc:
            pc_pkmn = json.load(pc)
        return pc_pkmn

    @staticmethod #Updates the pokemon databases. updates party or pc based on input
    def update_pkmn(pkmn,party_pkmn = False):
        if not party_pkmn:
            with open("pc pkmn.json", "w") as write:
                json.dump(pkmn, write)

        else:
            with open("party pkmn.json", "w") as write:
                json.dump(pkmn, write)

    #loads and returns the details on a pokemon
    def load_pokemon_details(self, box = None):

        if not self.party_is_loaded:
            pc = Load_Pokemon.load_pc()
            #add all the load details of this later when we get to pc stuff
            box_loaded = Load_Pokemon.load_pc_by_box(box)

            self.pc_ids = []
            for pkmn in box_loaded:
                pkmn_data = []

                pkmn_index = box_loaded[f"{pkmn}"]
                pkmn_data.append(pkmn_index["ID"])  # index of 0
                pkmn_data.append(pkmn_index["Nickname"])  # index of 1
                pkmn_data.append(pkmn_index["Species"])  # index of 2
                pkmn_data.append(pkmn_index["Level"])  # index of 3
                pkmn_data.append(pkmn_index["EV's"])  # index of 4
                pkmn_data.append(pkmn_index["IV's"])  # index of 5
                pkmn_data.append(pkmn_index["Stats"])  # index of 6

                pkmn_moves = []
                move_position = 1
                for move in pkmn_index["Moves"]:
                    pkmn_moves.append(pkmn_index["Moves"][f"Move {move_position}"])
                    move_position += 1
                pkmn_data.append(pkmn_moves)

                self.pc_ids.append(pkmn_data)
            return self.pc_ids

        elif self.party_is_loaded:
            party = Load_Pokemon.load_party()

            self.party_ids = []
            for pkmn in party:
                pkmn_data = []

                pkmn_index = party[f"{pkmn}"]
                pkmn_data.append(pkmn_index["ID"]) #index of 0
                pkmn_data.append(pkmn_index["Nickname"]) #index of 1
                pkmn_data.append(pkmn_index["Species"]) #index of 2
                pkmn_data.append(pkmn_index["Level"]) #index of 3
                pkmn_data.append(pkmn_index["EV's"]) #index of 4
                pkmn_data.append(pkmn_index["IV's"]) #index of 5
                pkmn_data.append(pkmn_index["Stats"]) #index of 6

                pkmn_moves = []
                move_position = 1
                for move in pkmn_index["Moves"]:
                    pkmn_moves.append(pkmn_index["Moves"][f"Move {move_position}"])
                    move_position+=1
                pkmn_data.append(pkmn_moves)

                self.party_ids.append(pkmn_data)
            return self.party_ids

    @staticmethod #load the pc by a specific box requested
    def load_pc_by_box(box):
        pc = Load_Pokemon.load_pc()
        return pc[f"Box {box}"]

    @staticmethod #loads a pokemon by its id
    def load_pkmn_by_id(id):
        """
        Loads a pokemon by its id.

        battle will take the id from the array and load the pokemon by said id.
        am also adding functionality for loading a pokemon from the pc. basically a loop that increases the box num
        and searches the boxes for said id by using the load_pc_by_box method that loads that specified index/box
        """
        party = Load_Pokemon.load_party()
        pc = Load_Pokemon.load_pc()

        if str(id) in party:
            return party[f"{id}"]

        for box in range(1,30):
            loaded_box = Load_Pokemon.load_pc_by_box(box)
            if str(id) in loaded_box:
                return loaded_box[f"{id}"]

class Battle(Load_Pokemon):
    def __init__(self, box_or_party, opponent):
        Load_Pokemon.__init__(self, box_or_party="Party") #maybe load box too as a para

        #change this to use existing pokemon instead of generating wild ones
        self.player = self.load_pokemon_details()[0]
        print(self.player)
        self.player_stats = self.player[6]
        self.player_hp = self.player_stats[0]
        self.player_statmods = [1.0, 1.0, 1.0, 1.0, 1.0]
        self.player_nickname = self.player[1]
        self.player_lvl = self.player[3]

        self.opponent = Pokemon(str(opponent), 6)
        self.opponent_hp = self.opponent.hp
        self.opponent_statmods = [1.0, 1.0, 1.0, 1.0, 1.0]


        battle_round = self.turn()

    def turn(self):

        """
        The basic round.
        
        It gets both user's inputs. any number from1-4 corresponding to the moves chosen by each player.
        the player's choice is attached to their known moves which is then linked to the move in the move database
        then, from the database, the move's data(name, power, accuracy, type, class and effect) are retrieved.
        
        After this, it evaluates both user's speed then executes the moves based on speed. 
        """
        someone_lost = False
        while not someone_lost:
            print(self.player_statmods)
            print(self.opponent_statmods)

            #Player stuff
            self.move = input(f"What will {self.player[1]} do? select a move\n"
                         f"{self.player[7]}\n")
            if self.move == "1":
                self.move = self.player[7][0]
            elif self.move == "2":
                self.move = self.player[7][1]
            elif self.move == "3":
                self.move = self.player[7][2]
            elif self.move == "4":
                self.move = self.player[7][3]

            self.move = Moves.search_for_move(self.move)

            #opponent stuff
            self.opponent_move = input(f"What will {self.opponent.nickname} do? select a move\n"
                         f"{self.opponent.moves}\n")
            if self.opponent_move == "1":
                self.opponent_move = self.opponent.moves[0]
            elif self.opponent_move == "2":
                self.opponent_move = self.opponent.moves[1]
            elif self.opponent_move == "3":
                self.opponent_move = self.opponent.moves[2]
            elif self.opponent_move == "4":
                self.opponent_move = self.opponent.moves[3]

            self.opponent_move = Moves.search_for_move(self.opponent_move)

            #takes the move choices and executes them. this is where all the action happens
            someone_lost = self.execute_moves()
            if someone_lost:
                break

    #mod this into stat mods in the move algo
    def check_for_stat_mods(self, user):
        if user == "Player":
            self.mod_stats_list = self.move["Mod stats"]
            if self.mod_stats_list == "False":  # if its false, there is no additional effect. else, continue
                pass

            else:
                stat_num = 1
                for stat in self.mod_stats_list:
                    # gets the stat mods and then executes it as a function based on who the target is
                    referenced_mod = self.mod_stats_list[f"Stat {str(stat_num)}"]
                    modded_stat = referenced_mod["Stat"]
                    degree = referenced_mod["Degree"]
                    target = referenced_mod["Target"]
                    opp_stat_mod = self.mod_stats(modded_stat, degree, user, target)
                    self.opponent_statmods = opp_stat_mod
                    stat_num += 1

        elif user == "Opponent":
            self.mod_stats_list = self.opponent_move["Mod stats"]
            if self.mod_stats_list == "False":  # if its false, there is no additional effect. else, continue
                pass

            else:
                stat_num = 1
                for stat in self.mod_stats_list:
                    # gets the stat mods and then executes it as a function based on who the target is
                    referenced_mod = self.mod_stats_list[f"Stat {str(stat_num)}"]
                    modded_stat = referenced_mod["Stat"]
                    degree = referenced_mod["Degree"]
                    target = referenced_mod["Target"]
                    stat_mod = self.mod_stats(modded_stat, degree, user, target)
                    self.player_statmods = stat_mod
                    stat_num += 1
    #same thing
    def mod_stats(self, stat, degree, user, target):
        if (user == "Opponent" and target == "Target") or (user == "Player" and target == "Self"):
            if stat == "Attack":
                self.player_statmods[0] = self.player_statmods[0]*degree
                if degree < 1:
                    print(f"{self.player[1]}'s Attack was decreased by {degree} to {self.player_statmods[0]}!")
                else:
                    print(f"{self.player[1]}'s Attack was increased by {degree} to {self.player_statmods[0]}!")

            elif stat == "Defence":
                self.player_statmods[1] = self.player_statmods[1]*degree
                if degree < 1:
                    print(f"{self.player[1]}'s Defence was decreased by {degree} to {self.player_statmods[1]}!")
                else:
                    print(f"{self.player[1]}'s Defence was increased by {degree} to {self.player_statmods[1]}!")

            elif stat == "Special Attack":
                self.player_statmods[2] = self.player_statmods[2]*degree
                if degree < 1:
                    print(f"{self.player[1]}'s Special Attack was decreased by {degree} to {self.player_statmods[2]}!")
                else:
                    print(f"{self.player[1]}'s Special Attack was increased by {degree} to {self.player_statmods[2]}!")

            elif stat == "Special Defence":
                self.player_statmods[3] = self.player_statmods[3]*degree
                if degree < 1:
                    print(f"{self.player[1]}'s Special Defence was decreased by {degree} to {self.player_statmods[3]}!")
                else:
                    print(f"{self.player[1]}'s Special Defence was increased by {degree} to {self.player_statmods[3]}!")

            elif stat == "Speed":
                self.player_statmods[4] = self.player_statmods[4]*degree
                if degree < 1:
                    print(f"{self.player[1]}'s Speed was decreased by {degree} to {self.player_statmods[4]}!")
                else:
                    print(f"{self.player[1]}'s Speed was increased by {degree} to {self.player_statmods[4]}!")

            return self.player_statmods

        elif (user == "Opponent" and target == "Self") or (user == "Player" and target == "Target"):
            if stat == "Attack":
                self.opponent_statmods[0] = self.opponent_statmods[0] * degree
                if degree <1:
                    print(f"{self.opponent.nickname}'s Attack was decreased by {degree} to {self.opponent_statmods[0]}!")
                else:
                    print(f"{self.opponent.nickname}'s Attack was increased by {degree} to {self.opponent_statmods[0]}!")

            elif stat == "Defence":
                self.opponent_statmods[1] = self.opponent_statmods[1] * degree
                if degree <1:
                    print(f"{self.opponent.nickname}'s Defence was decreased by {degree} to {self.opponent_statmods[1]}!")
                else:
                    print(f"{self.opponent.nickname}'s Defence was increased by {degree} to {self.opponent_statmods[1]}!")

            elif stat == "Special Attack":
                self.opponent_statmods[2] = self.opponent_statmods[2] * degree
                if degree <1:
                    print(f"{self.opponent.nickname}'s Special Attack was decreased by {degree} to {self.opponent_statmods[2]}!")
                else:
                    print(f"{self.opponent.nickname}'s Special Attack was increased by {degree} to {self.opponent_statmods[2]}!")

            elif stat == "Special Defence":
                self.opponent_statmods[3] = self.opponent_statmods[3] * degree
                if degree <1:
                    print(f"{self.opponent.nickname}'s Special Defence was decreased by {degree} to {self.opponent_statmods[3]}!")
                else:
                    print(f"{self.opponent.nickname}'s Special Defence was increased by {degree} to {self.opponent_statmods[3]}!")

            elif stat == "Speed":
                self.opponent_statmods[4] = self.opponent_statmods[4] * degree
                if degree <1:
                    print(f"{self.opponent.nickname}'s Speed was decreased by {degree} to {self.opponent_statmods[4]}!")
                else:
                    print(f"{self.opponent.nickname}'s Speed was increased by {degree} to {self.opponent_statmods[4]}!")

            return self.opponent_statmods

    def check_if_someone_fainted(self):
        someone_lost = False
        if self.opponent_hp <=0:
            self.opponent_hp = 0
            someone_lost = True
            print(f"{self.opponent.nickname} has {self.opponent_hp} hp remaining!\n")
        if self.player_hp <=0:
            self.player_hp = 0
            someone_lost = True
            print(f"{self.player_nickname} has {self.player_hp} hp remaining!\n")
        return someone_lost

    def execute_moves(self):

        def players_go():  # figure this out so execute moves is optimized
            print(f"{self.player[1]} used {self.move['Name']}!\n")

            run_move = Moves.search_and_run_move(self.move["Name"], self.player_lvl,
                                                 self.player_stats[1], self.player_stats[3],
                                                 self.opponent.def_, self.opponent.sp_def,
                                                 self.player_statmods[0], self.player_statmods[2],
                                                 self.opponent_statmods[1], self.opponent_statmods[3])
            if not run_move:
                print(f"{self.player_nickname}'s attack missed!\n")

            else:
                self.opponent_hp -= run_move[0]
                someone_lost = self.check_if_someone_fainted()
                if someone_lost:
                    return someone_lost

            print(f"{self.opponent.nickname} has {self.opponent_hp}/{self.opponent.hp}hp remaining!\n")

        def opponents_go():
            print(f"{self.opponent.nickname} used {self.opponent_move['Name']}!\n")
            run_move = Moves.search_and_run_move(self.opponent_move["Name"], self.opponent.level,
                                                 self.opponent.atk, self.opponent.sp_atk,
                                                 self.player_stats[2], self.player_stats[4],
                                                 self.opponent_statmods[0], self.opponent_statmods[2],
                                                 self.player_statmods[1], self.player_statmods[3])

            if not run_move:
                print(f"{self.opponent.nickname}'s attack missed!\n")

            else:
                self.player_hp -= run_move[0]
                someone_lost = self.check_if_someone_fainted()
                if someone_lost:
                    return someone_lost

            print(f"{self.player[1]} has {self.player_hp}/{self.player_stats[0]}hp remaining!\n")

        someone_lost = False
        if self.player_stats[5] >= self.opponent.speed:
            #players go
            someone_lost = players_go()
            if someone_lost: return someone_lost

            #opponents go
            someone_lost = opponents_go()
            if someone_lost: return someone_lost

            return someone_lost

        elif self.opponent.speed > self.player_stats[5]:
            # opponents go
            someone_lost = opponents_go()
            if someone_lost: return someone_lost

            # players go
            someone_lost = players_go()
            if someone_lost: return someone_lost

            return someone_lost

Bulbasaur = Pokemon("Bulbasaur", 5,"Bulby boi")
print(f"Name: {Bulbasaur.nickname}({Bulbasaur.name})")
print(f"Type: {Bulbasaur.pkmn_type}")
print(f"Level: {Bulbasaur.level}\n")
print(f"Hitpoints: {Bulbasaur.hp}\n"
      f"Attack: {Bulbasaur.atk}\n"
      f"Defence: {Bulbasaur.def_}\n"
      f"Special Attack: {Bulbasaur.sp_atk}\n"
      f"Special Defence: {Bulbasaur.sp_def}\n"
      f"Speed: {Bulbasaur.speed}\n")
print(f"Moves: {Bulbasaur.moves}")

print("")
print("")

Charmander = Pokemon("Charmander", 5,"flamethrowmer")
print(f"Name: {Charmander.nickname}({Charmander.name})")
print(f"Type: {Charmander.pkmn_type}")
print(f"Level: {Charmander.level}\n")
print(f"Hitpoints: {Charmander.hp}\n"
      f"Attack: {Charmander.atk}\n"
      f"Defence: {Charmander.def_}\n"
      f"Special Attack: {Charmander.sp_atk}\n"
      f"Special Defence: {Charmander.sp_def}\n"
      f"Speed: {Charmander.speed}\n")
print(f"Moves: {Charmander.moves}")

Bulbasaur.save_pkmn()
Charmander.save_pkmn()

Test = Battle("Party", "Charmander")

Party = Load_Pokemon("Party")
id = Party.load_pokemon_details()
print(id)