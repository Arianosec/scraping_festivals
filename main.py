import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains


def get_data():
    options = webdriver.ChromeOptions()
    options.add_argument("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36")
    driver = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))
    try:
        result = []
        while True:

            page=1
            driver.get(url=f"https://festagent.com/ru/festivals?page={page}")
            if "Таких фестивалей в каталоге нет. Попробуйте изменить условия поиска." in driver.find_element(By.TAG_NAME,"body").text:
                break
            page+=1
            driver.maximize_window()
            fest = driver.find_elements(By.CLASS_NAME,"title-link")
            urls = []
            for l in fest:
                url1= l.find_element(By.TAG_NAME,'a').get_attribute('href')
                urls.append(url1)

            time.sleep(5)
            for item in urls:
                driver.get(url=item)
                time.sleep(5)
                title = driver.find_element(By.CLASS_NAME, "festival-name").text.replace("\n", "")
                short = driver.find_element(By.CLASS_NAME,"short-description").text.strip().replace("\n", "")
                siite = driver.find_element(By.CLASS_NAME,"website").text.strip().replace("\n", "")
                email = driver.find_element(By.CLASS_NAME,"contacts").text.strip().replace("\n", "")
                country = driver.find_element(By.XPATH,'//div[contains(@class,"col-sm-pull-8")]/p[4]').text.strip().replace("\n", ", ")
                driver.back()
                time.sleep(5)

                result.append({
                    "Название": title,
                    "Короткое описание":short,
                    "Сайт": siite,
                    "Контакты":email,
                    "Страна":country

                })

                with open("result.json","a",encoding="utf-8") as file:
                    json.dump(result,file,indent=4,ensure_ascii=False)


    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()


def main():
    get_data()


if __name__ == "__main__":
    main()