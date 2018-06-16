import sys
import math
import os


stream = None if len(sys.argv) < 2 else open(sys.argv[1])
def inputr():
    if len(sys.argv) > 1:
        return stream.readline().strip()
    return input()


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def sibling_candidates(self):
        yield Point(self.x-1, self.y)
        yield Point(self.x, self.y-1)
        yield Point(self.x+1, self.y)
        yield Point(self.x, self.y+1)

    def sibling(self):
        yield from (x for x in self.sibling_candidates() if x.valid)

    def sibling_passable(self):
        yield from (x for x in self.sibling() if not x.wall)

    @property
    def valid(self):
        return (self.x>=0 and self.y>=0 and self.x<field.width and self.y<field.height)

    @property
    def wall(self):
        return field.lines[self.y][self.x] == '#'

    def distance_to(self, target):
        # Manhattan distance
        return abs(target.x - self.x) + abs(target.y - self.y)

    def __repr__(self):
        return str((self.x, self.y))


class Entity(Point):
    def __init__(self, id_, x, y, param_0, param_1, param_2):
        super().__init__(x, y)
        self.id = id_
        self.param_0 = param_0
        self.param_1 = param_1
        self.param_2 = param_2


class Explorer(Entity):
    def __init__(self, id_, x, y, param_0, param_1, param_2):
        super().__init__(id_, x, y, param_0, param_1, param_2)
        self.sanity = self.param_0
        self.plan = False

    def turn(self, enemies, explorers):
        # Write an action using print
        # To debug: print("Debug messages...", file=sys.stderr)
        # my_wanderers.sort(key=lambda x: x.distance_to_target)

        # MOVE <x> <y> | WAIT
        if not len(explorers):
            return 'MOVE {} {}'.format(0, 0)
        if not enemies:
            return 'WAIT'
        enemies = sorted(enemies, key=lambda x: x.distance_to(self))
        if enemies[0].distance_to(self) > 1:
            neare = list(filter(lambda x: x.distance_to(self)<4, enemies))
            if len(neare) > 1:
                if self.param_2 > 0:
                    return 'LIGHT'
        if enemies[0].distance_to(self) < 5:
            danger = enemies[0]
            candidates = self.sibling_passable()
            target = sorted(candidates, key=lambda x: -x.distance_to(danger))[0]
            return 'MOVE {} {}'.format(target.x, target.y)
            # target_x = self.x + (self.x - enemies[0].x)*2
            # target_y = self.y + (self.y - enemies[0].y)*2
            # return max(0, min(target_x, field.width)), max(0, min(target_y, field.height))
        elif self.sanity < 200:
            return 'PLAN'
        return 'MOVE {} {}'.format(sum(e.x for e in explorers)//len(explorers), sum(e.y for e in explorers)//len(explorers))


class Field:
    def __init__(self, lines):
        self.lines = lines

    @property
    def width(self):
        return len(self.lines[0])

    @property
    def height(self):
        return len(self.lines)

    def route(self, start, end):
        import pdb; pdb.set_trace()

    def __str__(self):
        return os.linesep.join(self.lines)


class Wanderer(Entity):
    def __init__(self, id_, x, y, param_0, param_1, param_2):
        super().__init__(id_, x, y, param_0, param_1, param_2)
        self.time_before_spawn_recalled = self.param_0
        self.state = self.param_1
        self.target = self.param_2
        self.target_entity = None

    @property
    def is_wandering(self):
        return self.state == 1

    @property
    def is_spawning(self):
        return self.state == 0

    @property
    def has_target(self):
        return self.target != -1


def create_entity(entity_type, id_, x, y, param_0, param_1, param_2):
    args = id_, x, y, param_0, param_1, param_2
    if entity_type == 'EXPLORER':
        return Explorer(*args)
    elif entity_type in ('WANDERER', 'SLASHER'):
        return Wanderer(*args)


# Survive the wrath of Kutulu
# Coded fearlessly by JohnnyYuge & nmahoude (ok we might have been a bit scared by the old god...but don't say anything)

width = int(inputr())
height = int(inputr())
print(width, file=sys.stderr)
print(height, file=sys.stderr)

LEFT_UPPER = "0 0"
LEFT_LOWER = "0 {}".format(height)
RIGHT_UPPER = "{} 0".format(width)
RIGHT_LOWER = "{} {}".format(width, height)

field = Field([inputr() for i in range(height)])
print(field, file=sys.stderr)
# sanity_loss_lonely: how much sanity you lose every turn when alone, always 3 until wood 1
# sanity_loss_group: how much sanity you lose every turn when near another player, always 1 until wood 1
# wanderer_spawn_time: how many turns the wanderer take to spawn, always 3 until wood 1
# wanderer_life_time: how many turns the wanderer is on map after spawning, always 40 until wood 1
sanity_loss_lonely, sanity_loss_group, wanderer_spawn_time, wanderer_life_time = [int(i) for i in inputr().split()]
print(sanity_loss_lonely, sanity_loss_group, wanderer_spawn_time, wanderer_life_time, file=sys.stderr)
# game loop
while True:
    # print(field, file=sys.stderr)
    entity_count = int(inputr())  # the first given entity corresponds to your explorer
    print(entity_count, file=sys.stderr)
    entities = []
    plan = False
    for i in range(entity_count):
        entity_type, *params = inputr().split()
        print(entity_type, *params, file=sys.stderr)
        if entity_type in ('EFFECT_PLAN', 'EFFECT_LIGHT', 'EFFECT_SHELTER', 'EFFECT_YELL'):
            if entity_type == 'EFFECT_PLAN':
                plan = True
            continue
        id_, x, y, param_0, param_1, param_2 = list(map(int, params))
        entities.append(
            create_entity(entity_type, id_, x, y, param_0, param_1, param_2)
        )
    entities_map = {e.id: e for e in entities}
    i_am, entities = entities[0], entities[1:]

    enemies = []
    explorers = []

    for entity in entities:
        if isinstance(entity, Wanderer):
            # Sets targets for Wanderers
            entity.target_entity = entities_map.get(entity.target, None)
            enemies.append(entity)
        if isinstance(entity, Explorer):
            entity.plan = plan
            explorers.append(entity)

    # print(field.route(i_am, Point(0, 0)))
    if len(sys.argv) > 2:
        import pdb; pdb.set_trace()
    print(i_am.turn(enemies, explorers))
