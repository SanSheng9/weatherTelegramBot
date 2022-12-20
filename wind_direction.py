def get_wind_direction(deg):
    if deg >= 326.25 or deg <= 33.75:
        return 'северный'
    elif deg >= 33.76 and deg <= 56.25:
        return 'северо-восточный'
    elif deg >= 56.26 and deg <= 123.75:
        return 'восточный'
    elif deg >= 123.75 and deg <= 168.75:
        return 'юго-восточный'
    elif deg >= 168.76 and deg <= 213.75:
        return 'южный'
    elif deg >= 213.76 and deg <= 258.75:
        return 'западно-восточный'
    elif deg >= 258.76 and deg <= 303.75:
        return 'западный'
    elif deg >= 303.76 and deg <= 326.24:
        return 'северо-западный'
