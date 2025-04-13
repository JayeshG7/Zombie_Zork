from aiohttp import web
from aiohttp.web import Request, Response, json_response
import random

routes = web.RouteTableDef()

# Global state for the domain
domain_state = {
    'users': {},  # Store user states
    'items': {},  # Store item locations
    'hub_data': None  # Store hub connection data
}

@routes.post('/newhub')
async def register_with_hub_server(req: Request) -> Response:
    """Used by web UI to connect this domain to a hub server.
    
    1. web calls domain's /register, with hub server URL payload
    2. domain calls hub server's /register, with name, description, and items
    3. hub server replies with domain's id, secret, and item identifiers
    """
    global domain_state
    url = await req.text()
    async with req.app.client.post(url+'/register', json={
          'url': whoami,
          'name': "Zombie Domain",
          'description': "A spooky domain filled with zombies and mysteries",
          'items': [
              {
                  'name': 'Rusty Key',
                  'description': 'An old rusty key that might unlock something important',
                  'verb': {'use': 'You try the key in various locks...', 'examine': 'The key looks very old'},
                  'depth': 1
              },
              {
                  'name': 'Zombie Antidote',
                  'description': 'A mysterious vial containing what appears to be a cure',
                  'verb': {'drink': 'You feel stronger...', 'examine': 'The liquid glows with an eerie green light'},
                  'depth': 2
              }
          ]
      }) as resp:
          data = await resp.json()
          if 'error' in data:
              return json_response(status=resp.status, data=data)
          
          # Store the domain data
          domain_state['hub_data'] = {
              'hub_url': url,
              'domain_id': data['id'],
              'secret': data['secret'],
              'items': data['items']
          }
          
          return json_response(data={'ok': 'Domain registered successfully'})

@routes.post('/arrive')
async def handle_arrival(req: Request) -> Response:
    """Called by hub server each time a user enters or re-enters this domain."""
    data = await req.json()
    user_id = data['user']
    
    # Store user state
    domain_state['users'][user_id] = {
        'location': 'entrance',
        'from': data.get('from', 'unknown')
    }
    
    # Handle items the user brings
    for item in data.get('carried', []):
        domain_state['items'][item['id']] = {'location': 'with_user', 'user': user_id}
    
    return json_response(data={'ok': 'Welcome to the Zombie Domain'})

@routes.post('/dropped')
async def handle_item_drop(req: Request) -> Response:
    """Called by hub server each time a user drops an item in this domain.
    The return value must be JSON, and will be given as the location on subsequent /arrive calls
    """
    data = await req.json()
    item_id = data['item']['id']
    user_id = data['user']
    
    # Generate a random location for the dropped item
    locations = ['near_entrance', 'in_corner', 'by_window', 'under_table']
    drop_location = random.choice(locations)
    
    # Store item location
    domain_state['items'][item_id] = {
        'location': drop_location,
        'dropped_by': user_id
    }
    
    return json_response(data=drop_location)

@routes.post("/command")
async def handle_command(req: Request) -> Response:
    """Handle hub-server commands"""
    data = await req.json()
    user_id = data['user']
    command = data.get('command', [])
    
    if not command:
        return json_response(data={'error': 'No command provided'})
    
    # Basic command handling
    action = command[0].lower()
    if action == 'look':
        return json_response(data={'message': 'You see zombies shuffling around in the darkness.'})
    elif action == 'inventory':
        items = [item_id for item_id, info in domain_state['items'].items() 
                if info.get('location') == 'with_user' and info.get('user') == user_id]
        return json_response(data={'items': items})
    else:
        return json_response(data={'message': f"You try to {action}, but nothing happens."})

# Do not modify code below this line

@web.middleware
async def allow_cors(req, handler):
    """Bypass cross-origin resource sharing protections,
    allowing anyone to send messages from anywhere.
    Generally unsafe, but for this class project it should be OK."""
    resp = await handler(req)
    resp.headers["Access-Control-Allow-Origin"] = "*"
    return resp

async def start_session(app):
    """To be run on startup of each event loop. Makes singleton ClientSession"""
    from aiohttp import ClientSession, ClientTimeout
    app.client = ClientSession(timeout=ClientTimeout(total=3))

async def end_session(app):
    """To be run on shutdown of each event loop. Closes the singleton ClientSession"""
    await app.client.close()


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', type=str, default="0.0.0.0")
    parser.add_argument('-p','--port', type=int, default=3400)
    args = parser.parse_args()

    import socket
    whoami = socket.getfqdn()
    if '.' not in whoami: whoami = 'localhost'
    whoami += ':'+str(args.port)
    whoami = 'http://' + whoami
    print("URL to type into web prompt:\n\t"+whoami)
    print()

    app = web.Application(middlewares=[allow_cors])
    app.on_startup.append(start_session)
    app.on_shutdown.append(end_session)
    app.add_routes(routes)
    web.run_app(app, host=args.host, port=args.port)
