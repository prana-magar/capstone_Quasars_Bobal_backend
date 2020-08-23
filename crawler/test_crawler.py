from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()
import time

def login():

    driver.implicitly_wait(3)
    email = driver.find_element_by_xpath('//*[@id="root"]/div/main/div[2]/div[1]/form/input[1]')
    email.clear()
    email.send_keys("prakashrana9847067614@gmail.com")



    password = driver.find_element_by_xpath('//*[@id="root"]/div/main/div[2]/div[1]/form/input[2]')
    password.clear()
    password.send_keys("Fifapesoccer2010")

    driver.implicitly_wait(3)

    submit = driver.find_element_by_id("submit-login")
    submit.click()


# login()
driver.implicitly_wait(3)


driver.get("https://gre.economist.com/gre-vocabulary")



def get_source_data(detail_link):

    # login()

    driver.implicitly_wait(3)

    word_dict = {}
    driver.get(detail_link)

    detail_view_link = driver.find_element_by_xpath('/html/body/div[3]/article/div[3]/div[2]/a')
    detail_view_link_text  = detail_view_link.get_attribute("href")
    print(detail_view_link_text)

    driver.get(detail_view_link_text)
    driver.implicitly_wait(3)


    login_spans = driver.find_elements_by_xpath("//*[contains(text(),'Log in')]")

    while(len(login_spans) != 0):

            login_spans[0].click()
            driver.implicitly_wait(3)

            login()
            driver.implicitly_wait(7)

            time.sleep(7)
            # driver.get(detail_view_link_text)
            # driver.implicitly_wait(5000)
            login_spans = driver.find_elements_by_xpath("//*[contains(text(),'Log in')]")

    title = driver.find_element_by_class_name("article__headline").get_attribute("innerHTML")
    print(title)

    word_dict["title"] = title

    description = driver.find_element_by_class_name("article__description").get_attribute("innerHTML")

    word_dict["description"] = description

    word_dict["body"] = ""
    article_body_texts = driver.find_elements_by_class_name("article__body-text")

    try:
        for text_block in article_body_texts:
            word_dict["body"] += " " + text_block.get_attribute("innerHTML")
    except:
        login_spans = driver.find_elements_by_xpath("//*[contains(text(),'Log in')]")
        login_spans[0].click()
        driver.implicitly_wait(3)

        login()
        driver.implicitly_wait(3)

        word_dict["body"] = ""
        article_body_texts = driver.find_elements_by_class_name("article__body-text")
        for text_block in article_body_texts:
            word_dict["body"] += " " + text_block.get_attribute("innerHTML")

    return word_dict

word_dict_list = []

teaser_elements = driver.find_elements_by_class_name("gre-vocabulary-teaser")
count = 0
for ele in teaser_elements:

    word_dict = {}

    word_div = ele.find_element_by_class_name("gre-vocabulary-teaser-word")
    anchor = word_div.find_element_by_tag_name('a')
    print(anchor.get_attribute("text"))
    word_dict['word'] = anchor.get_attribute("text")


    link_anchor= ele.find_element_by_class_name("gre-vocabulary-teaser-view-link")
    print(link_anchor.get_attribute("href"))

    word_dict['detail_link'] = link_anchor.get_attribute("href")
    word_dict_list.append(word_dict)
    count += 1
    if count > 10:
        break


for word_dict in word_dict_list:
    extra_info = get_source_data(word_dict['detail_link'])
    word_dict.update(extra_info)



driver.implicitly_wait(3)
driver.close()