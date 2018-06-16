import sys
import math


stream = None if len(sys.argv) < 2 else open(sys.argv[1])
def inputr():
    if len(sys.argv) > 1:
        return stream.readline().strip()
    return input()


class Entity:
    def __init__(self, id_, x, y, param_0, param_1, param_2):
        self.id = id_
        self.x = x
        self.y = y
        self.param_0 = param_0
        self.param_1 = param_1
        self.param_2 = param_2


class Explorer(Entity):
    def __init__(self, id_, x, y, param_0, param_1, param_2):
        super().__init__(id_, x, y, param_0, param_1, param_2)
        self.sanity = self.param_0

    def move_to(self, wanderers, explorers):
        # Write an action using print
        # To debug: print("Debug messages...", file=sys.stderr)
        # my_wanderers.sort(key=lambda x: x.distance_to_target)

        # MOVE <x> <y> | WAIT
        return sum(e.x for e in explorers)//3, sum(e.y for e in explorers)//3


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

    @property
    def distance_to_target(self):
        # Manhattan distance
        return abs(self.target_entity.x - self.x) + abs(self.target_entity.y - self.y)


def create_entity(entity_type, id_, x, y, param_0, param_1, param_2):
    args = id_, x, y, param_0, param_1, param_2
    if entity_type == 'EXPLORER':
        return Explorer(*args)
    elif entity_type == 'WANDERER':
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

field = [inputr() for i in range(height)]
for l in field:
    print(l, file=sys.stderr)
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
    for i in range(entity_count):
        entity_type, *params = inputr().split()
        print(entity_type, *params, file=sys.stderr)
        id_, x, y, param_0, param_1, param_2 = list(map(int, params))
        entities.append(
            create_entity(entity_type, id_, x, y, param_0, param_1, param_2)
        )
    entities_map = {e.id: e for e in entities}
    i_am, entities = entities[0], entities[1:]

    my_wanderers = []
    wanderers = []
    explorers = []

    for entity in entities:
        if isinstance(entity, Wanderer) and entity.has_target:
            # Sets targets for Wanderers
            entity.target_entity = entities_map[entity.target]
            if entity.target == i_am.id:
                my_wanderers.append(entity)
            wanderers.append(entity)
        if isinstance(entity, Explorer):
            explorers.append(entity)

    if len(sys.argv) > 1:
        import pdb; pdb.set_trace()
    move_to = i_am.move_to(my_wanderers, explorers)
    print("MOVE {} {}".format(*move_to))
