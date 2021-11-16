import re
from typing import List
from .types import Match, Tournament, Team
from .constants import file_path
from .util.files import read_json_file
from .util.date import string_to_datetime

def extract_teams(data) -> List[Team]:
    data = re.split('(?:\s*[\w|\s]*final[\w|\s]*[:|-]{1}\s+)|(?:\s*vs.?\s*)|(?:\s*-\s*)|(?:\s*\([\w|\s]*final[\w|\s]*\)\s*)', data)
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
    matches = []
    for event in data['eventos']:
        event['tour_id'] = data['id']
        event['tour_name'] = data['nombre']
        matches.append(extract_match(event))
    tour_data['matches'] = matches
    return Tournament(**tour_data)
