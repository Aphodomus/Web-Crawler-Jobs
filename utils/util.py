from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import csv, datetime
PATH = "C:\Windows\chromedriver.exe" # Change this to where your chromedrive path

def get_jobs(job, city, amount):
    # Config chrome, if you want
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    # Instance the obj driver
    driver = webdriver.Chrome(PATH, options=options)

    # Making the request for the url and set the params for search the job
    driver.get('https://www.glassdoor.com/blog/tag/job-search/')
    
    # Putting the job and the city
    driver.find_element_by_xpath('//*[@id="sc.keyword"]').send_keys(job)
    driver.find_element_by_xpath('//*[@id="sc.location"]').send_keys(city)
    driver.find_element_by_xpath('//*[@id="scBar"]/div/button').click()

    # List where will contain all the jobs found and count
    jobs = []
    count = 1
    x = 0

    try:
        # First click to show the sign up
        try:
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="Discover"]/div/div/div[1]/div[1]/div[3]/a'))
            )

            element.click()
        except:
            pass
        
        # Close the sign up
        try:
            driver.find_element_by_xpath('//*[@id="MainCol"]/div[1]/ul/li[1]').click()
            
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="JAModal"]/div/div[2]/span'))
            )

            element.click()
        except:
            pass

        while len(jobs) < amount:
            # Extract the job information
            try:
                # Select the job
                element = WebDriverWait(driver, 2).until(
                    EC.presence_of_element_located((By.XPATH, f'//*[@id="MainCol"]/div[1]/ul/li[{count}]'))
                )

                element.click()
                sleep(1)

                # Get the Company Name
                try:
                    company_name = driver.find_element_by_xpath(f'//*[@id="MainCol"]/div[1]/ul/li[{count}]/div[2]/div[1]/a/span').text
                except:
                    company_name = -1

                # Get the Job Name
                try:
                    job_name = driver.find_element_by_xpath(f'//*[@id="MainCol"]/div[1]/ul/li[{count}]/div[2]/a/span').text
                except:
                    job_name = -1

                # Get the Company Location
                try:
                    company_location = driver.find_element_by_xpath(f'//*[@id="MainCol"]/div[1]/ul/li[{count}]/div[2]/div[2]/span').text
                except:
                    company_location = -1

                # Get the Score
                try:
                    score = driver.find_element_by_xpath(f'//*[@id="MainCol"]/div[1]/ul/li[{count}]/div[1]/span').text
                except:
                    score = -1

                # Get the Estimate Salary
                try:
                    estimate_salary = driver.find_element_by_xpath(f'//*[@id="MainCol"]/div[1]/ul/li[{count}]/div[2]/div[3]/div[1]/span').text
                except:
                    estimate_salary = -1

                # Get the Average Salary
                try:
                    average_salary = WebDriverWait(driver, 2).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, '.css-1bluz6i.e2u4hf13'))
                    )

                    average_salary = average_salary.text
                except:
                    average_salary = -1

                # Get the Size
                try:
                    size = driver.find_element_by_xpath('//*[@id="EmpBasicInfo"]/div[1]/div/div[1]/span[2]').text
                except:
                    size = -1

                # Get the Founded
                try:
                    founded = driver.find_element_by_xpath('//*[@id="EmpBasicInfo"]/div[1]/div/div[2]/span[2]').text
                except:
                    founded = -1

                # Get the Type
                try:
                    type = driver.find_element_by_xpath('//*[@id="EmpBasicInfo"]/div[1]/div/div[3]/span[2]').text
                except:
                    type = -1

                # Get the Industry
                try:
                    industry = driver.find_element_by_xpath('//*[@id="EmpBasicInfo"]/div[1]/div/div[4]/span[2]').text
                except:
                    industry = -1

                # Get the Sector
                try:
                    sector = driver.find_element_by_xpath('//*[@id="EmpBasicInfo"]/div[1]/div/div[5]/span[2]').text
                except:
                    sector = -1

                # Get the Revenue
                try:
                    revenue = driver.find_element_by_xpath('//*[@id="EmpBasicInfo"]/div[1]/div/div[6]/span[2]').text
                except:
                    revenue = -1

                # Add count
                count += 1
            except:
                # Switch page if jobs end in the page
                count = 1
                driver.find_element_by_xpath('//*[@id="FooterPageNav"]/div/ul/li[7]/a').click()
            
            # Add the job in the list and print progress
            jobs.append([company_name, job_name, company_location, score, estimate_salary, average_salary, size, founded, type, industry, sector, revenue])
            x += 1
            print(f'Progress: {x}/{amount}')

    except:
        print("No results found")
        driver.quit()

    jobs.insert(0, ['Company name', 'Job name', 'Company location', 'Score', 'Estimate salary', 'Average salary', 'Size', 'Founded', 'Type', 'Industry', 'Sector', 'Revenue'])
    return(jobs)

def save_data_csv(dataframe, jobs, city):
    jobs1 = jobs.replace(' ', '_')
    city1 = city.replace(' ', '_').replace('-', '_')
    date = datetime.datetime.now().strftime('%d-%m-%Y')

    with open(f'{jobs1}_{city1}_{date}.csv', 'w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(dataframe)
    