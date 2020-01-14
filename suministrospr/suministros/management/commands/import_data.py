from django.core.management.base import BaseCommand, CommandError
from suministros.models import Suministro
from os import path
import glob
import json
from suministros.constants import MUNICIPALITIES

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_arguments(target_folder, type=str)

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
                        suministro.content = item.content
                        suministro.title = item.title
                        if item.municipio in MUNICIPALITIES:
                            suministro.municipality = item.municipio
                            suministro.save()
                        else :
                            self.stderr.write(f'Unrecognized municipality {item.municipio} in file {file_path}')
                            suministro.municipality = 'N/A'
            except EnvironmentError:
                self.stderr.write(f'There was an error reading file {file_path}')


