import yaml


def get_data(data_file_name, test_name):
    """
    适用于如下yaml格式的数据读取
    test_add_linkman01:
      test_add_linkman_001:
        name: "zhangsan"
        phone: "123456"
      test_add_linkman_002:
        name: "lisi"
        phone: "987654"
    test_add_linkman02:
      test_add_linkman_001:
        name: "zhangsan"
        phone: "123456"
      test_add_linkman_002:
        name: "lisi"
        phone: "987654"
    :param test_name:用例名， 例如：test_login
    :return:data_list  数据列表，格式为：[(), ()]
    """
    data_list = []
    # 从yaml文件读取字典数据
    with open("../data/{}.yaml".format(data_file_name), "r", encoding="utf-8") as f:
        result = yaml.load(f)
    for data_id_name in result:
        # 判断test_方法名
        print(data_id_name)
        if data_id_name == test_name:
            # 获取方法名下用例数据字典
            data = result.get(data_id_name)
            print(data)
            # 获取数据字典
            for sub_sub_dict in data.values():
                print(sub_sub_dict)
                dict_single = []
                #
                for value in sub_sub_dict.values():
                    dict_single.append(value)
                data_list.append(dict_single)
            return data_list


if __name__ == '__main__':
    get_data("data", "test_add")