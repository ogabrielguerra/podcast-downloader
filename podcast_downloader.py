from tokenize import String
from colorama import Back
import requests
from bs4 import BeautifulSoup
from os import mkdir
from os.path import isdir, isfile

class PodcastDownloader:

    def __init__(self, podcast_url, show_title: str, static_source: str=False) -> None:
        
        self.__TARGET_DIR = 'download'
        self.__SHOW_TITLE = show_title

        self.__html_source = None
        self.__files_path = set()
        
        self.create_target_dir()
        self.set_source(podcast_url, static_source)
        self.populate_set()
               
    
    def create_target_dir(self) -> None:
        target_path = self.__TARGET_DIR+'/'+self.__SHOW_TITLE
        if not isdir(self.__TARGET_DIR): mkdir(self.__TARGET_DIR)
        if not isdir(target_path): mkdir(target_path)


    def set_source(self, podcast_url, static_source: str=False) -> None:
        if static_source:
            source = open(static_source, 'r')
            html_source = source.read()
            source.close()
        else:            
            response = requests.get(podcast_url)
            html_source = response.text

        self.__html_source = html_source    


    def populate_set(self) -> None:
        parsed_html = BeautifulSoup(self.__html_source, 'html.parser')

        for link in parsed_html.findAll('a'):
            href = link.get('href')
            if href and r".mp3" in href: self.__files_path.add(href)


    def get_name(self, name_string) -> String:
        name_string = name_string.split('/')
        name_string = name_string[len(name_string)-1]
        name_string = name_string.split('?')
        return name_string[0]


    def download(self) -> None:

        print(Back.BLUE + f'\n\nPODCAST DOWNLOADER\nTotal files: {len(self.__files_path)}\n')

        for url in self.__files_path:
            
            name = self.get_name(url)
            file = self.__TARGET_DIR + '/' + self.__SHOW_TITLE + '/' + name

            if not isfile(file):
                response = requests.get(url, allow_redirects=True)
                open(file, 'wb').write(response.content)
                print(Back.GREEN + f"+ Downloaded [{name}].")
            else:
                print(Back.RED + f"- Skiping [{name}] because it already exists.")
                