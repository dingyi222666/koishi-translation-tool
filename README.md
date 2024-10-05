# Koishi YAML 翻译和合并工具

这个项目提供了一套 Python 脚本，用于将 YAML 文件从中文翻译成英文，以及合并多个 YAML 文件。它使用 OpenAI 的 GPT-3.5 模型进行翻译，并支持缓存以提高效率。

## 功能特点

1. 将 Koishi XLIFF 文件转换为 YAML 格式
2. 使用 OpenAI 的 GPT-3.5 模型将 YAML 文件从中文翻译成英文
3. 合并多个 YAML 文件
4. 缓存翻译结果以避免重复的 API 调用
5. 翻译过程中显示进度条

## 系统要求

- Python 3.6+
- PyYAML
- openai
- tqdm
- python-dotenv

## 安装步骤

1. 克隆此仓库：

   ```bash
   git clone https://github.com/yourusername/yaml-translation-tool.git
   cd yaml-translation-tool
   ```

2. 安装所需的包：

   ```bash
   pip install -r requirements.txt
   ```

3. 在项目根目录创建一个 `.env` 文件，并添加您的 OpenAI API 密钥：

   ```bash
   OPENAI_API_KEY=your_api_key_here
   OPENAI_API_BASE=https://api.openai.com/v1
   ```

## 使用方法

### 将 XLIFF 转换为 YAML 并合并文件

运行 `main.py` 脚本：

```bash
python main.py
```

这个脚本将会：

1. 将 XLIFF 文件转换为 YAML 格式
2. 创建一个 `zh-CN.yml` 文件
3. 将 `zh-CN.yml` 与 `ChatLuna.yml` 合并，并创建一个 `merged_output.yml` 文件

### 翻译 YAML 文件

运行 `translate_yaml.py` 脚本：

```bash
python translate_yaml.py
```

这个脚本将会：

1. 加载 `zh-CN.yml` 文件
2. 将其内容从中文翻译成英文
3. 将翻译后的内容保存到 `en-US.yml`
4. 使用缓存来存储翻译结果，避免重复的 API 调用

## 文件说明

- `main.py`：处理 XLIFF 到 YAML 的转换和 YAML 合并
- `translate_yaml.py`：使用 OpenAI 的 API 管理翻译过程
- `requirements.txt`：列出所有 Python 依赖
- `.env`：包含环境变量（API 密钥）
- `.gitignore`：指定 Git 要忽略的文件

## 注意事项

请确保保密您的 OpenAI API 密钥，不要将 `.env` 文件提交到版本控制系统。

## 贡献

欢迎贡献、提出问题和功能请求。如果您想贡献，请查看 [issues 页面](https://github.com/dingyi222666/koishi-translation-tool/issues)。

## 许可证

[MIT](https://choosealicense.com/licenses/mit/)
