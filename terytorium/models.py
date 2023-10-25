from django.db import models
from bs4 import BeautifulSoup
import requests
# from PodzialPolski.weather.pogoda import Weather


class Woj(models.Model):
    name = models.CharField(max_length=30, verbose_name='Nazwa')
    symbol = models.PositiveSmallIntegerField(verbose_name='Numer Województwa')
    update_date = models.DateField(verbose_name="Stan na")

    def __str__(self):
        return f'{self.name}'

    def new_name(self):
        name = self.name
        WOJ = {
            'dolnośląskie': 'dolnoslaskie',
            'łódzkie': 'lodzkie',
            'małopolskie': 'malopolskie',
            'śląskie': 'slaskie',
            'świętokrzyskie': 'swietokrzyskie',
            'warmińsko-mazurskie': 'warminsko-mazurskie',

        }
        if name.lower() in WOJ:
            new_woj = WOJ[name.lower()]
            return new_woj
        return name

    def get_data(self):

        url = f"https://www.paih.gov.pl/regiony/wojewodztwa/{self.new_name()}"
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')

        # Wyszukiwanie odpowiednich elementów w tabeli
        table_rows = soup.find_all("tr")

        # Inicjalizacja słownika na dane
        region_data = {}

        # Przetwarzanie wierszy tabeli
        for row in table_rows:
            columns = row.find_all("td")
            if len(columns) == 2:
                label = columns[0].text.strip()
                value = columns[1].text.strip()
                region_data[label] = value

        img = soup.find('img', alt='mapa Polski')['src']

        INFO = {
            'dane': {
                'Powierzchnia': region_data.get("Powierzchnia"),
                'Liczba_ludności': region_data.get('Liczba ludności:- w tym w miastach', region_data.get('Liczba ludności')),
                'Gęstość_zaludnienia': region_data.get("Gęstość zaludnienia", region_data.get('Gęstość\xa0 zaludnienia')),
                'Główne_miasta': region_data.get("Główne miasta", region_data.get('Główne miasto')),
                'img': img,
            }
        }

        liczba_ludnosci_key = 'Liczba ludności:- w tym w miastach'
        liczba_ludnosci_value = INFO['dane']['Liczba_ludności']

        if liczba_ludnosci_key in region_data:
            if INFO['dane']['Główne_miasta'] == 'Lublin' or len(liczba_ludnosci_value) == 14 or len(liczba_ludnosci_value) == 17:
                first_part = liczba_ludnosci_value[:-5]
                INFO['dane']['Liczba_ludności'] = first_part

            elif len(liczba_ludnosci_value) == 16 and INFO['dane']['Główne_miasta'] != 'Szczecin':
                first_part = liczba_ludnosci_value[:-7]
                INFO['dane']['Liczba_ludności'] = first_part

            elif len(liczba_ludnosci_value) == 11:
                first_part = liczba_ludnosci_value[:-3]
                INFO['dane']['Liczba_ludności'] = first_part

            elif len(liczba_ludnosci_value) == 15:
                first_part = liczba_ludnosci_value[:-6]
                INFO['dane']['Liczba_ludności'] = first_part

            elif len(liczba_ludnosci_value) > 26:
                first_part = liczba_ludnosci_value[:-26]
                INFO['dane']['Liczba_ludności'] = first_part

            elif INFO['dane']['Główne_miasta'] == 'Szczecin':
                first_part = liczba_ludnosci_value[:-5]
                INFO['dane']['Liczba_ludności'] = first_part

        return INFO

    class Meta:
        verbose_name = 'Województwo'
        verbose_name_plural = 'Województwa'

