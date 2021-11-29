from datetime import timezone, timedelta

class file_path:
    TEXT_TEMPLATES = './text_templates.json'
    CLUB_INFO = './clubsid.json'

class uri:
    SPORTS_AGENDA = 'https://www.tycsports.com/agenda-deportiva-hoy.html'

class time:
    TIME_ZONE = timezone(timedelta(hours=-3)) #Argentina UTC-3

TOURNAMENTS_IDS = [
    '1346', # LPA
    '3',    # CL
    '1324', # CA
    '14',   # CARG
]

ID_BIND_TYC = {
    '1346': 'Liga Profesional de Fútbol', # LPA
    # '3',    # CL
    # '1324', # CA
    '14': 'Copa Argentina',   # CARG
}
