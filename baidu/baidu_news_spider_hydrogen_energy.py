from multiprocessing import Pool
import time
import os

from baidu.baidu_base import doSpider

if __name__ == "__main__":
    import pandas as pd
    company_list = pd.read_excel(os.path.join('../company_data', '企业查询数据导出-【爱企查】-新能源企业.xls')).values.tolist()
    start_time = time.time()
    print("主进程开始执行>>> pid={}".format(os.getpid()))
    ps = Pool(16)
    for company_one in company_list:
        print(company_one)
        ps.apply_async(doSpider, args=(company_one[0], 'focus', '../export_data/氢能企业'))  # 异步执行
        ps.apply_async(doSpider,
                       args=(company_one[0] + " " + company_one[1], 'focus', '../export_data/氢能企业主要人员'))  # 异步执行
    # 关闭进程池，停止接受其它进程
    ps.close()
    # 阻塞进程
    ps.join()
