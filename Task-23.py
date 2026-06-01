import asyncio
from locust import FastHttpUser, task, between
from bs4 import BeautifulSoup
import aiohttp
from typing import List, Dict
import re


class TeacherUser(FastHttpUser):
    """
    Класс пользователя для нагрузочного тестирования страницы преподавателей
    """
    
    # Время ожидания между запросами от 1 до 3 секунд
    wait_time = between(1, 3)
    
    # Хост для тестирования
    host = "https://atlas.herzen.spb.ru"
    
    def on_start(self):
        """Метод, выполняемый при старте каждого пользователя"""
        print(f"[Пользователь {self.user_id}] Начинает тестирование страницы преподавателей")
    
    @task
    async def get_teachers_page(self):
        """
        Асинхронная задача: получение и обработка страницы с преподавателями
        """
        endpoint = "/teachers"
        
        try:
            # Выполняем GET-запрос с перехватом ответа для кастомной обработки
            with self.client.get(endpoint, catch_response=True) as response:
                
                # Проверяем HTTP статус
                if response.status_code != 200:
                    error_msg = f"HTTP ошибка: статус {response.status_code} при запросе к {endpoint}"
                    print(f"[Пользователь {self.user_id}] {error_msg}")
                    response.failure(error_msg)
                    return
                
                # Получаем HTML-код ответа
                html_content = response.text
                
                if not html_content:
                    error_msg = f"Пустой ответ от сервера при запросе к {endpoint}"
                    print(f"[Пользователь {self.user_id}] {error_msg}")
                    response.failure(error_msg)
                    return
                
                print(f"[Пользователь {self.user_id}] Страница загружена успешно. Размер HTML: {len(html_content)} символов")
                
                # Парсим HTML и извлекаем информацию о преподавателях
                teachers = await self.parse_teachers_page(html_content)
                
                if not teachers:
                    print(f"[Пользователь {self.user_id}] Преподаватели не найдены на странице")
                    response.success()
                    return
                
                print(f"[Пользователь {self.user_id}] Найдено преподавателей: {len(teachers)}")
                
                # Асинхронно обрабатываем всех преподавателей
                await self.process_teachers_async(teachers)
                
                # Отмечаем запрос как успешный
                response.success()
                
        except aiohttp.ClientError as e:
            error_msg = f"Сетевая ошибка при запросе к {endpoint}: {str(e)}"
            print(f"[Пользователь {self.user_id}] {error_msg}")
            self.client.get(endpoint, catch_response=True).failure(error_msg)
            
        except Exception as e:
            error_msg = f"Неожиданная ошибка: {str(e)}"
            print(f"[Пользователь {self.user_id}] {error_msg}")
            self.client.get(endpoint, catch_response=True).failure(error_msg)
    
    async def parse_teachers_page(self, html_content: str) -> List[Dict[str, str]]:
        """
        Парсинг HTML страницы для извлечения информации о преподавателях
        
        Args:
            html_content: HTML содержимое страницы
            
        Returns:
            List[Dict[str, str]]: Список преподавателей с их данными
        """
        teachers = []
        
        try:
            # Создаем объект Beautiful Soup для парсинга HTML
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Ищем элементы, которые могут содержать информацию о преподавателях
            # Варианты селекторов (адаптируйте под актуальную структуру страницы)
            teacher_selectors = [
                'div.teacher-card',           # Карточка преподавателя
                'div.teacher-item',            # Элемент преподавателя
                'div.teacher',                 # Общий контейнер преподавателя
                'div.card',                    # Карточка
                'li.teacher',                  # Список преподавателей
                'div.teacher-info',            # Информация о преподавателе
                '[data-teacher-id]',           # Элемент с data-атрибутом
                'div.teacher-name'             # Контейнер с именем
            ]
            
            found_elements = []
            for selector in teacher_selectors:
                elements = soup.select(selector)
                if elements:
                    found_elements = elements
                    print(f"[Парсинг] Найдено {len(elements)} элементов по селектору: {selector}")
                    break
            
            # Если не нашли по специфическим селекторам, ищем универсальные элементы
            if not found_elements:
                # Ищем заголовки, которые могут содержать ФИО
                name_candidates = soup.find_all(['h2', 'h3', 'h4', 'p', 'div', 'a'], 
                                                string=re.compile(r'[А-Я][а-я]+\s+[А-Я][а-я]+\s+[А-Я][а-я]+|^[А-Я][а-я]+\s+[А-Я]\.\s*[А-Я]\.'))
                if name_candidates:
                    for candidate in name_candidates[:10]:  # Ограничиваем количество
                        teacher_name = candidate.get_text(strip=True)
                        if len(teacher_name) > 5 and any(char.isalpha() for char in teacher_name):
                            teachers.append({
                                'name': teacher_name,
                                'element_type': candidate.name
                            })
                else:
                    # Демо-данные для тестирования, если структура страницы неизвестна
                    demo_teachers = [
                        "Иванов Иван Иванович",
                        "Петрова Мария Сергеевна",
                        "Сидоров Алексей Владимирович",
                        "Кузнецова Елена Александровна",
                        "Васильев Дмитрий Петрович"
                    ]
                    for teacher in demo_teachers:
                        teachers.append({
                            'name': teacher,
                            'element_type': 'demo'
                        })
                    print("[Парсинг] Используются демо-данные преподавателей")
            else:
                # Парсим найденные элементы
                for element in found_elements[:20]:  # Ограничиваем до 20 преподавателей для производительности
                    teacher_info = self.extract_teacher_info(element)
                    if teacher_info and teacher_info.get('name'):
                        teachers.append(teacher_info)
            
        except Exception as e:
            print(f"[Парсинг] Ошибка при парсинге HTML: {str(e)}")
            
        return teachers
    
    def extract_teacher_info(self, element) -> Dict[str, str]:
        """
        Извлечение информации о преподавателе из HTML элемента
        
        Args:
            element: BeautifulSoup элемент
            
        Returns:
            Dict[str, str]: Словарь с данными преподавателя
        """
        teacher_data = {}
        
        try:
            # Ищем имя преподавателя
            name_selectors = ['.teacher-name', '.name', 'h3', 'h4', 'strong', 'b', '.title']
            for selector in name_selectors:
                name_elem = element.select_one(selector)
                if name_elem:
                    teacher_data['name'] = name_elem.get_text(strip=True)
                    break
            
            # Если не нашли по селекторам, берем текст всего элемента
            if 'name' not in teacher_data:
                element_text = element.get_text(strip=True)
                # Извлекаем первый значимый фрагмент текста
                lines = [line.strip() for line in element_text.split('\n') if line.strip()]
                if lines:
                    teacher_data['name'] = lines[0]
            
            # Извлекаем должность или другую информацию (опционально)
            position_elem = element.select_one('.position, .teacher-position, .job-title')
            if position_elem:
                teacher_data['position'] = position_elem.get_text(strip=True)
            
            # Извлекаем кафедру (опционально)
            department_elem = element.select_one('.department, .department-name, .chair')
            if department_elem:
                teacher_data['department'] = department_elem.get_text(strip=True)
            
        except Exception as e:
            print(f"[Извлечение] Ошибка при извлечении данных: {str(e)}")
            
        return teacher_data
    
    async def process_teachers_async(self, teachers: List[Dict[str, str]]):
        """
        Асинхронная обработка списка преподавателей
        
        Args:
            teachers: Список преподавателей для обработки
        """
        # Создаем задачи для асинхронной обработки каждого преподавателя
        tasks = []
        for teacher in teachers:
            task = self.process_single_teacher(teacher)
            tasks.append(task)
        
        # Параллельно выполняем все задачи
        await asyncio.gather(*tasks)
        
        print(f"[Пользователь {self.user_id}] Обработка {len(teachers)} преподавателей завершена")
    
    async def process_single_teacher(self, teacher: Dict[str, str]):
        """
        Обработка одного преподавателя
        
        Args:
            teacher: Данные преподавателя
        """
        try:
            # Извлекаем ФИО преподавателя
            full_name = teacher.get('name', 'Имя не указано')
            
            # Выводим ФИО в консоль
            print(f"[Пользователь {self.user_id}] Обрабатывается преподаватель: {full_name}")
            
            # Дополнительная информация, если доступна
            if 'position' in teacher:
                print(f"  - Должность: {teacher['position']}")
            if 'department' in teacher:
                print(f"  - Кафедра: {teacher['department']}")
            
            # Искусственная задержка 0.1 секунды
            await asyncio.sleep(0.1)
            
        except Exception as e:
            print(f"[Обработка] Ошибка при обработке преподавателя {teacher.get('name', 'Unknown')}: {str(e)}")
    
    def on_stop(self):
        """Метод, выполняемый при остановке пользователя"""
        print(f"[Пользователь {self.user_id}] Завершает тестирование страницы преподавателей")


# Для тестирования скрипта в автономном режиме
async def test_single_request():
    """Функция для тестирования одного запроса"""
    print("Начало тестирования одного запроса...")
    user = TeacherUser(None)
    user.user_id = "TEST"
    await user.get_teachers_page()
    print("Тестирование завершено")


if __name__ == "__main__":
    print("=" * 80)
    print("Сценарий нагрузочного тестирования Атлас преподавателей РГПУ им. А. И. Герцена")
    print("=" * 80)
    print("\nДля запуска нагрузочного тестирования выполните команды:")
    print("\n1. Установка зависимостей:")
    print("   pip install locust beautifulsoup4 aiohttp")
    print("\n2. Запуск веб-интерфейса Locust:")
    print("   locust -f this_script.py")
    print("\n3. Или запуск в headless режиме (10 пользователей, 5 в секунду, 30 секунд):")
    print("   locust -f this_script.py --headless -u 10 -r 5 --run-time 30s")
    print("\n4. Тестирование одного запроса:")
    print("   python -c \"import asyncio; from this_script import test_single_request; asyncio.run(test_single_request())\"")
    print("=" * 80)