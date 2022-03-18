from datetime import timezone, timedelta

class file_path:
    CLUB_INFO = './clubsid.json'

class font_path:
    ROBOTO_BLACK = './fonts/Roboto-Black.ttf'
    ROBOTO_LIGHT = './fonts/Roboto-Light.ttf'
class uri:
    SPORTS_AGENDA = 'https://www.tycsports.com/agenda-deportiva-hoy.html'

class time:
    TIME_ZONE = timezone(timedelta(hours=-3)) #Argentina UTC-3

TOURNAMENTS_IDS = [
    '1346', # LPA
    '3',    # CL
    '1324', # CA
    '14',   # CARG
    '1437', # TDC
    '1247'  # ECS
]

ID_BIND_TYC = {
    '1346': 'Liga Profesional de Fútbol', # LPA
    '3': 'Copa Libertadores',    # CL
    # '1324', # CA
    '14': 'Copa Argentina',   # CARG
    '1437': 'Trofeo de Campeones',
    '1247': 'Eliminatorias CONMEBOL'
}
