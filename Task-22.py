from locust import HttpUser, task, between
from locust.exception import RescheduleTask


class HabrUser(HttpUser):
    
    # Время ожидания между задачами от 1 до 3 секунд
    wait_time = between(1, 3)
    
    # Хост для тестирования
    host = "https://habr.com"
    
    def on_start(self):
        """Метод, выполняемый при старте каждого пользователя"""
        print("Habr load test started")
    
    @task
    def load_main_page(self):
        """Задача: загрузка главной страницы"""
        
        # Выполняем GET-запрос к главной странице /ru
        # catch_response=True позволяет перехватить ответ для кастомной проверки
        with self.client.get("/ru", catch_response=True, name="Load main page /ru") as response:
            
            # Проверяем, что код ответа равен 200
            if response.status_code == 200:
                # Отмечаем запрос как успешный
                response.success()
                # Выводим сообщение в консоль
                print(f"Page loaded: /ru (Status: {response.status_code}, Time: {response.elapsed.total_seconds():.3f}s)")
            else:
                # Отмечаем запрос как неудачный с указанием причины
                response.failure(f"Expected status 200, got {response.status_code}")
                print(f"Failed to load page: /ru (Status: {response.status_code})")
    
    def on_stop(self):
        """Метод, выполняемый при остановке каждого пользователя"""
        print("Habr load test finished")


# Для запуска теста в автономном режиме (опционально)
if __name__ == "__main__":
    import os
    import sys
    
    print("=" * 50)
    print("Habr.com Load Test Setup")
    print("=" * 50)
    print("\nTo run the test, use one of these commands:")
    print("\n1. Web interface (recommended):")
    print("   locust -f this_script.py")
    print("\n2. Headless mode with 10 users, spawning 1 user per second for 30 seconds:")
    print("   locust -f this_script.py --headless -u 10 -r 1 --run-time 30s")
    print("\n3. Headless mode with custom parameters:")
    print("   locust -f this_script.py --headless -u 50 -r 5 --run-time 60s")
    print("\n" + "=" * 50)