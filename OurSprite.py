'''
class OurSprite (save to separate file OurSprite.py)
properties owned:
symbol - that represents it in the tile map such as letter 'C'
filename - string name of PNG image file that we load
pygameSprite - Pygame Sprite object used to blit

behaviors:
init - receive arguments for symbol, filename, and pygame sprite.
Assign values to respective properties.
Assume given Pygame sprite object has been loaded.

getSymbol - Receives nothing. Return symbol.

getFilename - Receives nothing. Return filename

getPygameSprite - Receives nothing. Return pygameSprite so Pygame can blit it.
'''

import pygame

class OurSprite:

    def __init__(self, symbol, filename, pygameSprite):

        self.symbol = symbol
        self.filename = filename
        self.pygameSprite = pygameSprite

    '''
    Gets the symbol for the object.
    @return: object's symbol
    '''
    def getSymbol(self):

        return self.symbol

    '''
    Gets the filename for the object.
    @return: object's filename
    '''
    def getFilename(self):

        return self.filename

    '''
    Gets the pygame sprite for the object.
    @return: object's pygame sprite
    '''
    def getPygameSprite(self):

        return self.pygameSprite
