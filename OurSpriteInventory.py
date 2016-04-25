'''
class OurSpriteInventory (save to separate file OurSpriteInventory.py)

properties:
sprites - list of OurSprite objects

behaviors:
init - create an empty Python list() or [].

addSprite - receive an OurSprite object (assume it has been fully initalized)
append it to end of sprites list and return True

getBySymbol - receive a character symbol
return OurSprite object whose symbol property matches given symbol;
else, return None if not found. Perform case sensitive string compare.

getNumSprites - receives nothing. Returns number of OurSprites in this inventory.
'''

import pygame

class OurSpriteInventory:

    def __init__(self):

        self.sprites = []

    '''
    Adds the sprite to the inventory.
    @param: sprite - a fully initialzied pygame OurSprite object
    @return: True that the function completed
    '''
    def addSprite(self, sprite):

        self.sprites.append(sprite)
        return True

    '''
    Gets the OurSprite object that matches a provided symbol.
    @param: symbol - the symbol to search for in the list of OurSprite objects
    @return: OurSprite object that matches the provided symbol; None otherwise
    '''
    def getBySymbol(self, symbol):

        for i in self.sprites:
            if i.getSymbol() == symbol:
                return i
        return None

    '''
    Gets the number of OurSprite objects in the list.
    @return: number of OurSprite objects
    '''
    def getNumSprites(self):

        return len(self.sprites)
