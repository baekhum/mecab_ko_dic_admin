import csv
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from mecab_ko_dic.models import Mecab_Ko_Dic, OriginType, PosTag


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
        parser.add_argument("--encoding", type=str, default="utf-8", help="File encoding (default: utf-8)")

    def handle(self, *args, **options):
        file_path = options["file_path"]
        origin_type = options["type"]
        batch_size = options["batch_size"]
        encoding = options["encoding"]

        processed_count = 0
        success_count = 0
        error_count = 0
        errors = []

        try:
            with open(file_path, "r", encoding=encoding, newline="") as f:
                reader = csv.reader(f)
                batch = []
                
                with transaction.atomic():
                    for line_num, row in enumerate(reader, start=1):
                        processed_count += 1
                        if not row:
                            continue

                        # Basic validation
                        if len(row) < 5:
                            error_msg = f"Line {line_num}: Malformed row (not enough fields)"
                            self.stderr.write(self.style.ERROR(error_msg))
                            errors.append(error_msg)
                            error_count += 1
                            continue

                        pos_tag = row[4]
                        if len(pos_tag) > 4:
                            error_msg = f"Line {line_num}: pos_tag too long: '{pos_tag}'"
                            self.stderr.write(self.style.ERROR(error_msg))
                            errors.append(error_msg)
                            error_count += 1
                            continue
                        
                        # Validate pos_tag exists in PosTag choices
                        if pos_tag not in [choice[0] for choice in PosTag.choices]:
                             error_msg = f"Line {line_num}: Invalid pos_tag: '{pos_tag}'"
                             self.stderr.write(self.style.ERROR(error_msg))
                             errors.append(error_msg)
                             error_count += 1
                             continue

                        try:
                            entry = Mecab_Ko_Dic(
                                표층형=row[0],
                                품사_태그=pos_tag,
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
                            success_count += 1
                        except Exception as e:
                            error_msg = f"Line {line_num}: unexpected error: {str(e)}"
                            self.stderr.write(self.style.ERROR(error_msg))
                            errors.append(error_msg)
                            error_count += 1
                            continue

                        if len(batch) >= batch_size:
                            Mecab_Ko_Dic.objects.bulk_create(batch)
                            batch = []
                            self.stdout.write(f"Imported {success_count} entries...")

                    if batch:
                        Mecab_Ko_Dic.objects.bulk_create(batch)

                    if error_count > 0:
                        # If the user wants "entire file succeeds or fails together",
                        # we should probably raise an exception if there are ANY errors.
                        # The prompt says: "ensure the entire batch (or entire file) succeeds or fails together."
                        raise CommandError(f"Import failed with {error_count} errors. Rolling back.")

                self.stdout.write(self.style.SUCCESS(
                    f"\nImport Summary:\n"
                    f"Total rows processed: {processed_count}\n"
                    f"Successfully imported: {success_count}\n"
                    f"Errors: {error_count}"
                ))

        except FileNotFoundError:
            raise CommandError(f'File "{file_path}" does not exist')
        except UnicodeDecodeError:
            raise CommandError(f"Failed to decode file with encoding '{encoding}'. Try specifying a different encoding.")
        except CommandError as e:
            # Re-raise CommandError to show the "Import failed" message
            raise e
        except Exception as e:
            raise CommandError(f"An unexpected error occurred: {str(e)}")
