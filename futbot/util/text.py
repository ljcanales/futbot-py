from typing import List
from futbot.types import Match, Tournament
from futbot.util.date import WEEK_DAYS

HASTAGS_BY_ID = {'3' : ['#Libertadores', '#CopaLibertadores'], '1276' : ['#CopaDeLaLiga'], '1324' : ['#CopaAmerica', '@CopaAmerica'], '441' : ['#EURO2020', '@EURO2020'], '1346' : ['#LPFA', '#LigaProfesional'], '14' : ['#CopaArgentina'], '1247' : ['#EliminatoriasSudamericanas', '#Qatar2022']}

class match_to_text:
    @staticmethod
    def full_info(match: Match) -> str:
        tt = ""
        #hashtag = ""
        if match.tour_id in HASTAGS_BY_ID.keys():
            hashtag = " ".join(HASTAGS_BY_ID[match.tour_id])

        tt += '⚽ {} vs {}\n\n'.format(match.team_1.name.upper(), match.team_2.name.upper())
        tt += '🗓️ {} {} ⏰ {}\n'.format(WEEK_DAYS[match.time.weekday()], match.time.strftime('%d/%m/%Y'), match.time.strftime('%H:%M'))
        tt += '🏆 {}\n'.format(match.tour_name)
        if match.tv:
            tt += '📺 {}\n'.format(" - ".join(match.tv))
        
        tt += '\n#{} #{}\n{}\n'.format(match.team_1.hashtag, match.team_2.hashtag, hashtag)

        return tt
    
    @staticmethod
    def basic_info(match: Match) -> str:
        return '⌚{} - {} vs {}\n'.format(match.time.strftime('%H:%M'), match.team_1.name, match.team_2.name)
    
    @staticmethod
    def message_info(match: Match) -> str:
        tt = ""
        tt += '⚽ Está por empezar ⚽\n\n{} vs {}'.format(match.team_1.name.upper(), match.team_2.name.upper())
        tt += '\n\n⏰ {}'.format(match.time.strftime('%H:%M'))
        tt += '\n\n Con un RT y MG me ayudas mucho!'
        return tt
    
    @staticmethod
    def message_by_template(match: Match, template: str) -> str:
        return template.format(match.team_1.name.upper(), match.team_2.name.upper(), match.time.strftime('%H:%M'))

class tour_to_text:
    @staticmethod
    def full_info_lst(tour: Tournament) -> List[str]:
        index = 0
        tt = [""]
        hashtag = ""

        tt[index] += '🏆 {}\n'.format(tour.name.upper())

        tt[index] += '🗓️ {} {}\n\n'.format(WEEK_DAYS[tour.date.weekday()], tour.date.strftime('%d/%m/%Y'))

        if tour.id in HASTAGS_BY_ID.keys():
            hashtag = "\n{}\n".format(" ".join(HASTAGS_BY_ID[tour.id]))

        for match in tour.matches:
            m_txt = match_to_text.basic_info(match)
            if len(tt[index] + m_txt) > 250:
                tt.append(m_txt)
                index += 1
            else:
                tt[index] += m_txt
        
        if len(tt[index] + hashtag) < 250:
            tt[index] += hashtag
        return tt
