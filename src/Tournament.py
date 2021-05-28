''' Tournament Module '''

import datetime

TIME_ZONE = datetime.timezone(datetime.timedelta(hours=-3)) #Argentina UTC-3
WEEK_DAYS = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
class Tournament():

    HASTAGS_BY_ID = {'3' : ['#Libertadores', '#CopaLibertadores'], '1276' : ['#CopaDeLaLiga']}

    def __init__(self, id):
        self.id = id
        self.name = ""
        self.date = ""
        self.matches = []
        self.day_name = ""
    
    def set_matches(self, new_lst):
        self.matches = new_lst

    def set_name(self, new_name):
        self.name = new_name
    
    def set_date(self, new_date):
        self.date = new_date

        d_numbers = [int(n) for n in self.date.split('-')]
        day_number = self.get_actual_datetime().replace(year=d_numbers[2], month=d_numbers[1], day=d_numbers[0]).weekday()
        
        self.day_name = WEEK_DAYS[day_number]
    
    def print_tournament(self):
        index = 0
        tt = [""]
        hashtag = ""

        tt[index] += '🏆 {}\n'.format(self.name.upper())

        tt[index] += '🗓️ {} {}\n\n'.format(self.day_name, self.date.replace('-','/'))

        if self.id in self.HASTAGS_BY_ID.keys():
            hashtag = "\n{}\n".format(" ".join(self.HASTAGS_BY_ID[self.id]))

        for m in self.matches:
            m_txt = m.print_basic_info()
            if len(tt[index] + m_txt) > 250:
                tt.append(m_txt)
                index += 1
            else:
                tt[index] += m_txt
        
        if len(tt[index] + hashtag) < 250:
            tt[index] += hashtag
        return tt

    def get_actual_datetime(self):
            ''' Returns actual datetime by TIME_ZONE '''

            return datetime.datetime.now().astimezone(TIME_ZONE)