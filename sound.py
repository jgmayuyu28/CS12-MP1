import pyxel
class PyxelSounds:

    TIMEOUT = 60

    def __init__(self):

        self.framestamp = 0


    def play_sound(self, snd):

        pyxel.play(0, snd)
