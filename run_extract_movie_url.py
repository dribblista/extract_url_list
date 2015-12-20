# -*- coding: utf-8 -*-

## ライブラリのインポート, データの読込み
import sys
from bs4 import BeautifulSoup
from urllib import request
import re
import pandas as pd
import time

def filter_list_by_keyword(movie_info, keyword):
    return movie_info[movie_info['title'].str.contains(keyword)]

def extract_movie_list(url, movie_info):
    
    try:
        response = request.urlopen(url)

        body = response.read()
        soup = BeautifulSoup(body)

        div_div = soup.div.findAll('div')

        for i, div_one in enumerate(div_div):
            try:
                if div_one['class'][0]=='da-zoom-normal':
                    pass
                    new_dic = {div_one.a['moviecode']:{'url':div_one.a['href'], 'title':div_one.img['alt']}}
                    new_df = pd.DataFrame(new_dic).T
                    movie_info = pd.concat([movie_info, new_df])
            except:
                pass
    except:
        print('end page.')
        raise
    finally:
        return movie_info

def run_extract_movie(base_url, max_page_number):
    
    res = pd.DataFrame()

    start = time.time()
    for i in range(int(max_page_number)):
        url = base_url + str(i+1)
        res = extract_movie_list(url, res)
    elapsed_time = time.time() - start
    print(("elapsed_time:{0}".format(elapsed_time)) + "[sec]")

    res.to_csv('list.csv')

    
    keyword_list_df = pd.read_csv('keyword_list.txt',header=None)
    keyword_list = keyword_list_df[0].tolist()
    print(keyword_list)

    for keyword in keyword_list:
        filterd_movie_list = filter_list_by_keyword(res, keyword)

    filterd_movie_list.to_csv('filterd_movie_list.csv')
    
    return 0

# コマンドライン実行用
if __name__ == "__main__":

    argvs = sys.argv
    argc = len(argvs)

    # 引数チェック
    if argc !=3:
        print('Usage: # python %s base_url max_page_number keyword_list' % argvs[0])
        sys.exit(255)

    # 引数の数が3の場合は、 オプションの解析
    else:
        run_extract_movie(argvs[1], argvs[2])

