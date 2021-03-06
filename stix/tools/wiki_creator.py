#create or edit an wiki page
#don't upload it to github
import sys
import time
import requests
from datetime import datetime
from dateutil import parser as dtparser
from stix.core import mongo_db as db
from stix.spice import solo
mdb = db.MongoDB()
S = requests.Session()
HOST= "https://pub023.cs.technik.fhnw.ch"
URL=HOST+"/wiki/api.php"
threshold=600
class WikiCreator(object):
    def __init__(self):
        self.CSRF_TOKEN=''
    #def wiki_login(self):
        # Step 1: GET request to fetch login token
        PARAMS_0 = {
            "action": "query",
            "meta": "tokens",
            "type": "login",
            "format": "json"
        }

        R = S.get(url=URL, params=PARAMS_0)
        DATA = R.json()
        print(DATA)

        LOGIN_TOKEN = DATA['query']['tokens']['logintoken']

        # Step 2: POST request to log in. Use of main account for login is not
        # supported. Obtain credentials via Special:BotPasswords
        # (https://www.mediawiki.org/wiki/Special:BotPasswords) for lgname & lgpassword
        PARAMS_1 = {
            "action": "login",
            "lgname": "data_center",
            "lgpassword": "gostix2021",
            "lgtoken": LOGIN_TOKEN,
            "format": "json"
        }

        R = S.post(URL, data=PARAMS_1)

        # Step 3: GET request to fetch CSRF token
        PARAMS_2 = {
            "action": "query",
            "meta": "tokens",
            "format": "json"
        }

        R = S.get(url=URL, params=PARAMS_2)
        DATA = R.json()
        print(DATA)

        try:
            self.CSRF_TOKEN = DATA['query']['tokens']['csrftoken']
        except Exception as e:
            print(e)

            print('Login failed!')



    def get_page(self, title):
        PARAMS = {
            "action": "parse",
            "page": title,
            "format": "json"
            }
        R = S.get(url=URL, params=PARAMS)
        DATA = R.json()
        try:
            return DATA["parse"]["text"]["*"]
        except KeyError:
            #page not exist
            return ''


    def format_page(self, flare):
        peak_utc=flare['peak_utc']
        uid=str(flare['peak_counts']).replace('.','')
        #unique_id, anti-bots
        print('Flare id: ', flare['_id'])
        now=datetime.now().strftime('%c')
        flare_id=flare['flare_id']
        goes_class_major='Unknown' 
        goes_class='Unknown'
        if 'goes' in  flare:
            goes_class=flare['goes'].get('class','Unknown') 
            if goes_class != 'Unknown':
                goes_class_major=goes_class[0]

        try:
            emph=solo.get_solo_ephemeris(peak_utc,peak_utc)
            tdiff=f"{emph['light_time_diff'][0]:.03f} s"
            angle=f"{emph['earth_sun_solo_angle'][0]:.03f} deg"
            sol_sc_dist=f"{emph['sun_solo_r'][0]:.03f} au"
            elevation=f"{emph['elevation'][0]:.03f} deg"
            sun_d=f"{emph['sun_angular_diameter'][0]*60:.03f} arcsec "
            light_time=emph['light_time_diff'][0]
        except Exception as e:
            light_time=0
            print(e)
            sol_sc_dist='N/A'
            elevation='N/A'
            tdiff='N/A'
            angle='N/A'
            sun_d='N/A'
        title=f"STIX_Flare:_{flare['flare_id']}"
        old_content=self.get_page(title)
        fields=[]
        if 'id="STIX"' not in old_content:
            header=(f'''[[Category:STIX_Flares]]\n'''
                    f'''[[Category:GOES Class {goes_class}]]\n'''
                    f'''[[Category:{goes_class_major} Class Flares]]\n'''
                f'''<!-- The session below was created by the data center wiki bot at {now}. \n '''
                f'''  Please contact hualin.xiao@fhnw.ch if you wish to contribute code to the bot. -->\n'''
                "== Flare Info == \n"
                f"** Flare ID: {flare['flare_id']}\n"
                f"** GOES Class: {goes_class}\n"
                f"** Light travel time difference: {tdiff}\n"
                f"** Earth-Sun-SC angle: {angle}\n"
                f"** Sun-SC distance: {sol_sc_dist}\n"
                f"** SC elevation : {elevation}\n"
                f"** Sun angular diameter (viewing from Solar Orbiter): {sun_d}\n"
                f"** Flare peak UTC: {flare['peak_utc']}\n")
            fields.append(header)
        fields.append('== STIX observation ==')
        fields.append(f'<div data-flareId="{flare_id}" data-lt="{light_time}"  data-uid="{uid}" data-peakUTC="{peak_utc}" id="stix-obs"></div>')
        utc_dt=dtparser.parse(peak_utc)
        date=utc_dt.strftime('%Y%m%d')
        year=utc_dt.year
        fields.append('== Simultaneous observations ==')
        fields.append(f'<div data-year="{year}" data-date="{date}" data-flareId="{flare_id}" data-lt="{light_time}"  data-uid="{uid}" data-peakUTC="{peak_utc}"  id="sim-obs"></div>')


        content='\n'.join(fields)+'\n'
        
        return title, content

    def create_page(self, title, content):
        if title is None or content is None:
            return
        if not self.CSRF_TOKEN:
            print("can not create page because CSRF token not ready")
        print("inserting:", title)
        print(content)
        time.sleep(10)
        # Step 4: POST request to edit a page
        PARAMS_3 = {
            "action": "edit",
            "bot":"true",
            "title": title,
            "token": self.CSRF_TOKEN,
            "format": "json",
            "sectiontitle":'Observations',
            "appendtext":content 

        }

        R = S.post(URL, data=PARAMS_3)
        DATA = R.json()
        print(DATA)
        PARAMS_3['captchaid']=DATA['edit']['captcha']['id']
        PARAMS_3['captchaword']='stix'
        R = S.post(URL, data=PARAMS_3)
        DATA = R.json()
        print(DATA)
    def touch_wiki_for_flare(self, _id):
        fdb=mdb.get_collection('flares')
        doc=fdb.find_one({'_id':_id, 'hidden':False})
        if not doc:
            print(f'Flare {_id} not file in db!')
            return
        title,content=self.format_page(doc)
        self.create_page(title, content)
        mdb.update_flare_joint_obs(_id, 'wiki', True)

    def touch_wiki_for_file(self,file_id):
        fdb=mdb.get_collection('flares')
        flares=fdb.find({'run_id':file_id, 'hidden':False})
        if not flares:
            print(f'Flare {file_id} not file in db!')
            return
        for doc in flares:
            if doc['peak_counts']<threshold:
                continue
            print(f'create wiki for {doc["_id"]}')
            _id=doc['_id']
            flare_id=doc['flare_id']
            self.touch_wiki_for_flare(_id)

wiki_bot=WikiCreator()

if __name__=='__main__':
    if len(sys.argv)==2:
        fid=int(sys.argv[1])
        wiki_bot.touch_wiki_for_flare(fid)
    elif len(sys.argv)==3:
        start_id=int(sys.argv[1])
        end_id=int(sys.argv[2])
        for i in range(start_id, end_id+1):
            wiki_bot.touch_wiki_for_flare(i)
    else:
        print('usage:\nmain <file id> \n main <start file_id> <end file_id>')
        print('file id not provided')
