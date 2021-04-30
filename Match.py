''' Match Module '''

class Match():
    def __init__(self, tournament, time, equipo1, equipo2, tv):
        self.tournament = tournament
        self.time = time
        self.equipo1 = equipo1
        self.equipo2 = equipo2
        self.tv = tv
    
    def get_equipos(self):
        return [self.equipo1, self.equipo2]

    def print_match(self):
        tt = ""
        hashtag = ""
        if self.tournament.id in self.tournament.HASTAGS_BY_ID.keys():
            hashtag = " ".join(self.tournament.HASTAGS_BY_ID[self.tournament.id])

        tt += '⚽ ' + self.equipo1.upper() + ' vs ' + self.equipo2.upper() + '\n\n'
        tt += '🗓️ ' + self.tournament.date + ' ⏰' + self.time + '\n'
        tt += '🏆 ' + self.tournament.name + '\n'
        if self.tv:
            tt += '📺 ' + " - ".join(self.tv) + '\n'
        
        tt += '\n#' + self.equipo1.replace(" ", "") + ' #' + self.equipo2.replace(" ", "") + ' ' + hashtag + '\n'

        return tt

    def print_basic_info(self):
        tt = ""
        tt += '⌚' + self.time + ' - ' + self.equipo1 + ' vs ' + self.equipo2 + '\n'
        return tt