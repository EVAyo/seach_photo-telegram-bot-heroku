# -*- coding: utf-8 -*-
import re
import requests
import base64
import time
import datetime
from urllib import parse
from bs4 import BeautifulSoup
import telebot
import json
import os
import telegraph
from telegraph import Telegraph
import sys

telegraph = Telegraph()

# Example of your code beginning
#           Config vars
token = str(sys.argv[1])

session = requests.session()
bot = telebot.TeleBot(token)
print(bot.get_me())

bot_name="@"+bot.get_me().username
print(bot_name)
url_dict={}

header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 5.8; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36",
    'Referer': 'https://accounts.pixiv.net/login?lang=zh&source=pc&view_type=page&ref=wwwtop_accounts_index',
}

def save(dict):
    if isinstance(dict, str):
        dict = eval(dict)
    with open('url.txt', 'w', encoding='utf-8') as f:
        # f.write(str(dict))  # 直接这样存储的时候，读取时会报错JSONDecodeError，因为json读取需要双引号{"aa":"BB"},python使用的是单引号{'aa':'bb'}
        str_ = json.dumps(dict, ensure_ascii=False) # TODO：dumps 使用单引号''的dict ——> 单引号''变双引号"" + dict变str
        print(type(str_), str_)
        f.write(str_)

def load():
    with open('url.txt', 'r', encoding='utf-8') as f:
        data = f.readline().strip()
        print(type(data), data)
        dict = json.loads(data)
        return dict

def dele(path):
    if os.path.exists(path):  # 如果文件存在
        # 删除文件，可使用以下两种方法。
        os.remove(path)
        # os.unlink(path)
    else:
        print('no such file' )  # 则返回文件不存在

def download(url, id):
    global session, header
    title = "name"
    path = "pixiv"
    if not os.path.exists(path):
        os.mkdir(path)
    title = str(title)
    id = str(id)

    title = eval(repr(title).replace('\\', ''))
    title = eval(repr(title).replace('/', ''))
    title = eval(repr(title).replace('?', ''))
    title = eval(repr(title).replace('*', ''))
    title = eval(repr(title).replace('・', ''))
    title = eval(repr(title).replace('！', ''))
    title = eval(repr(title).replace('|', ''))
    title = eval(repr(title).replace(' ', ''))
    r = session.get(url, headers=header)

    try:
        if r.status_code != 404:
            with open('pixiv/%s-id：%s.jpg' % (title, id), 'wb') as f:
                f.write(r.content)
            print("下载成功:" + title + "_id" + id)
            where = 'pixiv/%s-id：%s.jpg' % (title, id)
            return where
        if r.status_code == 404:
            url = eval(repr(url).replace('jpg', 'png'))
            r = session.get(url, headers=header)

            with open('pixiv/%s-id：%s.png' % (title, id), 'wb') as f:
                f.write(r.content)

            print("下载成功:" + title + "_id" + id)
            where = 'pixiv/%s-id：%s.png' % (title, id)
            return where

    except:
        print("下载失败:" + title + "_id" + id)
        return

def daily():
    url_list = []
    title_list = []
    id_list=[]
    print("正在进行下载...")
    url = "https://www.pixiv.net/ranking.php?mode=daily&p=1&format=json"  # 日榜json文件，一个50张
    try:
        html = session.get(url, headers=header)
    except:
        print("抓取榜单失败")
    josn = json.loads(html.text)
    josn = str(josn)
    imgurl = re.findall("'url': '(.*?)',", josn, re.S)
    name = re.findall("'title': '(.*?)',", josn, re.S)
    for c, d in zip(imgurl, name):
        c = str(c)
        id = re.findall("\d\d\d\d\d\d\d\d", c, re.S)[0]
        c = eval(repr(c).replace('c/240x480/img-master', 'img-original'))
        url = eval(repr(c).replace('_master1200', ''))

        # download(c, d, id)
        url_list.append(url)
        id_list.append(id)
        title_list.append(d)
    return url_list, id_list, title_list

