import pygame

class QuadTree:
    MAX_OBJECTS = 6
    MAX_LEVELS = 5

    def __init__(self, level, rect):
        self.level = level
        self.rect = rect
        self.objects = []
        self.nodes = [None] * 4

    def clear(self):
        self.objects.clear()
        for i in range(4):
            if self.nodes[i]:
                self.nodes[i].clear()
                self.nodes[i] = None

    def split(self):
        x, y, w, h = self.rect
        sw, sh = w // 2, h // 2

        self.nodes[0] = QuadTree(self.level+1, pygame.Rect(x,     y,     sw, sh))
        self.nodes[1] = QuadTree(self.level+1, pygame.Rect(x+sw, y,     sw, sh))
        self.nodes[2] = QuadTree(self.level+1, pygame.Rect(x,     y+sh, sw, sh))
        self.nodes[3] = QuadTree(self.level+1, pygame.Rect(x+sw, y+sh, sw, sh))

    def get_index(self, rect):
        index = -1

        x, y, w, h = self.rect
        vm = x + w // 2
        hm = y + h // 2

        top = rect.bottom < hm
        bottom = rect.top > hm
        left = rect.right < vm
        right = rect.left > vm

        if left:
            if top: index = 0
            elif bottom: index = 2
        elif right:
            if top: index = 1
            elif bottom: index = 3

        return index

    def insert(self, obj):
        if self.nodes[0]:
            idx = self.get_index(obj.rect)
            if idx != -1:
                self.nodes[idx].insert(obj)
                return

        self.objects.append(obj)

        if len(self.objects) > QuadTree.MAX_OBJECTS and self.level < QuadTree.MAX_LEVELS:
            if not self.nodes[0]:
                self.split()

            i = 0
            while i < len(self.objects):
                idx = self.get_index(self.objects[i].rect)
                if idx != -1:
                    self.nodes[idx].insert(self.objects.pop(i))
                else:
                    i += 1

    def retrieve(self, rect):
        idx = self.get_index(rect)
        res = list(self.objects)

        if self.nodes[0]:
            if idx != -1:
                res.extend(self.nodes[idx].retrieve(rect))
            else:
                for node in self.nodes:
                    res.extend(node.retrieve(rect))

        return res
    
CELL_SIZE = 64
CELL_THRESHOLD = 20   # Une cellule passe en QuadTree si elle dépasse ce nombre

def get_cell(pos):
    return (pos[0] // CELL_SIZE, pos[1] // CELL_SIZE)

class SpatialGrid:
    def __init__(self):
        self.cells = {}  # (cx, cy): { "entities": [...], "qt": QuadTree }

    def clear(self):
        for cell in self.cells.values():
            cell["entities"].clear()
            cell["qt"] = None

    def insert(self, entity):
        cx, cy = get_cell(entity.rect.center)

        if (cx, cy) not in self.cells:
            self.cells[(cx, cy)] = {
                "entities": [],
                "qt": None
            }

        self.cells[(cx, cy)]["entities"].append(entity)

    def update_quadtrees(self):
        for (cx, cy), cell in self.cells.items():
            entities = cell["entities"]

            if len(entities) > CELL_THRESHOLD:
                x = cx * CELL_SIZE
                y = cy * CELL_SIZE

                qt = QuadTree(0, pygame.Rect(x, y, CELL_SIZE, CELL_SIZE))

                for e in entities:
                    qt.insert(e)

                cell["qt"] = qt
            else:
                cell["qt"] = None

    def get_candidates(self, entity):
        cx, cy = get_cell(entity.rect.center)

        if (cx, cy) not in self.cells:
            return []

        cell = self.cells[(cx, cy)]

        # Si QuadTree local activé -> utiliser QuadTree
        if cell["qt"] is not None:
            return cell["qt"].retrieve(entity.rect)

        # Sinon -> liste simple
        return cell["entities"]