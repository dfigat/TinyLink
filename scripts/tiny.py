#!/usr/bin/env python3
import requests
import sys
import json

from dotenv import load_dotenv
from os import getenv, path


file_dir = '/'.join(sys.argv[0].split('/')[:-1])

load_dotenv(file_dir + '/' + '../db/.env')
API_URL = getenv('API_URL')
TOKEN_LOCATION = './tokens.json'
COMMANDS = ['help', 'config', 'code', 'all', 'get_all_count', 'delete_old']

# Kinda useless at the end of the day, unless not
def get_filename(dir = __file__):
    file_path = str(dir).split('.')
    print(file_path)
    if file_path[-1] == 'py':
        filename = file_path[-2]
    else: 
        filename = file_path[-1]
    return filename.lstrip('/')

# filename = get_filename()
filename = sys.argv[0]


class API_Manager:
    def __init__(self, api_url=API_URL, api_version='v1.0'):
        self.api_url = api_url
        self.api_version = api_version
        
        self.commands = COMMANDS
        
        self.token_file = TOKEN_LOCATION
        self.access_token = None
        self.refresh_token = None
        self.load_tokens()
    
    def display_error(self, msg):
        print('\nError: ' + msg)
    
    def display_help(self):
        print(f'Usage: {filename} [command]')
        print('Commands:')
        print(' help                    - Displays this message')
        print(' config                  - Shows server configuration')
        print(' code <link>             - Returns shortened url')
        print(' all                     - Prints all links')
        print(' get_all_count           - Gets count of all entries')
        print(' delete_old              - Deletes old (expired) entries')
        print(' login <name> <password> - Self explanatory')
    
    def display_more_info_msg(self):
        print(f'Type `{filename} help` for more information')
    
    def get_config(self):
        res = requests.get(f'{self.api_url}{self.api_version}/config')
        return res

    def create_short_link_api_key(self, long_url, api_key):
        body = {'long_link': long_url}
        headers = {'X-API-KEY': api_key}
        res = requests.post(f'{self.api_url}{self.api_version}/short/', json=body, headers=headers)
        return res
    
    def create_short_link(self, long_url):
        body = {'long_link': long_url}
        headers = {'Authorization': f'Bearer {self.access_token}'}
        res = requests.post(f'{self.api_url}{self.api_version}/short/', json=body, headers=headers)
        return res
    
    def get_all_entries(self):
        res = requests.get(f'{self.api_url}{self.api_version}/all')
        return res

    def get_all_entries_count(self):
        res = requests.get(f'{self.api_url}{self.api_version}/get_count_all')
        return res
    
    def delete_old_entries(self):
        res = requests.delete(f'{self.api_url}{self.api_version}/short/delete_old')
        return res
    
    def is_alive(self, timeout=3):
        res = requests.get(f'{self.api_url}{self.api_version}/is_alive', timeout=timeout)
        return res
    
    def print_data(self, res, property=''):
        data = res.json()
        if not res.ok:
            print(res.content)
            print('Failed at retrieving data')
            return
        if len(property) == 0:
            print(json.dumps(data, indent=4))
        else:
            print(json.dumps(data[property]))

    def check_connection(self):
        try:
            self.is_alive(timeout=3)
            return True
        except requests.ConnectionError:
            return False
        except requests.Timeout:
            return False


    # User methods
    def check_tokens(self):
        if not self.access_token or not self.refresh_token:
            self.display_error('No tokens found.\nMake sure you are logged in')
            return
        
    def load_tokens(self):
        if path.exists(self.token_file):
            with open(self.token_file, 'r') as token_file:
                tokens = json.load(token_file)
                self.access_token = tokens.get('access')
                self.refresh_token = tokens.get('refresh')
        else:
            self.display_error('Couldn\'t find tokens.\nRunning as guest')
    
    def save_tokens(self):
        self.check_tokens()
        
        with open(self.token_file, 'w') as token_file:
            json.dump({
                "refresh": self.refresh_token,
                "access": self.access_token
            }, token_file)
    
    def refresh_refresh_token(self):
        self.check_tokens()
        
        res = requests.post(f'{self.api_url}{self.api_version}/refresh_token/',
                            json={'refresh': self.refresh_token})
        if res.status_code == 200:
            d = res.json()
            self.access_token = d['access']
            print('Refresh of access_token successful')
        else:
            self.display_error('Failed at refreshing access token. Make sure you are logged in')
            print(res.json()['detail'])
    
    def login(self, username, password):
        res = requests.post(f'{self.api_url}{self.api_version}/get_tokens/',
                            json={'username': username, 'password': password})
        
        if res.status_code == 200:
            tokens = res.json()
            self.access_token = tokens['access']
            self.refresh_token = tokens['refresh']
            self.save_tokens()
            print('Logged in successfully as ->', username, '<- :3')
        else:
            self.display_error('Failed at logging in')


api_m = API_Manager()

if len(sys.argv) < 2:
    api_m.display_error('Inadequate argument count')
    api_m.display_more_info_msg()
    sys.exit(1)


if not api_m.check_connection():
    api_m.display_error('Unable to connect to the API service')
    sys.exit(1)

# match sys.argv[1]:
#     case 'help':
#         api_m.display_help()

command = sys.argv[1]
if command == 'help':
    api_m.display_help()
elif command == 'config':
    api_m.print_data(api_m.get_config())
elif command == 'code':
    if len(sys.argv) != 3:
        api_m.display_error('Inadequate argument count')
        api_m.display_more_info_msg()
        sys.exit(1)
    api_m.refresh_refresh_token()
    api_m.save_tokens()
    api_m.print_data(api_m.create_short_link(sys.argv[2]), property='code')
elif command == 'all':
    api_m.print_data(api_m.get_all_entries())
elif command == 'delete_old':
    api_m.print_data(api_m.delete_old_entries())
elif command == 'get_all_count':
    api_m.print_data(api_m.get_all_entries_count(), property='count')

# For user
elif command == 'login':
    if len(sys.argv) != 4:
        api_m.display_error('Inadequate argument count')
        api_m.display_more_info_msg()
        sys.exit(1)
    username = sys.argv[2]
    password = sys.argv[3]
    api_m.login(username, password)

else:
    api_m.display_error('Unknown command: ' + command)
    api_m.display_more_info_msg()