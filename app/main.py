import json
import os
import random
import bottle
import copy

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
    #print(json.dumps(data))

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
    #print(board_state)
    turn = data["turn"]
    food_list = board_state["food"]
    board_width = board_state["width"]
    board_height = board_state["height"]
    enemy_list = board_state["snakes"]
    me = data["you"]

    reset_directions = ['up', 'down', 'left', 'right']
    
    directions = path(reset_directions, data)
    direction = get_dat_grub(food_list, me)

    if direction not in directions:
        direction = random.choice(directions)

    return move_response(direction)

def get_dat_grub(food_list, me):
    if not food_list:
        return None
    
    minfood = food_list[0]
    min_distance = 100
    head = me["body"][0]
    head_x = head["x"]
    head_y = head["y"]

    for food in food_list:
        x = food["x"]
        y = food["y"]
        dif_x = head_x - x
        dif_y = head_y - y

        distance = (dif_x*dif_x) + (dif_y*dif_y)
        if distance < min_distance:
            min_distance = distance
            minfood = food

    target_x = minfood["x"]
    target_y = minfood["y"]

    dif_x = head_x - target_x
    dif_y = head_y - target_y
    if dif_x == 0:
        if dif_y < 0:
            return "down"
        else:
            return "up"
    elif dif_y == 0:
        if dif_x < 0:
            return "right"
        else:
            return "left"
    if dif_x < dif_y:
        if(dif_x > 0):
            return "left"
        else:
            return "right"
    elif dif_y < dif_x:
        if(dif_y < 0):
            return "down"
        else:
            return "up"


def avoid_sneks(no_no_zone, data):
    if data["board"]["snakes"]:
        for snake in data["board"]["snakes"]:
            for taken in snake["body"]:
                no_no_zone.append(taken)
            
            if len(snake["body"]) >= len(data["you"]["body"]):
                head = snake["body"][0]
                bad = [
                    {
                        "x": head["x"],
                        "y": head["y"] + 1
                    },
                    {
                        "x": head["x"],
                        "y": head["y"] - 1
                    },
                    {
                        "x": head["x"] + 1,
                        "y": head["y"]
                    },
                    {
                        "x": head["x"] - 1,
                        "y": head["y"]
                    },
                ]
                no_no_zone.extend(bad)
    
    return no_no_zone


def path(copy_directions, data):

    directions = copy.copy(copy_directions)
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

    no_no_zone = avoid_sneks(body[1:], data)

    height = data["board"]["height"]
    width = data["board"]["width"]

    if up_coords in no_no_zone or up_coords["y"] < 0:
        print("no up")
        if "up" in directions:
            directions.remove("up")

    if down_coords in no_no_zone or down_coords["y"] >= height:
        print("no down")
        if "down" in directions:
            directions.remove("down")
    
    if right_coords in no_no_zone or right_coords["x"] >= width:
        print("no right")
        if "right" in directions:
            directions.remove("right")
    
    if left_coords in no_no_zone or left_coords["x"] < 0:
        print("no left")
        if "left" in directions:
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
