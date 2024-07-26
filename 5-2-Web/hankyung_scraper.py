from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
from datetime import datetime, timedelta, date
import json
import requests

class HanKyungScraper:
    def __init__(self, start_date: str, end_date: str, output: str = ""):
        self.start_date = start_date
        self.end_date = end_date
        self.output = output
        self.driver = self._init_driver()
        self.results: list[dict[str, str]] = []

    def _init_driver(self) -> webdriver.Chrome:
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)
        chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
        service = Service()
        driver = webdriver.Chrome(service=service, options=chrome_options)
        return driver

    def _load_more_pages(self, previous_date_str: str) -> None:
        while True:
            try:
                more_btn = self.driver.find_elements(By.CSS_SELECTOR, ".btn-more")
                for btn in more_btn:
                    if btn.text == "더보기":
                        btn.click()
                        time.sleep(2)

                date_elements = self.driver.find_elements(By.CSS_SELECTOR, ".txt-date")
                for date_element in date_elements:
                    if date_element.text != "":
                        formatted_date = datetime.strptime(date_element.text, "%Y.%m.%d").strftime("%Y%m%d")
                        if formatted_date == previous_date_str:
                            return

            except Exception as e:
                print(f"에러가 발생했습니다: {str(e)}\n계속 진행합니다.")

    def _scrape_articles(self) -> list[dict[str, str]]:
        elements = self.driver.find_elements(By.CSS_SELECTOR, ".news-tit a")
        new_articles: list[dict[str, str]] = []
        titles_set: set[str] = set(article['title'] for article in self.results)

        if elements:
            for element in elements:
                if element.text != "" and element.text not in titles_set:
                    href = element.get_attribute("href") or ""  # None일 경우 빈 문자열로 처리
                    title = element.text
                    new_articles.append({
                        "title": title,
                        "href": href
                    })
                    titles_set.add(title)
        return new_articles

    def _process_article(self, article: dict[str, str], previous_date_str: str, end_date_obj: date) -> bool:
        try:
            response = requests.get(article["href"])
            response.raise_for_status()
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')

            date_list = soup.select(".txt-date")
            if len(date_list) < 2:
                raise ValueError("날짜 정보가 충분하지 않습니다.\n계속 진행합니다.")

            date = date_list[0].text
            formatted_date = datetime.strptime(date, "%Y.%m.%d %H:%M").strftime("%Y%m%d")
            formatted_date2 = datetime.strptime(date, "%Y.%m.%d %H:%M").date()

            if formatted_date2 > end_date_obj:
                print(f"{formatted_date2}가 {end_date_obj}를 초과합니다.")
                return True

            date_edit = date_list[1].text if len(date_list) > 1 else ""

            content = soup.select("#articletxt")
            if not content:
                raise ValueError("기사를 찾을 수 없습니다.\n계속 진행합니다.")

            article_text = content[0].get_text(separator="\n", strip=True)
            href = article["href"]
            title = article["title"]
            
            if previous_date_str == formatted_date:
                return False

            self.results.append({
                "date": date,
                "date_edit": date_edit,
                "href": href,
                "title": title,
                "content": article_text
            })
            print(f"{date} 기사까지 스크랩 완료!")
            
            return True
        
        except Exception as e:
            print(f"에러가 발생했습니다. URL: {article['href']}, 에러: {str(e)}\n계속 진행합니다.")
            return True

    def scrape(self) -> None:
        self.driver.get("https://www.hankyung.com/all-news")
        self.driver.implicitly_wait(5)
        self.driver.maximize_window()

        elements = self.driver.find_elements(By.CSS_SELECTOR, ".nav-link")
        economi = elements[14]
        economi.click()

        time.sleep(5)  # 페이지 로드 대기

        start_date_obj = datetime.strptime(self.start_date, "%Y%m%d")
        end_date_obj = datetime.strptime(self.end_date, "%Y%m%d").date()
        previous_date_obj = start_date_obj - timedelta(days=1)
        previous_date_str = previous_date_obj.strftime("%Y%m%d")

        try:
            self._load_more_pages(previous_date_str)
            new_articles = self._scrape_articles()

            for article in new_articles:
                if not self._process_article(article, previous_date_str, end_date_obj):
                    break

        except Exception as e:
            print(f"에러가 발생했습니다: {str(e)}\n계속 진행합니다.")
        finally:
            self._save_results()

    def _save_results(self) -> None:
        output_path = self.output if self.output else "result.json"
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(self.results, f, ensure_ascii=False, indent=4)
        print("기사 데이터를 JSON 파일로 저장했습니다.")

    def __del__(self):
        try:
            self.driver.quit()
        except Exception as e:
            print(f"에러가 발생했습니다: {str(e)}")