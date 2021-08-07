from utils.util import *

def main():
    jobs = 'data science'
    city = 'nova york'
    amount = 40
    all_data = get_jobs(jobs, city, amount)
    save_data_csv(all_data, jobs, city)

if __name__ == '__main__':
    main()