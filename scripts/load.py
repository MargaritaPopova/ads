import csv

from unesco.models import States, Site, ISO, Region, Category


# python3 manage.py runscript load


def run():
    fhand = open('unesco/whc-sites-2018-clean.csv')
    reader = csv.reader(fhand)
    next(reader)

    models = [Site, States, ISO, Region, Category]
    for model in models:
        model.objects.all().delete()

    for row in reader:
        state, created = States.objects.get_or_create(name=row[8])
        iso, created = ISO.objects.get_or_create(name=row[10])
        region, created = Region.objects.get_or_create(name=row[9])
        category, created = Category.objects.get_or_create(name=row[7])
        try:
            year = int(row[3])
            area = float(row[6])
        except ValueError:
            year = None
            area = None

        site = Site.objects.create(
            name=row[0],
            description=row[1],
            justification=row[2],
            year=year,
            longitude=row[4],
            latitude=row[5],
            area_hectares=area,
            category=category,
            states=state,
            region=region,
            iso=iso
        )
        site.save()
