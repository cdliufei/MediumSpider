# This is a sample Python script.
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import pycurl
import json
import re
from io import BytesIO
from time import sleep
def build_req(start):
    # 将本地的body.json文件中的内容读出来
    if start == 0:
        return
    else:
        with open('body.json', 'r', encoding='utf-8') as f:
            str1 = f.read()
        # 将body.json中的内容转换为json格式
        json_data = json.loads(str1)
        variables = json_data['variables']["paging"]
        # 修改variables中的,from从0开始，limit为25,即每页显示25条数据
        variables['from'] = str(start)
        variables['to'] = str(start + 25)
        # 将修改后的variables重新赋值给json_data中的variables
        json_data['variables']["paging"] = variables
        # 将json_data转换为字符串
        str1 = json.dumps(json_data)
        # 将修改后的字符串写入到body.json中
        with open('body.json', 'w', encoding='utf-8') as f:
            f.write(str1)


def get_claps():
    # 循环，从0开始，每次加25，直到获取到87000条数据
    for i in range(0, 88000, 25):
        # 调用build_req方法，修改body.json中的variables
        # sleep 1000ms
        sleep(1)
        print(f'Hi, 开始构建请求,开始位置为:{i}')
        build_req(i)
        print(f'Hi, 构建请求结束')
        # 调用curl方法，将修改后的body.json中的内容post到https://medium.com/_/graphql
        print(f'Hi, 开始请求数据')
        getTop10Pages()
        print(f'Hi, 请求数据结束')

def getTop10Pages():
    # Use a breakpoint in the code line below to debug your script.
    # 编写一个网络爬虫，抓取Medium上的文章，按照Claps数排序，取前10篇文章
    c = pycurl.Curl()
    c.setopt(pycurl.URL, 'https://medium.com/_/graphql')
    c.setopt(pycurl.HTTPHEADER, ['Accept:'])
    # 设置content_type为json
    c.setopt(pycurl.HTTPHEADER, ['Content-Type:application/json'])
    # 设置user_agent为chrome
    c.setopt(pycurl.USERAGENT, 'chrome')
    # 设置cookie
    c.setopt(pycurl.COOKIE,
             'nonce=T9gBnS4E; _gid=GA1.2.1967552318.1704459648; lightstep_guid/medium-web=7df35c06cb9fbee3; lightstep_session_id=2870c53ce5fc580b; sz=1208; pr=1; tz=-480; uid=5bbeb51517e5; sid=1:htiy1sqZbbQHd8joA75Y2Bh5L4ZY2a0beHjGgQzGEbS2oyZutUrUgQ6c8l/oJoxS; xsrf=Cx4lcE4MpVqsQ3RW; _ga=GA1.1.1014854283.1704459610; _ga_7JY7T788PK=GS1.1.1704510224.2.1.1704510241.0.0.0; dd_cookie_test_83eb4979-c032-4806-b245-5583f9269f04=test; _dd_s=rum=0&expire=1704511143548; dd_cookie_test_f8649df6-ea35-42e5-836b-4c925cd504fe=test')
    # curl采用post方式
    c.setopt(pycurl.POST, 1)

    buf = BytesIO()
    # 读取本地名为body.json的文件，将文件中的内容作为post的参数
    with open('body.json', 'r', encoding='utf-8') as f:
        str = f.read()
    c.setopt(pycurl.POSTFIELDS, str)
    # 将返回的内容写入到Buffer中
    c.setopt(pycurl.WRITEFUNCTION, buf.write)
    c.perform()
    response = buf.getvalue().decode('utf-8')

    # 将response转换为json格式
    json_data = json.loads(response)
    # 获取data下的personalisedTagFeed下的items下的post下的id,clapCount,uniqueSlug
    items = json_data['data']['personalisedTagFeed']['items']
    # 遍历items,获取id,clapCount,uniqueSlug
    for item in items:
        print(item['post']['id'], item['post']['clapCount'], item['post']['mediumUrl'])
        # 将id,clapCount,uniqueSlug传入tuple保存
        # 新建tuple，保存id,clapCount,uniqueSlug
        tuple = (item['post']['id'], item['post']['clapCount'], item['post']['mediumUrl'])
        sort(tuple)
    # 打印sortList
    print(sortList)
    # 将sortList转换为json格式
    sortList1 = json.dumps(sortList)
    # 将sortList中的数据写入到本地的top10.json文件中
    with open('top10.json', 'w', encoding='utf-8') as f:
        f.write(sortList1)


