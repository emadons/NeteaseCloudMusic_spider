#爬取歌手所有的专辑的全部歌曲并写入excel中
import requests
from bs4 import BeautifulSoup
import random
import numpy as np
import pandas as pd
#代理ip，每次运行可以随机返回一个代理ip，这样可以防止真实ip被封的可能性
def get_ip_list(url, headers):
    web_data = requests.get(url, headers=headers)
    soup = BeautifulSoup(web_data.text, 'lxml')
    ips = soup.find_all('tr')
    ip_list = []
    for i in range(1, len(ips)):
        ip_info = ips[i]
        tds = ip_info.find_all('td')
        ip_list.append(tds[1].text + ':' + tds[2].text)
    return ip_list
#从一个代理ip列表中随机获取一个代理ip
def get_random_ip(ip_list,flag):
    proxy_list_http = []
    for ip in ip_list:
        proxy_list_http.append('http://' + ip)
    proxy_ip = random.choice(proxy_list_http)
    if flag==True:
        proxies = {'http': proxy_ip}
    else:
        proxies = {'https': proxy_ip}
    return proxies

#获取网页内容
#url：地址 page：页数参    flag：ip代理选择加载http（True）还是https（False）
def get_html_soup(url,page,flag):
    #伪造头信息
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Cookie': 'mail_psc_fingerprint=2ee1cce82619e6d39b05cd9ac87c0973; _iuqxldmzr_=32; vjuids=48f43a56e.167350591c1.0.254f646cc86aa; vjlast=1542782817.1542782817.30; __utma=94650624.126431011.1535172083.1543980509.1545270351.6; usertrack=ezq0pFxK0eYSoynwBwIGAg==; vinfo_n_f_l_n3=2ce18c6c37e23bbf.1.2.1534662275510.1542782845658.1553265594869; _ntes_nnid=1d7d74ed396ed51f6fd833c858a3f884,1567001598477; _ntes_nuid=1d7d74ed396ed51f6fd833c858a3f884; mp_MA-9ADA-91BF1A6C9E06_hubble=%7B%22sessionReferrer%22%3A%20%22https%3A%2F%2Fcampus.163.com%2F%22%2C%22updatedTime%22%3A%201568789961150%2C%22sessionStartTime%22%3A%201568789961143%2C%22sendNumClass%22%3A%20%7B%22allNum%22%3A%202%2C%22errSendNum%22%3A%200%7D%2C%22deviceUdid%22%3A%20%227c2c47ce-b0f7-4ab9-9a1f-85cc06511cde%22%2C%22persistedTime%22%3A%201568789961137%2C%22LASTEVENT%22%3A%20%7B%22eventId%22%3A%20%22da_screen%22%2C%22time%22%3A%201568789961150%7D%2C%22sessionUuid%22%3A%20%228be60bd1-be00-49fc-9e9d-e784d2151c27%22%7D; hb_MA-BFF5-63705950A31C_source=www.baidu.com; __remember_me=true; ntes_kaola_ad=1; WM_TID=Bps1rPcbHWVEEBUVEVMs9%2FenuLfroEes; JSESSIONID-WYYY=mtuqJD%2BspMGBUP3B0ORU5TyxkHVOVF1rU8Jr8NMwu3eJN0i14o%2FYoeU61HuOdP%5Cj2N5t4I%2Bsg7iQjKQAoc7R8dWroe8XCq9v3I6JjuMueHBdmIq3gOIHTC6EpifioFm1fNEAlb9zopVTqf5Ic2cHCy5JVe9oyjA%5CWxrVY%2FvX3nfnCbmN%3A1571823989477; WM_NI=shOWkMSsHZ3TJW58WglID5CxZg3%2FX7BQuEqTj8jE06DpnkpH%2BcyKo0aQB%2By5tjERbzF4ci59eCtR1IUVYGBzT4nHDs%2Bik4iXTEc49uXvh9aXkdvAihmwTUymuoWWdW49RDE%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6eeb0f15f8593a4a4d03eb3bc8fa2d15e878f8faaf37cf5ecbbd7d634a9a7fa8bd02af0fea7c3b92ab1b881b8ea4791ad88bbb2608a89fbd9d66db0978cd6c2749ab9fdd0db3d828fbba6f460aae8a6a6b33e88b0a28cf344e9bdb7acee3ca38f8eccfc3fb8b68bb3e17286ecad8ab833a79dbcb3b443978a97a8c17298eca2a9c779e9b7a5d5ec54989badd5bc7f9caaa8dae454a9bcbaa2ec64afa99cb6fc67b7b199b8e75df8e79ea5c837e2a3; MUSIC_U=d95630ba0ce0ba34c7b54b3b25e5fd94ebd38203313a14876a1954d9a033ec18cc01b5f991042a13c1927cf96245d92841049cea1c6bb9b6; __csrf=3d284daa547a51dd1b4d5e1ffea18fc7',
        'Referer': 'https://music.163.com/',
        'Upgrade-Insecure-Requests': '1',
        'Host': 'music.163.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'}
    #加载代理ip  https://www.xicidaili.com/nn/  https://www.kuaidaili.com/free/  http://www.89ip.cn/index_1.html
    ip_list = get_ip_list('https://www.kuaidaili.com/free/', headers=headers)
    proxies = get_random_ip(ip_list,flag)
    print('此次代理ip为：',proxies)
    html = requests.get(url+'{}'.format(page), headers=headers,proxies=proxies).content
    soup = BeautifulSoup(html,'lxml')
    return soup

