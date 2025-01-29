def read_from_txt(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read().strip()
            cities = content.split(' ')
            return cities
    except FileNotFoundError:
        print(f"Error: File not found at path: {file_path}")
        return None
    except Exception as e:
        print(f"Error reading file: {e}")
        return None
    
def write_to_file(file_path, string):
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(string)
    except Exception as e:
        print(f"写入文件时发生错误: {e}")