import random

# Строковые константы с символами
digits = '0123456789'
lowercase_letters = 'abcdefghijklmnopqrstuvwxyz'
uppercase_letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
punctuation = '!#$%&*+-=?@^_.'
ambiguous_chars = 'il1Lo0O'  # Неоднозначные символы для исключения
negative_answers = {'нет', 'н', 'no', 'n', '0'}  # Все варианты отрицательных ответов

def get_user_parameters():
    """Запрашивает параметры генерации паролей у пользователя."""
    params = {}
    params['num_passwords'] = int(input("Сколько паролей нужно сгенерировать? "))
    params['password_length'] = int(input("Длина одного пароля: "))
    params['include_digits'] = input("Включать цифры? (д/н) ").lower() not in negative_answers
    params['include_uppercase'] = input("Включать прописные буквы? (д/н) ").lower() not in negative_answers
    params['include_lowercase'] = input("Включать строчные буквы? (д/н) ").lower() not in negative_answers
    params['include_punctuation'] = input("Включать символы? (д/н) ").lower() not in negative_answers
    params['exclude_ambiguous'] = input("Исключать неоднозначные символы? (д/н) ").lower() not in negative_answers
    params['exclude_duplicates'] = input("Исключать повторяющиеся символы? (д/н) ").lower() not in negative_answers
    return params

def build_chars(params):
    """Создает строку допустимых символов на основе параметров."""
    chars = ''
    if params['include_digits']:
        chars += digits
    if params['include_uppercase']:
        chars += uppercase_letters
    if params['include_lowercase']:
        chars += lowercase_letters
    if params['include_punctuation']:
        chars += punctuation
    
    # Удаление неоднозначных символов
    if params['exclude_ambiguous']:
        chars = ''.join([c for c in chars if c not in ambiguous_chars])
    
    return chars

def validate_params(params, chars):
    """Проверяет возможность генерации паролей с заданными параметрами."""
    if not chars:
        print("Ошибка: Нет доступных символов для генерации пароля.")
        return False

    # Проверка наличия символов для каждого включенного набора
    if params['include_digits'] and not set(chars) & set(digits):
        print("Ошибка: Цифры недоступны после фильтрации.")
        return False
    if params['include_uppercase'] and not set(chars) & set(uppercase_letters):
        print("Ошибка: Прописные буквы недоступны после фильтрации.")
        return False
    if params['include_lowercase'] and not set(chars) & set(lowercase_letters):
        print("Ошибка: Строчные буквы недоступны после фильтрации.")
        return False
    if params['include_punctuation'] and not set(chars) & set(punctuation):
        print("Ошибка: Символы недоступны после фильтрации.")
        return False

    # Проверка минимальной длины пароля
    mandatory_count = sum([params['include_digits'], params['include_uppercase'],
                          params['include_lowercase'], params['include_punctuation']])
    if params['password_length'] < mandatory_count:
        print(f"Ошибка: Длина пароля ({params['password_length']}) меньше количества обязательных наборов ({mandatory_count}).")
        return False

    # Проверка уникальности символов
    if params['exclude_duplicates']:
        unique_chars = len(set(chars))
        if unique_chars < params['password_length']:
            print(f"Ошибка: Недостаточно уникальных символов ({unique_chars}) для пароля длины {params['password_length']}.")
            return False
    
    return True

def generate_password(params, chars):
    """Генерирует один пароль с учетом всех требований."""
    mandatory_chars = []
    
    # Добавляем по одному символу из каждого обязательного набора
    if params['include_digits']:
        available = list(set(digits) & set(chars))
        mandatory_chars.append(random.choice(available))
    if params['include_uppercase']:
        available = list(set(uppercase_letters) & set(chars))
        mandatory_chars.append(random.choice(available))
    if params['include_lowercase']:
        available = list(set(lowercase_letters) & set(chars))
        mandatory_chars.append(random.choice(available))
    if params['include_punctuation']:
        available = list(set(punctuation) & set(chars))
        mandatory_chars.append(random.choice(available))
    
    # Генерация оставшихся символов
    remaining = params['password_length'] - len(mandatory_chars)
    if params['exclude_duplicates']:
        available = list(set(chars) - set(mandatory_chars))
        additional = random.sample(available, remaining)
    else:
        additional = random.choices(chars, k=remaining)
    
    # Собираем и перемешиваем пароль
    password_chars = mandatory_chars + additional
    random.shuffle(password_chars)
    return ''.join(password_chars)

def ask_retry():
    """Спрашивает пользователя о повторной генерации."""
    response = input("\nХотите сгенерировать пароли еще раз? (д/н) ").lower()
    return response not in negative_answers

def main_loop():
    """Основной цикл программы."""
    while True:
        params = get_user_parameters()
        chars = build_chars(params)
        
        if not validate_params(params, chars):
            if not ask_retry():
                break
            continue
        
        # Генерация паролей
        passwords = [generate_password(params, chars) for _ in range(params['num_passwords'])]
        
        print("\nСгенерированные пароли:")
        for pwd in passwords:
            print(pwd)
        
        if not ask_retry():
            break

if __name__ == "__main__":
    main_loop()
