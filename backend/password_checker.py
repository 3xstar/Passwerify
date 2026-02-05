import re

class PasswordChecker:
    """Класс для проверки и оценки паролей"""
    
    def __init__(self):
        # Список распространенных слабых паролей
        self.common_passwords = [
            "password", "123456", "12345678", "1234", "qwerty",
            "abc123", "password1", "12345", "123456789", "111111",
            "1234567", "iloveyou", "admin", "welcome", "monkey",
            "letmein", "sunshine", "master", "hello", "freedom"
        ]
        
        # Личные данные для проверки
        self.personal_keywords = [
            "name", "surname", "birthday", "birth", "year",
            "qwerty", "123", "admin", "user", "login",
            "password", "pass", "secret", "test", "demo"
        ]
        
    def analyze(self, password):
        """
        Полный анализ пароля
        
        Returns:
            dict: Результаты анализа
        """
        results = {
            'password': password,
            'length': len(password),
            'has_lower': False,
            'has_upper': False,
            'has_digit': False,
            'has_special': False,
            'good_moments': [],
            'bad_moments': [],
            'score': 0,
            'grade': 'F',
            'security_level': 'Very Low'
        }
        
        # Базовые проверки
        results['has_lower'] = any(c.islower() for c in password)
        results['has_upper'] = any(c.isupper() for c in password)
        results['has_digit'] = any(c.isdigit() for c in password)
        results['has_special'] = bool(re.search(r'[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]', password))
        
        # Проверка длины
        if results['length'] >= 16:
            results['good_moments'].append("Excellent length (16+ characters)")
        elif results['length'] >= 12:
            results['good_moments'].append("Good length (12+ characters)")
        elif results['length'] >= 8:
            results['good_moments'].append("Acceptable length (8+ characters)")
        else:
            results['bad_moments'].append("Too short (minimum 8 characters recommended)")
            
        # Проверка разнообразия символов
        char_types = sum([results['has_lower'], results['has_upper'], 
                          results['has_digit'], results['has_special']])
        
        if results['has_lower'] and results['has_upper']:
            results['good_moments'].append("Using both uppercase and lowercase letters")
        elif results['has_lower']:
            results['bad_moments'].append("No uppercase letters")
        elif results['has_upper']:
            results['bad_moments'].append("No lowercase letters")
            
        if results['has_digit']:
            results['good_moments'].append("Contains numbers")
        else:
            results['bad_moments'].append("No numbers")
            
        if results['has_special']:
            results['good_moments'].append("Contains special characters")
        else:
            results['bad_moments'].append("No special characters")
            
        # Проверка на сложность
        if char_types >= 4:
            results['good_moments'].append("Uses all character types (letters, numbers, symbols)")
        elif char_types >= 3:
            results['good_moments'].append("Good character variety")
            
        # Проверка на распространенные пароли
        if password.lower() in self.common_passwords:
            results['bad_moments'].append("This is a very common password (in top 20 most used)")
            
        # Проверка на личную информацию
        for keyword in self.personal_keywords:
            if keyword in password.lower():
                results['bad_moments'].append(f"It is advisable not to use personal data")
                break
                
        # Проверка на последовательности
        if self.has_sequence(password):
            results['bad_moments'].append("Contains sequential characters (e.g., 123, abc)")
            
        # Проверка на повторяющиеся символы
        if self.has_repeating_chars(password):
            results['bad_moments'].append("Contains repeating characters")
            
        # Расчет оценки
        results['score'] = self.calculate_score(results)
        results['grade'] = self.score_to_grade(results['score'])
        results['security_level'] = self.score_to_security_level(results['score'])
        
        return results
        
    def calculate_score(self, results):
        """Расчет числовой оценки от 0 до 100"""
        score = 0
        
        # Длина (макс 30)
        if results['length'] >= 16:
            score += 30
        elif results['length'] >= 12:
            score += 25
        elif results['length'] >= 8:
            score += 20
        elif results['length'] >= 6:
            score += 10
        else:
            score += 5
            
        # Сложность символов (макс 40)
        char_types = sum([results['has_lower'], results['has_upper'], 
                          results['has_digit'], results['has_special']])
        score += char_types * 10  # 10 за каждый тип
        
        # Бонус за хорошую длину и разнообразие (макс 20)
        if results['length'] >= 12 and char_types >= 3:
            score += 15
        elif results['length'] >= 8 and char_types >= 2:
            score += 10
            
        # Бонус за очень хорошую длину (макс 10)
        if results['length'] >= 16:
            score += 10
            
        # Штраф за распространенные пароли
        if results['password'].lower() in self.common_passwords:
            score -= 40
            
        # Штраф за личные данные
        for keyword in self.personal_keywords:
            if keyword in results['password'].lower():
                score -= 20
                break
                
        # Ограничиваем от 0 до 100
        return max(0, min(score, 100))
        
    def score_to_grade(self, score):
        """Конвертация оценки в буквенную оценку"""
        if score >= 90:
            return 'A'
        elif score >= 80:
            return 'B'
        elif score >= 70:
            return 'C'
        elif score >= 60:
            return 'D'
        else:
            return 'F'
            
    def score_to_security_level(self, score):
        """Конвертация оценки в уровень безопасности"""
        if score >= 85:
            return "Very High"
        elif score >= 70:
            return "High"
        elif score >= 55:
            return "Mid"
        elif score >= 40:
            return "Low"
        else:
            return "Very Low"
            
    def has_sequence(self, password):
        """Проверка на последовательные символы"""
        if len(password) < 3:
            return False
            
        password_lower = password.lower()
        
        # Проверяем последовательности типа "123", "abc"
        for i in range(len(password_lower) - 2):
            # Проверка числовых последовательностей
            if (password_lower[i].isdigit() and 
                password_lower[i+1].isdigit() and 
                password_lower[i+2].isdigit()):
                if (int(password_lower[i]) + 1 == int(password_lower[i+1]) and
                    int(password_lower[i+1]) + 1 == int(password_lower[i+2])):
                    return True
                    
            # Проверка буквенных последовательностей
            elif (password_lower[i].isalpha() and 
                  password_lower[i+1].isalpha() and 
                  password_lower[i+2].isalpha()):
                if (ord(password_lower[i]) + 1 == ord(password_lower[i+1]) and
                    ord(password_lower[i+1]) + 1 == ord(password_lower[i+2])):
                    return True
                    
        return False
        
    def has_repeating_chars(self, password):
        """Проверка на повторяющиеся символы"""
        if len(password) < 3:
            return False
            
        # Ищем 3 или более одинаковых символа подряд
        for i in range(len(password) - 2):
            if password[i] == password[i+1] == password[i+2]:
                return True
        return False