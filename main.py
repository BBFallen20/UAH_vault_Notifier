from bs4 import BeautifulSoup
from request import get_html
from win10toast import ToastNotifier
import time
import schedule


class Vault:
    def __init__(self):
        self.URL = 'https://finance.ua/ru/currency'
        self.html = get_html(self.URL)
        self.toaster = ToastNotifier()
        self.soup = BeautifulSoup(self.html.text, 'html.parser')

    def parse(self):
        if self.html.status_code == 200:
            vaults = self.content()
            result = []
            for item in vaults:
                result.append(item['name'])
                result.append(item['buy'])
                result.append(item['sell'])
            self.toaster.show_toast("UAH course:",
                                   "Vault: " + result[0] + '  ' + result[3] + '  ' + result[6] + '\n' + 'Buy: ' + result[1] + ' ' +result[4] + ' ' + result[7] + '\n' + 'Sell: ' + result[2] + ' ' + result[5] + ' ' +result[8],
                                    duration=10)
        else:
            self.toaster.show_toast("Error!!!", "Something wrong with connection to service.", duration=5)


    def content(self):
        vaults = []
        vaults_row = self.soup.find_all('tr', class_='major')
        for vault in vaults_row:
            vaults.append({
                'name': vault.find('td', class_='c1').get_text(),
                'buy': vault.find('td', class_='c2').get_text(),
                'sell': vault.find('td', class_='c3').get_text(),
            })
        return vaults
    
    
    def timer(self):
        schedule.every(1).minutes.do(self.parse)
        while True:
            schedule.run_pending()
            time.sleep(1)


Vault().timer()
