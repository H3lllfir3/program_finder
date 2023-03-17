import requests
import random
import logging
from typing import List
from dataclasses import dataclass
from models import Program, Programs


@dataclass
class Program:
    platform: str
    program_name: str
    company_name: str
    program_url: str



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

bugcrowd_programs = BugcrowdPrograms()
new_programs = bugcrowd_programs.get_programs()
