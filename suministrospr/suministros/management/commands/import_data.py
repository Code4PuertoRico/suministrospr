import glob
import json
from os import path

import unicodedata
from django.core.management.base import BaseCommand, CommandError

from ...forms import SuministroModelForm
from ...constants import MUNICIPALITIES
from ...models import Suministro

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
                        import_data = {
                            "title": item.get("title", ""),
                            "content": item.get("content", ""),
                            "municipality":self.normalize(item.get("municipio", ""))
                        }
                        suministro = SuministroModelForm(import_data)

                        if suministro.is_valid():
                            suministro.save()
                        else:
                            self.stderr.write(f"There's an issue with the data for {import_data} from file {file_path}")
            except EnvironmentError:
                self.stderr.write(f'There was an error reading file {file_path}')

