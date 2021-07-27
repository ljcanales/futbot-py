from typing import Dict, List
from src.model.Match import Match
from PIL import Image, ImageDraw, ImageFont
from textwrap import wrap
from requests import get

class BannerMaker:
    def __init__(self, url_teams: str):
        self.url_teams = url_teams

    def get_banners(self, ids: List[str], match: Match) -> Dict[str, str]:
        img_paths = {'horizontal': '', 'vertical': ''}
        try:
            if not ids[0] or not ids[1] or not type(ids[0])==str or not type(ids[1])==str:
                raise Exception("IDs not specified or not str type")
            
            image1 = self.get_team_badge(ids[0])
            image2 = self.get_team_badge(ids[1])

            img_paths['horizontal'] = self.get_horizontal_banner(image1, image2)
            img_paths['vertical'] = self.get_vertical_banner(image1, image2, match)
        except:
            pass

        return img_paths

    def get_horizontal_banner(self, image1: Image.Image, image2: Image.Image) -> str:

        try:
            # concatenate
            middle_image = Image.open('./outputs/middle_img.png')

            width_final = int((image1.width + image2.width) * 1.40)
            height_final = int(image1.height * 1.60)
            #final_img = Image.new('RGB', (width_final, height_final), (3, 64, 97))
            final_img = Image.open('./outputs/default_bg.jpg')
            #final_img = final_img.resize((width_final, height_final))

            final_img.paste(image1, (int((width_final / 2 - image1.width) / 3), int((height_final - image1.height)/2)), image1)
            final_img.paste(image2, (int((width_final / 2 + (width_final / 2 - image2.width) * 2 / 3)), int((height_final - image1.height)/2)), image2)

            final_img.paste(middle_image, (int((width_final - middle_image.width) / 2), int((height_final - middle_image.height) / 2)), middle_image)

            img_path = './outputs/img_horizontal_final.jpg'
            final_img.save(img_path)

            return img_path
        except Exception as e:
            print("ERROR: BannerMaker.get_horizontal_banner - e: ", str(e))

        return ''
    
    def get_vertical_banner(self, image1: Image.Image, image2: Image.Image, match: Match) -> str:

        try:
            # concatenate
            image1 = image1.resize((370,370))
            image2 = image2.resize((370,370))
            #middle_image = Image.open('./outputs/middle_img.png')

            #final_img = Image.new('RGB', (width_final, height_final), (3, 64, 97))
            final_img = Image.open('./outputs/default_vertical_bg.jpg')
            width_final = final_img.width
            height_final = final_img.height
            #final_img = final_img.resize((width_final, height_final))
            txt = GenerateText((width_final,height_final), 'white', match)
            # final_img.paste(image1, (int((width_final - image1.width)/2), int((height_final / 2 - image1.height) / 2)), image1)
            # final_img.paste(image2, (int((width_final - image1.width)/2), int((height_final / 2 + (height_final / 2 - image2.height) * 2 / 3))), image2)
            final_img.paste(image1, (int((width_final / 2 - image1.width) / 3), int((height_final - image1.height)/2)), image1)
            final_img.paste(image2, (int((width_final / 2 + (width_final / 2 - image2.width) * 2 / 3)), int((height_final - image1.height)/2)), image2)
            final_img.paste(txt,(0,0),txt)
            #final_img.paste(middle_image, (int((width_final - middle_image.width) / 2), int((height_final - middle_image.height) / 2)), middle_image)
            
            
            img_path = './outputs/img_vertical_final.jpg'
            final_img.save(img_path)

            return img_path
        except Exception as e:
            print("ERROR: BannerMaker.get_vertical_banner - e: ", str(e))

        return ''

    def get_team_badge(self, id: str) -> Image.Image:
        try:
            team_info = get(self.url_teams + id).json()
            img_url = team_info['teams'][0]['strTeamBadge']
            img = Image.open(get(img_url, stream=True).raw)
            return img
        except Exception as exception:
            raise Exception('ERROR: API_Sports.get_team_badge - e: ', str(exception))
    
    # def get_banner_by_urls(self, urls_lst):
    #     ''' Make match image from image urls given by parameter '''

    #     try:
    #         if not urls_lst[0] or not urls_lst[1] or not type(urls_lst[0])==str or not type(urls_lst[1])==str:
    #             raise Exception("URLs not specified or not str type")
            
    #         img1_data = requests.get(urls_lst[0]).content
    #         with open('./outputs/img_1.png', 'wb') as img1_file:
    #             img1_file.write(img1_data)

    #         img2_data = requests.get(urls_lst[1]).content
    #         with open('./outputs/img_2.png', 'wb') as img2_file:
    #             img2_file.write(img2_data)
            
    #         # concatenate
    #         image1 = Image.open('./outputs/img_1.png')
    #         image2 = Image.open('./outputs/img_2.png')
    #         middle_image = Image.open('./outputs/middle_img.png')
    #         final_img = Image.open('./outputs/default_bg.jpg')
    #         size = (400, 400)
    #         # Scale the images to be the size of the circle
    #         image1 = image1.resize(size, Image.ANTIALIAS)
    #         image2 = image2.resize(size, Image.ANTIALIAS)
    #         # Create the circle mask
    #         mask = Image.new('L', image1.size)
    #         draw = ImageDraw.Draw(mask)
    #         draw.ellipse((0, 0) + image1.size, fill=255)
            
    #         # Prepare final_img and paste
    #         width_final = final_img.width
    #         height_final = final_img.height
    #         final_img.paste(image1, (int((width_final / 2 - image1.width) / 3), int((height_final - image1.height)/2)), mask)
    #         final_img.paste(image2, (int((width_final / 2 + (width_final / 2 - image2.width) * 2 / 3)), int((height_final - image1.height)/2)), mask)
    #         final_img.paste(middle_image, (int((width_final - middle_image.width) / 2), int((height_final - middle_image.height) / 2)), middle_image)

    #         img_path = './outputs/img_users_final.jpg'
    #         final_img.save(img_path)

    #         return img_path
            
    #     except Exception as e:
    #         print("ERROR: get_banner_by_urls() "+str(e))
        
    #     return None
    

