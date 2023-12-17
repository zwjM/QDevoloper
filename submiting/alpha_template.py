import numpy as np
import logging
from data_api_py import *
from alpha_base_model import alpha_baase_model

# 创建一个文档处理器，将log输出到 example.log
file_handler = logging.FileHandler('example.log')
file_handler.setLevel(logging.INFO)
# 创建一个控制台处理器,将log输出到 console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Configure the logging settings
logging.basicConfig(
    level=logging.INFO,  # Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[file_handler,console_handler]
)

# Create a logger with the name __name__ (usually the name of the current module)
logger = logging.getLogger(__name__)
class PYMODEL(alpha_baase_model):
    def __init__(self, cfg):
        super(PYMODEL, self).__init__(cfg)
        cfg_root = cfg
        DATA = cfg_root.find('DATA').attrib['dataFileRoot']

        self.pydfch = data_api_py(DATA)
        logger.info(f"DATA:{cfg_root.find('DATA').attrib['dataFileRoot']}")

        '''
       load_data
        '''
       #
       #
        '''
        load necessary config from xml
        '''
        params = cfg_root.find("Config").attrib
        self.trimp = params['trimp']
        print(self.trimp)
       #
        '''
        user define variables;built factor df
        '''
       #
        factor = pd.read_csv('zwj/alpha004_rolling20.csv', index_col=0)
        factor.index = factor.index.astype('str')
        self.factor = factor
       #
        self.wts = np.zeros(len(self.tkrs))



    def push_interval_data(self, didx):
        #这个函数用来获取每一天的因子

        date = didx

        wts = self.factor.loc[date]

        self.wts = (wts).reindex(self.tkrs)

        logger.info(
            "alpha stats:{} ,Min({:.2f}), Q1({:.2f}), Mean({:.2f}), Median({:.2f}), Q9({:.2f}),Max({:.2f}), Cnt({:.0f})".format(didx,
                np.nanmin(wts), np.nanquantile(wts, 0.1), np.nanmean(wts), np.nanmedian(wts),
                np.nanquantile(wts, 0.9), np.nanmax(wts), len(self.tkrs) - np.isnan(wts).sum()
            ))

        return True

    def __del__(self):
        print("call __del__")


def create(cfg):
    return PYMODEL(cfg)

