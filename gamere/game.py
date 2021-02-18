import pygame
import sys
import os
import cv2
from pygame.locals import *
from time import time
from warnings import warn
from PIL.Image import open
from matplotlib import pyplot as plt
from pygame.draw import *
try:
    from pylab import mpl
except (ImportError, ModuleNotFoundError):
    from matplotlib.pylab import mpl


__version__ = '0.0.1'


def init(**kwargs):
    """
    Init all
    """
    pygame.init()
    pygame.mixer.init(**kwargs)
    pygame.font.init()
    return kwargs


def _pass(*args, **kwargs):
    """
    Pass
    """
    return args, kwargs


class GamereError(Exception):
    def __init__(self, msg):
        self.msg = msg
        self.__doc__ = 'Gamere error'
    
    def __str__(self):
        return self.msg


class GamereWarning(Warning):
    def __init__(self, msg):
        self.msg = msg
        self.__doc__ = 'Gamere warning'
    
    def __str__(self):
        return self.msg
    

if sys.version_info.major != 3:
    warn(GamereWarning, 'Please use python 3.8 or above.')
if sys.version_info.minor < 8:
    warn(GamereWarning, 'Please use python 3.8 or above.')


class Window(object):
    def __init__(self, background='', title='gamere window', size=(1000, 1000), flags=0, depth=0,
                 display=0, fps=20, icon=None,
                 running=True, music=None, bgm=None,
                 texts=None):
        if texts is None:
            texts = []
        self.title = title
        self.width, self.height = size
        self.fps = fps
        if background == '':
            self.background = None
        else:
            try:
                self.background = pygame.image.load(background)
                self.background = pygame.transform.scale(self.background, size)
            except (Exception, Warning):
                raise GamereError('invalid background')
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(size, flags, depth, display)
        self.running = running
        self.rectangle = self.screen.get_rect()
        self.music = music if bgm is None else bgm
        self.rates = 0
        self.texts = texts
        self.insleep = False
        self.fatime = 0
        self.beginfa = time()
        
        pygame.display.set_caption(self.title)
        if icon is not None:
            pygame.display.set_icon(pygame.image.load(icon))
    
    def __str__(self):
        return 'gamere.cpp.Window'
    
    def sleep(self, secs=0.1):
        self.fatime = secs
        self.insleep = True
        self.beginfa = time()
    
    def quit(self, *args, **kwargs):
        pygame.quit()
        sys.exit(*args, **kwargs)
        return args[0]
    
    def destroy(self, code, /):
        return self.quit(code)
    
    def spat(self):
        self.running = False
    
    def get(self):
        return self.screen
    
    def loop(self, handler=_pass, render=_pass, update=_pass, last=_pass,
             start=init, mode=False, press=False, font=None, size=16,
             fwidth=16, fheight=16, loops=0, maxtime=0):
        start()
        while self.running:
            now = time()
            if self.insleep:
                if now + self.fatime >= self.beginfa:
                    self.insleep = False
            self.rates += 1
            self.clock.tick(self.fps)
            if self.background is not None:
                self.screen.blit(self.background, (0, 0))
            render()
            if self.music is not None:
                pygame.mixer.Sound(self.music).play(loops, )
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.quit()
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.quit()
                if not self.insleep:
                    if mode:
                        handler(event, pygame.key.get_mods())
                    elif press:
                        handler(event, pygame.key.get_pressed())
                    else:
                        handler(event)
            if not self.insleep:
                update()
                if self.texts:
                    for row, i in enumerate(self.texts):
                        for column, j in enumerate(i):
                            if j is None:
                                continue
                            text = Text(font, self, size=size, text=str(j),
                                        x=row * fwidth, y=column * fheight)
                            text.update()
            pygame.display.update()
        last()
        return 'Game Over'
    
    def blit(self, image, x, y, rect=False, draw=False):
        if rect:
            image.rect.centerx, image.rect.centery = x, y
            image.draw()
        elif draw:
            self.window.screen.blit(image.image, (x, y))
        else:
            self.window.screen.blit(image, (x, y))
    
    def rect(self):
        return self.rectangle
    
    def settext(self, texts, /):
        self.texts = texts