# 声明全局变量sortList,用于存放排序后的数据
sortList = []


def sort(tuple):
    # 声明sortList,用于存放排序后的数据，长度为10
    # 当sortList的长度小于10时，将数据添加到sortList中
    if len(sortList) < 10:
        sortList.append(tuple)
        # 将sortList按照tuple中tuple[1]大小排序
        sortList.sort(key=lambda x: x[1])
    else:
        # 将传入的数据与sortList中的最小值进行比较，如果大于最小值，则将最小值替换为传入的数据
        if tuple[1] > sortList[0][1]:
            print("find  bigger claps, remove the smallest one: ", sortList[0][1], "new add claps is:", tuple[1])
            # 遍历sortList，判断tuple[1]是否和已存在数据相同
            isEqual = False
            for i in range(0, len(sortList)):
                # 如果相同，则将sortList[i]替换为tuple
                if sortList[i][0] == tuple[0]:
                    isEqual = True
                    print(" equal ,ignore")
                    break
            # 如果不相同，则将sortList[0]替换为tuple
            if isEqual == False:
                print("not equal ,replace")
                sortList[0] = tuple
            # 将sortList按照clapCount排序
            sortList.sort(key=lambda x: x[1])


# TODO 需要完善
def openURL(tuple):
    mediumUrl = "https://medium.com/@kajol_singh/must-know-system-design-concepts-a-comprehensive-guide-2bdc0926cef1"
    # 打开medium.com的页面，抓取文章的标题、作者，如:https://medium.com/@kajol_singh/must-know-system-design-concepts-a-comprehensive-guide-2bdc0926cef1
    # 爬虫抓取网页html中body的内容
    c = pycurl.Curl()
    c.setopt(pycurl.URL, mediumUrl)
    c.setopt(pycurl.HTTPHEADER, ['Accept:'])
    # 设置content_type为html
    c.setopt(pycurl.HTTPHEADER, ['Content-Type:text/html'])
    # 设置user_agent为chrome
    c.setopt(pycurl.USERAGENT, 'chrome')
    # 设置cookie
    c.setopt(pycurl.COOKIE,
             'nonce=T9gBnS4E; _gid=GA1.2.1967552318.1704459648; lightstep_guid/medium-web=7df35c06cb9fbee3; lightstep_session_id=2870c53ce5fc580b; sz=1208; pr=1; tz=-480; uid=5bbeb51517e5; sid=1:htiy1sqZbbQHd8joA75Y2Bh5L4ZY2a0beHjGgQzGEbS2oyZutUrUgQ6c8l/oJoxS; xsrf=Cx4lcE4MpVqsQ3RW; _ga=GA1.1.1014854283.1704459610; _ga_7JY7T788PK=GS1.1.1704510224.2.1.1704510241.0.0.0; dd_cookie_test_83eb4979-c032-4806-b245-5583f9269f04=test; _dd_s=rum=0&expire=1704511143548; dd_cookie_test_f8649df6-ea35-42e5-836b-4c925cd504fe=test')
    # curl采用get方式
    c.setopt(pycurl.HTTPGET, 1)
    buf = BytesIO()
    # 将返回的内容写入到Buffer中
    c.setopt(pycurl.WRITEFUNCTION, buf.write)
    c.perform()
    response = buf.getvalue().decode('utf-8')
    # 匹配出html标签<body></body>的内容
    pattern = re.compile(r'<body>(.*?)</body>', re.S)
    # 去除html中的<script>当中的内容
    print(pattern.findall(response))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # print_hi('PyCharm')
    get_claps()
    # openURL("")
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
