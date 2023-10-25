import csv
from django.core.management.base import BaseCommand
from terytorium.models import Woj


class Command(BaseCommand):
    def handle(self, *args, **options):
        filename = 'TERC.csv'
        with open(filename, 'r', encoding='utf-8') as TERC:
            reader = csv.DictReader(TERC, delimiter=';', fieldnames=[
                'WOJ',
                'POW',
                'GMI',
                'RODZ',
                'NAZWA',
                'NAZWA_DOD',
                'STAN_NA'
            ])
            for row in reader:
                if row['NAZWA_DOD'] == 'województwo':
                    woj = row['NAZWA']
                    key = row['WOJ']
                    stan = row['STAN_NA']
                    Woj.objects.create(name=woj, symbol=key, update_date=stan)
                    print(woj, 'dodane')

                # if row['NAZWA_DOD'] in ['powiat', 'miasto na prawach powiatu', 'miasto stołęczne, na prawach powiatu']:
                #     rodz_powiatu = {'powiat': 1, 'miasto na prawach powiatu': 2, 'miasto stołeczne, na prawach powiatu': 3}
                #     powiat = rodz_powiatu[row['NAZWA_DOD']]
                #     woj = Woj.objects.get(symbol=row['WOJ'])
                #     name = row['NAZWA']
                #     symbol = row['POW']
                #     date = row['STAN_NA']
                #     # print(f"{name} {row['POW']} {woj.name} POWIAT")
                #     #Pow.objects.create(woj=woj, name=name, symbol=symbol, update_date=date, rodz_powiat=powiat)
                #
                # if row['NAZWA_DOD'] in ['gmina miejska', 'gmina wiejska', 'gmina miejsko-wiejska']:
                #     RODZ_GMINY = {'gmina miejska': 1, 'gmina wiejska': 2, 'gmina miejsko-wiejska': 3, 'gmina miejska, miasto stołeczne': 4}
                #     rodz_gmi = RODZ_GMINY[row['NAZWA_DOD']]
                #     woj = Woj.objects.get(symbol=row['WOJ'])
                #     name = row['NAZWA']
                #     symbol = row['GMI']
                #     date = row['STAN_NA']
                #     # print(f"{name} {row['POW']} {woj.name} GMINA")
                #     # print([powiat.name for powiat in Pow.objects.filter(symbol=row['POW'], woj=woj)])
                #     powiat = Pow.objects.get(symbol=row['POW'], woj=woj)
                #     #Gmi.objects.create(powiat=powiat, name=name, symbol=symbol, update_date=date, rodz_gminy=rodz_gmi)
                #
                #    # City.objects.create(gmina=apps.get_model('PodzialPolski.Gmi').objects.get(symbol=row['GMI'], powiat__symbol=row['POW'], powiat__woj__symbol=row['WOJ']), name=row['NAZWA'])
