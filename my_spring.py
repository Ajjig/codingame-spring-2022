from math import hypot as hypot
from random import randint as rand
from sys import stderr as err

base_x, base_y = [int(i) for i in input().split()]
heroes_per_player = int(input())  # Always 3

busy = []
heros = []                                              #
enemies = []                                            #
mons = []                                               #
taken1 = []                                             #
taken0 = []                                             #
taken2 = []                                             #
mana = 0                                                #
enemana = 0                                             #
my_health = 0                                           #
enemy_health = 0                                        #
being_controlled = False                                #
target = {}                                             #
x = 'x'                                                 #
y = 'y'                                                 #
#   #   #   #   #   #   #   #   #   #   #   #   #   #   #

rounds = 0

def X(x):                                  #
    return x if base_x == 0 else 17630 - x # returns the valid x, y values even if the
def Y(y):                                  # map is reversed
    return y if base_y == 0 else 9000 - y  #

def default(hero):
    h = hero['id']
    if h > 2 : h -= 3
    return ('MOVE ' + (f"{X(5400)} {Y(2900)}" if h == 0 else f"{X(2500)} {Y(2500)}" if h == 1 else f"{X(2900)} {Y(5400)}"))


def is_my_target(_id, h):
    if h['id'] == 0 or h['id'] == 3 :
        return (_id in taken0)
    if h['id'] == 1 or h['id'] == 4 :
        return (_id in taken1)
    if h['id'] == 2 or h['id'] == 5:
        return (_id in taken2)
    return False

def append_takens(id_, h):
    if h['id'] == 0 or h['id'] == 3 :
        taken0.append(id_)
    if h['id'] == 1 or h['id'] == 4 :
        taken1.append(id_)
    if h['id'] == 2 or h['id'] == 5 :
        taken2.append(id_)

def is_taken(id_, h): 
    if (h['id'] == 0 or h['id'] == 3 ):
        return (id_ in taken1 or id_ in taken2)
    if (h['id'] == 1 or h['id'] == 4 ):
        return (id_ in taken0 or id_ in taken2)
    if (h['id'] == 2 or h['id'] == 5 ):
        return (id_ in taken1 or id_ in taken0)
    if (h['id'] == -1):
        return (id_ in taken0 or id_ in taken1 or id_ in taken2)

def is_closer(hero, target):
    global my_health, busy, heros
    dists = []
    for h in heros :
            if not h['id'] in busy : dists.append(hypot(h[x] - target[x], h[y] - target[y]))
    dists.sort()
    if dists == [] : return False
    if dists[0] == hypot(hero[x] - target[x], hero[y] - target[y]) :
        return True
    else :
        return False


def taken_remover(_id, hero):
    h = hero['id']
    if h > 2 : h -= 3
    if _id == -1 :
        if h == 0 : taken0.clear()
        if h == 1 : taken1.clear()
        if h == 2 : taken2.clear()
        return
    if (h == 0) and _id in taken0 : taken0.remove(_id)
    if (h == 1) and _id in taken1 : taken1.remove(_id)
    if (h == 2) and _id in taken2 : taken2.remove(_id)


def_x = X(17630)  #
def_y = Y(4000)   # When the mana is greater than 20 the heros moves between def_x, def-y and def_x2, def_y2 
def_x2 = X(12000) # waiting for the perfect time to control the enemy outside the base or to push a monster inside it
def_y2 = Y(8500)  #

def attacker(hero):
    global mana, enemies
    global def_x, def_y
    global x, y, def_x2, def_y2

    if def_x == hero[x] :
        def_x, def_x2 = def_x2, def_x
        def_y, def_y2 = def_y2, def_y

    limit_mana = 10
    rounds_limit = 0

    
    for i in mons:

        if mana >= limit_mana and rounds > rounds_limit:

            if i['shield'] == 0 and hypot(i[x] - hero[x], i[y] - hero[y]) < 1280 and i['base_enemy'] < 5000 + 2200 : # WIND
                mana -= 10
                return f"SPELL WIND {X(17630)} {Y(9000)}"

            elif i['shield'] == 0 and i['base_enemy'] < 5000 : # SHIELD
                mana -= 10
                return f"SPELL SHIELD {i['id']}"
            
            for e in enemies:
                if e['base_enemy'] < 8000 and hypot(hero[x] - e[x], hero[y] - e[y]) < 2200 and e['shield'] == 0 :
                    mana -= 10
                    return f"SPELL CONTROL {e['id']} {X(0)} {Y(0)}"

    
    
    for m in mons:
        if m['base_dist'] < 8000 : return f"MOVE {(17630 - m[x])} {9000 - m[y]}"

    return f"MOVE {def_x} {def_y}"



