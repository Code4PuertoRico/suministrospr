import glob
import json
import unicodedata

from django.core.management.base import BaseCommand
from django.utils.html import strip_tags
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
        except Suministro.DoesNotExist:
            return None

    def get_import_data(self, data):
        content = data.get("content", "")
        title = data.get("title", "")
        municipality = self.normalize(data.get("municipio", ""))

        if municipality == "las-maria":
            municipality = "las-marias"

        if title == "EMPTY_TITLE":
            striped_title = strip_tags(content).strip()[:20]

            if striped_title:
                title = f"{striped_title}..."
            else:
                title = "N/A"

        slug = (
            data.get("url")
            .replace("https://suministrospr.com/sectores", "")
            .replace("/", "")
        )
        return {
            "title": title,
            "content": content,
            "municipality": municipality,
            "slug": slug,
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
            self.stdout.write(f"=> Importing file {file_path}")
            try:
                with open(file_path, "r") as json_file:
                    data = json.load(json_file)
                    for item in data:
                        import_data = self.get_import_data(item)
                        slug = import_data.get("slug")
                        existing_suministro = self.get_suministro(slug)

                        suministro_form = self.get_form(
                            import_data, existing_suministro
                        )

                        if suministro_form.is_valid():
                            suministro = suministro_form.save(commit=False)
                            suministro.slug = slug
                            suministro.save()

                            if existing_suministro:
                                self.stdout.write(
                                    f"==> Updating slug={existing_suministro.slug}"
                                )
                            else:
                                self.stdout.write(
                                    f"==> Creating slug={suministro.slug}"
                                )
                        else:
                            self.stderr.write(
                                f"==> There's an issue with the data from file {file_path} - {suministro_form.errors.as_json()}"
                            )
            except EnvironmentError:
                self.stderr.write(f"=> There was an error reading file {file_path}")
