from spend_amount_scraper import SpendAmountScraper
from selenium_manager import SeleniumManager
from individual_investment_scraper import IndividualInvestmentScraper
import os

from time import sleep

def main():
    """Main function to assemble code from different classes.
    """
    path = os.path.join(os.getcwd(), 'output')
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=False)
    else:
        pass

    selenium_manager_instance = SeleniumManager()
    driver = selenium_manager_instance.get_chrome_driver()
    
    spend_amount_scraper_instance = SpendAmountScraper(driver, selenium_manager_instance)
    spend_amount_scraper_instance.start()
    
    individual_investment_scraper_instance = IndividualInvestmentScraper(driver, selenium_manager_instance)
    individual_investment_scraper_instance.start()
    
    driver.quit()


if __name__ == '__main__':
    main()