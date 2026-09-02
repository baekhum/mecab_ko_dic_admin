import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mecab_ko_dic_admin.config.settings')
django.setup()

from mecab_ko_dic.models import Mecab_Ko_Dic  # noqa: E402
from django.db.models import Count, Min  # noqa: E402

def run_cleanup():
    print("Finding duplicates...")
    duplicates = Mecab_Ko_Dic.objects.values('표층형', '품사_태그').annotate(min_id=Min('id'), count=Count('id')).filter(count__gt=1)
    
    total_to_check = duplicates.count()
    print(f"Found {total_to_check} duplicate groups.")
    
    all_ids_to_delete = []
    for i, dup in enumerate(duplicates, 1):
        ids = list(Mecab_Ko_Dic.objects.filter(표층형=dup['표층형'], 품사_태그=dup['품사_태그']).exclude(id=dup['min_id']).values_list('id', flat=True))
        all_ids_to_delete.extend(ids)
        if i % 1000 == 0:
            print(f"Collected {len(all_ids_to_delete)} IDs to delete ({i}/{total_to_check})...")
            
    print(f"Total IDs to delete: {len(all_ids_to_delete)}")
    
    # Delete in chunks
    chunk_size = 1000
    for i in range(0, len(all_ids_to_delete), chunk_size):
        chunk = all_ids_to_delete[i:i + chunk_size]
        Mecab_Ko_Dic.objects.filter(id__in=chunk).delete()
        if (i // chunk_size) % 10 == 0:
            print(f"Deleted {i + len(chunk)}/{len(all_ids_to_delete)}...")

if __name__ == "__main__":
    run_cleanup()
