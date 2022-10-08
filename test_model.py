from app.database import init_database
from app.models import Session
from app.models.user import User
from app.models.character import Character
from app.models.game import Game, GameJoinRequest
from app.schemas.character import CharacterPublicScheme


database.init_database()


def test(db=Session()):
    player_name = 'player1'
    game_master_name = 'gm_player'
    char1_name = 'Daivor Lightbringer'
    char2_name = 'Kryll the Monk'

    users = db.query(User).all()

    # create user 1
    user1 = User(username=player_name)
    db.add(user1)
    db.flush()

    # user 1 create character
    ch1 = Character(name=char1_name, biography='Paladin')
    ch2 = Character(name=char2_name, biography='Very odd monk')
    # user1.characters.append(ch1)
    # user1.characters.append(ch2)
    user1.characters.extend([ch1, ch2])
    # create user 2
    if (user2 := db.query(User).filter(User.username == game_master_name).first()) is None:
        user2 = User(username=game_master_name)

    # user 2 create game A
    user2.games.append(
        Game()
    )
    db.add(user2)
    db.flush()

    ch1.load()
    ch2.load()

    # get game id
    game = user2.games[0]

    # user 1 join game A

    join_request = GameJoinRequest(
        user_id=user1.user_id,
        game_id=game.game_id,
        character_id=user1.characters[0].character_id,
        message='Wanna play? Lets PLAY!'
    )
    db.add(join_request)
    db.flush()

    db.commit()

    users = db.query(User).all()

    # user 2 approves user's 1 request
    requests = db.query(GameJoinRequest).all()
    for r in requests:
        r.status_code = 2
        # db.add(r)

    # append character to game
    game.characters.append(ch1)

    db.commit()

    users = db.query(User).all()

    character = user1.characters[0]
    character.load()

    character_dict = CharacterPublicScheme.from_orm(character)

    return


if __name__ == '__main__':
    test()
