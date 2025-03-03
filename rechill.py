import numpy as np
from math import gcd


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


# Функция для вычисления обратной матрицы по модулю
def inv_matrix(matrix, mod):
    det = int(round(np.linalg.det(matrix)))  # Определитель матрицы
    det = det % mod
    if det == 0 or gcd(det, mod) != 1:
        raise ValueError('Матрица не имеет обратной!')

    det_inv = pow(det, -1, mod)
    ad_matrix = np.round(det * np.linalg.inv(matrix)).astype(int)
    ad_matrix = ad_matrix % mod
    inverse = (det_inv * ad_matrix) % mod
    return inverse.astype(int)


# Функция для шифрования
def rechill_encrypt(text, key_matrix1, key_matrix2, alphabet='АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'):
    mod = len(alphabet)
    block_size = len(key_matrix1)
    ciphertext = ''
    #текст в числовые значения
    text = ''.join(filter(lambda x: x in alphabet, text.upper()))
    text_numbers = [alphabet.index(char) for char in text]
    # Дополняем если не кратно
    padding_length = (block_size - len(text_numbers) % block_size) % block_size
    text_numbers.extend([0] * padding_length)
    blocks = [text_numbers[i:i + block_size] for i in range(0, len(text_numbers), block_size)]
    curr_key = key_matrix1
    prev_key = key_matrix1
    prevx2_key = None

    for block in blocks:
        block_vector = np.array(block).reshape(block_size, 1)
        encrypted_block = np.dot(curr_key, block_vector) % mod
        ciphertext += ''.join(alphabet[num] for num in encrypted_block.ravel())
        # Обновляем ключи
        if prevx2_key is None:
            curr_key = key_matrix2
            prevx2_key = prev_key
            prev_key = key_matrix2
        else:
            new_key = np.dot(prevx2_key, prev_key)
            prevx2_key = prev_key
            prev_key = new_key
            curr_key = new_key
    return ciphertext


# Функция для расшифрования
def rechill_decrypt(ciphertext, key_matrix1, key_matrix2, alphabet='АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'):
    mod = len(alphabet)
    block_size = len(key_matrix1)
    text = ''
    ciphertext_numbers = [alphabet.index(char) for char in ciphertext]
    blocks = [ciphertext_numbers[i:i + block_size] for i in range(0, len(ciphertext_numbers), block_size)]

    try:
        key_matrix1_inv = inv_matrix(key_matrix1, mod)
        key_matrix2_inv = inv_matrix(key_matrix2, mod)
    except ValueError as e:
        print(e)
        return None
    curr_key_inv = key_matrix1_inv
    prev_key = key_matrix1
    prevx2_key = None

    for block in blocks:
        block_vector = np.array(block).reshape(block_size, 1)
        decrypted_block = np.dot(curr_key_inv, block_vector) % mod
        text += ''.join(alphabet[int(num)] for num in decrypted_block.ravel())
        if prevx2_key is None:
            curr_key_inv = key_matrix2_inv
            prevx2_key = prev_key
            prev_key = key_matrix2
        else:
            new_key = np.dot(prevx2_key, prev_key)
            new_key_inv = inv_matrix(new_key, mod)
            prevx2_key = prev_key
            prev_key = new_key
            curr_key_inv = new_key_inv

    return text


# Основная программа
def main():
    print('Рекуррентный шифр Хилла')
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

    print('Введите первую матрицу ключа:')
    key_matrix1 = create_key_matrix(size)
    print('Матрица ключа 1:')
    for row in key_matrix1:
        print(f'[{' '.join(map(str, row))}]')

    print('Введите вторую матрицу ключа:')
    key_matrix2 = create_key_matrix(size)
    print('Матрица ключа 2:')
    for row in key_matrix2:
        print(f'[{' '.join(map(str, row))}]')

    if choice == 1:
        plaintext = input('Введите текст для шифрования: ')
        ciphertext = rechill_encrypt(plaintext, key_matrix1, key_matrix2)
        print('Зашифрованный текст:', ciphertext)
    else:
        ciphertext = input('Введите текст для расшифровки: ')
        plaintext = rechill_decrypt(ciphertext, key_matrix1, key_matrix2)
        print('Расшифрованный текст:', plaintext)


if __name__ == '__main__':
    main()