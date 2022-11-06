import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from PIL import Image
from selenium import webdriver
WINDOW_SIZE = "1920,1080"

# mail_address = "anltce150602@fpt.edu.vn"
mail_address = input("Nhập Email @fpt: ")
password= input("Nhập Pass: ")

options = Options()
options.add_argument(r"--user-data-dir=C:\Users\Username\AppData\Local\Google\Chrome\User Data")
try:
    driver = webdriver.Chrome(executable_path="chromedriver.exe", chrome_options=options)
except:
    driver = webdriver.Chrome(executable_path="chromedriver.exe")
driver.get("https://fu.edunext.vn/")
wait = WebDriverWait(driver, 30)


loginbtn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,".btn-login-v4")))
loginbtn.click()

loginOauth = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,".btn-social-login")))
loginOauth.click()

time.sleep(2)
googleLogin = None
googleLogin = False if driver.current_url == "https://fu.edunext.vn/en/home" else True

if googleLogin:
    driver.find_element(By.CSS_SELECTOR,"#identifierId").send_keys(mail_address)
    driver.find_element(By.CSS_SELECTOR,".VfPpkd-LgbsSe-OWXEXe-k8QpJ").click()
    time.sleep(5)
    driver.find_element(By.CSS_SELECTOR,".zHQkBf").send_keys(password)
    driver.find_element(By.XPATH,"//button[@class='VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-k8QpJ VfPpkd-LgbsSe-OWXEXe-dgl2Hf nCP5yc AjY5Oe DuMIQc LQeN7 qIypjc TrZEUc lw1w4b']").click()
    time.sleep(5)


listCourse = wait.until(EC.presence_of_all_elements_located((By.XPATH,"//div[@class='list-course row']//a")))
# courses = listCourse.find_elements(By.TAG_NAME,'a')

coursesText = []
for e in listCourse:
    title = e.get_attribute('title')
    if not title.startswith("Go to course"):
        coursesText.append(title)

for i in range(len(coursesText)):
    print(f'{i}.{coursesText[i]}')
i = input("Chọn môn học: ")
# i=1

try:
    i =int(i)
except:
    print("Ủa, ủa dì dạ, cook")
    driver.quit()
    exit()
    
if (i>=len(coursesText)) or i<0:
    print("Ủa, ủa dì dạ, cook")
    driver.quit()
    exit()
    
listCourse[i*2].click()
time.sleep(2)
# all_item = driver.find_elements(By.XPATH,"//ul[@class='list-slots none-list mg-0']/li[@class='slot-item']/ul[@class='list-activities none-list']/li[contains(@class,'activity-item')]//a[@class='mg-b-0 text-normal activity-name text-decoration-none']")
all_item = wait.until(EC.presence_of_all_elements_located((By.XPATH,"//ul[@class='list-slots none-list mg-0']/li[@class='slot-item']/ul[@class='list-activities none-list']/li[contains(@class,'activity-item')]//a[@class='mg-b-0 text-normal activity-name text-decoration-none']")))
def gradeStarInsideGroup(question):
    url = question.get_attribute('href')
    d2 = driver.execute_script(f'window.open("{url}","_blank");')
    driver.switch_to.window(driver.window_handles[1])
    try:
        # driver.find_element(By.CSS_SELECTOR,"#get-evaluate-inside-group").click()
        gradebtn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,"#get-evaluate-inside-group")))
        gradebtn.click()
        # groupMem = driver.find_elements(By.XPATH,"//div[@class='wrap-table']//tbody/tr")
        groupMem = wait.until(EC.presence_of_all_elements_located((By.XPATH,"//div[@class='wrap-table']//tbody/tr")))
        stars1 = groupMem[0].find_elements(By.XPATH,"//i[@data-point='1']")
        for star in stars1:
            star.click()
        stars5 = groupMem[0].find_elements(By.XPATH,"//i[@data-point='5']")
        for star in stars5:
            star.click()
        # submitbtn = driver.find_element(By.CSS_SELECTOR,'#btn-evaluate-inside-group').click()
        submitbtn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#btn-evaluate-inside-group')))
        submitbtn.click()
    except:
        print("Lỗi, Mạng load không kịp, Vui lòng tự Grade lại tại:",driver.current_url)
    time.sleep(1)
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
# commentList = driver.find_elements(By.CSS_SELECTOR,".main-comment") 


on_going_questions = []
for slot in all_item:
    state = slot.find_elements(By.TAG_NAME,'span')
    if state[2].get_attribute('innerHTML').startswith("On-Going"):
        print(state[0].get_attribute('innerHTML'),":",state[1].get_attribute('innerHTML'))
        on_going_questions.append(slot)
        
for question in on_going_questions:
    gradeStarInsideGroup(question)

