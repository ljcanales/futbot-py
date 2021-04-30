''' Tournament Module '''

class Tournament():

    HASTAGS_BY_ID = {'3' : ['#Libertadores', '#CopaLibertadores'], '1276' : ['CopaDeLaLiga']}

    def __init__(self, id):
        self.id = id
        self.name = ""
        self.date = ""
        self.matches = []
    
    def set_matches(self, new_lst):
        self.matches = new_lst

    def set_name(self, new_name):
        self.name = new_name
    
    def set_date(self, new_date):
        self.date = new_date
    
    def print_tournament(self):
        index = 0
        tt = [""]
        hashtag = ""
    
        tt[index] += '🗓️ ' + self.date + '\n'
        tt[index] += '🏆 ' + self.name + '\n\n'

        if self.id in self.HASTAGS_BY_ID.keys():
            hashtag = "\n" + " ".join(self.HASTAGS_BY_ID[self.id]) + "\n"

        for m in self.matches:
            m_txt = m.print_basic_info()
            if len(tt[index] + m_txt) > 279:
                tt.append(m_txt)
                index += 1
            else:
                tt[index] += m_txt
        
        if len(tt[index] + hashtag) < 279:
            tt[index] += hashtag
        return tt
