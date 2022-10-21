"""
Basic tests of endpoints
"""
import json
import pytest
from random import choice

from app.crud import user as crud
from app.models.character import Character
from app.models.game import Game

"""
Test suite
"""

TEST_DATA = [
    {
        'username': 'player_1_test',
        'nickname': 'MrWhite',
        'characters_to_create': [
            {
                'name': 'Gandalf',
                'biography': 'Gandalf the Grey is a wizard'
            },
            {
                'name': 'Bilbo',
                'biography': 'Bilbo Baggins is a strange and wonderful hobbit'
            }
        ]
    },
    {
        'username': 'player_2_test',
        'nickname': 'MrOrange',
        'characters_to_create': [
            {
                'name': 'Frodo',
                'biography': 'Frodo is the Ring-Bearer'
            },
            {
                'name': 'Sam',
                'biography': 'Samwise Gamgee, a hobbit, is Frodo\'s gardener, and dear friend'
            }
        ]
    },
    {
        'username': 'player_3_test',
        'nickname': 'MrBlonde',
        'characters_to_create': [
            {
                'name': 'Aragorn',
                'biography': 'Aragorn, also known as Strider'
            },
            {
                'name': 'Boromir',
                'biography': 'Boromir is the son of the Steward of Gondor'
            }
        ]
    }
]


class TestCharacter:

    def __init__(self, name: str, biography: str):
        self.name = name
        self.biography = biography
        self.character_id = None


class TestAccount:

    def __init__(self,
                 username: str,
                 nickname: str,
                 characters_to_create: list[dict]):
        self.username = username
        self.nickname = nickname
        self.user_id = None
        self.authorization_header = {'Authorization': f'Bearer {self.username}'}
        self.characters: list[TestCharacter] = [TestCharacter(**character) for character in characters_to_create]
        self.games = []

    @property
    def character(self) -> TestCharacter | None:
        """Get random character"""
        return choice(self.characters)


class TestSuite:

    def __init__(self, users: list[TestAccount]):
        self.users = users
        self.__current_user = choice(self.users)
        # generate users attributes
        for user in self.users:
            setattr(self, user.username, user)

    @property
    def user(self) -> TestAccount:
        return self.__current_user

    @property
    def another_user(self) -> TestAccount:
        """Returns """
        return [user for user in self.users if user.username != self.__current_user.username][0]

    def re_roll_user(self):
        self.__current_user = choice(self.users)


@pytest.fixture(scope='module', autouse=True)
def test_suite():
    return TestSuite(users=[TestAccount(**user) for user in TEST_DATA])


"""
Tests start here
"""


class TestUsersEndpoints:

    def test_create(self, test_app, test_suite):
        """Test POST request on /users"""
        # Create users
        for user in test_suite.users:
            response = test_app.post('/users/', data=json.dumps({
                'username': user.username,
                'nickname': user.nickname
            }), headers=user.authorization_header)
            assert response.status_code == 201
            created_user = response.json()
            user.user_id = created_user['user_id']

    def test_create_same_username(self, test_app, test_suite):
        """Check username uniqueness constraint"""
        response = test_app.post('/users/', data=json.dumps({
            'username': test_suite.user.username,
            'nickname': test_suite.user.nickname
        }), headers=test_suite.user.authorization_header)
        assert response.status_code == 400

    def test_read_all(self, test_app, test_suite):
        """Test GET /users"""
        response = test_app.get('/users', headers=test_suite.user.authorization_header)
        users = response.json()
        assert response.status_code == 200
        assert len(users) > 1

    def test_read_all_unauthorized(self, test_app):
        """Test GET /users"""
        response = test_app.get('/users')
        assert response.status_code == 403

    def test_read_one(self, test_app, test_suite):
        """Test GET /users/{user_id}"""
        response = test_app.get(f'/users/{test_suite.user.user_id}',
                                headers=test_suite.user.authorization_header)
        user = response.json()
        assert response.status_code == 200
        assert user.get('username') == test_suite.user.username
        assert user.get('nickname') == test_suite.user.nickname

    def test_read_one_unauthorized(self, test_app, test_suite):
        """Test GET /users/{user_id} by unauthorized user"""
        response = test_app.get(f'/users/{test_suite.user.user_id}')
        assert response.status_code == 403

    def test_update(self, test_app, test_suite):
        """Test PUT /users"""
        test_suite.user.nickname = 'Mr nickname_is_changed '
        response = test_app.put(f'/users/{test_suite.user.user_id}', data=json.dumps({
            'nickname': test_suite.user.nickname
        }), headers=test_suite.user.authorization_header)
        updated_user = response.json()
        assert response.status_code == 200
        assert updated_user.get('username') == test_suite.user.username
        assert updated_user.get('nickname') == test_suite.user.nickname

    def test_update_not_by_owner(self, test_app, test_suite):
        """Test PUT /users/{user_id}"""
        new_nickname = 'Daivor the Lightbringer'
        response = test_app.put(f'/users/{test_suite.user.user_id}', data=json.dumps({
            'nickname': new_nickname
        }), headers=test_suite.another_user.authorization_header)
        assert response.status_code == 403

    def test_update_unauthorized(self, test_app, test_suite):
        """Test PUT /users/{user_id}"""
        new_nickname = 'Daivor the Lightbringer'
        response = test_app.put(f'/users/{test_suite.user.user_id}', data=json.dumps({
            'nickname': new_nickname
        }))
        assert response.status_code == 403

    def test_delete(self, test_app, test_db_connection, test_suite):
        """Test DELETE /users/{user_id}"""
        response = test_app.delete(f'/users/{test_suite.user.user_id}',
                                   headers=test_suite.user.authorization_header)
        user = crud.get_user_by_id(test_db_connection, test_suite.user.user_id)
        assert response.status_code == 200
        assert user.disabled is True
        # enable user as we need this be enabled for other tests
        crud.enable_user(test_db_connection, test_suite.user.user_id)

    def test_delete_not_by_owner(self, test_app, test_db_connection, test_suite):
        """Test DELETE /users/{user_id}"""
        response = test_app.delete(f'/users/{test_suite.user.user_id}',
                                   headers=test_suite.another_user.authorization_header)
        assert response.status_code == 403

    def test_delete_unauthorized(self, test_app, test_suite):
        """Test DELETE /users/1"""
        response = test_app.delete(f'/users/{test_suite.user.user_id}')
        assert response.status_code == 403


