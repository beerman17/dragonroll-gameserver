
# Users

USERNAME_IS_NOT_UNIQUE = 'Username is not unique'


class CharacterErrorsDetails:
    CHARACTER_NOT_FOUND = 'No character with specified id'


class GameErrorsDetails:
    USER_IS_NOT_GM = 'The user is not the game master of the game'
    CHARACTER_ALREADY_USED = 'Provided character already participates another game'


character_errors = CharacterErrorsDetails()
game_errors = GameErrorsDetails()
