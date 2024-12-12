import re
from datetime import datetime

# 数字到单词的映射
num_to_word = {
    0: "zero", 1: "one", 2: "two", 3: "three", 4: "four", 5: "five",
    6: "six", 7: "seven", 8: "eight", 9: "nine", 10: "ten", 11: "eleven",
    12: "twelve", 13: "thirteen", 14: "fourteen", 15: "fifteen", 16: "sixteen",
    17: "seventeen", 18: "eighteen", 19: "nineteen", 20: "twenty", 30: "thirty",
    40: "forty", 50: "fifty", 60: "sixty", 70: "seventy", 80: "eighty", 90: "ninety"
}

# 数字转单词函数
def number_to_words(n):
    """Convert number to words"""
    if n < 10:  # 单位数字直接从字典中查找
        return num_to_word[n]
    elif 10 <= n <= 20:  # 添加对 10-20 之间数字的处理
        return num_to_word[n]
    elif n < 100:
        tens, remainder = divmod(n, 10)
        return f"{num_to_word[tens * 10]}{'' if remainder == 0 else ' ' + num_to_word[remainder]}"
    elif n < 1000:
        hundreds, remainder = divmod(n, 100)
        return f"{num_to_word[hundreds]} hundred" + (f" {number_to_words(remainder)}" if remainder else "")
    else:
        return str(n)   

# 数字到英文的词典
number_to_words_dict = {
    1: "first", 2: "second", 3: "third", 4: "fourth", 5: "fifth",
    6: "sixth", 7: "seventh", 8: "eighth", 9: "ninth", 10: "tenth",
    11: "eleventh", 12: "twelfth", 13: "thirteenth", 14: "fourteenth", 
    15: "fifteenth", 16: "sixteenth", 17: "seventeenth", 18: "eighteenth", 
    19: "nineteenth", 20: "twentieth", 21: "twenty-first", 22: "twenty-second",
    23: "twenty-third", 24: "twenty-fourth", 25: "twenty-fifth", 26: "twenty-sixth",
    27: "twenty-seventh", 28: "twenty-eighth", 29: "twenty-ninth", 30: "thirtieth",
    31: "thirty-first"
}

def ordinal_number(n):
    """Convert integer to ordinal number using a dictionary."""
    return number_to_words_dict.get(n, "Invalid number")

def process_decimal_part(decimal_part):
    """Process decimal part of a number when it has more than two digits"""
    if len(decimal_part) > 2:
        return ' '.join(number_to_words(int(digit)) for digit in decimal_part)
    else:
        return number_to_words(int(decimal_part))

def process_percentage(text):
    """Convert percentages"""
    return re.sub(r'(\d+)(\.\d+)?%', 
                  lambda m: f"{number_to_words(int(m.group(1)))} point " + process_decimal_part(m.group(2)[1:]) + " percent" if m.group(2) else f"{number_to_words(int(m.group(1)))} percent", 
                  text)

def process_date(text):
    """Convert date format YYYY-MM-DD"""
    def date_match(m):
        try:
            date_str = m.group(0)
            date = datetime.strptime(date_str, "%Y-%m-%d")

            month_name = date.strftime('%B')
            day = int(date.strftime('%d'))
            day_ordinal = ordinal_number(day)
            year = date.year
            if year < 100:
                year_str = number_to_words(year)
            else:
                first_part = year // 100
                second_part = year % 100
                year_str = f"{number_to_words(first_part)} {number_to_words(second_part)}"
            
            return f"{month_name} {day_ordinal}, {year_str}"
        except ValueError:
            return m.group(0)

    return re.sub(r'\d{4}-\d{2}-\d{2}', date_match, text)

def process_number_with_unit(text):
    """Convert numbers with units or nouns"""
    return re.sub(r'(\d+)\s*([a-zA-Z]+)', 
                  lambda m: f"{number_to_words(int(m.group(1)))} {m.group(2)}", 
                  text)

def process_decimal_large(text):
    """Convert decimal numbers with more than 2 digits after point"""
    return re.sub(r'(\d+)\.(\d{3,})', 
                  lambda m: f"{number_to_words(int(m.group(1)))} point {' '.join(number_to_words(int(digit)) for digit in m.group(2))}",
                  text)

def process_pure_number(text):
    """Convert pure numbers (no units or nouns) to word-by-word"""
    return re.sub(r'\b\d+\b', 
                  lambda m: ' '.join(number_to_words(int(digit)) for digit in m.group(0)), 
                  text)

def process_text(text):
    text = process_date(text)
    text = process_percentage(text)
    text = process_number_with_unit(text)
    text = process_decimal_large(text)
    text = process_pure_number(text)
    return text


class ConvertNumbersToWordsNode:
    """
    Node to convert numbers in text to words
    """

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input_text": ("STRING", {
                    "multiline": True,  # Allows for multi-line input
                    "default": "输入需要转换的文本"
                })
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "convert_numbers_to_words"
    CATEGORY = "🔢NumberConvert"

    def convert_numbers_to_words(self, input_text):
        converted_text = process_text(input_text)
        return (converted_text,)


NODE_CLASS_MAPPINGS = {
    "ConvertNumbersToWords": ConvertNumbersToWordsNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ConvertNumbersToWords": "Convert Numbers to Words"
}
