import json
from pathlib import Path

DEFAULT_RATES = {
    "RUB": 1.0,
    "USD": 84,
    "EUR": 97.29
}

def load_rates(filename='vallet.json'):
    '''Загружает курсы валют из JSON-файла. Если файла нет, создаёт с начальными курсами.'''
    if Path(filename).exists():
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        # Создаём файл с курсами по умолчанию
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(DEFAULT_RATES, f, ensure_ascii=False, indent=4)
        return DEFAULT_RATES

def save_rates(rates, filename='vallet.json'):
     """Сохраняет курсы валют в JSON-файл."""
     with open(filename, 'w', encoding='utf-8') as f:
        json.dump(rates, f, ensure_ascii=False, indent=4)


def main():
    '''Главная функция'''
    rates = load_rates()

    while True:
        print('\nКонвертер валют')
        print('-----------------')
        print()
        print('1. Показать курсы')
        print('2. Конвертировать')
        print('3. Добавить валюту')
        print('4. Обновить курс существующей валюты')
        print('5. Выход')
        print()
        choise = input('Выберите действие: ').strip()
        print()
        if choise == '1':
            # показать курсы
            for curensy, rate in rates.items():
                print(f'{curensy} - {rate} руб.')
        elif choise == '2':
            try:
                # конвертация
                amount = float(input('Введите сумму: '))

                from_curr = input('Из какой валюты (например, USD): ').upper()
                to_curr = input('В какую валюту (например, USD): ').upper()

                if from_curr in rates and to_curr in rates:
                    # переводим из from_curr в рубли, затем в to_curr
                    rubles = amount * rates[from_curr]
                    result = rubles / rates[to_curr]

                    print(f'{amount} {from_curr} = {result:.2f} {to_curr}')
                else:
                    print('Одна из валют не найдена')
            except ValueError:
                print('Введите число')
        elif choise == '3':
            code = input('Введите код валюты (например, GBP): ').upper().strip()
            if not code:
                print('Код не может быть пустым.')
                continue
            if code in rates:
                print(f'Валюта {code} уже существует.')
                continue
            try:
                rate = float(input(f'Введите курс {code} к рублю: '))
                if rate <= 0:
                    print('Курс должен быть положительным.')
                    continue
            except ValueError:
                print('Введите число.')
                continue

            # Если все хорошо, добавляем валюту

            rates[code] = rate
            save_rates(rates)

            print(f'Валюта {code} добавлена с курсом {rate} руб.')
        elif choise == '4':
            code = input('Введите код валюты (например, GBP): ').upper().strip()
            if code not in rates:
                print('Введённого кода нет')
                continue
            try:
                rate = float(input(f'Введите новый курс для {code}: '))
                if rate <= 0:
                    print('Курс должен быть положительным.')
                    continue
            except ValueError:
                print('Введите число.')
                continue

            rates[code] = rate
            save_rates(rates)

            print(f'Курс {code} обновлён на {rate} руб.')
        elif choise == '5':
            print('До свидания!')
            break

if __name__ == '__main__':
    main()