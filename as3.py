import random
import time

# universe size
# Setting objects regarding universe size
# X and Y use the random function to give a random starting position for the enterprise

WIDTH = 12
HEIGHT = 9
X = random.randint(0, WIDTH - 1)
Y = random.randint(0, HEIGHT - 1)

# objects
# used assignment 4 major spoilers (https://pages.cpsc.ucalgary.ca/~aycock/217/as3.html)

EMPTY = '.'
ENTERPRISE = 'E'
KLINGON = 'K'
STAR = '*'
enterprise_energy = 125
klingons = {}
stars = []

# functions
# defining a function that randomly generates coordinates within our universes bounds
# if the positions generated are the same as the ones created for the enterprise re-generate

def random_position():
    rand_x = random.randint(0, WIDTH - 1)
    rand_y = random.randint(0, HEIGHT - 1)
    while rand_x == X and rand_y == Y:
        rand_x = random.randint(0, WIDTH - 1)
        rand_y = random.randint(0, HEIGHT - 1)
    return rand_x, rand_y

# printing 2D list to create map

def map_print(p_map):
    for h in p_map:
        for w in h:
            print(w, end=' ')
        print()

# defining a function that checks if a klingon is within 2 units of the enterprise
# if they are in range they shoot with a 42% chance of hitting (21 / 50)
# randomly generating a random integer to use as the damage of the attack
# if they hit the enterprise print klingon location and the remaining energy of the enterprise
# if they miss print where the klingon is and that they missed

def klingon_range():
    global enterprise_energy
    for i in range(-2, 3):
        t_x = i + X
        for p in range(-2, 3):
            t_y = p + Y
            if (t_y, t_x) in klingons:
                klingon_shoot = random.randint(0, 50)
                if klingon_shoot <= 21:
                    enterprise_energy = enterprise_energy - random.randint(5, 10)
                    print('The Klingon at', (t_x, t_y), 'fired and hit! \nenergy remaining: ', enterprise_energy)
                else:
                    print('The Klingon at', (t_x, t_y), 'fired and missed!')

# bounds check function to limit the enterprise going in unwanted positions
# first bounds check on x and y is to keep the enterprise from looping around
# then checking if the movement is blocked by a star
# lastly checking if the space is a klingon in which place the boop command is run
# if klinon health is greater then 0 return the variable if it is below 0 pop it off the dictionary

def bounds_check(p_x, p_y):
    global X
    global Y

    if X + p_x >= WIDTH or X + p_x <= -1:
        print('cant move there')
        return
    if Y + p_y >= HEIGHT or Y + p_y <= -1:
        print('cant move there')
        return
    if (p_x + X, p_y + Y) in stars:
        print('star in the way')
        return
    if (p_y + Y, p_x + X) in klingons:
        boop = random.randint(23, 28)
        klingons[p_y + Y, p_x + X] = klingons[p_y + Y, p_x + X] - boop
        if klingons[p_y + Y, p_x + X] > 0:
            return
        klingons.pop((p_y + Y, p_x + X))
        print('klingon destroyed')
# making it so movements don't leave a trace of 'E's

    map[Y][X] = "."
    X = p_x + X
    Y = p_y + Y
    map[Y][X] = 'E'

    print(klingons)
# map
# used assignment 3 major spoilers (https://pages.cpsc.ucalgary.ca/~aycock/217/as3.html)

map = []
for y in range(HEIGHT):
    map.append([EMPTY] * WIDTH)

# aliases
# wrote aliases as we did in the adventure game

ALIASES = {
    'exit': 'quit',
    'q': 'quit',
    'n': 'north',
    's': 'south',
    'w': 'west',
    'e': 'east',
}
# stars and klingons
# calling the random_position function to generate 10 stars on putting them onto the map
# checking if two stars are generated in the same spot
# if so repeat the function until there arent repeats

for _ in range(10):
    star = random_position()
    map[star[1]][star[0]] = '*'
    while star in stars:
        star = random_position()
        map[star[1]][star[0]] = '*'
    stars.append(star)

# Using the same random_position function to generate 4 klingons and putting them onto the map
# checking if the klingon position is a previously generated star or klingon
# if so repeating the function until they all have individual coordinates

for _ in range(4):
    K = random_position()
    while K in stars:
        K = random_position()
    map[K[1]][K[0]] = 'K'
    while K in klingons:
        K = random_position()
        map[K[1]][K[0]] = 'K'

# assigning klingon coordinates to 50 energy each

    klingons[K[1], K[0]] = 50

# commands
# putting the enterprise on the map

map[Y][X] = "E"

# calling the function for klingons to attack

klingon_range()
map_print(map)

while True:

# setting cmd variable to the input and making it so the input isn't case sensitive
# (also took this from the adventure game shown in class)

    cmd = input('command: ')
    cmd = cmd.strip()
    cmd = cmd.lower()

# testing if an alias is been inputted

    if cmd in ALIASES:
        cmd = ALIASES[cmd]

# destruct command using time function

    if cmd == 'destruct':
        print('5 ...')
        time.sleep(1)
        print('4 ...')
        time.sleep(1)
        print('3 ...')
        time.sleep(1)
        print('2 ...')
        time.sleep(1)
        print('1 ...')
        time.sleep(1)
        print('*** the Enterprise has self-destructed ***')
        break

# testing to see the enterprise has 0 health or lower

    if enterprise_energy <= 0:
        break

# using bound_check function for movement

    elif cmd == 'north':
        bounds_check(0, -1)
    elif cmd == 'south':
        bounds_check(0, 1)
    elif cmd == 'east':
        bounds_check(1, 0)
    elif cmd == 'west':
        bounds_check(-1, 0)
    elif cmd == 'quit':
        break

# checking for incorrect input

    else:
        print("i don't know that command")
        continue

# calling the klingon function again but this time inside the loop
# as in the demo the klingon's attack as soon as the game starts if within range

    klingon_range()
    map_print(map)

# checking if all klingons are destroyed if so you win and the game ends

    if len(klingons) == 0:
        print('YOU WIN!')
        break
print('GAME OVER')