def monthly():
    url_list = []
    title_list = []
    id_list=[]
    print("正在进行下载...")
    url = "https://www.pixiv.net/ranking.php?mode=monthly&p=1&format=json"  # 日榜json文件，一个50张
    try:
        html = session.get(url, headers=header)
    except:
        print("抓取榜单失败")
    josn = json.loads(html.text)
    josn = str(josn)
    imgurl = re.findall("'url': '(.*?)',", josn, re.S)
    name = re.findall("'title': '(.*?)',", josn, re.S)
    for c, d in zip(imgurl, name):
        c = str(c)
        id = re.findall("\d\d\d\d\d\d\d\d", c, re.S)[0]
        c = eval(repr(c).replace('c/240x480/img-master', 'img-original'))
        url = eval(repr(c).replace('_master1200', ''))

        # download(c, d, id)
        url_list.append(url)
        id_list.append(id)
        title_list.append(d)
    return url_list, id_list, title_list

def weekly():
    url_list = []
    title_list = []
    id_list = []
    print("正在进行下载...")
    url = "https://www.pixiv.net/ranking.php?mode=weekly&p=1&format=json"  # 日榜json文件，一个50张
    try:
        html = session.get(url, headers=header)
    except:
        print("抓取榜单失败")
    josn = json.loads(html.text)
    josn = str(josn)
    imgurl = re.findall("'url': '(.*?)',", josn, re.S)
    name = re.findall("'title': '(.*?)',", josn, re.S)
    for c, d in zip(imgurl, name):
        c = str(c)
        id = re.findall("\d\d\d\d\d\d\d\d", c, re.S)[0]
        c = eval(repr(c).replace('c/240x480/img-master', 'img-original'))
        url = eval(repr(c).replace('_master1200', ''))

        # download(c, d, id)
        url_list.append(url)
        id_list.append(id)
        title_list.append(d)
    return url_list, id_list,title_list

def upload_file(photo_url,id):
    print(photo_url)
    where=download(photo_url,id)

    files = {"file": (
        "file", open(where, "rb"), "image/png")}
    url="https://telegra.ph/upload"

    r = requests.post(url=url,  files=files)
    print(r.text)

    try:
        print(r.json()[0]["src"])
        imgurl="https://telegra.ph"+r.json()[0]["src"]
        print(imgurl)
        dele(where)
        return imgurl
    except:
        return 0

def post_new(img_list,title_list,id_list,more):
    html_content =""

    for img ,title,id in zip(img_list,title_list,id_list):

        imgurl=upload_file(img,id)
        if imgurl!=0:
            text = f"<p>作品名:{title}{more}</p>" \
                   f"<p>id:{id}</p>" \
                   f"<img id=\"\" src=\"{imgurl}\"  />" \
                   f" <p>\n</p>" \

            html_content =html_content+text


    telegraph.create_account(short_name='pixiv_bot')
    response = telegraph.create_page(
        title='Pixiv',
        author_name="pixiv_bot",
        html_content=html_content
    )

    print('https://telegra.ph/{}'.format(response['path']))
    art_url='https://telegra.ph/{}'.format(response['path'])

    return str(art_url)


@bot.message_handler(commands=['day'])
def pixiv_day(message):
    print(message)
    global url_dict
    url_list, id_list,title_list = daily()
    date = time.strftime(" %Y-%m-%d 日榜", time.localtime())
    bot.send_message(chat_id=message.chat.id, text="开始获取日榜", parse_mode="MarkdownV2")
    try:
        url_dict=load()
        art_url=url_dict[date]
        print(art_url)
        bot.send_message(chat_id=message.chat.id, text=f"{art_url}")
    except:
        bot.send_message(chat_id=message.chat.id, text="今日未获取，正在获取", parse_mode="MarkdownV2")
        art_url=post_new(url_list,title_list,id_list,date)
        print(art_url)
        bot.send_message(chat_id=message.chat.id, text=f"{art_url}")
        url_dict[date]=art_url
        save(url_dict)

@bot.message_handler(commands=['month'])
def pixiv_monthy(message):
    print(message)
    global url_dict
    url_list, id_list,title_list = monthly()
    date = time.strftime(" %Y-%m-%d 月榜", time.localtime())
    bot.send_message(chat_id=message.chat.id, text="开始获取月榜", parse_mode="MarkdownV2")
    try:
        url_dict=load()

        art_url=url_dict[date]
        print(art_url)
        bot.send_message(chat_id=message.chat.id, text=f"{art_url}")
    except:
        bot.send_message(chat_id=message.chat.id, text="今日未获取，正在获取", parse_mode="MarkdownV2")
        art_url=post_new(url_list,title_list,id_list,date)
        print(art_url)
        bot.send_message(chat_id=message.chat.id, text=f"{art_url}")
        url_dict[date]=art_url
        save(url_dict)

