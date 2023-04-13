

if __name__ == '__main__':
    str = "同时执行一个子,顺序aa,然后一起"
    list = ["同时", "并行", "一起"]
    print(any(x in str for x in list))