def is_enemy_attacked() :                               #
    for i in mons :                                     #
        if i['base_enemy'] < 5000 :                     #
            return True                                 # Checks if the my base or enemy base is getting attacked.
    return False                                        #
def is_attack() :                                       #
    for m in mons :                                     #
        if m['tf'] == 1 and m['base_dist'] < 5000:      #
            return True                                 #
    return False                                        #


def get_next(hero):
    global being_controlled, target
    global enemies, target, mana
    global x, y, busy

    near_base = float('inf')

    if (hero['id'] == 1 or hero['id'] == 4) :
        if not hero['id'] in busy : busy.append(hero['id'])
        taken1.clear()
        return attacker(hero)

    if mons == [] or hero['base_dist'] > 9000 :   # if there is no monsters aroun the heros
        if hero['id'] in busy : busy.remove(hero['id'])
        taken_remover(-1, hero)                     # moves to the default defensing positions.
        return default(hero)

    if hero['ctrled'] == 1 :
        busy.append(hero['id'])
        taken_remover(-1, hero)
        being_controlled = True                                                     #
    if  mana > 10 :                                                                 #
        for e in enemies:                                                           #
            if hypot(e[x] - hero[x], e[y] - hero[y]) < 2200 + 800 and being_controlled and hero['shield'] == 0: # Checks if the enemy used the control spell on my heros
                mana -= 10                                                          #   # and protect them with shield if so.
                return f"SPELL SHIELD {hero['id']}"                                 #
                                                                                    #

    for mon in mons :
        if is_my_target(mon['id'], hero):
            if (mon['base'] == 0 and is_attack()) or (mon['tf'] != 1 and rounds > 100) :
                if hero['id'] in busy : busy.remove(hero['id'])
                taken_remover(mon['id'], hero)
            elif mana > 10 and mon['base_dist'] < 3000 and hypot(mon[x] - hero[x], mon[y] - hero[y]) < 1280 and not mon['shield']:
                if hero['id'] in busy : busy.remove(hero['id'])
                taken_remover(mon['id'], hero)
                mana -= 10
                return f"SPELL WIND {X(17630)} {Y(9000)}"
            elif mana > 10 and mon['base_dist'] < 2500 and 800 < hypot(mon[x] - hero[x], mon[y] - hero[y]) < 2200 and not mon['shield'] and not mon['ctrled']:
                mana -= 10
                return f"SPELL CONTROL {mon['id']} {X(17630)} {Y(9000)}"
            if is_my_target(mon['id'], hero) : return f"MOVE {mon[x] + rand(-100, 100)} {mon[y]}"
        t = mon['base_dist']  # check is a valid target....                  #check is taken by another hero                              #check if that hero is enough                             
        if t < near_base and (mon['tf'] == 1 or rounds < 100) and ((not is_taken(mon['id'], hero) and is_closer(hero, mon)) or (mon['shield'] and mon['tf'] == 1 and t < 5500)) :
            near_base = t
            target = mon

    if target != {} and target['base_dist'] < 8000 and (target['tf'] == 1 or rounds < 100 or (target['shield'] and target['tf'] == 1)) and is_closer(hero, target):
        taken_remover(-1, hero)
        append_takens(target['id'], hero)
        busy.append(hero['id'])
        return f"MOVE {target[x] + rand(-100, 100)} {target[y]}"
    if hero['id'] in busy : busy.remove(hero['id'])
    return default(hero)

while True:
    mons = []
    heros = []
    enemies = []
    
    my_health, mana = [int(j) for j in input().split()]
    enemy_health, enemana = [int(j) for j in input().split()]

    entity_count = int(input())

    for i in range(entity_count):
        _id, _type, x_, y_, shield_life, is_controlled, health, vx, vy, near_base, threat_for = [int(j) for j in input().split()]
        tmp = {
            'id': _id,
            'type': _type,
            'x': x_,
            'y': y_,
            'shield': shield_life,
            'ctrled': is_controlled,
            'hp': health,
            'vx': vx,
            'vy': vy,
            'base': near_base,
            'tf': threat_for, 
            'base_dist': int(hypot(X(0) - x_, Y(0) - y_)),
            'base_enemy': int(hypot(x_ - X(17630), y_ - Y(9000)))
        }
        if (_type == 1) : heros.append(tmp)
        if (_type == 0) : mons.append(tmp)
        if (_type == 2) : enemies.append(tmp)
    for i in range(heroes_per_player): 
        print(f"{get_next(heros[i])}")
        if i == 2 :
            rounds += 1
            print("ROUNDS == ", rounds, file=err)
            print("MANA   == ", mana, file=err)
            print("HEALTH == ", enemy_health, file=err)
            print(busy, file=err)

