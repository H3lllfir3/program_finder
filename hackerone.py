import random
import logging
import requests

from typing import List
from dataclasses import dataclass

@dataclass
class Program:
    platform: str
    program_name: str
    company_name: str
    program_url: str

class HackeroneScraper:
    """
    A class to scrape programs from Hackerone and store them in a database
    """
    def __init__(self, user_agents: List[str], username: str, password: str):
        self.user_agents = user_agents
        self.username = username
        self.password = password

    def get_programs(self) -> List[Program]:
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
                'User-Agent': random.choice(self.user_agents)
            }
            url = f'https://api.hackerone.com/v1/hackers/programs?page%5Bnumber%5D={page}'
            r = requests.get(
                url,
                auth=(self.username, self.password),
                headers=headers
            )
            logging.info(f'Request sent to - {url}')
            page += 1
            if not r.json()['data']:
                logging.warning(f"Data doesn't exist at - {url}")
                break
            programs += r.json()['data']
        return programs

    def _process_programs(self, programs: List[dict]) -> List[Program]:
        """
        Processes scraped programs and returns a list of Program instances
        """
        lst = []
        programs_in_db = Programs.objects.filter(data__platform='Hackerone')
        list_of_programs_in_db = [program.data for program in programs_in_db]
        for program in programs:
            url = f"https://hackerone.com/{program['attributes']['handle'].lower()}"
            if program['attributes']['submission_state'] == 'open' and program['attributes']['state'] == 'public_mode':
                data = Program(
                    platform='Hackerone',
                    program_name=program['attributes']['handle'].lower(),
                    company_name=program['attributes']['name'].lower(),
                    program_url=url
                )
                if data not in list_of_programs_in_db:
                    Programs.objects.create(data=data)
                    lst.append(data)
        return lst

from myapp.models import Programs  # assuming this is the model used to store programs in the database
from myapp.constants import USER_AGENTS  # assuming this is a list of user agents used to make HTTP requests

scraper = HackeroneScraper(user_agents=USER_AGENTS, username='h3llfir3', password='FbLO2BcOLeGeHZsd7KnlyJ0yk5JLxsoJKTFdAgEvnrw=')

programs = scraper.get_programs()

# Do something with the list of programs returned by the get_programs method
