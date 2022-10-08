"""
Utils
"""
from random import randint


class CharacterAbilities:
    """
    Class is used for calculating characters stats

    hp - Hit Points
    ac - Armor Class

    str - Strength
    dex - Dexterity
    con - Constitution
    int - Intelligence
    wis - Wisdom
    cha - Charisma
    """

    def __init__(self, character_id):
        """
        Get character abilities values
        :param character_id:
        """
        self.__character_id = character_id
        self._ab_hp = 0
        self._ab_ac = 0
        self._ab_str = 0
        self._ab_dex = 0
        self._ab_con = 0
        self._ab_int = 0
        self._ab_wis = 0
        self._ab_cha = 0
        self.__set_random()

    def __set_random(self):
        for attr in [ability for ability in self.__dict__ if ability.startswith('_ab_')]:
            setattr(self, attr, randint(10, 18))

    @property
    def hp(self):
        return self._ab_hp

    @property
    def ac(self):
        return self._ab_ac

    @property
    def str(self):
        return self._ab_str

    @property
    def dex(self):
        return self._ab_dex

    @property
    def con(self):
        return self._ab_con

    @property
    def int(self):
        return self._ab_wis

    @property
    def cha(self):
        return self._ab_cha


if __name__ == '__main__':

    abilities = CharacterAbilities(1)

    pass
