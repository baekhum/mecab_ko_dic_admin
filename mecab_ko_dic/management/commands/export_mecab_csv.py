import csv
import os
from django.core.management.base import BaseCommand, CommandError
from mecab_ko_dic.models import Mecab_Ko_Dic, OriginType


class Command(BaseCommand):
    help = "Export MeCab dictionary entries to CSV"

    def add_arguments(self, parser):
        parser.add_argument("output_path", type=str, help="Path to the output CSV file")
        parser.add_argument(
            "--type",
            type=str,
            choices=[t.value for t in OriginType],
            default=OriginType.USER.value,
            help="Origin type to export (default: USER)",
        )
        parser.add_argument(
            "--category",
            type=str,
            help="Filter by semantic class (의미_부류), e.g., '지명'",
        )
        parser.add_argument("--encoding", type=str, default="utf-8", help="File encoding (default: utf-8)")

    def handle(self, *args, **options):
        output_path = options["output_path"]
        origin_type = options["type"]
        category = options["category"]
        encoding = options["encoding"]

        queryset = Mecab_Ko_Dic.objects.filter(origin_type=origin_type)
        if category:
            queryset = queryset.filter(의미_부류__icontains=category)

        count = queryset.count()
        if count == 0:
            self.stdout.write(self.style.WARNING("No entries found matching the criteria."))
            return

        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)

            with open(output_path, "w", encoding=encoding, newline="") as f:
                writer = csv.writer(f)
                for entry in queryset:
                    writer.writerow([
                        entry.표층형,
                        "0", "0", "0", # LID, RID, Cost (defaults)
                        entry.품사_태그,
                        entry.의미_부류 or "*",
                        entry.종성_유무 or "*",
                        entry.읽기 or entry.표층형,
                        entry.타입 or "*",
                        entry.첫번째_품사 or "*",
                        entry.마지막_품사 or "*",
                        entry.표현 or "*"
                    ])

            self.stdout.write(self.style.SUCCESS(f"Successfully exported {count} entries to {output_path}"))

        except Exception as e:
            raise CommandError(f"Export failed: {str(e)}")
