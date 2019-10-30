#读取excel并爬取歌词，制作成词云
from wordCloud import read_song_excel
import pandas as pd
import json
import re
import jieba
from PIL import Image
import numpy as np
from wordcloud import WordCloud
import matplotlib.pyplot as plt
#爬取歌词并保存进李荣浩（含歌词）.csv
def get_read_songs():
    df = pd.read_excel('李荣浩.xlsx')
    # print(message[['歌曲','歌曲链接']])
    print(df['歌曲链接'][1])
    # 遍历dataframe
    for index, row in df.iterrows():
        href = row["歌曲链接"]
        id = href[30:]
        print(id)
        url = 'http://music.163.com/api/song/lyric?' + 'id=' + str(id) + '&lv=1&kv=1&tv=-1'
        print(url)
        lyric = read_song_excel.get_html_soup(url, '', False)
        json_obj = lyric.text
        j = json.loads(json_obj)
        # 正则表达式，清理文本中带有作词，作曲等无关词部分
        lrc = j['lrc']['lyric']
        pat = re.compile(r'[作曲.*?作词.*?编曲.*?李荣浩.*?吉他.*?录音.*?]')
        lrc = pat.sub('', lrc)
        pat = re.compile(r'[^\u4e00-\u9fa5]')  # 删除非中文字符
        lrc = pat.sub('', lrc)
        lrc = lrc.strip()
        #df增加一列
        row['歌词'] = lrc
        print(row['歌词'])
        if index==0:
            df.insert(3,'歌词',row)
            df.loc[index, '歌词'] = lrc
        else:
            df.loc[index,'歌词']=lrc
    df.to_csv('李荣浩（含歌词）.csv',encoding="utf_8_sig")

#读取excel中的歌词，并进行文本jieba分词
#导入歌词数据
def word_cut():
    inf=pd.read_csv('李荣浩（含歌词）.csv')
    text=''.join(inf['歌词'])
    # 结巴分词
    segs = jieba.cut(text, True)
    # 过滤点单个字
    word_list = []
    for seg in segs:
        if len(seg) > 1:
            word_list.append(seg)
    # 存储
    word = pd.DataFrame({'word': word_list})
    # print(word['word'].value_counts())
    word.to_excel('分词统计表.xlsx')
    return word['word'].value_counts()

#生成词云
def word_pic():
    color_mask = np.array(Image.open("4.jpg"))
    wc = WordCloud(font_path='simsun.ttc', background_color="white", max_words=3000, mask=color_mask)
    wc.generate_from_frequencies(word_cut())
    wc.to_file("词云.png")
    # show
    plt.imshow(wc, interpolation='bilinear')
    plt.axis("off")
    plt.show()

#爬取歌词，存入excel中
get_read_songs()
#生成词云
word_pic()
