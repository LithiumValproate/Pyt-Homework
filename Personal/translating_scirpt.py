import pandas as pd
from dotenv import load_dotenv
import os
import json
from tencentcloud.common import credential
from tencentcloud.tmt.v20180321 import tmt_client, models
from tqdm import tqdm

load_dotenv(".env")


def tencent_translate(text, src_lang, tgt_lang, client):
    req = models.TextTranslateRequest()
    params = {
        "SourceText": text,
        "Source": src_lang,
        "Target": tgt_lang,
        "ProjectId": 0
    }
    req.from_json_string(json.dumps(params))
    try:
        resp = client.TextTranslate(req)
        return resp.TargetText
    except Exception as e:

        print(f"\n[Error] Failed to translate '{text}': {e}")
        return ''


def translate_script(input_excel='/Users/kasugano/Documents/Pyt Homework/Personal/vocabulary_list.xlsx',
                     output_excel='vocabulary_list_with_chinese.xlsx',
                     src_col='English',
                     dest_col='Chinese',
                     src_lang='en',
                     dest_lang='zh',
                     region='ap-chongqing'):  # 将 region 作为参数

    secret_id = os.getenv("TENCENT_SEC_ID")
    secret_key = os.getenv("TENCENT_SEC_KEY")

    if not secret_id or not secret_key:
        print("错误：未在 .env 文件或环境变量中找到 TENCENT_SEC_ID 或 TENCENT_SEC_KEY。")
        print("请参考 .env.example 文件创建 .env 文件并填入你的密钥。")
        return

    try:
        cred = credential.Credential(secret_id, secret_key)
        client = tmt_client.TmtClient(cred, region)

        df = pd.read_excel(input_excel)
        translations = []

        print(f"Starting translation for {len(df)} words...")
        for word in tqdm(df[src_col], desc="Translating words"):

            if pd.notna(word):
                translation = tencent_translate(str(word), src_lang, dest_lang, client)
                translations.append(translation)
            else:
                translations.append('')

        df[dest_col] = translations
        df.to_excel(output_excel, index=False)
        print(f'\nTranslation complete! Translated {len(df)} words and saved to "{output_excel}".')

    except FileNotFoundError:
        print(f'错误：输入文件 "{input_excel}" 不存在。')
    except Exception as e:
        print(f'发生了未知错误: {e}')


if __name__ == '__main__':
    translate_script()
