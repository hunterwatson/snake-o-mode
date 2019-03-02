import json
import os
import random
import bottle

from api import ping_response, start_response, move_response, end_response

@bottle.route('/')
def index():
    return '''
    Battlesnake documentation can be found at
       <a href="https://docs.battlesnake.io">https://docs.battlesnake.io</a>.
    '''

@bottle.route('/static/<path:path>')
def static(path):
    """
    Given a path, return the static file located relative
    to the static folder.

    This can be used to return the snake head URL in an API response.
    """
    return bottle.static_file(path, root='static/')

@bottle.post('/ping')
def ping():
    """
    A keep-alive endpoint used to prevent cloud application platforms,
    such as Heroku, from sleeping the application instance.
    """
    return ping_response()

@bottle.post('/start')
def start():
    data = bottle.request.json

    """
    TODO: If you intend to have a stateful snake AI,
            initialize your snake state here using the
            request's data if necessary.
    """
    print(json.dumps(data))

    color = "#FFD700"
    headType = "safe"
    tailType = "round-bum"

    return start_response(color, headType, tailType)


@bottle.post('/move')
def move():

    data = bottle.request.json

    """
    TODO: Using the data from the endpoint request object, your
            snake AI must choose a direction to move in.
    """


    board_state = data["board"]
    print(board_state)
    turn = data["turn"]
    food_list = board_state["food"]
    board_width = board_state["width"]
    board_height = board_state["height"]
    enemy_list = board_state["snakes"]
    me = data["you"]

    directions = ['up', 'down', 'left', 'right']

    directions = path(directions, data)
    direction = random.choice(directions)
    
    return move_response(direction)

def path(directions, data):
    body = data["you"]["body"]
    head = body[0]
    
    up_coords = {
        "x": head["x"],
        "y": head["y"] - 1,
    }

    down_coords = {
        "x": head["x"],
        "y": head["y"] + 1,
    }

    right_coords = {
        "x": head["x"] + 1,
        "y": head["y"],
    }

    left_coords = {
        "x": head["x"] - 1,
        "y": head["y"],
    }

    no_no_zone = body[1:]
    height = data["board"]["height"]
    width = data["board"]["width"]

    if (up_coords in no_no_zone and "up" in directions) or up_coords["y"] < 0:
        directions.remove("up")
    
    if (down_coords in no_no_zone and "down" in directions) or down_coords >= height:
        directions.remove("down")
    
    if (right_coords in no_no_zone and "right" in directions) or right_coords >= width:
        directions.remove("right")
    
    if (left_coords in no_no_zone and "left" in directions) or left_coords < 0:
        directions.remove("left")
    
    return directions


@bottle.post('/end')
def end():
    data = bottle.request.json

    """
    TODO: If your snake AI was stateful,
        clean up any stateful objects here.
    """
    print(json.dumps(data))

    return end_response()

# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()

if __name__ == '__main__':
    bottle.run(
        application,
        host=os.getenv('IP', '0.0.0.0'),
        port=os.getenv('PORT', '8080'),
        debug=os.getenv('DEBUG', True)
    )