@bot.message_handler(commands=['week'])
def pixiv_week(message):
    print(message)
    global url_dict
    url_list, id_list,title_list = weekly()
    date = time.strftime(" %Y-%m-%d 周榜", time.localtime())
    bot.send_message(chat_id=message.chat.id, text="开始获取周榜", parse_mode="MarkdownV2")
    try:
        url_dict=load()

        art_url=url_dict[date]
        print(art_url)
        bot.send_message(chat_id=message.chat.id, text=f"{art_url}")
    except:
        bot.send_message(chat_id=message.chat.id, text="今日未获取，正在获取", parse_mode="MarkdownV2")
        art_url=post_new(url_list,title_list,id_list,date)
        print(art_url)
        bot.send_message(chat_id=message.chat.id, text=f"{art_url}")
        url_dict[date]=art_url
        save(url_dict)

@bot.message_handler(commands=['saucenao'],func=lambda message: message.text==f"/saucenao{bot_name}" and ( message.chat.type == "group" or message.chat.type == "supergroup" ))
def send_saucenao_group(message):
    print(message)
    #bot.send_message(chat_id=message.chat.id, text="请发送图片,或回复此条信息 /cancel 取消",parse_mode="MarkdownV2")
    bot.register_next_step_handler(message, get_saucenao_group)
    bot.reply_to(message, text="请回复图片,或点击 /cancel 取消",parse_mode="MarkdownV2")

def get_saucenao_group(message):
    print(message)
    print(message.text)

    if message.text==f"/cancel{bot_name}":
        bot.reply_to(message, text="已退出搜图模式", parse_mode="MarkdownV2")
        return
    if message.content_type!="photo":
        bot.reply_to(message, text=f"请回复图片,或点击 /cancel 取消",parse_mode="MarkdownV2")
        bot.register_next_step_handler(message, get_ascii2d)
        return
    else:
        url = bot.get_file_url(message.photo[-1].file_id)
        print(url)
        saucenao_group(url, message)
        bot.reply_to(message, text="搜索完成", parse_mode="MarkdownV2")

def saucenao_group(photo_url,message):
    try:
        url="https://saucenao.com/search.php"
        #url = "https://saucenao.com"
        Header = {
            'Host': 'saucenao.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0',
             'Accept': 'text / html, application / xhtml + xml, application / xml;q = 0.9, * / *;q = 0.8',
            'Accept - Language': 'zh - CN, zh;q = 0.8, zh - TW;q = 0.7, zh - HK;q = 0.5, en - US;q = 0.3, en;q = 0.2',
             'Accept - Encoding': 'gzip, deflate, br',
            'Connection': 'keep - alive',

        }
        payloaddata = {

            'frame': 1,
            'hide': 0,
            'database': 999,
        }
        #files = {"file": "file": ('saber.jpg', open("saber.jpg", "rb", , "image/png")}
        photo_file=requests.get(photo_url)
        files = {"file": (
        "saucenao.jpg", photo_file.content, "image/png")}

        bot.reply_to(message,text="正在搜索saucenao")
        r = session.post(url=url, headers=Header, data=payloaddata,files=files)
        #r = session .get(url=url,headers=Header)
        soup = BeautifulSoup(r.text, 'html.parser')
        #print(soup.prettify())
        result=0
        choice=0
        for img in soup.find_all('div', attrs={'class': 'result'}):  # 找到class="wrap"的div里面的所有<img>标签
            #print(img)
            if('hidden' in str(img['class']))==False:
                try:
                    name=img.find("div",attrs={'class': 'resulttitle'}).get_text()
                    img_url=str(img.img['src'])
                    describe_list=img.find("div",attrs={'class': 'resultcontentcolumn'})
                    url_list = img.find("div", attrs={'class': 'resultcontentcolumn'}).find_all("a",  attrs={'class': 'linkify'})
                    similarity = str(img.find("div", attrs={'class': 'resultsimilarityinfo'}).get_text())
                    print(name)
                except:
                    continue
                try:
                    describe = str(url_list[0].previous_sibling.string)
                    describe_id = str(url_list[0].string)
                    describe_url = str(url_list[0]['href'])
                    auther_url = str(url_list[1]['href'])
                    auther = str(url_list[1].previous_sibling.string)
                    auther_id = str(url_list[1].string)
                    '''print(name)
                    print(img_url)
                    print(describe)
                    print(describe_id)
                    print(similarity)
                    print(auther)
                    print(auther_id)
                    print(describe_url)'''
                    text = f"{name}\n{describe}[{describe_id}]({describe_url})\n{auther}:[{auther_id}]({auther_url})\n相似度{similarity}"
                except:
                    '''print(describe_list.get_text())
                    print(describe_list.strong.string)
                    print(describe_list.strong.next_sibling.string)
                    print(describe_list.small.string)
                    print(describe_list.small.next_sibling.next_sibling.string)'''
                    auther = str(describe_list.strong.string)
                    auther_id = str(describe_list.strong.next_sibling.string)
                    describe = str(describe_list.small.string) + "\n" + str(describe_list.small.next_sibling.next_sibling.string)
                    text = f"{name}\n{auther}:{auther_id}\n{describe}\n相似度{similarity}"

                photo_file = session.get(img_url)
                bot.send_photo(chat_id=message.chat.id,reply_to_message_id=message.message_id,photo=photo_file.content,parse_mode='Markdown',caption=text)


                result=1
        if result==0:
            bot.reply_to(message, text="saucenao无结果")
    except:
        print("saucenao")


