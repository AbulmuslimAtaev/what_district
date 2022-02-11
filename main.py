# С КОНСОЛИ ВВОД
# вот к примеру: "python main.py Мирзабекова 62 Махачкала"

import sys
import requests
from geocoder import get_coordinates


def geocoder_district(address):
    geocoder_request = address
    response = requests.get(geocoder_request)
    print(response.url)

    if response:
        json_response = response.json()
    else:
        raise RuntimeError(
            f"""Ошибка выполнения запроса:
            {geocoder_request}
            Http статус: {response.status_code} ({response.reason})""")
    features = json_response["response"]["GeoObjectCollection"]["featureMember"]
    return features[0]["GeoObject"] if features else None


def main():
    toponym_to_find = " ".join(sys.argv[1:])
    if toponym_to_find:
        lat, lon = get_coordinates(toponym_to_find)
        adress_ll = f"{lat},{lon}"
        req = "https://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&" \
              f"geocode={adress_ll}&kind=district&format=json"
        data = [i["name"] for i in
                reversed(geocoder_district(req)["metaDataProperty"]["GeocoderMetaData"]["Address"]["Components"])]
        print(data)
        print(f"РАЙОН: {data[0]}")


if __name__ == '__main__':
    main()
