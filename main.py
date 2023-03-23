import logging
import random
import requests

from typing import List

import sys
sys.dont_write_bytecode = False


import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')


import django
import jdatetime
from dotenv import load_dotenv
django.setup()


from db.models import Programs
from bot import DiscordClient
from hackerone import HackeroneScraper


logging.basicConfig(filename='debug.log',
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setLevel(logging.DEBUG)
handler.setFormatter(logging.Formatter('%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s'))

logger = logging.getLogger(__name__)
logger.addHandler(handler)


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

log_messages = []


class Program:
    platform: str
    program_name: str
    company_name: str
    program_url: str

    def dict(self):
        return {'platform': self.platform, 'program_name': self.program_name, 'company_name': self.company_name, 'program_url': self.program_url}


class BugcrowdPrograms:
    BASE_URL = 'https://bugcrowd.com/programs.json'
    PAGE_SIZE = 20

    def __init__(self):
        self.programs = []

    def get_programs(self) -> List[Program]:
        """
        Get bugcrowd programs list and return a list of Program objects
        containing program url and program information
        """
        self._fetch_programs()
        lst = self._filter_new_programs()
        self._add_programs_to_db(lst)
        return lst

    def _fetch_programs(self):
        page = 0
        while True:
            url = f'{self.BASE_URL}?sort[]=promoted-desc&vdp[]=false&page[]={page}'
            headers = {'User-Agent': random.choice(USER_AGENTS)}
            try:
                response = requests.get(url, timeout=10, headers=headers)
                response.raise_for_status()
                logging.info(f'Request sent to - {url}')
                page += 1
                json_data = response.json()
                if not json_data['programs']:
                    logging.info(f'The last page of the programs is - {page}')
                    break
                self.programs += json_data['programs']
            except requests.exceptions.RequestException as e:
                logging.error(f'Request to {url} failed - {e}')
                break

    def _filter_new_programs(self) -> List[Program]:
        lst = []
        programs_in_db = Programs.objects.filter(data__platform='Bugcrowd')
        list_of_programs_in_db = [program.data for program in programs_in_db]

        for program in self.programs:
            url = f'https://bugcrowd.com{program["program_url"]}'
            try:
                program_data = Program(platform='Bugcrowd',
                                       program_name=program['name'].lower(),
                                       company_name=program['tagline'].lower(),
                                       program_url=url)
                if program_data not in list_of_programs_in_db:
                    lst.append(program_data)
            except Exception as e:
                logging.error(f'Error while parsing data - {e}')
        return lst

    def _add_programs_to_db(self, lst: List[Program]):
        Programs.objects.bulk_create([Programs(data=program) for program in lst])

class Intigriti:
    def __init__(self):
        self.log_messages = []
    
    def get_programs(self) -> List[dict]:
        """
        Get intigriti programs list and returns 
        Json object contains Company name and program URI.
        """
        logging.info('Intigriti function runs.')
        url = "https://api.intigriti.com/core/researcher/program"
        headers = self._get_headers()
        response = self._send_request(url, headers)
        logging.info(f'Request send to - {url}')
        lst = self._parse_response(response, url)
        return lst

    def _get_headers(self) -> dict:
        return {
            "accept": "application/json",
            "authorization": "Bearer 0855A112E633BD46EC3C04A206C67DCA673744694B693083E18F40C6CB366324-1",
            "User-Agent": random.choice(USER_AGENTS)
        }

    def _send_request(self, url: str, headers: dict) -> requests.Response:
        try:
            response = requests.get(url, headers=headers)
            return response
        except requests.exceptions.RequestException as e:
            logging.error(f"Error while sending request - {e}")
            self.log_messages.append(f"Error while sending request - {e}")
            return None

    def _parse_response(self, response: requests.Response, url: str) -> List[dict]:
        lst = []
        try:
            programs_lst = response.json()
            if not programs_lst:
                logging.warning(f"Data doesn't exist at - {url}")
                self.log_messages.append(f"Data doesn't exist at - {url}")
            if programs_lst:
                lst = self._get_new_programs(programs_lst)
        except:
            logging.error(f'Error while parsing response - {response}')
            self.log_messages.append(f'Error while parsing response - {response}')
        return lst

    def _get_new_programs(self, programs_lst: List[dict]) -> List[dict]:
        lst = []
        # list of programs which are already in the database.
        programs_in_db = Programs.objects.filter(data__platform='Intigriti')
        list_of_programs_in_db = [program.data for program in programs_in_db]
        for program in programs_lst:
            try:
                company_handle = program['companyHandle'].lower()
                handle = program['handle'].lower()
                program_url = f'https://app.intigriti.com/programs/{company_handle}/{handle}/detail'
                data = ProgramData(platform='Intigriti', program_name=handle, company_name=company_handle, program_url=program_url).dict()

                if not data in list_of_programs_in_db:
                    Programs.objects.create(data=data)
                    lst.append(data)

            except Exception as e:
                logging.error(f'Error while parsing data - {e}')
                self.log_messages.append(f"The form of the data changed {url}")
        return lst
        

def main():
    # # Print start time
    # time = jdatetime.datetime.now().strftime("%a, %d %b %Y")
    # print(f'Program started at {time}')

    # # Initialize lists
    # bugcrowd_lst = []
    # intigriti_lst = []
    # hackerone_lst = []

    # # Get data from Bugcrowd
    # print(f'Getting data from Bugcrowd...')
    # try:
    #     bugcrowd_lst = get_bugcrowd_programs()
    #     print(f'Got {len(bugcrowd_lst)} programs from Bugcrowd')
    # except Exception as e:
    #     print(f'Error while getting Bugcrowd data: {str(e)}')

    # # Get data from Intigriti
    # print(f'Getting data from Intigriti...')
    # try:
    #     intigriti_lst = get_intigriti_programs()
    #     print(f'Got {len(intigriti_lst)} programs from Intigriti')
    # except Exception as e:
    #     print(f'Error while getting Intigriti data: {str(e)}')

    # # Get data from Hackerone
    # print(f'Getting data from Hackerone...')
    # try:
    #     hackerone_lst = get_hackerone_programs()
    #     print(f'Got {len(hackerone_lst)} programs from Hackerone')
    # except Exception as e:
    #     print(f'Error while getting Hackerone data: {str(e)}')

    # # Merge lists
    # lst = bugcrowd_lst + intigriti_lst + hackerone_lst

    # # Send data to Discord
    # print('Sending data to Discord...')
    # send_data_to_discord(lst)
    hackerone = HackeroneScraper(token='FbLO2BcOLeGeHZsd7KnlyJ0yk5JLxsoJKTFdAgEvnrw=',username='h3llfir3')

    programs = hackerone.get_programs()
    print(programs)
    print('ended.')


if __name__ == '__main__':
    main()
