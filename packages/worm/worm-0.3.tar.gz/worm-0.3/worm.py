"""
    Crawling worms progress indicator
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Well, what can you say really? It's a crawling worm that animates when you
    call a certain function. Simple as that.

    How to use:

    .. code-block:: python

       import worm

       for datum_to_churn in data:
           worm.animate()
           churn_churn(datum_to_churn)
"""
__version__ = '0.3'

import sys
import time
from itertools import count

class WriggleWormBase(object):
    def __init__(self, velocity=10, world_length=79, outfile=sys.stderr):
        self.delta_t = 1./velocity
        self.ts = time.time()
        self.position = 0
        self.move = 0
        self.reverse = False
        self.animation_frame = 0
        self.world_length = world_length
        self.outfile = outfile

    def animate(self, outfile=None, force=False):
        if force:
            self.step()
            return

        if time.time() > self.ts + self.delta_t:
            self.ts = time.time()
            self.step(outfile)

    def step(self, outfile=None):
        if outfile is None:
            outfile = self.outfile

        if self.animation_frame == 4:
            if self.move == 3:
                self.animation_frame = 0
                self.move = 0
                if self.reverse:
                    self.position -= 4
                    if self.position == 0:
                        self.reverse = False
                else:
                    self.position += 4
                    if self.position + 4 + self.own_length > self.world_length:
                        self.reverse = True
            else:
                self.move += 1
        else:
            self.animation_frame += 1

        if self.reverse:
            if self.animation_frame == 4:
                worm = self.render(-self.animation_frame + self.move)
            else:
                worm = self.render(-self.animation_frame)
            pos = self.position - self.move
        else:
            if self.animation_frame == 4:
                worm = self.render(self.animation_frame - self.move)
            else:
                worm = self.render(self.animation_frame)
            pos = self.position + self.move

        lead = " " * pos
        trail = " " * (self.world_length - len(worm) - pos)
        self.outfile.write("\x1b[2K\r" + lead + worm + trail + "\r")
        self.outfile.flush()

class WormLook(WriggleWormBase):
    frames = [
        'O0OOooo....',  # left 4
        'oO0Ooooo...',  # left 3
        'ooO0Ooooo..',  # left 2
        '.ooO0Ooooo.',  # left 1
        '.oooO0Oooo.',  # mid
        '.ooooO0Ooo.',  # right 1
        '..ooooO0Ooo',  # right 2
        '...ooooO0Oo',  # right 3
        '....oooOO0O',  # right 4
    ]
    def render(self, frame, reverse=False):
        if reverse:
            return self.frames[4-frame]
        else:
            return self.frames[4+frame]

    own_length = len(frames[0])

class Worm(WormLook):
    """The default crawling worm, the one you very likely want to use.
    See module-level documentation.
    """

default_worm = Worm()
animate = default_worm.animate

if __name__ == "__main__":
    worm = Worm()
    animate = worm.animate
    while True:
        animate()
        time.sleep(.1)

