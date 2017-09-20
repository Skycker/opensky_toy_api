Библиотека для получения списка самолетов, находящихся в пределах заданного радиуса от заданного места.

Источником данных служит сервис [OpenSky](https://opensky-network.org/).

### Установка

    pip install git+https://github.com/Skycker/opensky_toy_api

### Использование

Работа с API сервиса производится через `opensky_toy_api.OpenSkyApi`

    >>> from opensky_toy_api import OpenSkyApi

Получить список всех показаний с самолетов в определенный момент можно с помощью `OpenSkyApi.get_states`

    >>> from opensky_toy_api import OpenSkyApi
    >>> api = OpenSkyApi()
    >>> states = api.get_states()

`OpenSkyApi.get_states` возвращает список объектов `opensky_toy_api.AirplaneState`. Каждый из объектов отражает показание с самолета.
Объекты `opensky_toy_api.AirplaneState` имеют следующие атрибуты:

1. callsign - название самолета. Может быть None
2. latitude - широта WGS-84 в градусах. Может быть None
3. longitude - долгота WGS-84 в градусах. Может быть None

Получить список всех показаний в пределах заданного радиуса от заданного места можно с помощью `OpenSkyApi.get_states_near_place(latitude, longitude, radius)`

    >>> from opensky_toy_api import OpenSkyApi
    >>> api = OpenSkyApi()
    >>> states = api.get_states_near_place(54.7800533, 31.8598796, 100)

Аргументы:

1. latitude и longitude - широта и долгота места (WGS-84, в градусах)
2. radius - радиус окружности для поиска с центром в указанном месте (в км)

По аналогии с `OpenSkyApi.get_states` `OpenSkyApi.get_states_near_place` возвращает список объектов `opensky_toy_api.AirplaneState`

Метод может быть вызван без указания координат и радиуса. В этом случае библиотека вернет все самолеты в радиусе 450 км от Парижа (значения по умолчанию)

    >>> from opensky_toy_api import OpenSkyApi
    >>> api = OpenSkyApi()
    >>> states = api.get_states_near_place()

### Ограничения

Протестировано для Python 3