class Layout(object):
    def __init__(self, layout, /):
        self.layout = layout
    
    def __iter__(self):
        return self.layout
    
    def __str__(self):
        return self.layout.__str__()
    
    def loop(self, window: Window, width=40, height=40, rect=False, draw=False, warning=True, **kwargs):
        def show():
            for row, i in enumerate(self.layout):
                for column, j in enumerate(i):
                    if rect:
                        j.draw()
                    elif draw:
                        window.screen.blit(j.image, (row * width, column * height))
                    else:
                        window.screen.blit(j, (row * width, column * height))
        
        if (not draw) and warning:
            warn('draw is false', GamereWarning)
        return window.loop(render=show, **kwargs)
    
    def find(self, target, judge=True):
        for row, i in enumerate(self.layout):
            for column, j in enumerate(i):
                if j == target and judge:
                    return row, column
                if j is target and not judge:
                    return row, column
        raise GamereError(f'target {target} not found')
    
    def get(self, pos, /):
        try:
            return self.layout[pos[0]][pos[1]]
        except IndexError:
            raise GamereError(f'index{pos} out of range')
    
    def value(self):
        return self.layout
    
    def set(self, value, /):
        self.layout = value
    
    def __copy__(self):
        return self.layout[:]
    
    def __deepcopy__(self, memodict={}, /):
        return [i[:] for i in self.layout]
    
    def copy(self):
        return self.__copy__()
    
    def deepcopy(self, memodict=None, /):
        if memodict is None:
            memodict = {}
        return self.__deepcopy__(memodict)


class Image(object):
    def __init__(self, path, size=(40, 40), center=(0, 0), look=True, opencv=True,
                 flags=None):
        self.path = path
        self.size = size
        self.image = pygame.image.load(path)
        self.image = pygame.transform.scale(self.image, self.size)
        self.rect = self.image.get_rect()
        self.rect.centerx, self.rect.centery = center
        if look:
            self.pillow = open(path)
        if opencv:
            self.opencv = cv2.imread(path, flags=flags)
            if self.opencv is None:
                raise GamereError('invalid opencv-python image path')
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)
    
    def width(self):
        return self.size[0]
    
    def height(self):
        return self.size[1]
    
    def render(self, window: Window):
        window.screen.blit(self.image, self.rect)
    
    def setpos(self, pos):
        self.rect.centerx, self.rect.centery = pos
    
    def getpos(self):
        return self.rect.centerx, self.rect.centery
    
    def getsize(self):
        return self.size

    def plot(self, text='', font='FangSong', fontdb='font.sans-serif',
                encodedb='axes.unicode_minus', title=''):
        mpl.rcParams[fontdb] = [font]
        mpl.rcParams[encodedb] = False
        plt.figure().canvas.set_window_title(title)
        plt.title(text)
        plt.imshow(self.pillow)
        plt.show()
        
    def pil(self):
        self.pillow.show()
        
    def cvshow(self, delay=0, title=''):
        cv2.imshow(title, self.opencv)
        cv2.waitKey(delay)
        cv2.destroyAllWindows()


class Text(object):
    def __init__(self, font, window: Window, size=16, text='', color=(0, 0, 0),
                 antialias=True, x=0, y=0):
        self.font = pygame.font.Font(font, size)
        self.window = window
        self.antialias = antialias
        self.color = color
        self.text = self.font.render(text, self.antialias, self.color)
        self.redo(text)
        self.x, self.y = x, y
    
    def __str__(self):
        return self.text
    
    def __missing__(self, key):
        raise GamereError(f'key {key} not found')
    
    def __getitem__(self, item):
        warn('not use __getitem__, use pos()', GamereWarning)
        return dir(self)[item]
    
    def pos(self):
        return self.x, self.y
    
    def update(self):
        self.window.screen.blit(self.text, (self.x, self.y))
    
    def redo(self, text):
        self.text = self.font.render(text, self.antialias, self.color)


class Timer(object):
    def __init__(self):
        self.start = time()
    
    def get(self):
        return time() - self.start
    
    def timer(self, mode=2):
        return round(time() - self.start, mode)
    
    def __int__(self):
        return self.timer().__int__()
    
    def __float__(self):
        return self.get()
    
    def __str__(self):
        return self.get().__str__()


class Mouse(object):
    def __init__(self, **kwargs):
        self.mouse = pygame.mouse
    
    def getx(self):
        return self.mouse.get_pos()[0]
    
    def gety(self):
        return self.mouse.get_pos()[1]
    
    def pos(self):
        return self.mouse.get_pos()
    
    def __str__(self):
        return str(self.pos())
    
    def __iter__(self):
        return self.pos()
    
    def __bool__(self):
        return True


class LeftImage(Image):
    def setpos(self, pos):
        self.rect.left, self.rect.top = pos
        
        
class RightImage(Image):
    def setpos(self, pos):
        self.rect.right, self.rect.bottom = pos
