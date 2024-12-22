import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import List, Dict, Any
import time
import logging
from datetime import datetime
import os
from tabulate import tabulate

class WebScraper:
    """
    A web scraping class that collects journal data from SINTA (Science and Technology Index)
    """

    def __init__(self, base_url: str, keyword: str):
        """
        Initialize the scraper with base URL and search keyword

        Args:
            base_url (str): The base URL to scrape from
            keyword (str): Search keyword for filtering journals
        """
        self.base_url = base_url
        self.keyword = keyword
        self.data = []

        # Create directory for the keyword
        self.output_dir = self._create_output_directory()

        # Setup file paths
        self.filename = os.path.join(self.output_dir, f"journal_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")
        self.log_filename = os.path.join(self.output_dir, f"scraping_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
        self.viz_dir = os.path.join(self.output_dir, 'visualizations')

        # Create visualizations directory
        os.makedirs(self.viz_dir, exist_ok=True)

        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            filename=self.log_filename
        )
        self.logger = logging.getLogger(__name__)

        # Log initial setup
        self.logger.info(f"Output directory created at: {self.output_dir}")
        self.logger.info(f"Visualization directory created at: {self.viz_dir}")

    def _create_output_directory(self) -> str:
        """
        Create output directory based on keyword and timestamp

        Returns:
            str: Path to created directory
        """
        # Create base output directory if it doesn't exist
        base_dir = 'scraped_data'
        os.makedirs(base_dir, exist_ok=True)

        # Create keyword-specific directory with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        keyword_dir = os.path.join(base_dir, f"{self.keyword}_{timestamp}")
        os.makedirs(keyword_dir, exist_ok=True)

        return keyword_dir

    def fetch_page(self, url: str) -> BeautifulSoup:
        """
        Fetch and parse a webpage

        Args:
            url (str): URL to fetch

        Returns:
            BeautifulSoup: Parsed HTML content
        """
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return BeautifulSoup(response.content, 'html.parser')
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error fetching page {url}: {str(e)}")
            raise SystemExit(f"An error occurred! Log file has been written to {self.log_filename}")

    def get_pagination(self, soup: BeautifulSoup) -> int:
        """
        Extract the total number of pages

        Args:
            soup (BeautifulSoup): Parsed HTML content

        Returns:
            int: Total number of pages
        """
        try:
            pagination = soup.find_all('div', class_='text-center pagination-text')
            num_pagination_text = pagination[0].get_text()
            num_split = num_pagination_text.split()
            return int(num_split[3])
        except Exception as e:
            raise SystemExit("Aborted, Keyword Not Found!!!")

    def extract_journal_data(self, soup: BeautifulSoup) -> List[Dict[str, Any]]:
        """
        Extract journal information from the page

        Args:
            soup (BeautifulSoup): Parsed HTML content

        Returns:
            List[Dict]: List of dictionaries containing journal information
        """
        try:
            journals = []

            # Find journal names and links
            journal_names = soup.find_all('div', class_='affil-name mb-3')
            affiliations = soup.find_all('div', class_='affil-loc mt-2')
            accreditations = soup.find_all('span', class_='num-stat accredited')

            for i in range(len(journal_names)):
                journal = {
                    'name': journal_names[i].text.strip(),
                    'link': journal_names[i].find('a')['href'] if journal_names[i].find('a') else '',
                    'affiliation': affiliations[i].text.strip() if i < len(affiliations) else '',
                    'accreditation': accreditations[i].text.strip() if i < len(accreditations) else ''
                }
                journals.append(journal)

            return journals
        except Exception as e:
            self.logger.error(f"Error extracting journal data: {str(e)}")
            raise SystemExit("Aborted, Keyword Not Found!!!")

    def save_to_csv(self, data: List[Dict[str, Any]]) -> None:
        """
        Save scraped data to CSV file

        Args:
            data (List[Dict]): List of dictionaries containing journal data
        """
        try:
            df = pd.DataFrame(data)
            df.to_csv(self.filename, index=False)
            self.logger.info(f"Data saved to {self.filename}")
        except Exception as e:
            raise SystemExit(f"Error saving to CSV: {str(e)}")

    def visualize_data(self) -> None:
        """
        Create visualizations of the scraped data
        """
        try:
            df = pd.read_csv(self.filename)

            # 1. Journal distribution by affiliation
            plt.figure(figsize=(12, 6))
            affiliation_counts = df['affiliation'].value_counts().head(10)
            sns.barplot(x=affiliation_counts.values, y=affiliation_counts.index)
            plt.title('Top 10 Affiliations by Number of Journals')
            plt.xlabel('Number of Journals')
            plt.tight_layout()
            plt.savefig(os.path.join(self.viz_dir, 'affiliation_distribution.png'))
            plt.close()

            # 2. Accreditation distribution
            plt.figure(figsize=(8, 8))
            df['accreditation'].value_counts().plot(kind='pie', autopct='%1.1f%%')
            plt.title('Distribution of Journal Accreditations')
            plt.axis('equal')
            plt.savefig(os.path.join(self.viz_dir, 'accreditation_distribution.png'))
            plt.close()

            self.logger.info("Visualizations created successfully")
        except Exception as e:
            raise SystemExit(f"Error creating visualizations")

    def run(self) -> None:
        """
        Main method to run the scraping process
        """
        try:
            all_journals = []

            # Get initial page to determine pagination
            initial_url = f"{self.base_url}?q={self.keyword}"
            initial_soup = self.fetch_page(initial_url)
            total_pages = self.get_pagination(initial_soup)

            self.logger.info(f"Starting scraping process for {total_pages} pages")

            # Iterate through all pages
            for page in range(1, total_pages + 1):
                url = f"{self.base_url}?page={page}&q={self.keyword}"
                self.logger.info(f"Scraping page {page}/{total_pages}")

                soup = self.fetch_page(url)
                journals = self.extract_journal_data(soup)
                all_journals.extend(journals)

                # Respect the server by adding delay between requests
                time.sleep(2)

            # Save and visualize the collected data
            self.save_to_csv(all_journals)
            self.visualize_data()
            
            # Menampilkan tabel data journal
            headers = ['Name', 'Affiliation', 'Accreditation', 'Link']
            table_data = [[j['name'], j['affiliation'], j['accreditation'], j['link']] for j in all_journals]
            print(tabulate(table_data, headers=headers, tablefmt='grid'))


            self.logger.info("Scraping process completed successfully")
            print(f"Scraping completed. Data saved to {self.filename}")
            print(f"Visualizations saved in {self.viz_dir}")
            print(f"Log file location: {self.log_filename}")

        except Exception as e:
            self.logger.error(f"Error in scraping process: {str(e)}")
            print(f"An error occurred: {str(e)}")
            raise

def main():
    """
    Main function to run the scraper
    """
    base_url = "https://sinta.kemdikbud.go.id/journals/"
    keyword = "teknologi informasi"

    scraper = WebScraper(base_url, keyword)
    scraper.run()

if __name__ == "__main__":
    main()