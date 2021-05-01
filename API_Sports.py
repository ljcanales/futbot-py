''' API_Sports Module '''

import requests
from Tournament import Tournament
from Match import Match

from PIL import Image
class API_Sports():
    def __init__(self, api_url, url_teams):
        self.url_teams = url_teams
        try:
            self.res = requests.get(api_url).json()
            self.status = True
        except Exception:
            self.status = False
            print("ERROR: API_Sports.init()")
    
    def get_by_id(self, id_event):
        tour = Tournament(id_event)
        try:
            if self.res and self.res['fechas'] and self.res['fechas'][0]:
                d = self.res['fechas'][0]['fecha'].split('-')
                tour.set_date(d[2] + "-" + d[1] + "-" + d[0])

                matches = []
                for t in self.res['fechas'][0]['torneos']:
                    if t['id'] == id_event:
                        tour.set_name(t['nombre'])
                        for e in t['eventos']:
                            
                            mat_time = e['fecha'][11:][:5]
                            equipos = e['nombre'].split(' vs ')
                            mat_tv = []
                            for c in e['canales']:
                                mat_tv.append(c['nombre'])
                            
                            match = Match(tour, mat_time, equipos[0], equipos[1], mat_tv)
                            matches.append(match)
                        break
                
                tour.set_matches(matches)
        except Exception as e:
            print("ERROR: API_Sports.get_by_id()", e)
            tour = None
        
        return tour
    
    def get_img_by_ids(self, ids):
        try:
            id1 = ids[0]
            id2 = ids[1]
            team1_info = requests.get(self.url_teams + id1).json()
            team2_info = requests.get(self.url_teams + id2).json()

            if team1_info['teams'] and team2_info['teams']:
                # get images
                img1_url = team1_info['teams'][0]['strTeamBadge']
                img1_data = requests.get(img1_url).content

                with open('./outputs/img_1.png', 'wb') as img1_file:
                    img1_file.write(img1_data)

                img2_url = team2_info['teams'][0]['strTeamBadge']
                img2_data = requests.get(img2_url).content

                with open('./outputs/img_2.png', 'wb') as img2_file:
                    img2_file.write(img2_data)

                # concatenate
                image1 = Image.open('./outputs/img_1.png')
                image2 = Image.open('./outputs/img_2.png')
                middle_image = Image.open('./outputs/middle_img.png')

                width_final = int((image1.width + image2.width) * 1.40)
                height_final = int(image1.height * 1.60)
                final_img = Image.new('RGB', (width_final, height_final), (68, 73, 73))

                final_img.paste(image1, (int((width_final / 2 - image1.width) / 3), int((height_final - image1.height)/2)), image1)
                final_img.paste(image2, (int((width_final / 2 + (width_final / 2 - image2.width) * 2 / 3)), int((height_final - image1.height)/2)), image2)

                final_img.paste(middle_image, (int((width_final - middle_image.width) / 2), int((height_final - middle_image.height) / 2)), middle_image)

                img_path = './outputs/img_final.jpg'
                final_img.save(img_path)

                return img_path
        except Exception as e:
            print("error"+str(e))

        return None
