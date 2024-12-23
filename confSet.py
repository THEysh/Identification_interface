import configparser

# 定义全局变量字典
ConfGlobals = {}

def readConfig(file_path):
    """读取配置文件并将内容存储在全局变量中"""
    config = configparser.ConfigParser()

    # 读取文件，指定编码为 UTF-8
    with open(file_path, 'r', encoding='utf-8') as f:
        config.read_file(f)

    # 将配置项存储到全局变量
    ConfGlobals['path'] = config.get('data', 'path')
    ConfGlobals['dataSaveDirectory'] = config.get('data', 'dataSaveDirectory')
    ConfGlobals['modelPath'] = config.get('data', 'modelPath')
    ConfGlobals['conf'] = config.getfloat('data', 'conf')
    ConfGlobals['iou'] = config.getfloat('data', 'iou')
    ConfGlobals['threadCount'] = config.getint('data', 'threadCount')


if __name__ == "__main__":
    # 读取配置文件
    readConfig('config.ini')
    # 打印全局变量的内容以验证正确性
    print("全局配置:")
    print(ConfGlobals)
