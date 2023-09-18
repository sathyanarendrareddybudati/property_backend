import time
from django.core.management.base import BaseCommand
from selenium import webdriver
from bs4 import BeautifulSoup
from schedules.models import Property, TaskRecord
from django.utils import timezone

class Command(BaseCommand):

    help = 'Scrape property data from 99acres'

    def add_arguments(self, parser):
        parser.add_argument('task_id', type=int, help='The ID of the task to scrape property data for.')

    def handle(self, *args, **options):

        task_id = options['task_id']

        try:
            
            task = TaskRecord.objects.get(pk=task_id)

            driver = webdriver.Chrome()

            cities = [
                {"name": "Pune, Maharashtra", "url": "https://www.99acres.com/property-in-pune-ffid"},
                {"name": "Delhi, Delhi", "url": "https://www.99acres.com/property-in-delhi-ncr-ffid"},
                {"name": "Mumbai, Maharashtra", "url": "https://www.99acres.com/property-in-mumbai-ffid"},
                {"name": "Lucknow, Uttar Pradesh", "url": "https://www.99acres.com/independent-house-in-lucknow-ffid"},
                {"name": "Agra, Uttar Pradesh", "url": "https://www.99acres.com/residential-land-in-agra-ffid"}
            ]

            def scrape_individual_property_data(link):
                property_type = ''
                property_locality = ''
                property_city = ''

                driver.get(link)
                time.sleep(2)  

                soup = BeautifulSoup(driver.page_source, 'html.parser')

                property_element = soup.find('h1', class_='banner__propDetails')
                if property_element:
                    property_types = property_element.find('div', class_='banner__sizePropType')
                    property_localitys = property_element.find('div', class_='banner__projectLocation')
                    if property_types:
                        property_type = property_types.text.strip()
                    else:
                        property_type = ""
                    if property_localitys:
                        property_locality = property_localitys.text.strip().split(',')[0]
                        property_city = property_localitys.text.strip().split(',')[1]
                    else:
                        property_locality = ""
                        property_city = ""

                property_costs = soup.find('div', class_='factTableComponent__npPrice')
                if property_costs:
                    property_cost = property_costs.text.strip()
                else:
                    property_cost = ""

                return {
                    "property_cost": property_cost,
                    "property_type": property_type,
                    "property_locality": property_locality,
                    "property_city": property_city
                }

            for city in cities:
                print('Scraping data for', city['name'])
                driver.get(city['url'])
                time.sleep(2)

                soup = BeautifulSoup(driver.page_source, 'html.parser')
                property_listings = soup.find_all('div', class_='srpTuple__cardWrap')

                for listing in property_listings:
                    property_names = listing.find('a', class_='srpTuple__dFlex')
                    if property_names:
                        property_name = property_names.text
                    else:
                        property_name = ""

                    property_area_element = listing.find('td', id='srp_tuple_primary_area')
                    if property_area_element:
                        property_area_text = property_area_element.text.strip()
                        parts = property_area_text.split()
                        if len(parts) >= 2 and parts[1] == 'sq.ft.':
                            property_area = " ".join(parts[:2])
                        else:
                            property_area = ""
                    else:
                        property_area = ""

                    individual_property_link_element = listing.find('a', class_='body_med srpTuple__propertyName')
                    if individual_property_link_element:
                        individual_property_link = individual_property_link_element.get('href', '')
                    else:
                        individual_property_link = ''

                    if individual_property_link:
                        property_data = scrape_individual_property_data(individual_property_link)

                        Property.objects.create(
                            property_name=property_name,
                            property_cost=property_data["property_cost"],
                            property_type=property_data["property_type"],
                            property_area=property_area,
                            property_locality=property_data["property_locality"],
                            property_city=property_data['property_city'],
                            individual_property_link=individual_property_link
                        )

            task.records_scraped = len(property_listings)
            task.end_time = timezone.now()
            task.status = 'completed'
            task.save()

            driver.quit()
            self.stdout.write(self.style.SUCCESS('Successfully scraped property data from 99acres'))

        except TaskRecord.DoesNotExist:
            self.stderr.write(self.style.ERROR('Task with ID {} does not exist.'.format(task_id)))

        except Exception as e:
            self.stderr.write(self.style.ERROR(f"An error occurred: {str(e)}"))
            if task:
                task.status = 'failed'
                task.save()
