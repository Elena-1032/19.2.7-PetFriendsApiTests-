from api import PetFriends
from settings import valid_email, valid_password, invalid_email, invalid_password
import os

pf = PetFriends()

# ___________________1_______________________ + Проверяем что запрос api ключа возвращает статус 200 и в результате содержится слово key
def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    status, result = pf.get_api_key(email, password) # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    assert status == 200# Сверяем полученные данные с нашими ожиданиями
    assert 'key' in result
    print(f'====================\nСтатус теста: код {status},\nЛОГИН {email},\n ПАРОЛЬ {password},\n{result}')


# ___________________2_______________________ - Проверяем что при вводе не существующего email/ password запрос выдает ошибку 403
def test_get_api_key_for_invalid_user(email=invalid_email, password=invalid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result
    print(f'====================\nСтатус теста: код {status},\nЛОГИН {email} не зарегистрирован,\n{result}')


# ___________________3________________________ + Проверяем что запрос всех питомцев возвращает не пустой список
def test_get_all_pets_with_valid_key(filter=''):
    """ Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
    запрашиваем список всех питомцев и проверяем что список не пустой.
    Доступное значение параметра filter - 'my_pets' либо '' """
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0
    print(f'====================\nСтатус теста: код {status},\n {result}')

# ___________________4________________________Проверяем что можно добавить питомца с корректными данными + ФОТО
def test_add_new_pet_with_valid_data(name='Куку', animal_type='черепаха', age='100', pet_photo='images/turtle.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)# 1. Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    _, auth_key = pf.get_api_key(valid_email, valid_password)# Запрашиваем ключ api и сохраняем в переменую api_key
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)# Добавляем питомца
    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name
    print(f'====================\nСтатус теста: код {status},\nПитомец {name}, {animal_type}, возраст {age},\nДобавлен с фото\n{result}')

# ___________________5________________________- Проверяем что нельзя добавить + .txt вместо ФОТО / не обнаруживает файл
def test_add_new_pet_with_invalid_data(name='Рыбка', animal_type='рыба', age='0,3', pet_photo='images/foto.txt'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)# 1. Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    _, auth_key = pf.get_api_key(valid_email, valid_password)# Запрашиваем ключ api и сохраняем в переменую api_key
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)# Добавляем питомца
    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    print(f'====================\nСтатус теста: код {status},\nПитомец {name}, {animal_type}, возраст {age},\nдобавлен. Некорректный формат фото')

# ___________________6________________________Проверяем что можно добавить питомца с корректными данными без ФОТО
def test_add_pet_with_valid_data_without_photo(name='Мишка', animal_type='медоед', age='0,5'):
   _, auth_key = pf.get_api_key(valid_email, valid_password)
   _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
   status, result = pf.add_new_pet_nopic(auth_key, name, animal_type, age)
   assert status == 200
   assert result['name'] == name
   kol = len(my_pets['pets'])
   print(f'====================\nСтатус теста: код {status}\nПитомец {name}, {animal_type}, возраст {age}, Добавлен\nколичество животных {kol}\n{result}')

# ___________________7________________________Проверяем что можно добавить питомца с корректными данными без ФОТО
def test_add_pet_with_valid_data_without_age(name='милаш?', animal_type='мураш', age='---'):
   _, auth_key = pf.get_api_key(valid_email, valid_password)
   _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
   status, result = pf.add_new_pet_nopic(auth_key, name, animal_type, age)
   assert status == 200
   assert result['age'] == age
   # kol = len(my_pets['pets'])
   print(f'====================\nСтатус теста: код {status}\nПитомец {name}, {animal_type}, возраст {age}, Добавлен')


# ___________________8________________________- сценарий. Добавление питомца с некорректным типом животного
def test_add_pet_with_numbers_in_variable_animal_type(name='Кука', animal_type='-9-9-9-', age='0', pet_photo='images/turtle.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, api_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(api_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert animal_type in result['animal_type'], 'Питомец добавлен в приложение с цифрами вместо букв в поле "Порода".'
    print(f'\n Добавлен питомец с цифрами вместо букв в поле "Порода". {animal_type}')

# ___________________9________________________+ сценарий. Проверяем возможность удаления питомца
def test_successful_delete_self_pet():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) == 0: # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
        pf.add_new_pet(auth_key, "Соня", "медоед", "3", "images/medoyed.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_id = my_pets['pets'][0]['id']# Берём id первого питомца из списка и отправляем запрос на удаление
    status, _ = pf.delete_pet(auth_key, pet_id)
    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()
    kol = len(my_pets['pets'])
    print(f'__________________\nСтатус теста: код {status},\nколичество животных {kol},\n')


#___________________10________________________+ сценарий. Проверяем возможность обновления информации о питомце
def test_successful_update_self_pet_info(name='Мурзик', animal_type='Котэ', age=5):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:# Еслди список не пустой, то пробуем обновить его имя, тип и возраст
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")


