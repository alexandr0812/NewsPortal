from django import template
import re

register = template.Library()


bad_words = ['редиска', 'петрушка']


@register.filter()
def censor(value):
   if not isinstance(value, str):
      raise ValueError("Фильтр censor применяется только к строковым переменным.")

   # Функция для замены плохих слов на цензурированные
   def replace_bad_word(match):
      word = match.group(0)
      return word[0] + '*' * (len(word) - 1)

   # Создаем регулярное выражение для поиска плохих слов
   pattern = re.compile(r'\b(' + '|'.join(map(re.escape, bad_words)) + r')\b', re.IGNORECASE)

   # Заменяем плохие слова на цензурированные
   censored_value = pattern.sub(replace_bad_word, value)

   return censored_value
