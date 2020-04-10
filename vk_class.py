from datetime import datetime

import requests

VK_URL = 'https://api.vk.com/method/'
VK_TOKEN = '958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008'
VK_API_VERSION = 5.103


class User:
    
    def __init__(self, user_id):
        self.user_id = user_id
        self.payload = {
            'user_id': self.user_id,
            'access_token': VK_TOKEN,
            'v': VK_API_VERSION,
        }

    def get_friends(self):
        method_name = "friends.get"
        response = requests.get(f"{VK_URL}{method_name}", params=self.payload)
        json_dict = response.json()
        try:
            if json_dict['error']['error_code'] == 18 or json_dict['error']['error_code'] == 30:
                raise Exception(f'Пользователь {self.user_id} удален, либо его аккаунт приватный!')
        except KeyError:
            return json_dict['response']['items']

    def __and__(self, friend):
        print(f"{datetime.now()} - Получение списка друзей пользователя '{self.user_id}'")
        first_user = set(self.get_friends())

        print(f"{datetime.now()} - Получение списка друзей пользователя '{friend.user_id}'")
        second_user = set(friend.get_friends())

        print('\nСписок общих друзей:')
        friends = first_user & second_user
        return list(map(User, friends)) or ['Общих друзей - нет!']

    def __str__(self):

        return f'https://vk.com/id{self.user_id}'


def get_user_id(user_id):
    method_name = "users.get"

    response = requests.get(f"{VK_URL}{method_name}", params={
        "user_ids": user_id,
        "access_token": VK_TOKEN,
        "v": VK_API_VERSION
    })

    return response.json()['response'][0]['id']


def main():
    first_user_id = input('Введите ID первого пользователя(можно буквенный): ')
    first_user_id = get_user_id(first_user_id)
    second_user_id = input('Введите ID второго пользователя(можно буквенный): ')
    second_user_id = get_user_id(second_user_id)

    first_user = User(first_user_id)
    second_user = User(second_user_id)

    print(*(first_user & second_user), sep="\n")


if __name__ == '__main__':
    main()