def GenerateText(size, fg, match):
    """Generate a piece of canvas and draw text on it"""
    h_acc = 200
    canvas = Image.new('RGBA', size, (0,0,0,0))
    width, height = size
    # Get a drawing context
    draw = ImageDraw.Draw(canvas)

    # Fonts
    font_equipos = ImageFont.truetype('./fonts/Roboto-Black.ttf', 110)
    font_vs = ImageFont.truetype('./fonts/Roboto-Black.ttf', 70)
    font_info = ImageFont.truetype('./fonts/Roboto-Light.ttf', 50)

    w_text, h_text = draw.textsize(match.equipo1, font=font_equipos)
    draw.text(((width-w_text)/2, h_acc), match.equipo1, fg, font=font_equipos)
    h_acc = h_acc + h_text + 60

    w_text, h_text = draw.textsize('vs', font=font_vs)
    draw.text(((width-w_text)/2, h_acc), 'vs', fg, font=font_vs)
    h_acc = h_acc + h_text + 60

    w_text, h_text = draw.textsize(match.equipo2, font=font_equipos)
    draw.text(((width-w_text)/2, h_acc), match.equipo2, fg, font=font_equipos)

    # Info text
    h_acc = int(height * 2 / 3)

    date_txt = 'Día: {} {}'.format(match.tournament.day_name, match.tournament.date.replace('-','/'))
    w_text, h_text = draw.textsize(date_txt, font=font_info)
    draw.text((20, h_acc), date_txt, fg, font=font_info)
    h_acc = h_acc + h_text + 60

    w_text, h_text = draw.textsize('Hora: {}'.format(match.time), font=font_info)
    draw.text((20, h_acc), 'Hora: {}'.format(match.time), fg, font=font_info)
    h_acc = h_acc + h_text + 60

    tv_text = wrap('TV: ' + ' - '.join(match.tv), 40)
    for t in tv_text:
        draw.text((20, h_acc), t, fg, font=font_info)
        w_text, h_text = draw.textsize(t, font=font_info)
        h_acc = h_acc + h_text + 20

    return canvas


