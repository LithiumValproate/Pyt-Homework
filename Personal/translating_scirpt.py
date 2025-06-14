# Usage:
# 1. Install dependencies:
#      pip install pandas openpyxl googletrans==4.0.0-rc1

import pandas as pd
from googletrans import Translator

def translate_on_demand(input_excel='vocabulary_list.xlsx',
                        output_excel='vocabulary_list_with_chinese.xlsx',
                        src_col='English',
                        dest_col='Chinese',
                        src_lang='en',
                        dest_lang='zh-cn'):
    # Load the English-only sheet
    df = pd.read_excel(input_excel)
    
    # Initialize translator
    translator = Translator()
    
    # Translate each word on demand
    translations = []
    for word in df[src_col]:
        result = translator.translate(word, src=src_lang, dest=dest_lang)
        translations.append(result.text)
    
    # Add translations column
    df[dest_col] = translations
    
    # Save to new Excel
    df.to_excel(output_excel, index=False)
    print(f"Translated {len(df)} words and saved to '{output_excel}'.")

if __name__ == '__main__':
    translate_on_demand()