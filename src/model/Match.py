''' Match Module '''

from src.model.Tournament import Tournament

class Match():
    def __init__(self, tournament, time, equipo1, equipo2, tv):
        self.tournament: Tournament = tournament
        self.time = time
        self.equipo1 = equipo1
        self.equipo2 = equipo2
        self.tv = tv
        self.tweet_id = ""
    
    def get_equipos(self):
        return [self.equipo1, self.equipo2]

    def print_match(self):
        tt = ""
        hashtag = ""
        if self.tournament.id in self.tournament.HASTAGS_BY_ID.keys():
            hashtag = " ".join(self.tournament.HASTAGS_BY_ID[self.tournament.id])

        tt += '⚽ {} vs {}\n\n'.format(self.equipo1.upper(), self.equipo2.upper())
        tt += '🗓️ {} {} ⏰ {}\n'.format(self.tournament.day_name, self.tournament.date.replace('-','/'), self.time)
        tt += '🏆 {}\n'.format(self.tournament.name)
        if self.tv:
            tt += '📺 {}\n'.format(" - ".join(self.tv))
        
        tt += '\n#{} #{} {}\n'.format(self.equipo1.replace(" ", ""), self.equipo2.replace(" ", ""), hashtag)

        return tt

    def print_basic_info(self):
        tt = ""
        tt += '⌚{} - {} vs {}\n'.format(self.time, self.equipo1, self.equipo2)
        return tt
    
    def print_message_info(self):
        tt = ""
        tt += '⚽ Está por empezar ⚽\n\n{} vs {}'.format(self.equipo1.upper(), self.equipo2.upper())
        tt += '\n\n⏰ {}'.format(self.time)
        tt += '\n\n Con un RT y MG me ayudas mucho!'
        return tt
    
    def message_by_template(self, template):
        return template.format(self.equipo1.upper(), self.equipo2.upper(), self.time)