#!/usr/bin/env python3
import requests
import sys
import json

COMMANDS = ['help', 'config']

# Kinda useless at the end of the day
def get_filename(dir = __file__):
    file_path = str(dir).split('.')
    if file_path[-1] == 'py':
        filename = file_path[-2]
    else: 
        filename = file_path[-1]
    return filename.lstrip('/')

# filename = get_filename()
filename = sys.argv[0]


class API_Manager:
    def __init__(self, api_url='https://link.cbpio.pl:8080/api/', api_version='v1.0'):
        self.api_url = api_url
        self.api_version = api_version
        
        self.commands = COMMANDS
    
    def display_error(self, msg):
        print('\nError: ' + msg)
    
    def display_help(self):
        print(f'Usage: {filename} [command]')
        print('Commands:')
        print(' help        - Displays this message')
        print(' config      - Shows server configuration')
        print(' code <link> - Returns shortened url')
        print(' all         - Prints all')
        print(' delete_old  - Delete old (expired) entries')
    
    def display_more_info_msg(self):
        print(f'Type `{filename} help` for more information')
    
    def get_config(self):
        res = requests.get(f'{self.api_url}{self.api_version}/config')
        return res

    def create_short_link(self, long_url):
        body = {'long_link': long_url}
        res = requests.post(f'{self.api_url}{self.api_version}/short', json=body)
        print(f'{self.api_url}{self.api_version}/short/')
        return res
    
    def get_all_entries(self):
        res = requests.get(f'{self.api_url}{self.api_version}/all')
        return res
    
    def delete_old_entries(self):
        res = requests.delete(f'{self.api_url}{self.api_version}/short/delete_old')
        print(f'{self.api_url}{self.api_version}/short/delete_old')
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
            requests.get(f'{self.api_url}{self.api_version}/config', timeout=3)
            return True
        except requests.ConnectionError:
            return False
        except requests.Timeout:
            return False

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
    api_m.print_data(api_m.create_short_link(sys.argv[2]), property='code')
elif command == 'all':
    api_m.print_data(api_m.get_all_entries())
elif command == 'delete_old':
    api_m.print_data(api_m.delete_old_entries())
    
    
else:
    api_m.display_error('Unknown command: ' + command)
    api_m.display_more_info_msg()