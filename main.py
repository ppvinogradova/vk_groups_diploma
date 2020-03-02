from urllib.parse import urlencode
import requests

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

    a = get_friends.text.split('[')
    b = a[1].split(']')
    friends_list = b[0].split(',')
    #print(friends_list)
    
    return friends_list

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

    a = get_groups.text.split('[')
    b = a[1].split(']')
    groups_set = set(b[0].split(','))
    print(groups_set)

user = User(171691064)
user.friends()
user.groups()