#返回一个以 专辑链接：名字 为键值对的字典对象
def get_abum_info(soup):
    # 获取歌手所有专辑
    # 获取有class='tit s-fc0'的所有节点，即专辑信息（专辑名、链接）
    abum_list_element = soup.find_all(attrs={'class': 'tit s-fc0'})
    # 提取专辑名、链接
    for i in abum_list_element:
        temp = str(i).split('">')
        abum_info_dic['https://music.163.com'+temp[0][27:]]=temp[1][:-4]
    return abum_info_dic

#获取所有专辑的全部歌曲，并返回一个以 歌曲链接：歌名 为键值对的字典对象
def get_songs(abum_info_dic):
    for key in abum_info_dic:
        #根据获取的专辑链接，再进行专辑中歌曲的爬取
        songs_html_soup=get_html_soup(key,'',True)
        #问题，到第二项页面就只能加载一个,已解决：key值被覆盖，键值对调换一下就可以了
        songs_list_element=songs_html_soup.find_all('meta',{'property':{'og:music:album:song'}})
        # print('专辑歌曲有：',songs_list_element)
        #切割字符
        for i in songs_list_element:
            #切割成两个子字符串
            temp = str(i).split(';url=')
            print(temp)
            key = temp[1][:-34]
            value = temp[0][21:]
            songs_dic[key]=value
            print(songs_dic)
    return songs_dic

#将专辑 专辑链接 歌曲 歌曲链接 存入excel
def save_message_excel(abum_info_dic,songs_dic):
    sun = pd.DataFrame(np.zeros((71, 2)),columns=['歌曲', '歌曲链接'])
    num = 0
    for key1 in songs_dic:
        sun['歌曲'].loc[num] = songs_dic.get(key1)
        sun['歌曲链接'].loc[num] = key1
        num += 1
    sun.to_excel('李荣浩.xlsx')

if __name__ == '__main__':
    album_url = 'https://music.163.com/artist/album?id=4292&limit=12&offset='
    # 存放专辑地址
    abum_info_dic = {}
    songs_dic = {}
    for page in range(0,13,12):
        print("正在爬取第{}页专辑信息".format(int((page/12)+1)))
        print(page)
        soup=get_html_soup(album_url,page,True)
        # 获取专辑链接、名字(字典对象)
        abum_info_dic = get_abum_info(soup)
        # 获取所有专辑的全部歌曲，并存放至字典songs_dic中
        songs_dic = get_songs(abum_info_dic)
        print(songs_dic)#打印歌曲信息
    save_message_excel(abum_info_dic,songs_dic)#最终存入excel表，然后再由read_song_words.py进行调用，生成词云


