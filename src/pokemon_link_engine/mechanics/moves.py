import random
import json

class Moves:

    """
    This class will contain static methods of all listed pokemon moves.

    Opposed to keeping the move data in jsons, several moves are quite unique and have several properties such as:
    payday, metronome, return/frustration etc etc etc. these moves are harder to deal with and giving generic tags
    such as power, accuracy and stat/weather mods wont do them justice. so several moves can have custom functions
    in this section. there shall be 617 moves, but probably less if several are grouped together if their the same

    Example: Moves like scratch, tackle, dragon claw and others have no side effects at all and are only different
    due to type, power, accuracy and class. all of those can be given as inputs and produce the same effect.

    Moves like fire fang, ice fang and more all have the same properties and can be given types and power/accuracy
    along with anything else needed. otherwise they all share properties like a status effect and flinching.
    punch moves also work the same.

    More specific moves such as the ones referenced in the beginning can have their own custom functions.

    details: all moves will be recorded in the json file, but executing them will be done here.

    notes: basic moves, stat modifying moves, moves in succession(outrage), moves that hit multiple times etc
    """

    @staticmethod
    def load_move_database():
        with open("moves.json") as move:
            data = json.load(move)
        return data

    @staticmethod
    def search_for_move(name):
        categories = Moves.load_move_database()
        for category in categories:
            moves = categories[f"{category}"]
            for move in moves:
                if name == move:
                    return categories[f"{category}"][f"{move}"]

    @staticmethod
    def search_and_run_move(name, level, atk = None, sp_atk = None, def_ = None, sp_def = None, atk_mod = None, sp_atk_mod = None, def_mod = None, sp_def_mod = None):
        categories = Moves.load_move_database()
        execute = None
        for category in categories:
            moves = categories[f"{category}"]
            for move in moves:
                move_data = moves[move]
                execute = None
                if name == move:
                    execute = Moves.basic_moves(move_data["Class"], move_data["Type"], move_data["Power"], move_data["Accuracy"], level, atk, sp_atk, def_, sp_def, atk_mod, sp_atk_mod, def_mod, sp_def_mod)
                    break

            return execute

    @staticmethod #calculates accuracy
    def calc_accuracy(accuracy):
        chance = random.randint(1, 100)
        if chance > accuracy: return False

        return True

    @staticmethod #executes basic moves that deal damage without side effects. add in crit ratio
    def basic_moves(Class, type, power, accuracy, level, atk = None, sp_atk = None, def_ = None, sp_def = None, atk_mod = None, sp_atk_mod = None, def_mod = None, sp_def_mod = None):
        hits = Moves.calc_accuracy(accuracy)
        dmg = 0
        if hits:
            if Class == "Physical":
                dmg = (((((2 * level) / (5 + 2)) * power * ((atk * atk_mod) / (def_ * def_mod))) / 50) + 2)

            elif Class == "Special":
                dmg = (((((2 * level) / (5 + 2)) * power * ((sp_atk * sp_atk_mod) / (sp_def * sp_def_mod))) / 50) + 2)

            return [dmg, type]

        return False
