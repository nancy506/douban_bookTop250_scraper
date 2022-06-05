#ref:https://zhuanlan.zhihu.com/p/231532655
import requests
from bs4 import BeautifulSoup
import time
import pandas as pd

# 定义函数，用于获取豆瓣top250每一个页面的网址
def get_urls(n):
    '''
    n:页面数量
    '''
    urls = []   # 列表用于存放网址
    num = (n-1)*25+1
    for i in range(0, num, 25):
        url = 'https://book.douban.com/top250?start={}&filter='.format(i)
        urls.append(url)
    return urls

# 定义函数，用来处理User-Agent和Cookie
def ua_ck():
    '''
    网站需要登录才能采集，需要从Network--Doc里复制User-Agent和Cookie，Cookie要转化为字典，否则会采集失败！！！！！
    '''

    user_agent = {
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36'}
    
    cookies = 'bid=0j9QQ73f1Qw; douban-fav-remind=1; __utma=30149280.919969233.1633157285.1633157285.1633157285.1; __utmc=30149280; __utmz=30149280.1633157285.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); ll="108258"; dbcl2="161210208:hjyg/Lte92o"; ck=SyLN; push_noty_num=0; ap_v=0,6.0; push_doumail_num=0'
    cookies = 'bid=0j9QQ73f1Qw; douban-fav-remind=1; __utma=30149280.919969233.1633157285.1633157285.1633157285.1; __utmc=30149280; __utmz=30149280.1633157285.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); ll="108258"; dbcl2="161210208:hjyg/Lte92o"; ck=SyLN; push_noty_num=0; ap_v=0,6.0; push_doumail_num=0'
    # Cookie转化为字典
    cookies = cookies.split('; ')
    cookies_dict = {}
    for i in cookies:
        cookies_dict[i.split('=')[0]] = i.split('=')[1]

    return user_agent, cookies_dict

# 定义函数，获取每一部书的详细信息
def get_info(href, u_a, c_d):
    '''
    href：每一部书的链接
    u_a：User-Agent
    c_d：cookies
    '''

    html = requests.get(href,
                        headers=u_a,
                        cookies=c_d,
                        timeout=10)
    soup = BeautifulSoup(html.text, 'html.parser')  # 用 html.parser 来解析网页
    #print (soup.prettify())
    items = soup.find('div', id='content').find('div', class_='indent').find_all('table')
    #items = soup.find('table')#('tr', class_ ='item')
    #.find_all('item')
    book_titles = []  # 新建字典，存放书信息
    book_subs=[]

    # 名
    for item in items:
        title = item.find('div', class_='pl2').find('a')['title']
        sub = item.find('div', class_='pl2').find('a').find('span')
        if sub is None:
            translation = item.find('div', class_='pl2').find('span')
        else:
            translation = item.find('div', class_='pl2').find('a').find_next_sibling('span')
        #if 'style' not in translation:
            #translation = None
        #print (translation)
        if translation is not None:
            title = translation.text

        #print (title)

        #if len(original)==1:
        #     title = original[0]
        # else:
        #     title = original[1]
        book_titles.append(title)
        if sub is None:
            book_subs.append('')
        else:
            book_subs.append(sub.text)
    #print (book_titles)

    return book_titles, book_subs

#scrape book info
def scrape_book(u_a, c_d):
    '''
    n:页面数量
    '''
    n = 10  # 总共有10个页面
    print('开始采集数据，预计耗时5分钟')

    # 获取豆瓣top250每一页的链接，共10页
    urls = get_urls(n)
    print('豆瓣10个网页链接已生成！！')

    # 获取每一部书的详细信息
    top250_book = []  # 储存每部书的信息
    subs = []
    error_href = []  #

    for href in urls:
        try:
            book, sub = get_info(href, u_a, c_d)
            top250_book.append(book)
            subs.append(sub)

        except:
            error_href.append(href)
            print('采集失败，失败网址是{}'.format(href))        
        time.sleep(0.4)    # 设置时间间隔，0.4秒采集一次，避免频繁登录网页

    print('书详细信息采集完成！！总共采集{}条数据'.format(len(top250_book)))

    df = pd.DataFrame(columns = ['booktitle', 'subtitles']) 
    for book, sub in zip(top250_book, subs):
        df = pd.concat([df, pd.DataFrame({'booktitle': book, 'subtitles': sub})], ignore_index=True)
    print (df)
    df.to_csv('titles.csv')
    return top250_book, error_href

#get html
def get_html(href, u_a, c_d):
    '''
    href：链接
    u_a：User-Agent
    c_d：cookies
    '''
    links =[]
    html = requests.get(href,
                        headers=u_a,
                        cookies=c_d,
                        timeout=10)

    soup = BeautifulSoup(html.text, 'html.parser')  # 用 html.parser 来解析网页
    #print (soup.prettify())
    for link in soup.findAll('a'):
        if link.has_attr('href'):
            links.append(link['href'])

    return soup, links

def scrape_single_page(url, u_a, c_d, num_layer, num_page=0):
    if num_layer < 0:
        return
    error_hrefs = []


    try:
        soup, links = get_html(url, u_a, c_d)
        print (soup.title.string.strip())
        filename =  soup.title.string + str(num_layer) + '_'+ str(num_page) + '.html'
        print (filename)
        with open(filename, "w") as file:
                file.write(str(soup))
    except:
        print('采集失败，失败网址是{}'.format(url))  
        error_hrefs.append(url) 

    num_layer = num_layer -1    
    for link in links: 
        num_page = num_page + 1
        scrape_single_page(link, u_a, c_d, num_layer, num_page)
        time.sleep(1)    # 设置时间间隔，1秒采集一次，避免频繁登录网页

    return error_hrefs

# 设置主函数，运行上面设置好的函数
def main():
    '''
    u_a：User-Agent
    c_d：cookies
    '''

    # 处理User-Agent和Cookie
    login = ua_ck()
    u_a = login[0]
    c_d = login[1]

    #url
    url = 'https://www.douban.com/people/161210208/'

    #layer of recursive to go
    num_layer = 1
    #re = scrape_book(u_a, c_d)
    ans = scrape_single_page(url, u_a, c_d, num_layer)
    print (ans)
    return

if __name__ == "__main__":
    # execute only if run as a script
    main()