class TestCharactersEndpoints:

    def test_create(self, test_app, test_suite):
        """Test POST /characters"""
        # create characters for both test players
        for user in test_suite.users:
            for char in user.characters:
                response = test_app.post('/characters/', data=json.dumps({
                    'name': char.name,
                    'biography': char.biography
                }), headers=user.authorization_header)
                character = response.json()
                assert response.status_code == 201
                assert character.get('character_id') is not None
                char.character_id = character.get('character_id')

    def test_create_unauthorized(self, test_app, test_suite):
        """Test POST /characters without Authorization header provided"""
        response = test_app.post('/characters/', data=json.dumps({
            'name': 'Some name',
            'biography': 'Some biography'
        }))
        assert response.status_code == 403

    def test_read_all(self, test_app, test_suite):
        """Test GET /characters"""
        response = test_app.get('/characters', headers=test_suite.user.authorization_header)
        characters_ids = sorted([char['character_id'] for char in response.json()])
        assert response.status_code == 200
        assert characters_ids == sorted([char.character_id for char in test_suite.user.characters])

    def test_read_all_unauthorized(self, test_app):
        """Test GET /characters"""
        response = test_app.get('/characters')
        assert response.status_code == 403

    def test_read_one(self, test_app, test_suite):
        """Test GET /characters/{character_id}"""
        user = test_suite.user
        character_id = user.characters[0].character_id
        response = test_app.get(f'/characters/{character_id}', headers=user.authorization_header)
        character = response.json()
        assert response.status_code == 200
        assert character.get('name') == user.characters[0].name
        assert character.get('biography') == user.characters[0].biography

    def test_read_one_not_by_owner(self, test_app, test_suite):
        """Test GET /characters/{character_id}"""
        character_id = test_suite.user.characters[0].character_id
        response = test_app.get(f'/characters/{character_id}', headers=test_suite.another_user.authorization_header)
        assert response.status_code == 404

    def test_update(self, test_app, test_suite):
        """Test PUT /characters/{character_id}"""
        user = test_suite.user
        character = user.characters[0]
        response = test_app.put(f'/characters/{character.character_id}', data=json.dumps({
            'name': 'NAME-IS-CHANGED',
            'biography': 'BIO-IS-CHANGED'
        }), headers=user.authorization_header)
        assert response.status_code == 200
        assert character.name != response.json()['name']
        assert character.biography != response.json()['biography']

    def test_update_not_owned(self, test_app, test_suite):
        """Test PUT /characters/{character_id} which is not owned by player 1"""
        character_id = test_suite.user.characters[0].character_id
        response = test_app.put(f'/characters/{character_id}', data=json.dumps({
            'name': 'This should not be changed'
        }), headers=test_suite.another_user.authorization_header)
        assert response.status_code == 404

    def test_delete(self, test_app, test_suite, test_db_connection):
        """Test DELETE /characters/{character_id}"""
        character_id = test_suite.user.characters[0].character_id
        response = test_app.delete(f'/characters/{character_id}', headers=test_suite.user.authorization_header)
        # get current character state from database
        character = test_db_connection.get(Character, character_id)
        assert response.status_code == 200
        assert character.disabled is True

    def test_delete_not_owned(self, test_app, test_suite):
        """Test DELETE /characters/{character_id} which os not owned by user"""
        character_id = test_suite.user.characters[0].character_id
        response = test_app.delete(f'/characters/{character_id}', headers=test_suite.another_user.authorization_header)
        assert response.status_code == 404


class TestGamesEndpoints:

    def test_create(self, test_app, test_suite):
        """Test POST on /games"""
        response = test_app.post('/games/', data=json.dumps({}), headers=test_suite.user.authorization_header)
        assert response.status_code == 200
        assert response.json().get('game_id') is not None
        test_suite.user.games.append(response.json())

    def test_delete_not_by_owner(self, test_app, test_suite):
        """Test DELETE on /games/{game_id} by unauthorized user"""
        game_id = test_suite.user.games[0]['game_id']
        response = test_app.delete(f'/games/{game_id}', headers=test_suite.another_user.authorization_header)
        assert response.status_code == 403

    def test_delete(self, test_app, test_db_connection, test_suite):
        """Test DELETE on /games/{game_id}"""
        game_id = test_suite.user.games[0]['game_id']
        response = test_app.delete(f'/games/{game_id}', headers=test_suite.user.authorization_header)
        assert response.status_code == 200
        game = test_db_connection.get(Game, game_id)
        assert game.disabled is True
