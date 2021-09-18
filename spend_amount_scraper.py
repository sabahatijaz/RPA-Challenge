import os
import csv


class SpendAmountScraper:
    
    def __init__(self, driver, selenium_manager):
        
        self.selenium_manager = selenium_manager
        self.driver = driver
    
    def extract_information(self, html_tag, link=False):
        """Takes in a tag and extract meaningful information from it.

        Args:
            html_tag (BeautifulSoup): Html tag from which information is needed to be extracted.
            link (bool, optional): If True, link is extracted from tag. Defaults to False.

        Returns:
            str: Information to be used for further processing.
        """
        
        if link:
            return f'https://itdashboard.gov{html_tag.get("href")}'
        
        return html_tag.get_text().strip()
    
    def export_agencies_data(self, agencies_tiles):
        """Gets agencies html structure, extracts data from it and exports to
        output/Agencies.csv.

        Args:
            agencies_tiles (BeautifulSoup): agencies html structure in BeautifulSoup instance.
        """
        
        with open(os.path.join('output', 'Agencies.csv'), 'w') as f:
            writer = csv.DictWriter(f, fieldnames=['Agency Link', 'Agency Name', 'Spend Amount'])
            
            writer.writeheader()

            for agency in agencies_tiles:
                
                agency_data = {}
                
                agency_data['Agency Link'] = self.extract_information(agency.find('a'), True)
                agency_data['Agency Name'] = self.extract_information(agency.find(class_='h4'))
                agency_data['Spend Amount'] = self.extract_information(agency.find(class_='w900'))
                
                writer.writerow(agency_data)
    
    def get_list_of_agencies(self, link='https://itdashboard.gov/'):
        """Extracts agencies information from https://itdashboard.gov/.

        Args:
            link (str, optional): Link to extract data from. Defaults to 'https://itdashboard.gov/'.
        """
        
        self.driver.get(link)
        
        self.selenium_manager.wait_for_element('//*[@id="node-23"]/div/div/div/div/div/div/div/a', self.driver, 5)
        
        self.selenium_manager.click_button(self.driver.find_element_by_xpath('//*[@id="node-23"]/div/div/div/div/div/div/div/a'), self.driver)
        
        # self.driver.find_element_by_xpath('//*[@id="node-23"]/div/div/div/div/div/div/div/a').click()
        
        soup = self.selenium_manager.get_beautiful_soup(self.driver)
        
        agencies_tiles = soup.find(id='agency-tiles-container').find_all(class_='tuck-5')
        self.export_agencies_data(agencies_tiles)

    def start(self):
        """Assebling function for SpendAmountScraper class.
        """
        
        self.get_list_of_agencies()
