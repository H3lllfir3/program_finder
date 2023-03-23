from dataclasses import dataclass


@dataclass
class ProgramData:
    platform: str
    program_name: str
    company_name: str
    program_url: str

    def dict(self):
        return {'platform': self.platform, 'program_name': self.program_name, 'company_name': self.company_name, 'program_url': self.program_url}
