import yaml
import openai
import os
from tqdm import tqdm
import json
import time
from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv()

# 从环境变量读取 OpenAI API 密钥和基础 URL
openai.api_key = os.getenv('OPENAI_API_KEY')
openai.api_base = os.getenv('OPENAI_API_BASE')

if not openai.api_key:
    raise ValueError("请在 .env 文件中设置 OPENAI_API_KEY")

if not openai.api_base:
    print("警告：未在 .env 文件中设置 OPENAI_API_BASE，将使用默认 API 基础 URL")

# 输入和输出文件
input_file = 'zh-CN.yml'
output_file = 'en-US.yml'
cache_file = 'translation_cache.json'

def load_yaml(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)

def save_yaml(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        yaml.dump(data, file, allow_unicode=True, sort_keys=False)

def load_cache():
    if os.path.exists(cache_file):
        with open(cache_file, 'r', encoding='utf-8') as file:
            return json.load(file)
    return {}

def save_cache(cache):
    with open(cache_file, 'w', encoding='utf-8') as file:
        json.dump(cache, file, ensure_ascii=False, indent=2)

def translate_text(text):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a translator. Translate the following Chinese text to English."},
                {"role": "user", "content": text}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Translation error: {e}")
        return None

def translate_recursive(data, cache, path=[]):
    if isinstance(data, dict):
        for key, value in data.items():
            new_path = path + [key]
            data[key] = translate_recursive(value, cache, new_path)
    elif isinstance(data, list):
        for i, item in enumerate(data):
            new_path = path + [str(i)]
            data[i] = translate_recursive(item, cache, new_path)
    elif isinstance(data, str):
        cache_key = '.'.join(path)
        if cache_key in cache:
            return cache[cache_key]
        
        translated = translate_text(data)
        if translated:
            cache[cache_key] = translated
            save_cache(cache)  # 保存缓存
            return translated
        else:
            return data
    return data

def main():
    yaml_data = load_yaml(input_file)
    cache = load_cache()

    total_items = sum(1 for _ in yaml.dump(yaml_data).splitlines())
    
    with tqdm(total=total_items, desc="Translating") as pbar:
        def update_progress(path):
            pbar.update(1)
            pbar.set_description(f"Translating: {'.'.join(path)}")

        def translate_with_progress(data, cache, path=[]):
            result = translate_recursive(data, cache, path)
            update_progress(path)
            return result

        translated_data = translate_with_progress(yaml_data, cache)

    save_yaml(translated_data, output_file)
    print(f"Translation completed. Output saved to {output_file}")

if __name__ == "__main__":
    main()