@bot.message_handler(commands=['ascii2d'],func=lambda message: message.text==f"/ascii2d{bot_name}" and ( message.chat.type == "group" or message.chat.type == "supergroup" ))
def send_ascii2d_group(message):
    bot.send_message(chat_id=message.chat.id, text="请回复图片,或输入 /cancel 取消",parse_mode="MarkdownV2")
    bot.register_next_step_handler(message, get_ascii2d_group)

def get_ascii2d_group(message):
    print(message)
    if message.text==f"/cancel{bot_name}":
        bot.send_message(chat_id=message.chat.id, text="已退出搜图模式", parse_mode="MarkdownV2")
        return
    if message.content_type!="photo":
        bot.send_message(chat_id=message.chat.id, text="请回复图片,或输入 /cancel 取消",parse_mode="MarkdownV2")

        bot.register_next_step_handler(message, get_ascii2d_group)
        return
    else:
        url = bot.get_file_url(message.photo[-1].file_id)
        print(url)
        ascii2d_group(url, message)
        bot.send_message(chat_id=message.chat.id, text="搜索完成", parse_mode="MarkdownV2")

def ascii2d_group(photo_url,message):
    try:
        url = "https://ascii2d.net/"
        # url = "https://saucenao.com"
        Header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0',
        }
        html = session.get(url, headers=Header)
        print(html)
        authenticity_token = re.findall("<input type=\"hidden\" name=\"authenticity_token\" value=\"(.*?)\" />", html.text, re.S)[0]
        payloaddata = {

            'authenticity_token': authenticity_token,
            'utf8': "✓",
        }
        # files = {"file": "file": ('saber.jpg', open("saber.jpg", "rb", , "image/png")}
        bot.reply_to(message, text="正在搜索ascii2d")
        photo_file = requests.get(photo_url)
        files = {"file": (
            "saucenao.jpg", photo_file.content, "image/png")}
        url = "https://ascii2d.net/search/multi"
        r = session.post(url=url, headers=Header, data=payloaddata, files=files)
        soup = BeautifulSoup(r.text, 'html.parser')
        # print(soup.prettify())
        pan = 0
        for img in soup.find_all('div', attrs={'class': 'row item-box'}):  # 找到class="wrap"的div里面的所有<img>标签
            # print(img)
            if pan != 0:
                img_url = "https://ascii2d.net" + str(img.img['src'])
                the_list = img.find_all('a')
                title = str(the_list[0].get_text())
                title_url = str(the_list[0]["href"])
                auther = str(the_list[1].get_text())
                auther_url = str(the_list[1]["href"])

                photo_file = session.get(img_url)
                text=f"titile:[{title}]({title_url})\nauther:[{auther}]({auther_url})"
                bot.send_photo(chat_id=message.chat.id,reply_to_message_id=message.message_id, caption=text, parse_mode='Markdown',photo=photo_file.content)
            pan = pan + 1
            if pan == 3:
                break
    except:
        print("ascii2d faild")

@bot.message_handler(commands=['anime'],func=lambda message: message.text==f"/anime{bot_name}" and ( message.chat.type == "group" or message.chat.type == "supergroup" ))
def send_anime_group(message):
    bot.send_message(chat_id=message.chat.id, text="请回复图片,或输入 /cancel 取消",parse_mode="MarkdownV2")
    bot.register_next_step_handler(message, get_anime)

