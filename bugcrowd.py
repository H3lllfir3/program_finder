import requests
import random
import logging
from typing import List

from datahandler import ProgramData
from db.models import Programs
from constants import USER_AGENTS


class Bugcrowd:
    def __init__(self):
        self.BASE_URL = 'https://bugcrowd.com/programs.json'
        self.PAGE_SIZE = 20

    def get_programs(self) -> List[Programs]:
        """
        Get bugcrowd programs list and return a list of Program objects
        containing program url and program information
        """
        programs = self._fetch_programs()
        lst = self._filter_new_programs(programs)
        return lst

    def _fetch_programs(self) -> List:
        programs = []
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
                programs += json_data['programs']
            except requests.exceptions.RequestException as e:
                logging.error(f'Request to {url} failed - {e}')
                break
        return programs

    def _filter_new_programs(self, programs: List) -> List[Programs]:
        lst = []
        programs_in_db = Programs.objects.filter(data__platform='Bugcrowd').values_list('data', flat=True)

        for program in programs:
            url = f'https://bugcrowd.com{program["program_url"]}'
            try:
                program_data = ProgramData(platform='Bugcrowd',
                                       program_name=program['name'].lower(),
                                       company_name=program['tagline'].lower(),
                                       program_url=url).dict()
                if program_data not in programs_in_db:
                    Programs.objects.create(data=program_data)
                    lst.append(program_data)
            except Exception as e:
                logging.error(f'Error while parsing data - {e}')
        return lst


