from ofxstatement.parser import CsvStatementParser
from ofxstatement.plugin import Plugin
import csv


class DABCsvStatementParser(CsvStatementParser):

    # 0 Buchungstag
    # 1 Valuta
    # 2 Buchungstext
    # 3 Kontonummer
    # 4 Auftraggeber / Empfänger
    # 5 Konto/IBAN
    # 6 BLZ/BIC
    # 7 Verwendungszweck
    # 8 Betrag in EUR

    mappings = {"date": 1, "payee": 4, "memo": 7, "amount": 8}
    date_format = "%d.%m.%Y"

    def split_records(self):
        return csv.reader(self.fin, delimiter=';')

    def parse_record(self, line):

        if self.cur_record == 2:
            self.statement.currency = line[8].strip('Betrag in ')
            return None

        if self.cur_record <= 2:
            return None

        # Remove dots (German decimal point handling)
        # 2.000,00 => 2000,00
        line[8] = line[8].replace('.', '')

        # Replace comma with dot (German decimal point handling)
        # 2000.00 => 2000.00
        line[8] = line[8].replace(',', '.')

        # fill statement line according to mappings
        sl = super(DABCsvStatementParser, self).parse_record(line)
        return sl


class DABPlugin(Plugin):
    name = "dab"

    def get_parser(self, fin):
        f = open(fin, "r", encoding='utf-8')
        parser = DABCsvStatementParser(f)
#        parser.statement.account_id = self.settings['account']
#        parser.statement.bank_id = self.settings.get('bank', 'DAB Depotkonto')
        parser.statement.account_id = "DAB Depotkonto"
        parser.statement.bank_id = "DAB"
        return parser