def get_anime_group(message):
    print(message)
    if message.text==f"/cancel{bot_name}":
        bot.send_message(chat_id=message.chat.id, text="已退出搜图模式", parse_mode="MarkdownV2")
        return
    if message.content_type!="photo":
        bot.send_message(chat_id=message.chat.id, text="请回复图片,或输入 /cancel 取消",parse_mode="MarkdownV2")

        bot.register_next_step_handler(message, get_anime_group())
        return
    else:
        url = bot.get_file_url(message.photo[-1].file_id)
        print(url)
        anime_group(url, message)
        bot.send_message(chat_id=message.chat.id, text="搜索完成", parse_mode="MarkdownV2")

def anime_group(photo_url,message):
    try:
        url = "https://trace.moe/api/search"
        # url = "https://saucenao.com"
        photo_file = requests.get(photo_url)
        ls_f = base64.b64encode(photo_file.content)

        data = {
            "image": ls_f,
        }
        # files = {"file": "file": ('saber.jpg', open("saber.jpg", "rb", , "image/png")}

        r = session.post(url=url, data=data)
        # r = session .get(url=url,headers=Header)
        bot.reply_to(message,text="正在搜索 trace.moe")
        information = r.json()
        anilist_id = information['docs'][0]["anilist_id"]
        filename = information['docs'][0]['filename']
        tokenthumb = information['docs'][0]['tokenthumb']
        at = information['docs'][0]['at']
        limit = information['limit']  # 剩余搜索次数
        limit_ttl = information['limit_ttl']  # 剩余重置时间
        title = information['docs'][0]['title_chinese']
        episode = information['docs'][0]['episode']
        quota = information['quota']
        quota_ttl = information['quota_ttl']
        similarity=information['docs'][0]['similarity']
        similarity_num="%.2f%%" % (similarity * 100)
        img_url = f"https://trace.moe/thumbnail.php?anilist_id={anilist_id}&file={parse.quote(filename)}&t={at}&token={tokenthumb}"
        print(img_url)
        video_url = f"https://trace.moe/preview.php?anilist_id={anilist_id}&file={parse.quote(filename)}&t={at}&token={tokenthumb}"
        print(video_url)
        video = f"https://media.trace.moe/video/{anilist_id}/{parse.quote(filename)}?t={at}&token={tokenthumb}"
        print(video)
        more_url = f"https://anilist.co/anime/{anilist_id}"
        text = f"{similarity_num}\nTitle:{title}\n集数:{episode}\n时间：{datetime.timedelta(seconds=int(at))}\n来源：{filename}\n[更多信息]({more_url})\n分钟剩余搜索次数:{limit}\n分钟剩余次数重置时间:{limit_ttl}s\n24小时剩余搜索次数:{quota}\n24小时剩余次数重置时间:{datetime.timedelta(seconds=int(quota_ttl))}"
        print(text)
        photo_file = session.get(img_url)
        bot.send_photo(chat_id=message.chat.id,reply_to_message_id=message.message_id, photo=photo_file.content, parse_mode='Markdown', caption=text)
        photo_file = session.get(video)
        bot.send_video(chat_id=message.chat.id,reply_to_message_id=message.message_id,data=photo_file.content)
    except:
        print("anime faild")



@bot.message_handler(commands=['saucenao'],func=lambda message: message.chat.type == "private")
def send_saucenao(message):
    print(message)
    bot.send_message(chat_id=message.chat.id, text="请发送图片,或输入 /cancel 取消",parse_mode="MarkdownV2")
    bot.register_next_step_handler(message, get_saucenao)

def get_saucenao(message):
    print(message)

    if message.text=="/cancel":
        bot.send_message(chat_id=message.chat.id, text="已退出搜图模式", parse_mode="MarkdownV2")
        return
    if message.content_type!="photo":
        bot.send_message(chat_id=message.chat.id, text="请发送图片,或输入 /cancel 取消",parse_mode="MarkdownV2")

        bot.register_next_step_handler(message, get_ascii2d)
        return
    else:
        url = bot.get_file_url(message.photo[-1].file_id)
        print(url)
        saucenao(url, message.chat.id)
        bot.send_message(chat_id=message.chat.id, text="搜索完成", parse_mode="MarkdownV2")


@bot.message_handler(commands=['ascii2d'],func=lambda message: message.chat.type == "private")
def send_ascii2d(message):
    bot.send_message(chat_id=message.chat.id, text="请发送图片,或输入 /cancel 取消",parse_mode="MarkdownV2")
    bot.register_next_step_handler(message, get_ascii2d)

