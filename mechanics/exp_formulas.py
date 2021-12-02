"""
the different levelling rates:
Fast
Medium Fast
Medium Slow
Slow
Fluctuating
Erratic
"""

def calc_exp(rate:str, level:int)->int:
    """
    Calculates the amount of EXP needed to level up based on the pokemon's level and levelling rate.
    """

    if level <1: level =1
    if level >100: level =100

    if rate == "Fast":
        return (4*(level**3))/5
    elif rate == "Medium Fast":
        return level**3
    elif rate == "Medium Slow":
        return (((6/5)*(level**3)) - (15*(level**2)) + (100*level) - 140)
    elif rate == "Slow":
        return (5*(level**3))/4
    elif rate == "Fluctuating":
        if level <15: return (level**3)*((((level+1)/3)+24)/50)
        if level >=15 and level <36: return (level**3)*((level+14)/50)
        else: return (level**3)*(((level/2)+32)/50)
    elif rate == "erratic":
        if level <50: return ((level**3)*(100-level))/50
        if level >=50 and level <68: return ((level**3)*(150-level))/100
        if level >=68 and level < 98: return ((level**3)*((1911-(10*level))/3))/500
        else: return ((level**3)*(160-level))/100