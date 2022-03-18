import re
from unicodedata import normalize
from typing import List
import unicodedata
from .types import Match, Tournament, Team
from .constants import file_path, ID_BIND_TYC
from .util.files import read_json_file
from .util.date import get_actual_datetime, string_to_datetime, day_month_year_to_datetime
from lxml.html import HtmlElement

def extract_teams(data) -> List[Team]:
    data = re.split('(?:\s*[\w|\s]*[:|-]{1}\s+)|(?:\s*vs.?\s*)|(?:\s*-\s*)|(?:\s*\([\w|\s]*final[\w|\s]*\)\s*)', data)
    data = [x.strip() for x in data if x != '']
    assert len(data) == 2, 'extract_teams failed'
    teams: List[Team] = []
    teams_info = read_json_file(file_path.CLUB_INFO)
    for name in data:
        team_data = {'name': name}
        name = name.replace(' ', '')
        if name in teams_info.keys():
            team_data.update(teams_info[name])
        teams.append(Team(**team_data))
    return teams

def extract_match(data) -> Match:
    mat_data = {}
    mat_data['tour_id'] = data['tour_id']
    mat_data['tour_name'] = data['tour_name']
    mat_data['time'] = string_to_datetime(data['fecha'], '%Y-%m-%d %H:%M:%S')
    teams = extract_teams(data['nombre'])
    assert len(teams) == 2, 'extract_match failed'
    mat_data['team_1'] = teams[0]
    mat_data['team_2'] = teams[1]
    mat_data['tv'] = []
    for c in data['canales']:
        mat_data['tv'].append(c['nombre'])
    return Match(**mat_data)

def extract_tournament(data) -> Tournament:
    tour_data = {}
    tour_data['id'] = data['id']
    tour_data['name'] = data['nombre']
    tour_data['date'] = string_to_datetime(data["primerFecha"], '%Y-%m-%d %H:%M:%S')
    matches: List[Match] = []
    for event in data['eventos']:
        event['tour_id'] = data['id']
        event['tour_name'] = data['nombre']
        matches.append(extract_match(event))
    tour_data['matches'] = matches
    return Tournament(**tour_data)

def extract_tournaments_v2(data: HtmlElement, tours_ids: List[str]=None) -> List[Tournament]:
    tours_names = [ID_BIND_TYC[id] for id in tours_ids if id in ID_BIND_TYC.keys()]
    tours_condition = " or ".join([f"contains(text(), '{x}')" for x in tours_names])
    today_info: HtmlElement = data.xpath(f"//div[@class='agendaWrap']//div[@class='container_fecha' and ./div[@class='agenda_top-date']/div[@class='tag_hoy']][1]")[0]
    tours_info: List[HtmlElement] = today_info.xpath(f".//div[@class='container_competicion' and ./div[@class='agenda_top-title']/h3[{tours_condition}]]")
    
    tours: List[Tournament] = []
    for x in tours_info:
        tour_name: str = x.xpath("./div[@class='agenda_top-title']/h3/text()")[0]
        tour_id: str = '0000'
        tours.append(Tournament(**{
            'id': tour_id,
            'name': tour_name,
            'date': day_month_year_to_datetime(today_info.xpath("./div[@class='agenda_top-date']/span/text()")[0]),
            'matches': [extract_match_v2(event, tour_id, tour_name) for event in x.xpath(".//div[@class='agenda_eventoWrap']")]
        }))

    return tours

def extract_match_v2(data: HtmlElement, tour_id: str, tour_name: str) -> Match:
    teams_info: List[HtmlElement] = data.xpath(".//h3[@class='agenda__match']/span[contains(@class,'agenda__match-team')]")
    assert len(teams_info) == 2, 'extract_teams failed'
    time_info = string_to_datetime(data.xpath(".//div[@class='agenda__time']/span/text()")[0], "%H:%M Hs")
    tv_info: str = data.xpath(".//span[@class='transmitions']/text()")
    
    return Match(**{
        'tour_id': tour_id,
        'tour_name': tour_name,
        'time': get_actual_datetime().replace(hour=time_info.hour, minute=time_info.minute, second=time_info.second),
        'team_1': extract_team_v2(teams_info[0]),
        'team_2': extract_team_v2(teams_info[1]),
        'tv': [x for x in re.split("(?:^TRANSMITE\s:\s)|(?:\s\\|\s)", tv_info[0]) if x] if tv_info else []
    })

def extract_team_v2(data: HtmlElement) -> Team:
    team_name = data.xpath(".//span[contains(@class,'teamDesktop')]/text()")[0]
    return Team(**{
        'name': team_name,
        'img_url': data.xpath(".//span[contains(@class,'escudo')]/img/@src")[0],
        'hashtag': re.sub('[^A-Za-z0-9]+', '', unicodedata.normalize('NFD', team_name))
    })