def get_ascii2d(message):
    print(message)
    if message.text=="/cancel":
        bot.send_message(chat_id=message.chat.id, text="已退出搜图模式", parse_mode="MarkdownV2")
        return
    if message.content_type!="photo":
        bot.send_message(chat_id=message.chat.id, text="请发送图片,或输入 /cancel 取消",parse_mode="MarkdownV2")

        bot.register_next_step_handler(message, get_ascii2d)
        return
    else:
        url = bot.get_file_url(message.photo[-1].file_id)
        print(url)
        ascii2d(url, message.chat.id)
        bot.send_message(chat_id=message.chat.id, text="搜索完成", parse_mode="MarkdownV2")

@bot.message_handler(commands=['anime'],func=lambda message: message.chat.type == "private")
def send_anime(message):
    bot.send_message(chat_id=message.chat.id, text="请发送图片,或输入 /cancel 取消",parse_mode="MarkdownV2")
    bot.register_next_step_handler(message, get_anime)

def get_anime(message):
    print(message)
    if message.text=="/cancel":
        bot.send_message(chat_id=message.chat.id, text="已退出搜图模式", parse_mode="MarkdownV2")
        return
    if message.content_type!="photo":
        bot.send_message(chat_id=message.chat.id, text="请发送图片,或输入 /cancel 取消",parse_mode="MarkdownV2")

        bot.register_next_step_handler(message, get_anime)
        return
    else:
        url = bot.get_file_url(message.photo[-1].file_id)
        print(url)
        anime(url, message.chat.id)
        bot.send_message(chat_id=message.chat.id, text="搜索完成", parse_mode="MarkdownV2")

@bot.message_handler(commands=['iqdb'],func=lambda message: message.chat.type == "private")
def send_iqdb(message):
    bot.send_message(chat_id=message.chat.id, text="请发送图片,或输入 /cancel 取消",parse_mode="MarkdownV2")
    bot.register_next_step_handler(message, get_iqdb)

def get_iqdb(message):
    print(message)
    if message.text=="/cancel":
        bot.send_message(chat_id=message.chat.id, text="已退出搜图模式", parse_mode="MarkdownV2")
        return
    if message.content_type!="photo":
        bot.send_message(chat_id=message.chat.id, text="请发送图片,或输入 /cancel 取消",parse_mode="MarkdownV2")

        bot.register_next_step_handler(message, get_ascii2d)
        return
    else:
        url = bot.get_file_url(message.photo[-1].file_id)
        print(url)
        iqdb(url, message.chat.id)
        bot.send_message(chat_id=message.chat.id, text="搜索完成", parse_mode="MarkdownV2")

@bot.message_handler(commands=['all'],func=lambda message: message.text==f"/all{bot_name}" and ( message.chat.type == "group" or message.chat.type == "supergroup" ))
def send_all_group(message):
    bot.send_message(chat_id=message.chat.id, text="此模式仅支持私聊",parse_mode="MarkdownV2")

@bot.message_handler(commands=['all'],func=lambda message: message.chat.type == "private")
def send_all(message):
    bot.send_message(chat_id=message.chat.id, text="请发送图片,或输入 /cancel 取消",parse_mode="MarkdownV2")
    bot.register_next_step_handler(message, get_all)

def get_all(message):
    print(message)
    if message.text=="/cancel":
        bot.send_message(chat_id=message.chat.id, text="已退出搜图模式", parse_mode="MarkdownV2")
        return
    if message.content_type!="photo":
        bot.send_message(chat_id=message.chat.id, text="请发送图片,或输入 /cancel 取消",parse_mode="MarkdownV2")

        bot.register_next_step_handler(message, get_ascii2d)
        return
    else:
        url = bot.get_file_url(message.photo[-1].file_id)
        print(url)
        saucenao(url, message.chat.id)
        ascii2d(url, message.chat.id)
        anime(url, message.chat.id)
        iqdb(url, message.chat.id)
        bot.send_message(chat_id=message.chat.id, text="搜索完成", parse_mode="MarkdownV2")

