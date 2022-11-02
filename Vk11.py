import vk_api
import networkx as nx # библиотека для графов


def group_users_friends_of_friends(users_id, user_id):
    G = nx.Graph()
    for user in users_id:
        G.app_edge(user_id, user)
    return G


def group_users_friends(input_user, user_id):
    G = nx.Graph()
    for user in user_id:
        G.add_edge(input_user, user)
    return G


def group_users(session):  # функция смотрит друзей наших одногруппников
    F = nx.Graph()
    with open("users.txt") as file:  # начинается сессия. открываем файлик с айдишками
        for user in file.readlines():  # считываем айди и каждый айди попадает в group_user_friends
            F = nx.compose(F, group_users_friends(user.strip("/n"),  # массив друзей какого пользователя по айди
                                                  session.get_api().friends.get(user_id=user.strip("\n"))["items"]))
    return F


def autoriz(login, password):  # функция возвращает сессию с которой мы работаем и передает ее в group_users
    vk_session = vk_api.VkApi(login=login, password=password) # пишется логин и пароль
    try:
        vk_session.auth(reauth=True) # делается подключение
    except vk_api.Captcha as cap: # если вылетает капча
        print(cap.get_url()) # он принтит "Бро, вылетела капча, введи ее руками!!!"
        cap.try_again(key=input())
    return vk_session


if __name__ == '__main__':
    from test import login, password

    group_user = group_users(autoriz(login, password)) #  передаем сессию
    nx.write_gexf(group_user, "UsersFriends.gexf")