import numpy as np
import pandas as pd
import os

class alpha_baase_model:
    def __init__(self,cfg):
        pass
        #根据cfg配置股票池和回测区间
        self.cfg_root  = cfg
        with open('E:\Pycharm_files\Quant\devolop\submiting\data/daily_time_list.txt', 'r') as f:
            self.datelist = [i.strip('\n')[:8] for i in f.readlines()]
        with open("E:\Pycharm_files\Quant\devolop\submiting\data/tkrs.txt", 'r') as f:
            self.tkrs = [i.strip('\n') for i in f.readlines()]

        self.factor_series_list =[]
        self.wts = np.zeros(len(self.tkrs))
    def push_interval_data(self,didx):
        pass

        return True

    def save_data(self):
        for didx in self.datelist:
            if self.push_interval_data(didx):
                self.factor_series_list.append(self.wts)

        pd.concat(self.factor_series_list,axis=1).T.to_csv(os.path.join(self.cfg_root.attrib['dumpAlphaDir'],self.cfg_root.attrib['id']+'.csv'))
        print('save_data done！')