import glob
import json
from os import path

import unicodedata
from django.core.management.base import BaseCommand, CommandError

from ...models import Suministro
from ...constants import MUNICIPALITIES

class Command(BaseCommand):
    def normalize(self, text):
        nfkd_form = unicodedata.normalize('NFKD', text)
        return "".join([c for c in nfkd_form if not unicodedata.combining(c)])

    def add_arguments(self, parser):
        parser.add_argument('target_folder', type=str)

    def handle(self, *args, **options):
        target_folder = options['target_folder']

        file_paths = glob.glob(f'{target_folder}/*.json')

        for file_path in file_paths:
            self.stdout.write(f'Importing file {file_path}')
            try:
                with open(file_path, 'r') as json_file:
                    data = json.load(json_file)
                    for item in data:
                        suministro = Suministro()
                        suministro.content = item['content']
                        suministro.title = item['title']

                        municipio = self.normalize(item.get('municipio', ''))
                        
                        if municipio in MUNICIPALITIES:
                            suministro.municipality = municipio
                            suministro.save()
                        else :
                            self.stderr.write(f'Unrecognized municipality {municipio} in file {file_path}')
                            suministro = None
            except EnvironmentError:
                self.stderr.write(f'There was an error reading file {file_path}')

