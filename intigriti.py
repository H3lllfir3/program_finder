import requests
import logging
import random
from typing import List
from dataclasses import dataclass

@dataclass
class Data:
    platform: str
    program_name: str
    company_name: str
    program_url: str
    
    def dict(self):
        return {'platform': self.platform, 'program_name': self.program_name, 'company_name': self.company_name, 'program_url': self.program_url}

class Programs:
    def __init__(self):
        self.log_messages = []
    
    def intigriti(self) -> List[dict]:
        """
        Get intigriti programs list and returns 
        Json object contains Company name and program URI.
        """
        logging.info('Intigriti function runs.')
        url = "https://api.intigriti.com/core/researcher/program"
        headers = self.get_headers()
        response = self.send_request(url, headers)
        logging.info(f'Request send to - {url}')
        lst = self.parse_response(response, url)
        return lst

    def get_headers(self) -> dict:
        return {
            "accept": "application/json",
            "authorization": "Bearer 0855A112E633BD46EC3C04A206C67DCA673744694B693083E18F40C6CB366324-1",
            "User-Agent": random.choice(USER_AGENTS)
        }

    def send_request(self, url: str, headers: dict) -> requests.Response:
        try:
            response = requests.get(url, headers=headers)
            return response
        except requests.exceptions.RequestException as e:
            logging.error(f"Error while sending request - {e}")
            self.log_messages.append(f"Error while sending request - {e}")
            return None

    def parse_response(self, response: requests.Response, url: str) -> List[dict]:
        lst = []
        try:
            programs_lst = response.json()
            if not programs_lst:
                logging.warning(f"Data doesn't exist at - {url}")
                self.log_messages.append(f"Data doesn't exist at - {url}")
            if programs_lst:
                lst = self.get_new_programs(programs_lst)
        except:
            logging.error(f'Error while parsing response - {response}')
            self.log_messages.append(f'Error while parsing response - {response}')
        return lst

    def get_new_programs(self, programs_lst: List[dict]) -> List[dict]:
        lst = []
        # list of programs which are already in the database.
        programs_in_db = Programs.objects.filter(data__platform='Intigriti')
        list_of_programs_in_db = [program.data for program in programs_in_db]
        for program in programs_lst:
            try:
                company_handle = program['companyHandle'].lower()
                handle = program['handle'].lower()
                program_url = f'https://app.intigriti.com/programs/{company_handle}/{handle}/detail'
                data = Data(platform='Intigriti', program_name=handle, company_name=company_handle, program_url=program_url).dict()

                if not data in list_of_programs_in_db:
                    Programs.objects.create(data=data)
                    lst.append(data)

            except Exception as e:
                logging.error(f'Error while parsing data - {e}')
                self.log_messages.append(f"The form of the data changed {url}")
        return lst

programs = Programs()
results = programs.intigriti()