import pygame


class QuadTree:
    MAX_OBJECTS = 5
    MAX_LEVELS = 5

    def __init__(self, level, rect):
        self.level = level
        self.objects = []
        self.rect = rect
        self.nodes = [None, None, None, None]

    def clear(self):
        self.objects = []
        for i in range(4):
            if self.nodes[i] is not None:
                self.nodes[i].clear()
                self.nodes[i] = None

    def split(self):
        x, y, w, h = self.rect
        sub_w = w // 2
        sub_h = h // 2

        self.nodes[0] = QuadTree(self.level+1, pygame.Rect(x,       y,       sub_w, sub_h))
        self.nodes[1] = QuadTree(self.level+1, pygame.Rect(x+sub_w, y,       sub_w, sub_h))
        self.nodes[2] = QuadTree(self.level+1, pygame.Rect(x,       y+sub_h, sub_w, sub_h))
        self.nodes[3] = QuadTree(self.level+1, pygame.Rect(x+sub_w, y+sub_h, sub_w, sub_h))

    def get_index(self, rect):
        index = -1
        x, y, w, h = self.rect
        vertical_mid = x + w // 2
        horizontal_mid = y + h // 2

        top = rect.top < horizontal_mid and rect.bottom < horizontal_mid
        bottom = rect.top > horizontal_mid

        if rect.left < vertical_mid and rect.right < vertical_mid:
            if top:
                index = 0
            elif bottom:
                index = 2
        elif rect.left > vertical_mid:
            if top:
                index = 1
            elif bottom:
                index = 3

        return index

    def insert(self, obj):
        if self.nodes[0] is not None:
            index = self.get_index(obj.rect)
            if index != -1:
                self.nodes[index].insert(obj)
                return

        self.objects.append(obj)

        if len(self.objects) > QuadTree.MAX_OBJECTS and self.level < QuadTree.MAX_LEVELS:
            if self.nodes[0] is None:
                self.split()

            i = 0
            while i < len(self.objects):
                index = self.get_index(self.objects[i].rect)
                if index != -1:
                    self.nodes[index].insert(self.objects.pop(i))
                else:
                    i += 1

    def retrieve(self, rect):
        index = self.get_index(rect)
        result = list(self.objects)

        if self.nodes[0] is not None:
            if index != -1:
                result.extend(self.nodes[index].retrieve(rect))
            else:
                for node in self.nodes:
                    result.extend(node.retrieve(rect))

        return result
