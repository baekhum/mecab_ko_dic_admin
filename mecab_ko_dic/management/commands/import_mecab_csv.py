import csv
from django.core.management.base import BaseCommand, CommandError
from mecab_ko_dic.models import Mecab_Ko_Dic, OriginType


class Command(BaseCommand):
    help = "Import MeCab dictionary from CSV file"

    def add_arguments(self, parser):
        parser.add_argument("file_path", type=str, help="Path to the CSV file")
        parser.add_argument(
            "--type",
            type=str,
            choices=[t.value for t in OriginType],
            default=OriginType.SYSTEM.value,
            help="Origin type (SYSTEM, USER, COMPOUND)",
        )
        parser.add_argument("--batch_size", type=int, default=1000, help="Batch size for bulk_create")

    def handle(self, *args, **options):
        file_path = options["file_path"]
        origin_type = options["type"]
        batch_size = options["batch_size"]

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                reader = csv.reader(f)
                batch = []
                count = 0

                for row in reader:
                    if not row:
                        continue

                    entry = Mecab_Ko_Dic(
                        표층형=row[0],
                        품사_태그=row[4] if len(row) > 4 else "",
                        의미_부류=row[5] if len(row) > 5 else None,
                        종성_유무=row[6] if len(row) > 6 else "",
                        읽기=row[7] if len(row) > 7 else "",
                        타입=row[8] if len(row) > 8 else None,
                        첫번째_품사=row[9] if len(row) > 9 else None,
                        마지막_품사=row[10] if len(row) > 10 else None,
                        표현=row[11] if len(row) > 11 else None,
                        origin_type=origin_type,
                    )
                    batch.append(entry)

                    if len(batch) >= batch_size:
                        Mecab_Ko_Dic.objects.bulk_create(batch)
                        count += len(batch)
                        batch = []
                        self.stdout.write(f"Imported {count} entries...")

                if batch:
                    Mecab_Ko_Dic.objects.bulk_create(batch)
                    count += len(batch)

                self.stdout.write(self.style.SUCCESS(f"Successfully imported {count} entries from {file_path}"))

        except FileNotFoundError:
            raise CommandError(f'File "{file_path}" does not exist')
        except Exception as e:
            raise CommandError(f"An error occurred: {str(e)}")
