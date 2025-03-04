import numpy as np

# Функция для создания матрицы ключа
def create_key_matrix(size):
    key_matrix = []
    print(f'Введите значения матрицы {size}x{size} (по строкам):')
    for i in range(size):
        row = list(map(int, input(f'Введите {size} значения для строки {i + 1}: ').split()))
        if len(row) != size:
            print('Неверное количество значений. Попробуйте снова.')
            return create_key_matrix(size)
        key_matrix.append(row)
    return np.array(key_matrix)

# Функция для вычисления обратной матрицы
def inv_matrix(matrix, size):
    det = int(round(np.linalg.det(matrix)))  # Определитель матрицы
    if det == 0:
        return None  # Обратной матрицы не существует
    det_inv = pow(det, -1, 33)  # Модулярное обратное для определителя (33 буквы в русском алфавите)
    adjugate = np.linalg.inv(matrix) * det  # Присоединенная матрица
    adjugate = np.round(adjugate).astype(int)  # Округление до целых чисел
    inv_matrix = (adjugate * det_inv) % 33  # Обратная матрица
    return inv_matrix

# Функция для преобразования текста в числа
def text_in_numbers(text):
    alphabet = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
    return [alphabet.index(char.upper()) for char in text if char.upper() in alphabet]

# Функция для преобразования числа в текст
def numbers_in_text(numbers):
    alphabet = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
    return ''.join([alphabet[num] for num in numbers])

# Функция для шифрования
def hill_encrypt(plaintext, key_matrix):
    size = len(key_matrix)
    text_num = text_in_numbers(plaintext)

    # Дополнение текста, если его длина не кратна размеру матрицы
    if len(text_num) % size != 0:
        text_num += [0] * (size - len(text_num) % size)

    ciphernum = []
    for i in range(0, len(text_num), size):
        block = text_num[i:i + size]
        vector = np.array(block).reshape(size, 1)
        encrypted_block = np.dot(key_matrix, vector) % 33
        ciphernum.extend(encrypted_block.flatten().tolist())

    return numbers_in_text(ciphernum)

# Функция для расшифрования
def hill_decrypt(ciphertext, key_matrix):
    size = len(key_matrix)
    inv_key_matrix = inv_matrix(key_matrix, size)
    if inv_key_matrix is None:
        return 'Невозможно дешифровать: определитель матрицы равен 0.'

    ciphernum = text_in_numbers(ciphertext)
    plaintext_numbers = []
    for i in range(0, len(ciphernum), size):
        block = ciphernum[i:i + size]
        vector = np.array(block).reshape(size, 1)
        decrypted_block = np.dot(inv_key_matrix, vector) % 33
        plaintext_numbers.extend(decrypted_block.flatten().tolist())

    return numbers_in_text(plaintext_numbers)

# Основная функция
def main():
    print('Шифр Хилла')
    print('Выберите действие:')
    print('1. Зашифровать текст')
    print('2. Расшифровать текст')
    choice = int(input('Ваш выбор: '))

    if choice not in [1, 2]:
        print('Неверный выбор.')
        return

    print('Выберите размер матрицы ключа (2 или 3):')
    size = int(input('Размер: '))
    if size not in [2, 3]:
        print('Неверный размер матрицы.')
        return

    key_matrix = create_key_matrix(size)
    print('Матрица ключа:')
    for row in key_matrix:
        print(f'[{' '.join(map(str, row))}]')

    if choice == 1:
        plaintext = input('Введите текст для шифрования: ')
        ciphertext = hill_encrypt(plaintext, key_matrix)
        print('Зашифрованный текст:', ciphertext)
    else:
        ciphertext = input('Введите текст для дешифрования: ')
        plaintext = hill_decrypt(ciphertext, key_matrix)
        print('Расшифрованный текст:', plaintext)

if __name__ == '__main__':
    main()
