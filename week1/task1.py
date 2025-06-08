def process_string(s):
    vowels = 'aeiouAEIOU'
    
    vowel_letters = ''.join(char for char in s if char in vowels)
    consonant_letters = ''.join(char for char in s if char.isalpha() and char not in vowels)
    
    return (vowel_letters, len(vowel_letters), consonant_letters)

input_string = input("Введіть строку: ")
result = process_string(input_string)
print(result)