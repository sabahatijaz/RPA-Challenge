import os
import csv
import sys
import time
import _stat
from time import sleep
from os import stat
import PyPDF2


class IndividualInvestmentScraper:

    def __init__(self, driver, selenium_manager):

        self.driver = driver
        self.selenium_manager = selenium_manager

    def download_pdf(self, link):
        """Downloads pdf from a button located at in specific link.

        Args:
            link (str): link to find the pdf button and click on it.
        """
        if link != '':
            try:
                self.driver.get(link)
            except:
                return

            try:
                self.selenium_manager.wait_for_element('//*[@id="business-case-pdf"]/a', self.driver, 4)
                pdf_button = self.driver.find_element_by_xpath('//*[@id="business-case-pdf"]/a')
            except:
                return

            self.selenium_manager.click_button(pdf_button, self.driver)

            sleep(6)

    def extract_information(self, html_tag, link=False):
        """Takes in a tag and extract meaningful information from it.

        Args:
            html_tag (BeautifulSoup): Html tag from which information is needed to be extracted.
            link (bool, optional): If True, link is extracted from tag. Defaults to False.

        Returns:
            str: Information to be used for further processing.
        """

        if link:
            if html_tag.find('a'):
                return f'https://itdashboard.gov{html_tag.find("a").get("href")}'
            else:
                return None

        return html_tag.get_text().strip()

    def parse_investment_table(self, individual_investment_writer, agency):
        soup = self.selenium_manager.get_beautiful_soup(self.driver)

        investment_table = soup.find(id='investments-table-object').find('tbody').find_all('tr')
        with open(os.path.join('output', 'Comparison.csv'), 'w') as f3:
            Comparison_writer = csv.DictWriter(f3, fieldnames=[
                'UII',
                'Unique_Investment_Identifier',
                'ComparisonStatus',
                'Name_of_this_Investment',
                'Investment_Title',
                'ComparisonStatus2'
            ])
            Comparison_writer.writeheader()

        for row in investment_table:
            investment_data = {}
            Comparison_data = {}

            row = row.find_all('td')

            investment_data['Agency Link'] = agency.get('Agency Link')
            investment_data['Agency Name'] = agency.get('Agency Name')
            investment_data['Spend Amount'] = agency.get('Spend Amount')

            investment_data['UII'] = self.extract_information(row[0])
            investment_data['UII Link'] = self.extract_information(row[0], True)
            #############################################################################################################################################
            self.download_pdf(investment_data['UII Link'])
            pdfname = self.extract_information(row[0])
            path = os.path.join(os.getcwd(), 'output', str(pdfname) + '.pdf')

            while True:
                if os.path.exists(path):
                    break
                else:
                    continue
            # Creating a pdf file object
            st = os.stat(path)
            os.chmod(path, st.st_mode | _stat.S_IWOTH)
            pdfFileObj = open(path, 'rb')
            # Creang a pdf reader object
            pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
            pageObj = pdfReader.getPage(0)
            text = pageObj.extractText().split("  ")
            result = text[3].find('Name of this Investment')
            result = result + 22
            txt2 = text[3].find('Unique Investment Identifier (UII):')
            Name_of_this_Investment = text[3][result + 5:txt2 - 4]
            txt2 = txt2 + 33
            txt3 = text[3].find('Section B')
            Unique_Investment_Identifier = text[3][txt2 + 5:txt3 - 1]
            self.extract_information(row[0])
            Comparison_data['Unique_Investment_Identifier'] = Unique_Investment_Identifier
            Comparison_data['UII'] = self.extract_information(row[0])
            if self.extract_information(row[0]) == Unique_Investment_Identifier:
                Comparison_data['ComparisonStatus'] = "same"
            else:
                Comparison_data['ComparisonStatus'] = "Different"
            #
            #
            #
            ####################################################################################################################
            investment_data['Bureau'] = self.extract_information(row[1])
            investment_data['Investment Title'] = self.extract_information(row[2])
            Comparison_data['Name_of_this_Investment'] = Name_of_this_Investment
            Comparison_data['Investment_Title'] = self.extract_information(row[2])
            if Name_of_this_Investment == self.extract_information(row[2]):
                Comparison_data['ComparisonStatus2'] = "same"
            else:
                Comparison_data['ComparisonStatus2'] = "Different"

            investment_data['Total FY2021 Spending ($M)'] = self.extract_information(row[3])
            investment_data['Type'] = self.extract_information(row[4])
            investment_data['CIO Rating'] = self.extract_information(row[5])
            investment_data['# of Projects'] = self.extract_information(row[6])

            individual_investment_writer.writerow(investment_data)
            with open(os.path.join('output', 'Comparison.csv'), 'a') as f3:
                Comparison_writer = csv.DictWriter(f3, fieldnames=[
                    'UII',
                    'Unique_Investment_Identifier',
                    'ComparisonStatus',
                    'Name_of_this_Investment',
                    'Investment_Title',
                    'ComparisonStatus2'
                ])
                Comparison_writer.writerow(Comparison_data)
            pdfFileObj.close()

    def parse_agencies(self, file_path='./output/Agencies.csv'):

        with open(file_path) as f:
            agencies = csv.DictReader(f)

            with open(os.path.join('output', 'individual_investments.csv'), 'w') as f2:
                individual_investment_writer = csv.DictWriter(f2, fieldnames=[
                    'Agency Link',
                    'Agency Name',
                    'Spend Amount',
                    'UII',
                    'UII Link',
                    'Bureau',
                    'Investment Title',
                    'Total FY2021 Spending ($M)',
                    'Type',
                    'CIO Rating',
                    '# of Projects'
                ])

                individual_investment_writer.writeheader()

                for agency in agencies:
                    self.driver.get(agency.get('Agency Link'))

                    list_all_xpath = '//*[@id="investments-table-object_length"]/label/select/option[4]'

                    self.selenium_manager.wait_for_element(list_all_xpath, self.driver, 10)
                    self.driver.find_element_by_xpath(list_all_xpath).click()

                    try:
                        self.selenium_manager.wait_for_element('//*[@id="investments-table-object"]/tbody/tr[11]/td[2]',
                                                               self.driver, 20)
                    except:
                        pass

                    self.parse_investment_table(individual_investment_writer, agency)

    def start(self):
        self.parse_agencies()
