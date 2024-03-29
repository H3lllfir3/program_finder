import random
import logging
import requests

from typing import List
from django.db import IntegrityError

from db.models import Programs
from datahandler import ProgramData


class HackeroneScraper:
    """
    A class to scrape programs from Hackerone and store them in a database
    """
    def __init__(self, username: str, token: str) -> None:
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
        while True: # paginate to get all data.
            url = f'https://api.hackerone.com/v1/hackers/programs?page[number]={page}'
            r = requests.get(
                url,
                auth=(self.username, self.token),
                headers={'Accept': 'application/json'}
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
        new_programs = []
        programs_in_db = Programs.objects.filter(data__platform='Hackerone')
        list_of_programs_url = [program.data['program_url'] for program in programs_in_db]
        for program in programs:
            url = f"https://hackerone.com/{program['attributes']['handle'].lower()}"
            if program['attributes']['submission_state'] == 'open' and program['attributes']['state'] == 'public_mode':
                try:
                    data = ProgramData(
                        platform='Hackerone',
                        program_name=program['attributes']['handle'].lower(),
                        company_name=program['attributes']['name'].lower(),
                        program_url=url
                    ).dict()
                    if url not in list_of_programs_url:
                        new_programs.append(Programs(data=data))
                except Exception as e:
                    logging.error(f'Error happend while parsing data - {e}')
        try:
            Programs.objects.bulk_create(new_programs)
            lst = [program.data['program_url']  for program in new_programs]
        except IntegrityError as e:
            logging.error(f'Error while bulk creating programs - {e}')
        return lst