def saucenao(photo_url,chat_id):
    try:
        url="https://saucenao.com/search.php"
        #url = "https://saucenao.com"
        Header = {
            'Host': 'saucenao.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0',
             'Accept': 'text / html, application / xhtml + xml, application / xml;q = 0.9, * / *;q = 0.8',
            'Accept - Language': 'zh - CN, zh;q = 0.8, zh - TW;q = 0.7, zh - HK;q = 0.5, en - US;q = 0.3, en;q = 0.2',
             'Accept - Encoding': 'gzip, deflate, br',
            'Connection': 'keep - alive',

        }
        payloaddata = {

            'frame': 1,
            'hide': 0,
            'database': 999,
        }
        #files = {"file": "file": ('saber.jpg', open("saber.jpg", "rb", , "image/png")}
        photo_file=requests.get(photo_url)
        files = {"file": (
        "saucenao.jpg", photo_file.content, "image/png")}
        bot.send_message(chat_id=chat_id,text="正在搜索saucenao")
        r = session.post(url=url, headers=Header, data=payloaddata,files=files)
        #r = session .get(url=url,headers=Header)
        soup = BeautifulSoup(r.text, 'html.parser')
        #print(soup.prettify())
        result=0
        choice=0
        for img in soup.find_all('div', attrs={'class': 'result'}):  # 找到class="wrap"的div里面的所有<img>标签
            #print(img)
            if('hidden' in str(img['class']))==False:
                try:
                    name=img.find("div",attrs={'class': 'resulttitle'}).get_text()
                    img_url=str(img.img['src'])
                    describe_list=img.find("div",attrs={'class': 'resultcontentcolumn'})
                    url_list = img.find("div", attrs={'class': 'resultcontentcolumn'}).find_all("a",  attrs={'class': 'linkify'})
                    similarity = str(img.find("div", attrs={'class': 'resultsimilarityinfo'}).get_text())
                    print(name)
                except:
                    continue
                try:
                    describe = str(url_list[0].previous_sibling.string)
                    describe_id = str(url_list[0].string)
                    describe_url = str(url_list[0]['href'])
                    auther_url = str(url_list[1]['href'])
                    auther = str(url_list[1].previous_sibling.string)
                    auther_id = str(url_list[1].string)
                    '''print(name)
                    print(img_url)
                    print(describe)
                    print(describe_id)
                    print(similarity)
                    print(auther)
                    print(auther_id)
                    print(describe_url)'''
                    text = f"{name}\n{describe}[{describe_id}]({describe_url})\n{auther}:[{auther_id}]({auther_url})\n相似度{similarity}"
                except:
                    '''print(describe_list.get_text())
                    print(describe_list.strong.string)
                    print(describe_list.strong.next_sibling.string)
                    print(describe_list.small.string)
                    print(describe_list.small.next_sibling.next_sibling.string)'''
                    auther = str(describe_list.strong.string)
                    auther_id = str(describe_list.strong.next_sibling.string)
                    describe = str(describe_list.small.string) + "\n" + str(describe_list.small.next_sibling.next_sibling.string)
                    text = f"{name}\n{auther}:{auther_id}\n{describe}\n相似度{similarity}"

                photo_file = session.get(img_url)
                bot.send_photo(chat_id=chat_id,photo=photo_file.content,parse_mode='Markdown',caption=text)


                result=1
        if result==0:
            bot.send_message(chat_id=chat_id, text="saucenao无结果")
    except:
        print("saucenao")

def ascii2d(photo_url,chat_id):
    try:
        url = "https://ascii2d.net/"
        # url = "https://saucenao.com"
        Header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0',
        }
        html = session.get(url, headers=Header)
        print(html)
        authenticity_token = re.findall("<input type=\"hidden\" name=\"authenticity_token\" value=\"(.*?)\" />", html.text, re.S)[0]
        payloaddata = {

            'authenticity_token': authenticity_token,
            'utf8': "✓",
        }
        # files = {"file": "file": ('saber.jpg', open("saber.jpg", "rb", , "image/png")}
        bot.send_message(chat_id=chat_id, text="正在搜索ascii2d")
        photo_file = requests.get(photo_url)
        files = {"file": (
            "saucenao.jpg", photo_file.content, "image/png")}
        url = "https://ascii2d.net/search/multi"
        r = session.post(url=url, headers=Header, data=payloaddata, files=files)
        soup = BeautifulSoup(r.text, 'html.parser')
        # print(soup.prettify())
        pan = 0
        for img in soup.find_all('div', attrs={'class': 'row item-box'}):  # 找到class="wrap"的div里面的所有<img>标签
            # print(img)
            if pan != 0:
                img_url = "https://ascii2d.net" + str(img.img['src'])
                the_list = img.find_all('a')
                title = str(the_list[0].get_text())
                title_url = str(the_list[0]["href"])
                auther = str(the_list[1].get_text())
                auther_url = str(the_list[1]["href"])

                photo_file = session.get(img_url)
                text=f"titile:[{title}]({title_url})\nauther:[{auther}]({auther_url})"
                bot.send_photo(chat_id=chat_id, caption=text, parse_mode='Markdown',photo=photo_file.content)
            pan = pan + 1
            if pan == 3:
                break
    except:
        print("ascii2d faild")


