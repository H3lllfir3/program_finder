import requests
import logging
import random
from typing import List

from datahandler import ProgramData
from constants import USER_AGENTS
from db.models import Programs


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
            "authorization": "Bearer 94B4C1FCD1F452E0288284CBEAA04F447E6E0F5FAF4B9D430EABF5BDFA834644-1",
            "User-Agent": random.choice(USER_AGENTS)
        }

    def _send_request(self, url: str, headers: dict) -> requests.Response:
        try:
            response = requests.get(url, headers=headers)
            return response
        except requests.exceptions.RequestException as e:
            logging.error(f"1Error while sending request - {e}")
            return None

    def _parse_response(self, response: requests.Response, url: str) -> List[dict]:
        lst = []
        try:
            programs_lst = response.json()
            if not programs_lst:
                message = f"Data doesn't exist at - {url}"
                logging.warning(message)
            else:
                lst = self._get_new_programs(programs_lst)
        except Exception as e:
            message = f'Error while parsing response - {response}: {e}'
            logging.error(message)
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

        return lst

