from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By # 추가
from selenium.webdriver.support.ui import WebDriverWait # 추가
from selenium.webdriver.support import expected_conditions as EC # 추가
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException # 추가
from webdriver_manager.chrome import ChromeDriverManager
import time
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def setup_chrome_options():
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    #chrome_options.add_argument("--headless")  # 디버깅을 위해 헤드리스 모드 비활성화 # 주석처리
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    return chrome_options

def create_driver():
    logger.info("ChromeDriver 설정 중...")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=setup_chrome_options())
    return driver

def click_element_by_xpath(driver, xpath, element_name, wait_time=10):
    try:
        element = WebDriverWait(driver, wait_time).until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        )
        element.click()
        logger.info(f"{element_name} 클릭 완료")
        time.sleep(2)  # 클릭 후 잠시 대기
    except TimeoutException:
        logger.error(f"{element_name} 요소를 찾는 데 시간이 초과되었습니다.")
    except ElementClickInterceptedException:
        logger.error(f"{element_name} 요소를 클릭할 수 없습니다. 다른 요소에 가려져 있을 수 있습니다.")
    except Exception as e:
        logger.error(f"{element_name} 클릭 중 오류 발생: {e}")

def perform_chart_actions(driver):
    # 시간 메뉴 클릭
    click_element_by_xpath(
        driver,
        #"/html/body/div[1]/div[3]/div[3]/span/div/div/div[1]/div/div/cq-menu[1]",
        "/html/body/div[1]/div[2]/div[3]/span/div/div/div[1]/div/div/cq-menu[1]", # 수정필요
        "시간 메뉴"
    )

    # 1시간 옵션 선택
    click_element_by_xpath(
        driver,
        #"/html/body/div[1]/div[3]/div[3]/span/div/div/div[1]/div/div/cq-menu[1]/cq-menu-dropdown/cq-item[8]",
        "/html/body/div[1]/div[2]/div[3]/span/div/div/div[1]/div/div/cq-menu[1]/cq-menu-dropdown/cq-item[8]", # 수정필요
        "1시간 옵션"
    )

    # 지표 메뉴 클릭
    click_element_by_xpath(
        driver,
        #"/html/body/div[1]/div[3]/div[3]/span/div/div/div[1]/div/div/cq-menu[3]",
        "/html/body/div[1]/div[2]/div[3]/span/div/div/div[1]/div/div/cq-menu[3]", # 수정필요
        "지표 메뉴"
    )

    # 볼린저 밴드 옵션 선택
    click_element_by_xpath(
        driver,
        #"/html/body/div[1]/div[3]/div[3]/span/div/div/div[1]/div/div/cq-menu[3]/cq-menu-dropdown/cq-scroll/cq-studies/cq-studies-content/cq-item[15]",
        "/html/body/div[1]/div[2]/div[3]/span/div/div/div[1]/div/div/cq-menu[3]/cq-menu-dropdown/cq-scroll/cq-studies/cq-studies-content/cq-item[15]", # 수정필요
        "볼린저 밴드 옵션"
    )

def capture_full_page_screenshot(driver, url, filename):
    logger.info(f"{url} 로딩 중...")
    driver.get(url)
    
    # 페이지 로딩을 위한 대기 시간
    logger.info("페이지 로딩 대기 중...")
    time.sleep(10)  # 페이지 로딩을 위해 10초 대기
    
    logger.info("전체 페이지 스크린샷 촬영 중...")
    driver.save_screenshot(filename)
    logger.info(f"스크린샷이 성공적으로 저장되었습니다: {filename}")

def main():
    driver = None
    try:
        driver = create_driver()
        driver.get("https://upbit.com/full_chart?code=CRIX.UPBIT.KRW-BTC") # 추가
        perform_chart_actions(driver)
        capture_full_page_screenshot(
            driver, 
            "https://upbit.com/full_chart?code=CRIX.UPBIT.KRW-BTC",
            "upbit_btc_full_chart.png"
        )
    except Exception as e:
        logger.error(f"오류 발생: {e}")
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    main()