def anime(photo_url,chat_id):
    try:
        url = "https://trace.moe/api/search"
        # url = "https://saucenao.com"
        photo_file = requests.get(photo_url)
        ls_f = base64.b64encode(photo_file.content)

        data = {
            "image": ls_f,
        }
        # files = {"file": "file": ('saber.jpg', open("saber.jpg", "rb", , "image/png")}

        r = session.post(url=url, data=data)
        # r = session .get(url=url,headers=Header)
        bot.send_message(chat_id=chat_id,text="正在搜索 trace.moe")
        information = r.json()
        anilist_id = information['docs'][0]["anilist_id"]
        filename = information['docs'][0]['filename']
        tokenthumb = information['docs'][0]['tokenthumb']
        at = information['docs'][0]['at']
        limit = information['limit']  # 剩余搜索次数
        limit_ttl = information['limit_ttl']  # 剩余重置时间
        title = information['docs'][0]['title_chinese']
        episode = information['docs'][0]['episode']
        quota = information['quota']
        quota_ttl = information['quota_ttl']
        similarity=information['docs'][0]['similarity']
        similarity_num="%.2f%%" % (similarity * 100)
        img_url = f"https://trace.moe/thumbnail.php?anilist_id={anilist_id}&file={parse.quote(filename)}&t={at}&token={tokenthumb}"
        print(img_url)
        video_url = f"https://trace.moe/preview.php?anilist_id={anilist_id}&file={parse.quote(filename)}&t={at}&token={tokenthumb}"
        print(video_url)
        video = f"https://media.trace.moe/video/{anilist_id}/{parse.quote(filename)}?t={at}&token={tokenthumb}"
        print(video)
        more_url = f"https://anilist.co/anime/{anilist_id}"
        text = f"{similarity_num}\nTitle:{title}\n集数:{episode}\n时间：{datetime.timedelta(seconds=int(at))}\n来源：{filename}\n[更多信息]({more_url})\n分钟剩余搜索次数:{limit}\n分钟剩余次数重置时间:{limit_ttl}s\n24小时剩余搜索次数:{quota}\n24小时剩余次数重置时间:{datetime.timedelta(seconds=int(quota_ttl))}"
        print(text)
        photo_file = session.get(img_url)
        bot.send_photo(chat_id=chat_id, photo=photo_file.content, parse_mode='Markdown', caption=text)
        photo_file = session.get(video)
        bot.send_video(chat_id=chat_id,data=photo_file.content)
    except:
        print("anime faild")

def iqdb(photo_url,chat_id):
    try:
        bot.send_message(chat_id=chat_id, text="正在搜索 iqdb", parse_mode="MarkdownV2")
        url = "http://iqdb.org/"
        # url = "https://saucenao.com"
        photo_file = requests.get(photo_url)
        files = {"file": (
            "iqdb.jpg", photo_file.content, "image/png")}
        # files = {"file": "file": ('saber.jpg', open("saber.jpg", "rb", , "image/png")}

        r = requests.post(url=url, files=files)
        #print(r.text)
        soup = BeautifulSoup(r.text, 'html.parser')
        a=1
        for img in soup.find_all('td', attrs={'class': 'image'}):  # 找到class="wrap"的div里面的所有<img>标签
            #print(img)
            if a==7:
                break
            try:
                #print(img.a.get('href'))
                img_html=img.a.get('href')
                if "http:" not in img_html and "https:" not in img_html:

                    img_html="https:"+img_html

                img_url="http://iqdb.org"+img.img.get('src')

                text=f"[图片详情]({img_html})"
                photo_file = session.get(img_url)
                bot.send_photo(chat_id=chat_id, photo=photo_file.content, parse_mode='Markdown', caption=text)
                a=a+1
            except:
                None
    except:
        None


if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            log = open('log.txt', 'a')
            log.writelines("Qualcosa è andato storto con la connessione agli API Telegram: {}\n".format(e))
            log.close()
            time.sleep(30)
