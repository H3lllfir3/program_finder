import random
import logging
import requests

from typing import List

from constants import USER_AGENTS 
from db.models import Programs
from datahandler import ProgramData


class HackeroneScraper:
    """
    A class to scrape programs from Hackerone and store them in a database
    """
    def __init__(self, username: str, token: str):
        self.username = username
        self.token = token

    def get_programs(self) -> List[Programs]:
        """
        Get hackerone programs list and returns 
        Json object contains Company name and program URI.
        """
        programs = self._scrape_programs()
        lst = self._process_programs(programs)
        return lst

    def _scrape_programs(self) -> List[dict]:
        """
        Scrapes programs from Hackerone
        """
        programs = []
        page: int = 0
        while True:
            headers = {
                'Accept': 'application/json',
                'User-Agent': random.choice(USER_AGENTS)
            }
            url = f'https://api.hackerone.com/v1/hackers/programs?page%5Bnumber%5D={page}'
            r = requests.get(
                url,
                auth=(self.username, self.token),
                headers=headers
            )
            logging.info(f'Request sent to - {url}')
            page += 1
            if not r.json()['data']:
                logging.warning(f"Data doesn't exist at - {url}")
                break
            programs += r.json()['data']
        return programs

    def _process_programs(self, programs: List[dict]) -> List[Programs]:
        """
        Processes scraped programs and returns a list of Program instances
        """
        lst = []
        programs_in_db = Programs.objects.filter(data__platform='Hackerone')
        list_of_programs_in_db = [program.data for program in programs_in_db]
        for program in programs:
            url = f"https://hackerone.com/{program['attributes']['handle'].lower()}"
            if program['attributes']['submission_state'] == 'open' and program['attributes']['state'] == 'public_mode':
                data = ProgramData(
                    platform='Hackerone',
                    program_name=program['attributes']['handle'].lower(),
                    company_name=program['attributes']['name'].lower(),
                    program_url=url
                ).dict()
                if data not in list_of_programs_in_db:
                    Programs.objects.create(data=data)
                    lst.append(data)
        return lst
