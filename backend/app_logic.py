import os
import random
import string

class PasswordAppLogic:
    """Основная логика приложения"""
    
    def __init__(self):
        from password_checker import PasswordChecker
        self.checker = PasswordChecker()
        
    def check_password_input(self, password):
        """
        Проверка ввода пароля
        
        Returns:
            tuple: (success, message)
        """
        if not password:
            return False, "Please enter a password!"
            
        if len(password) > 50:
            return False, "Password is too long (max 50 characters)"
            
        if len(password) < 1:
            return False, "Password cannot be empty"
            
        # Проверка на недопустимые символы
        if any(ord(c) < 32 or ord(c) > 126 for c in password):
            return False, "Password contains invalid characters"
            
        return True, "OK"
        
    def analyze_password(self, password):
        """
        Полный анализ пароля с подготовкой данных для UI
        
        Returns:
            dict: Результаты для отображения
        """
        # Получаем анализ от checker
        analysis = self.checker.analyze(password)
        
        # Форматируем для UI
        result = {
            'password': password,
            'security_level': analysis['security_level'],
            'good_moments': analysis['good_moments'],
            'bad_moments': analysis['bad_moments'],
            'score': analysis['score'],
            'grade': analysis['grade']
        }
        
        return result
        
    def get_grade_image_path(self, grade):
        """Получение пути к изображению оценки"""
        return os.path.join("images", f"{grade.lower()}grade.png")
        
    def generate_strong_password(self, length=12):
        """
        Генерация сильного пароля
        
        Args:
            length: длина пароля
            
        Returns:
            str: сгенерированный пароль
        """
        # Определяем наборы символов
        lowercase = string.ascii_lowercase
        uppercase = string.ascii_uppercase
        digits = string.digits
        special = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        
        # Гарантируем наличие хотя бы одного символа из каждой группы
        password = [
            random.choice(lowercase),
            random.choice(uppercase),
            random.choice(digits),
            random.choice(special)
        ]
        
        # Заполняем оставшуюся длину случайными символами из всех групп
        all_chars = lowercase + uppercase + digits + special
        password.extend(random.choice(all_chars) for _ in range(length - 4))
        
        # Перемешиваем символы
        random.shuffle(password)
        
        return ''.join(password)