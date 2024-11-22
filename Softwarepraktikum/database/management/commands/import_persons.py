import pandas as pd
from django.core.management.base import BaseCommand
from database.models import Person, status, food, group, groupleader, facility

def read_csv_pandas(csvfile_path):
    import pandas as pd
    df = pd.read_csv(csvfile_path)
    return df

class Command(BaseCommand):
    help = 'Import persons from csv file'

    def handle(self, *args, **options):
        df = read_csv_pandas('C:/Users/Jiniji/Downloads/persons.csv')


        persons = []
        for _, row in df.iterrows():
            group_name = row['Gruppe-Nr.']
            try:
                group_instance = group.objects.get(group_name=group_name)
            except group.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'Group {group_name} does not exist'))
                continue

            facility_name = row['Bereich']
            facility_instance = facility.objects.get(facility_name=facility_name)

            person = Person.objects.create(
                first_name= row['Kürzel'].split('.')[-1],
                last_name= row['Kürzel'].split('.')[0],
                facility_id=facility_instance,
                group_id=group_instance
            )
            persons.append(person)
        Person.objects.bulk_create(persons)
        self.stdout.write(self.style.SUCCESS(f'Persons created'))