# 从SQL文件中获取data_a, data_b, data_c,


def get_anomaly():
    data_a = []
    data_b = []
    data_c = []
    # win10
    anomaly_path = 'D:\\Code\\MetisBackend\\MetisModels\\management\\commands\\anomaly.sql'
    # mac
    # anomaly_path = '/Users/xxx/Git/MetisBackend/MetisModels/management/commands/anomaly.sql'
    with open(anomaly_path, 'r') as f_r:
        for line in f_r.readlines():
            if line.startswith('INSERT INTO'):
                item = line.split()
                if item:
                    data_a.append(item[13].rstrip(",").replace("'", ""))
                    data_b.append(item[12].rstrip(",").replace("'", ""))
                    data_c.append(item[11].rstrip(",").replace("'", ""))
    return data_a, data_b, data_c


def get_sample_set():
    data_a = []
    data_b = []
    data_c = []
    sample_set_path = 'D:\\Code\\MetisBackend\\MetisModels\\management\\commands\\sample_set.sql'
    # sample_set_path = '/Users/xxx/Git/MetisBackend/MetisModels/management/commands/sample_set.sql'
    with open(sample_set_path, 'r') as f_r:
        for line in f_r.readlines():
            if line.startswith('INSERT INTO'):
                item = line.split()
                if item:
                    data_a.append(item[18].rstrip(",").replace("'", ""))
                    data_b.append(item[17].rstrip(",").replace("'", ""))
                    data_c.append(item[16].rstrip(",").replace("'", ""))
    return data_a, data_b, data_c


if __name__ == '__main__':
    # get_anomaly()
    get_sample_set()

