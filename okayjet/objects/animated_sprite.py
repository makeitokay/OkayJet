import pygame

from .gameobject import GameObject


def cut_sheet(sheet, columns, rows, rect):
    frames = []
    for j in range(rows):
        for i in range(columns):
            frame_location = (rect.w * i, rect.h * j)
            frames.append(sheet.subsurface(pygame.Rect(frame_location, rect.size)))
    return frames


class AnimatedSprite(GameObject):
    COLUMNS = 1
    ROWS = 1
    FRAMES_CHANGING = 150

    def __init__(self, game, pos):
        super().__init__(game, pos)
        self.rect = pygame.Rect(*pos, self.image.get_width() // self.COLUMNS,
                                self.image.get_height() // self.ROWS)
        self.frames = cut_sheet(self.image, self.COLUMNS, self.ROWS, self.rect)
        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.next_frame = pygame.time.get_ticks()

    def update(self):
        super().update()

        if pygame.time.get_ticks() > self.next_frame:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]
            self.next_frame += self.FRAMES_CHANGING
