import xml.etree.ElementTree as ET
import os
import yaml


def read_xliff(file_path):
    # 解析 XLIFF 文件
    tree = ET.parse(file_path)
    root = tree.getroot()

    # 获取 XLIFF 命名空间
    namespaces = {'xliff': 'urn:oasis:names:tc:xliff:document:1.2'}

    # 存储翻译单元的字典
    translations = {}

    # 遍历所有 file 元素
    for file_elem in root.findall('.//xliff:file', namespaces):
        # 获取 file 的 original 属性
        original = file_elem.get('original')

        # 只处理 original 为 'zh-CN.yml' 的文件
        if os.path.basename(original) == 'zh-CN.yml':
            # 遍历该文件中的所有 trans-unit 元素
            for trans_unit in file_elem.findall('.//xliff:trans-unit', namespaces):
                # 获取 trans-unit 的 id
                unit_id = trans_unit.get('id')

                # 获取 resname（如果存在）
                resname = trans_unit.get('resname')

                # 获取源文本
                source = trans_unit.find('xliff:source', namespaces).text

                # 获取目标文本（如果存在）
                target_elem = trans_unit.find('xliff:target', namespaces)
                target = target_elem.text if target_elem is not None else None

                # 将翻译单元添加到字典中
                translations[unit_id] = {
                    'resname': resname, 'source': source, 'target': target, 'file': original}

    return translations


def merge_dict(target, source):
    for key, value in source.items():
        if isinstance(value, dict):
            if key not in target:
                target[key] = {}
            if isinstance(target[key], dict):
                merge_dict(target[key], value)
            else:
                target[key] = value
        elif isinstance(value, list):
            if key not in target:
                target[key] = value
            elif isinstance(target[key], list):
                # 扩展目标列表以匹配源列表的长度
                target[key].extend([None] * (len(value) - len(target[key])))
                for i, v in enumerate(value):
                    if v is not None:
                        if isinstance(v, (dict, list)):
                            if target[key][i] is None:
                                target[key][i] = type(v)()
                            merge_dict(target[key][i], v)
                        else:
                            target[key][i] = v
            else:
                target[key] = value
        else:
            target[key] = value
    return target


def remove_quotes(key):
    return key.strip('"')


def create_yaml_from_translations(translations, output_file):
    yaml_data = {}

    for unit_id, translation in translations.items():
        file_path = translation['file']
        resname = translation['resname']
        source = translation['source']

        if "[koishijs.webui]" in file_path:
            continue

        path = [remove_quotes(part) for part in resname.split('.')]
        print(path)
        current = source
        for i in range(len(path) - 1, -1, -1):
            if path[i].isdigit():
                index = int(path[i])
                new_current = [None] * (index + 1)
                new_current[index] = current
                current = new_current
            else:
                current = {path[i]: current}

        yaml_data = merge_dict(yaml_data, current)

    class MultilineDumper(yaml.SafeDumper):
        def ignore_aliases(self, data):
            return True

        def represent_scalar(self, tag, value, style=None):
            if isinstance(value, str) and '\n' in value:
                style = '|'
            return super().represent_scalar(tag, value, style)

    with open(output_file, 'w', encoding='utf-8') as f:
        yaml.dump(yaml_data, f, allow_unicode=True, sort_keys=False, Dumper=MultilineDumper)


def load_yaml(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)


def merge_yaml_files(file1, file2, output_file):
    # 加载两个 YAML 文件
    data1 = load_yaml(file1)
    data2 = load_yaml(file2)

    # 合并两个字典
    merged_data = merge_dict(data1, data2)

    # 保存合并后的 YAML 文件
    class MultilineDumper(yaml.SafeDumper):
        def ignore_aliases(self, data):
            return True

        def represent_scalar(self, tag, value, style=None):
            if isinstance(value, str) and '\n' in value:
                style = '|'
            return super().represent_scalar(tag, value, style)

    with open(output_file, 'w', encoding='utf-8') as f:
        yaml.dump(merged_data, f, allow_unicode=True,
                  sort_keys=False, Dumper=MultilineDumper)


# 使用示例
if __name__ == '__main__':
    xliff_file = 'koishi_zh-TW.xliff'  # 替换为您的 XLIFF 文件路径
    result = read_xliff(xliff_file)

    # 打印结果
    for unit_id, translation in result.items():
        """ print(f"ID: {unit_id}")
        print(f"File: {translation['file']}")
        print(f"Resname: {translation['resname']}")
        print(f"Source: {translation['source']}")
        print(f"Target: {translation['target']}")
        print("---") """

    # 打印条目数量
    print(f"原始条目数量: {len(result)}")

    # 创建 YAML 文件
    output_yaml = 'zh-CN.yml'  # 输出的 YAML 文件名
    create_yaml_from_translations(result, output_yaml)
    print(f"YAML 文件已创建: {output_yaml}")

    # 统计过滤后的条目数量
    with open(output_yaml, 'r', encoding='utf-8') as f:
        filtered_yaml = yaml.safe_load(f)

    def count_items(d):
        count = 0
        for v in d.values():
            if isinstance(v, dict):
                count += count_items(v)
            else:
                count += 1
        return count

    filtered_count = count_items(filtered_yaml)
    print(f"过滤后条目数量: {filtered_count}")

    # 合并 zh-CN.yml 和 ChatLuna.yml
    merge_yaml_files('zh-CN.yml', 'ChatLuna.yml', 'merged_output.yml')
    print("已合并 zh-CN.yml 和 ChatLuna.yml 到 merged_output.yml")

    # 统计合并后的条目数量
    with open('merged_output.yml', 'r', encoding='utf-8') as f:
        merged_yaml = yaml.safe_load(f)

    merged_count = count_items(merged_yaml)
    print(f"合并后条目数量: {merged_count}")
