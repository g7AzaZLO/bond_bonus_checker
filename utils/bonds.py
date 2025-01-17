import requests

def get_bonus_for_bond_index(api_url, target_index):
    """
    Делает запрос к API, находит бонд с заданным индексом и возвращает значение bonus.

    :param api_url: str, URL API
    :param target_index: int, индекс искомого бонда
    :return: float, значение бонуса, либо None, если бонд не найден
    """
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()

        for bond in data.get("bonds", []):
            if bond.get("index") == target_index:
                return bond.get("bonus")

        return None
    except requests.RequestException as e:
        print(f"Ошибка при запросе: {e}")
        return None

# Использование
# api_url = "https://realtime-api.ape.bond/bonds"
# index = 2015
# bonus = get_bonus_for_bond_index(api_url, index)
#
# if bonus is not None:
#     print(f"Бонус для бонда с индексом {index}: {bonus}")
# else:
#     print(f"Бонд с индексом {index} не найден или произошла ошибка.")
