from bs4 import BeautifulSoup
import requests
# from main.models import TreeType, TreeAddress

page_link = 'https://en.wikipedia.org/wiki/List_of_individual_trees'
page_response = requests.get(page_link, timeout=10)
page_content = BeautifulSoup(page_response.content, 'html.parser')

tree_names = {}
all_tables = page_content.findChildren('table', attrs={'class':'wikitable'})
for table in all_tables:
    rows = table.findChildren(['tr'])
    for row in rows:
        cells = row.find_all('td')
        if len(cells) == 5:
            name = cells[0].text.strip()
            description = cells[4].text.strip().split('[')[0] # gets rid of citation at end of string
            location = cells[2].text

            try:
                age = int(cells[3].text)
            except:
                age = 5 # if there isn't a default age found
    
            if len(location) == 0:
                location = "USA" # default value to USA is valid one isn't found
            if len(description) == 0:
                description = "No description available."
            if len(name) > 0:
                tree_names[name] = { 'description': description, 'age': age, 'location': location }


for name in tree_names:
    desc = tree_names[name]['description']
    location = tree_names[name]['location']
    age = tree_names[name]['age']

    # TODO : save this stuff to DB
    # new_tree_type = TreeType(breed=name, description=desc)
    # new_tree_type.save()
    # new_tree_type.id