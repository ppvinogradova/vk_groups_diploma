#LOGGING DECORATOR
import datetime

def log_into_path(path):
  def logger_decor(old_foo):
    def new_foo(*args, **kwargs):
      log = open(path, 'w')
      output = []
      date = str(datetime.datetime.today())+'\n'
      output.append(date)
      something = old_foo(*args, **kwargs)
      name = f'{old_foo}'+'\n'
      output.append(name)
      args = str(args)+'\n'
      output.append(args)
      kwargs = str(kwargs)+'\n'
      output.append(kwargs)
      result = str(something)+'\n'
      output.append(result)
      for line in output:
        log.write(line)
      log.close()
      return something
    return new_foo
  return logger_decor

#from urllib.parse import urlencode
import requests
import time
import json

# APP_ID = 7336572

# AUTH_URL = 'https://oauth.vk.com/authorize'
# params = {
#     'client_id': APP_ID,
#     'display': 'page',
#     'scope': ['friends', 'groups'],
#     'response_type': 'token',
#     'v': 5.103
# }

#print('?'.join((AUTH_URL, urlencode(params))))

TOKEN = '73eaea320bdc0d3299faa475c196cfea1c4df9da4c6d291633f9fe8f83c08c4de2a3abf89fbc3ed8a44e1'

class User:

  def __init__(self, id):
    self.id = id
    self.user_friends = []
    self.user_groups_set = {}
    self.user_groups_set = set()
    self.friends_groups_set = {}
    self.friends_groups_set = set()

  def friends(self):

    request_params = {
      'access_token': TOKEN,
      'user_id': self.id,
      'v': 5.103
    }

    get_friends = requests.get(
      'https://api.vk.com/method/friends.get',
      params=request_params
    )
    print('.')
    response = get_friends.json()
    try:
      assert 'response' in response.keys()
      friends_list = response['response']['items']
      for id_num in friends_list:
        self.user_friends.append(id_num)
    except AssertionError:
      print('Произошла ошибка запроса к API VK:')
      print(response)

  def groups(self):

    request_params = {
      'access_token': TOKEN,
      'user_id': self.id,
      'count': 1000,
      'v': 5.103
    }
  
    get_groups = requests.get(
      'https://api.vk.com/method/groups.get',
      params=request_params
    )
    print('.')
    response = get_groups.json()
    try:
      assert 'response' in response.keys()
      user_groups = response['response']['items']
      for id_num in user_groups:
        self.user_groups_set.add(id_num)
    except AssertionError:
      print('Произошла ошибка запроса к API VK:')
      print(response)

  def friends_groups(self):

    for id_num in self.user_friends:
      request_params = {
        'access_token': TOKEN,
        'user_id': id_num,
        'count': 1000,
        'v': 5.103
      }
      try:
        get_friends_groups = requests.get(
          'https://api.vk.com/method/groups.get',
          params=request_params
        )
        print('.')
        response = get_friends_groups.text
        assert '"error_code":6' not in response
      except AssertionError:
        time.sleep(1.500)
      finally:
        if 'items' in response:
          json_response = get_friends_groups.json()
          friends_groups = json_response['response']['items']
          for id_num in friends_groups:
            self.friends_groups_set.add(id_num)

  def find_secrets(self):
    self.user_groups_set.difference_update(self.friends_groups_set)

  @log_into_path('result.txt')
  def output_info(self):
    response_list = []
    for group_id in self.user_groups_set:
      request_params = {
        'access_token': TOKEN,
        'group_ids': group_id,
        'fields': 'members_count',
        'v': 5.103
      }
      get_groups_info = requests.get(
        'https://api.vk.com/method/groups.getById',
        params=request_params
      )
      print('.')
      response = get_groups_info.json()
      try:
        assert 'response' in response.keys()
        dict_ = response['response'][0]
        response_dict = {'name': dict_['name'], 'gid': dict_['id'], 'members_count': dict_['members_count']}
        response_list.append(response_dict)
      except AssertionError:
        print('Произошла ошибка запроса к API VK:')
        print(response)
    with open('groups.json', 'w') as f:
      json.dump(response_list, f)

input_data = input('Введите id или короткое имя пользователя: ')
def name_id(data):
  if data.isdigit == True:
    return data
  else:
    request_params = {
      'access_token': TOKEN,
      'user_ids': data,
      'v': 5.103
    }
    get_user_info = requests.get(
      'https://api.vk.com/method/users.get',
      params=request_params
    )
    print('.')
    response = get_user_info.json()
    try:
      assert 'response' in response.keys()
      id_num = response['response'][0]['id']
      return id_num
    except AssertionError:
      print('Произошла ошибка запроса к API VK:')
      print(response)

name = name_id(input_data)
user = User(name)
user.friends()
user.groups()
user.friends_groups()
user.find_secrets()
user.output_info()