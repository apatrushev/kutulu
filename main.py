import sys
import math


class Entity:
    def __init__(self, id_, x, y, param_0, param_1, param_2):
        self.id = int(id_)
        self.x = int(x)
        self.y = int(y)
        self.param_0 = int(param_0)
        self.param_1 = int(param_1)
        self.param_2 = int(param_2)


class Explorer(Entity):
    def __init__(self, id_, x, y, param_0, param_1, param_2):
        super().__init__(id_, x, y, param_0, param_1, param_2)
        self.sanity = self.param_0

    def move_to(self, wanderer):
        return RIGHT_LOWER


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

width = int(input())
height = int(input())
print(width, file=sys.stderr)
print(height, file=sys.stderr)

LEFT_UPPER = "0 0"
LEFT_LOWER = "0 {}".format(height)
RIGHT_UPPER = "{} 0".format(width)
RIGHT_LOWER = "{} {}".format(width, height)

field = [input() for i in range(height)]
print(field, file=sys.stderr)
# sanity_loss_lonely: how much sanity you lose every turn when alone, always 3 until wood 1
# sanity_loss_group: how much sanity you lose every turn when near another player, always 1 until wood 1
# wanderer_spawn_time: how many turns the wanderer take to spawn, always 3 until wood 1
# wanderer_life_time: how many turns the wanderer is on map after spawning, always 40 until wood 1
sanity_loss_lonely, sanity_loss_group, wanderer_spawn_time, wanderer_life_time = [int(i) for i in input().split()]
print(sanity_loss_lonely, sanity_loss_group, wanderer_spawn_time, wanderer_life_time, file=sys.stderr)
# game loop
while True:
    # print(field, file=sys.stderr)
    entity_count = int(input())  # the first given entity corresponds to your explorer
    entities = []
    for i in range(entity_count):
        entity_type, *params = input().split()
        print(entity_type, *params, file=sys.stderr)
        id_, x, y, param_0, param_1, param_2 = list(map(int, params))
        entities.append(
            create_entity(entity_type, id_, x, y, param_0, param_1, param_2)
        )
    print(entities)
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

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr)
    my_wanderers.sort(key=lambda x: x.distance_to_target)

    # MOVE <x> <y> | WAIT
    if len(my_wanderers):
        move_to = i_am.move_to(my_wanderers[0])
        print("MOVE {}".format(move_to))
    else:
        print("WAIT")
