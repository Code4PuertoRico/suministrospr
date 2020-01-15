import glob
import json

import unicodedata
from django.core.management.base import BaseCommand
from django.utils.text import slugify

from ...forms import SuministroModelForm
from ...models import Suministro


class Command(BaseCommand):
    def normalize(self, text):
        nfkd_form = unicodedata.normalize("NFKD", text)
        return slugify("".join([c for c in nfkd_form if not unicodedata.combining(c)]))

    def add_arguments(self, parser):
        parser.add_argument("target_folder", type=str)

    def get_suministro(self, slug):
        try:
            return Suministro.objects.get(slug=slug)
        except:
            return None

    def get_import_data(self, data):
        municipality = self.normalize(data.get("municipio", ""))
        title = data.get("title", "")
        return {
            "title": title,
            "content": data.get("content", ""),
            "municipality": municipality,
        }

    def get_form(self, import_data, suministro):
        if suministro:
            return SuministroModelForm(import_data, instance=suministro)
        else:
            return SuministroModelForm(import_data)

    def handle(self, *args, **options):
        target_folder = options["target_folder"]

        file_paths = glob.glob(f"{target_folder}/*.json")

        for file_path in file_paths:
            self.stdout.write(f"Importing file {file_path}")
            try:
                with open(file_path, "r") as json_file:
                    data = json.load(json_file)
                    for item in data:
                        import_data = self.get_import_data(item)
                        slug = slugify(f"{import_data.get('title')} {import_data.get('municipality')}")
                        suministro = self.get_suministro(slug)

                        suministro_form = self.get_form(import_data, suministro)

                        if suministro_form.is_valid():
                            suministro_form.save()
                        else:
                            self.stderr.write(
                                f"There's an issue with the data from file {file_path} - {suministro.errors.as_json()}"
                            )
            except EnvironmentError:
                self.stderr.write(f"There was an error reading file {file_path}")

