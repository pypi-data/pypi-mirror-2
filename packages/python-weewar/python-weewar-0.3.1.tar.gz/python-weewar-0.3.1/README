
=====================================
Python wrapper for the Weewar XML API
=====================================

Weewar (http://weewar.com) is an "Award winning turn based multiplayer strategy
game". Apart from being highly addictive, it provides 2 APIs: 

- one read-only API for players and 
- a bot API called ELIZA 

Further documentation on both is available at http://weewar.wikispaces.com/api. 

This module aims enables you to conveniently call each of these API functions
from within your python script.

Available API calls
-------------------

The following functions are supplied:

- ``game(id)`` returns the status of a game and gives information about the
  participating players.
   
- ``open_games()`` returns all currently available open games as a list of IDs.
   
- ``all_users()`` returns a list of all users who have been online in the last
  7 days, including their current ranking.
   
- ``user(username)`` Returns detailed information about a single user,
  including everything that is visible on the profile page and the games the
  user is participating in.

- ``latest_maps()`` returns the latest published maps including urls for
  previews, images, and other details.
   
- ``headquarter(username, apikey)`` returns all games that are listed in your
  Headquarters. Includes information about the id, the url, the state, and the
  name of the game.  An attribute is added if the game is in need of attention,
  e.g: its the users turn or the game is not yet started or the user is invited
  to this game (requires authentication).

- ``game_state(username, apikey, id)`` offers more information about the state
  of a game (requires authentication).

- ``map_layout(id)`` returns complete map layout.

Each game can also be controlled via these commands (which are part of the
ELIZA API):

- ``finish_turn(username, apikey, id)`` finishes turn in game.

- ``accept_invitation(username, apikey, id)`` accepts invitation to a game.

- ``decline_invitation(username, apikey, id)`` declines invitation to a game.

- ``send_reminder(username, apikey, id)`` sends a reminder about the game.

- ``surrender_game(username, apikey, id)`` surrenders!

- ``abandon_game(username, apikey, id)`` abondons a game.

- ``remove_game(username, apikey, id)`` removes a game.

- ``chat(username, apikey, game_id, msg)`` sends a chat message to the game
  board.

- ``build_unit(username, apikey, game_id, (x, y), unit)`` sends a chat message
  to the game board.

- ``unit_move_options(username, apikey, game_id, unit, (x, y))`` requests unit
  movement options. This is pretty much like what you get when you select a
  unit in a regular game.

- ``unit_attack_options(username, apikey, game_id, unit, (x, y), moved=None)``
  requests possible targets. The 'moved' attribute is optional and describes
  the number of turns a unit has already moved. This is helpful for Jets and
  Battleships.

- ``move_unit(username, apikey, game_id, unit, from, to)`` moves a unit.
   
- ``attack_with(username, apikey, game_id, unit, from, target)`` attacks target
  with unit at specified location.
   
- ``capture_base(username, apikey, game_id, unit, at)`` captures a base with
  unit.  You have to move there first! 

- ``repair_unit(username, apikey, game_id, unit, at)`` repairs a unit. 

Authentication
--------------

Some of the provided functions require a username and a password. Use your
Weewar account username and the API token accessible via
http://weewar.com/apiToken.

License
-------

The code for this module is released under the GNU LESSER GENERAL PUBLIC
LICENSE Version 3.
