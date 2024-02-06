import requests
from bs4 import BeautifulSoup
from lxml import etree as ET

# URLs to fetch EPG data from
urls = [
    "https://www.epgschedule.in/asianet-news-program-guide.html",
    "https://www.epgschedule.in/asianet-hd-program-guide.html",
    "https://www.epgschedule.in/asianet-movies-hd-program-guide.html",
    "https://www.epgschedule.in/asianet-plus-program-guide.html",
    "https://www.epgschedule.in/dd-malayalam-program-guide.html",
    "https://www.epgschedule.in/kairali-news-program-guide.html",
    
]

def fetch_html(url):
    response = requests.get(url)
    response.raise_for_status()  # Raises an HTTPError if the response status code is 4XX/5XX
    return response.text

def parse_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    channel_title = soup.find('h2').text.strip()
    schedule = []

    for row in soup.find_all('tr'):
        cells = row.find_all('td')
        if len(cells) == 2:  # Ensure row has correct number of columns
            time_duration, program_details = cells
            schedule.append({
                'time': time_duration.get_text(strip=True),
                'details': program_details.get_text(strip=True)
            })

    return channel_title, schedule

def create_xmltv(schedule_data):
    root = ET.Element("tv")
    for channel, programs in schedule_data.items():
        channel_element = ET.SubElement(root, "channel", id=channel)
        display_name = ET.SubElement(channel_element, "display-name")
        display_name.text = channel

        for program in programs:
            programme = ET.SubElement(root, "programme", start=program['time'], channel=channel)
            title = ET.SubElement(programme, "title")
            title.text = program['details']

    tree = ET.ElementTree(root)
    tree.write("epg.xml", pretty_print=True, xml_declaration=True, encoding="UTF-8")

def main():
    schedule_data = {}
    for url in urls:
        html = fetch_html(url)
        channel_title, schedule = parse_html(html)
        schedule_data[channel_title] = schedule

    create_xmltv(schedule_data)

if __name__ == "__main__":
    main()
