import argparse
import xml.etree.ElementTree as ET
import importlib
import os

initial_pymodels=[]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config','-c',type=str)
    args = parser.parse_args()
    assert args.config ,"please define the absolute config file path"

    #parse the .xml file
    cfg = ET.parse(args.config)
    root = cfg.getroot()
    # 遍历每个Alpha节点
    for i in root.findall("Alpha"):

    #找到计算alpha的代码文件，指的是alpha_template.py
        config = i.find('Config')
        alpha_code_file = config.attrib['alphacode']
    #引入alpha_template.py,获取create函数 用于创建对象。
        moudle = importlib.import_module(alpha_code_file)
        globals()['create'] = getattr(moudle, 'create')
    #处理Alpha节点，添加必要的其它节点信息
        i.append(root.find("DATA"))
        i.append(root.find("Constants"))
        i.append(root.find("Universe"))
    #创建实力对象
        initial_pymodels.append(create(i))
    for i in initial_pymodels:
        i.save_data()

if __name__ == '__main__':
    main()


