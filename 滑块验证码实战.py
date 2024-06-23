from random import random
import random
import time
import cv2
from selenium import webdriver
import base64
import io
from PIL import Image
from selenium.webdriver.chrome.options import Options
# chrome_options = Options()
# chrome_options.add_argument('--headless')
# chrome_options.add_argument('--disable-gpu')
# driver = webdriver.Chrome(executable_path=path,options=chrome_options)


path = 'C:\\Users\\86198\\PycharmProjects\\pythonProject\\chromedriver.exe'

def var():
    global message
    message = []


def web():
    global driver
    driver = webdriver.Chrome(path)
    driver.maximize_window()
    driver.implicitly_wait(10)
    driver.get('https://passport.jd.com/new/login.aspx')
    time.sleep(1)


def login():
    driver.find_element_by_xpath('//*[@id="loginname"]').send_keys('114514aaa')
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="nloginpwd"]').send_keys('114514aaa')
    time.sleep(1)
    button = driver.find_element_by_xpath('//*[@id="loginsubmit"]')
    button.click()
    time.sleep(2)
    if driver.current_url == 'https://www.jd.com/':
        a = '登陆成功'
        message.append(a)
    else:
        code_download()


def code_download():
    global target, template
    target = driver.find_element_by_xpath('//*[@id="JDJRV-wrap-loginsubmit"]/div/div/div/div[1]/div[2]/div[1]/img')
    base64_string = str(target.get_attribute("src")).split("base64,")[1]
    image_data = base64.b64decode(base64_string)
    image = Image.open(io.BytesIO(image_data))
    image.save("target.png")

    template = driver.find_element_by_xpath('//*[@id="JDJRV-wrap-loginsubmit"]/div/div/div/div[1]/div[2]/div[2]/img')
    base64_string = str(template.get_attribute("src")).split("base64,")[1]
    image_data = base64.b64decode(base64_string)
    image = Image.open(io.BytesIO(image_data))
    image.save("template.png")
    time.sleep(2)
    move()


def FinPic(target='target.png', template="template.png"):
    target_rgb = cv2.imread(target)
    target_gray = cv2.cvtColor(target_rgb, cv2.COLOR_BGR2GRAY)
    template_rgb = cv2.imread(template, 0)
    res = cv2.matchTemplate(target_gray, template_rgb, cv2.TM_CCOEFF_NORMED)
    value = cv2.minMaxLoc(res)
    return value[2][0]


def move():
    x = FinPic()
    img = cv2.imread('target.png')
    w1 = img.shape[1]
    w2 = target.size['width']
    x = x * w2 / w1
    x = int(x + 9.3 - 1)
    x1 = int(x * 2 / 3)
    x2 = x - x1

    def move2():
        def generate_list():
            while True:
                lst = random.sample(range(1, 10), random.randint(2, 4))
                if sum(lst) == 5:
                    return lst

        action = webdriver.ActionChains(driver)
        action.click_and_hold(template).perform()
        action.move_by_offset(x1, 0).pause(0.5)
        action.move_by_offset(x2, 0).pause(0.8)
        time.sleep(random.uniform(0.5, 0.8))

        for x in generate_list():
            action.move_by_offset(- x, x).perform()
            time.sleep(random.uniform(0.1, 0.3))

        action.release().perform()
        time.sleep(2)

    move2()

    if driver.current_url != 'https://passport.jd.com/new/login.aspx':
        b = '登陆成功'
        print(b)
        message.append(b)
    else:
        time.sleep(3)
        driver.refresh()
        login()


def choose_good(good_name):
    goods = good_name
    driver.find_element_by_xpath('//*[@id="key"]').send_keys(goods)
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="search"]/div/div[2]/button').click()
    driver.implicitly_wait(10)


def load_content():
    for i in range(4):
        js_bottom = f'document.documentElement.scrollTop={i}000'
        driver.execute_script(js_bottom)
        time.sleep(1)

    try:
        while driver.find_element_by_xpath('/html/body/div[5]/div[2]/div[2]/div[1]/div/div[3]/span/a'):
            driver.find_element_by_xpath('/html/body/div[5]/div[2]/div[2]/div[1]/div/div[3]/span/a').click()
            c = '检测到懒加载，需要重新加载图片数据'
            print(c)
            message.append(c)
            driver.implicitly_wait(10)

    except:
        d = '已加载完全'
        print(d)
        message.append(d)

    for i in range(4, 7):
        js_bottom = f'document.documentElement.scrollTop={i}000'
        driver.execute_script(js_bottom)
        time.sleep(1)


def w_file():
    price_elements = driver.find_elements_by_xpath('//*[@id="J_goodsList"]/ul//div/div[@class="p-price"]')
    name_elements = driver.find_elements_by_xpath('//*[@id="J_goodsList"]/ul//div/div[@class="p-name p-name-type-2"]')
    comment_elements = driver.find_elements_by_xpath('//*[@id="J_goodsList"]/ul//div/div[@class="p-commit"]')
    with open('./京东手机数据.txt', 'a', encoding='utf-8') as fp:
        for i in range(len(price_elements)):
            name = name_elements[i].text
            name = name.replace('\n', ' ')
            price = price_elements[i].text
            price = price.replace('￥', '')
            comment = comment_elements[i].text
            comment = comment.replace('万', '0000')
            comment = comment.replace('千', '000')
            comment = comment.replace('+', '')
            comment = comment.replace('条评价', '')
            data = price + '\t\t\t\t' + comment + '\t\t\t\t\t' + name + '\n'
            fp.write(data)


def page():
    time.sleep(5)
    ver_url = ('https://cfe.m.jd.com/privatedomain/risk_handler/03101900/?returnurl=https%3A%2F%2Fsearch.jd.com%'
               '2FSearch%3Fkeyword%3D%25E4%25B9%25A6%25E5%258C%2585%26enc%3Dutf-8%26wq%3D%25E4%25B9%25A6%25E5%25'
               '8C%2585%26pvid%3D2d4af71d53564d3d814a9301a702dead%26isList%3D0%26page%3D13%26s%3D356%26click%3D0'
               '&rqhost=https%3A%2F%2Fapi.m.jd.com&rpid=rp-188591562-10274-1711034148774&evtype=2&evapi=color_pc'
               '_search_batch_stock&source=1&forceCurrentView=1')
    current_url = driver.current_url
    max_page = driver.find_element_by_xpath('//*[@id="J_bottomPage"]/span[2]/em[1]/b').text
    e = f"当前商品页数尾页为：{max_page}"
    print(e)
    message.append(e)
    with open('./京东手机数据.txt', 'w') as file:
        pass
    for i in range(3):
        if i > 0:
            url = current_url + f'&isList=0&page={1 + 2 * i}&s={56 + (i - 1) * 60}&click=0'
            driver.get(url)
            driver.implicitly_wait(10)
            if driver.current_url == ver_url:
                f = '出现检查界面,结束数据爬取。'
                print(f)
                message.append(f)
                break
            g = f"当前加载进度为{i / 12}"
            print(g)
            message.append(g)
        load_content()
        driver.implicitly_wait(10)
        w_file()
    h = '文件运行结束，请检查文本内容。'
    print(h)
    message.append(h)


def startup(good_name):
        var()
        web()
        login()
        choose_good(good_name)
        page()
        return message

def end():
    driver.quit()

if __name__ == '__main__':
    var()
    web()
    login()
    choose_good('水杯')
    page()

