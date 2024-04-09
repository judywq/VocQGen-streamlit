import pandas as pd
from vocqgen.utils import setup_log
from vocqgen.config import Config
from vocqgen.core import generate_from_df



def test_with_file():
    path = './test-data/AWL_sublist1_small.xlsx'
    df = pd.read_excel(path)
    config = Config()
    res = generate_from_df(df, config)
    print(res['result'])
    
if __name__ == '__main__':
    setup_log()
    test_with_file()
