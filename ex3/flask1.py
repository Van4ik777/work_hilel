import csv
import requests

from flask import Flask
from faker import Faker

from webargs.flaskparser import use_kwargs
from webargs import validate, fields

fake = Faker()

app = Flask(__name__)
CURRENCY_SYMBOLS = {
    'USD': '$',
    'EUR': '€',
    'UAH': '₴',
    'GBP': '£',
    'JPY': '¥',
    'CAD': 'C$',
    'AUD': 'A$',
    'CNY': '¥',
    'CHF': 'CHF',
    'SEK': 'kr',
    'NZD': 'NZ$',
    'KRW': '₩',
    'ETH': 'Ξ',
    'LTC': 'Ł',
    'XRP': 'Ʀ',
    'AED': 'د.إ',
    'AFN': '؋',
    'ALL': 'L',
    'AMD': '֏',
    'ANG': 'ƒ',
    'AOA': 'Kz',
    'ARS': '$',
    'AWG': 'ƒ',
    'AZN': '₼',
    'BAM': 'KM',
    'BBD': '$',
    'BDT': '৳',
    'BGN': 'лв',
    'BHD': '.د.ب',
    'BIF': 'FBu',
    'BMD': '$',
    'BND': '$',
    'BOB': 'Bs.',
    'BRL': 'R$',
    'BSD': '$',
    'BTN': 'Nu.',
    'BWP': 'P',
    'BYN': 'Br',
    'BZD': '$',
    'CDF': 'FC',
    'CLF': 'UF',
    'CLP': '$',
    'COP': '$',
    'CRC': '₡',
    'CUP': '$',
    'CVE': '$',
    'CZK': 'Kč',
    'DJF': 'Fdj',
    'DKK': 'kr',
    'DOP': 'RD$',
    'DZD': 'د.ج',
    'EGP': '£',
    'ETB': 'Br',
    'FJD': '$',
    'FKP': '£',
    'GEL': '₾',
    'GHS': '₵',
    'GIP': '£',
    'GMD': 'D',
    'GNF': 'FG',
    'GTQ': 'Q',
    'GYD': '$',
    'HKD': '$',
    'HNL': 'L',
    'HRK': 'kn',
    'HTG': 'G',
    'HUF': 'Ft',
    'IDR': 'Rp',
    'ILS': '₪',
    'INR': '₹',
    'IQD': 'ع.د',
    'IRR': '﷼',
    'ISK': 'kr',
    'JEP': '£',
    'JMD': '$',
    'JOD': 'د.ا',
    'KES': 'KSh',
    'KGS': 'лв',
    'KHR': '៛',
    'KMF': 'CF',
    'KPW': '₩',
    'KWD': 'د.ك',
    'KYD': '$',
    'KZT': '₸',
    'LAK': '₭',
    'LBP': 'ل.ل',
    'LKR': 'Rs',
    'LRD': '$',
    'LSL': 'L',
    'LYD': 'ل.د',
    'MAD': 'د.م.',
    'MDL': 'L',
    'MGA': 'Ar',
    'MKD': 'ден',
    'MMK': 'K',
    'MNT': '₮',
    'MOP': 'MOP$',
    'MRU': 'UM',
    'MUR': '₨',
    'MVR': 'Rf',
    'MWK': 'MK',
    'MXN': '$',
    'MYR': 'RM',
    'MZN': 'MT',
    'NAD': '$',
    'NGN': '₦',
    'NIO': 'C$',
    'NOK': 'kr',
    'NPR': '₨',
    'OMR': 'ر.ع.',
    'PAB': 'B/.',
    'PEN': 'S/',
    'PGK': 'K',
    'PHP': '₱',
    'PKR': '₨',
    'PLN': 'zł',
    'PYG': '₲',
    'QAR': 'ر.ق',
    'RON': 'lei',
    'RSD': 'дин',
    'RUB': '₽',
    'RWF': 'FRw',
    'SAR': 'ر.س',
    'SBD': '$',
    'SCR': '₨',
    'SDG': '£',
    'SGD': '$',
    'SHP': '£',
    'SLL': 'Le',
    'SOS': 'S',
    'SRD': '$',
    'STN': 'Db',
    'SVC': '$',
    'SYP': '£',
    'SZL': 'E',
    'THB': '฿',
    'TJS': 'ЅМ',
    'TMT': 'm',
    'TND': 'د.ت',
    'TOP': 'T$',
    'TRY': '₺',
    'TTD': '$',
    'TWD': 'NT$',
    'TZS': 'TSh',
    'UGX': 'USh',
    'UYU': '$U',
    'UZS': 'лв',
    'VES': 'Bs.S',
    'VND': '₫',
    'VUV': 'VT',
    'XAF': 'FCFA',
    'XAG': 'XAG',
    'XAU': 'XAU',
    'XCD': '$',
    'XOF': 'CFA',
    'XPF': 'F',
    'YER': '﷼',
    'ZAR': 'R',
    'ZMW': 'ZK',
    'ZWL': '$'
}


@app.route("/generate_students")
@use_kwargs(
    {
        "count": fields.Integer(
            missing=1,
            validate=[validate.Range(min=1, max=1000, min_inclusive=True, max_inclusive=True)]
        )
    },
    location="query"
)
def generate_students(count):
    # count should be as input GET parameter
    # first_name, last_name, email, password, birthday (18-60)
    # save to csv and show on web page
    # set limit as 1000

    students = []
    for i in range(count):
        "creating a fake student object"
        first_name = fake.first_name()
        last_name = fake.last_name()
        email = fake.email()
        password = fake.password()
        birth_date = fake.date_of_birth(minimum_age=18, maximum_age=60)
        student = [first_name, last_name, email, password, birth_date]

        students.append(student)

    csv_file = 'students.csv'
    with open(csv_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['First Name', 'Last Name', 'Email', 'Password', 'Birthday'])
        writer.writerows(students)

    return students


def get_bitcoin_rate(currency):
    response = requests.get('https://bitpay.com/api/rates')

    if response.status_code != 200:
        return None
    rates = response.json()

    for rate in rates:
        if rate['code'] == currency:
            return rate['rate']
    return None


@app.route("/bitcoin_rate")
@use_kwargs(
    {
        "currency": fields.Str(load_default='USD'),
        "convert": fields.Integer( missing=1,)
    },
    location="query"
)
def get_bitcoin_value(currency, convert):
    # https://bitpay.com/api/rates
    # /bitcoin_rate?currency=UAH&convert=100
    # input parameter currency code
    # default is USD
    # default count is 1
    # return value currency of bitcoin
    # add one more input parameter count and multiply by currency (int)
    # * https://bitpay.com/api/
    # * Example: $, €, ₴
    # * return symbol of input currency code
    rate = get_bitcoin_rate(currency)
    if rate is None:
        return 'Invalid currency'

    value = rate * convert
    symbol = CURRENCY_SYMBOLS.get(currency, currency)

    return f'one Bitcoin = {value} {currency}({symbol})'


if __name__ == '__main__':
    app.run(
        port=5000, debug=True
    )
