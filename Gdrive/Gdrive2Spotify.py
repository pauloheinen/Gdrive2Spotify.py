"""
client ID GDRIVE 112307785324623293295
api KEY GDRIVE AIzaSyDV7ZD8MPZy44akQdQ3ixFZCllxLueGsNI

Client ID SPOTIFY 8ad707a87c8445b481c240424ad5998c
Client Secret SPOTIFY d00fda6a444f41cbb4e3bd5528fd8475

https://imasters.com.br/back-end/google-search-usando-selenium-e-python-o-basico-sobre-selenium-python
Make a script that takes .mp3 from Gdrive and add that .mp3 on Spotify.
"""

# GDRIVE
from __future__ import print_function
import os.path

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']

# musica 1Q5gkiWnZaQ9UKgF-dtpZk9isOrfVsuTf
# Random 1nyd0LFdYpzNEaLIIvBwc6jBSY-wpiUkr
# Rap, eletro 11zEAVrmBwRG_urikO7uVCVV3VRRi6f4T


# SELENIUM
from selenium import webdriver

BING = "https://www.bing.com/search?q={0}"
GOOGLE = "https://www.google.com/search?q={0}"
YANDEX = "https://yandex.com/search/?text={0}"
YAHOO = "https://search.yahoo.com/search;_ylt=A0geKei5QEZhFKAAL1xDDWVH;_ylc=X1MDMTE5NzgwNDg2NwRfcgMyBGZyAwRmcjIDcDpzLHY6c2ZwLG06c2ItdG9wBGdwcmlkAzJVOExwOFkuU1ZXUG4uazRvTDZHZUEEbl9yc2x0AzAEbl9zdWdnAzAEb3JpZ2luA3NlYXJjaC55YWhvby5jb20EcG9zAzAEcHFzdHIDBHBxc3RybAMwBHFzdHJsAzgxBHF1ZXJ5A0h1bmdyaWElMjBIaXAlMjBIb3AlMjAtJTIwQW1vciUyMGUlMjBGJUMzJUE5JTIwKE9mZmljaWFsJTIwTXVzaWMlMjBWaWRlbyklMjAlMjNDaGVpcm9Eb01hdG8lMjAobXAzY3V0Lm5ldCkubXAzBHRfc3RtcAMxNjMxOTk0MDQ2?p={0}&fr=sfp&fr2=p%3As%2Cv%3Asfp%2Cm%3Asb-top&iscqry="
engines = [YAHOO, YANDEX, GOOGLE, BING]


def rec(drive):
    print(
        'What do you want to search for?\n[1] Folder\n[2] Image\n[3] Audio\n[4] Video\n[5] PDF\n[6] Text\n[7] Is '
        'Trash?\n '
        '[8] Hidden file?\n[9] Name contains\n[10] All files')
    choice = None
    query = []
    if choice == '1':
        query.append("'application/vnd.google-apps.folder'")
    if choice == '2':
        query.append("'image/jpeg'")
    if choice == '3':
        query.append("'audio/mpeg'")
    if choice == '4':
        query.append("'video/mp4'")
    if choice == '5':
        query.append("'application/pdf'")
    if choice == '6':
        query.append("'text/plain'")
    if choice == '7':
        query.append("'true'")
    if choice == '8':
        query.append("'true'")
    if choice == '9':
        query.append(str(input("What 'name' contains?: ")))
    if choice == '10':
        query.clear()
        query.append("not yet")

    page_token = None
    rec2(page_token, drive)


def rec2(page_token, drive):
    if page_token is not None:
        while True:
            results = drive.files().list(q="mimeType='application/vnd.google-apps.folder'",
                                         pageSize=500,
                                         spaces='drive',
                                         fields='nextPageToken, files(id, name, parents)',
                                         pageToken=page_token).execute()
            for file in results.get('files', []):
                if file.get('parents' == drive):
                    return None
                print('Found file: %s (%s)' % (file.get('name'), file.get('parents')))
            page_token = results.get('nextPageToken', None)
            if page_token is None:
                break


def retrieve(drive):
    listaItens = []
    count = 0
    query_str = "mimeType='audio/mpeg' and parents in \'1nyd0LFdYpzNEaLIIvBwc6jBSY-wpiUkr\' and trashed != true"
    page_token = None
    while True:
        results = drive.files().list(q=query_str,
                                     corpora='user',
                                     pageSize=500,
                                     spaces='drive',
                                     fields='nextPageToken, *',
                                     pageToken=page_token).execute()
        for file in results.get('files', []):
            listaItens.append(file.get('name'))
            count += 1
            print('%s  ID(%s)  %s' % (file.get('name'), file.get('id'), file.get('mimeType')))

        page_token = results.get('nextPageToken', None)
        if page_token is None:
            break
    print("Quantidade de itens " + str(count))
    return listaItens


def main():
    creds = None
    if os.path.exists('../Tokens/token.json'):
        creds = Credentials.from_authorized_user_file('../Tokens/token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('../Tokens/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('../Tokens/token.json', 'w') as token:
            token.write(creds.to_json())

    drive = build('drive', 'v3', credentials=creds)

    lista = retrieve(drive)

    configBrowser(lista)


def configBrowser(lista):

    # options and config
    options = webdriver.ChromeOptions()
    count = 0
    key = 'https://open.spotify.com/track/'

    for item in lista:
        count += 1
        options.add_argument('--headless')
        options.add_argument('--disable-extensions')
        options.add_argument('--profile-directory=Default')
        options.add_argument("--incognito")
        options.add_argument("--disable-plugins-discovery")
        options.add_argument("--start-maximized")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)

        # connection
        driver = webdriver.Chrome(executable_path='chromedriver.exe')
        driver.delete_all_cookies()
        q = "spotify track " + "Unlike Pluto ft. Why Mona - Happy Together (Cover)_160k.mp3"
        q.replace(' ', '')

        Browser(driver, q, engines[0], key, item, count)


def Browser(driver, q, SE, key, item, count):

    # gathering information
    driver.get(SE.format(q))  # starts the chrome and searches the query
    driver.implicitly_wait(2)

    if driver.current_url == "https://www.google.com/sorry/index?continue=":
        Browser(driver, q, engines[engines.index(SE)+1], key, item, count)  # uses another search engine
    else:
        tags = driver.find_elements_by_xpath("//a[@href]")  # find <a </a>
        tagcounter = 0

        # filtering information
        for tag in tags:  # for every tag in tags[]
            tagcounter += 1
            tag = tag.get_attribute("href")  # i want only href="" in <a </a>

            # filtering information ++
            if tag.startswith(key):  # if that url start with the key that i want to
                print(tag + '(' + item + ')' + ' ' + str(count))

                with open('lista gdrive.txt', 'a', encoding='utf-8') as arquivo:  # write on a txt
                    arquivo.write(str(count) + ' ' + item + ' (' + tag + ')\n')
                    arquivo.close()
                    driver.close()
                    break

            elif len(tags) == tagcounter:  # if it is at the end of tags[] then
                if engines.index(SE) != len(engines):  # if hasn't ended the searches engine[]
                    Browser(driver, q, engines[engines.index(SE)+1], key, item, count)  # uses another search engine
                else:
                    print("I couldnt find " + item)
                    with open('lista failed.txt', 'a', encoding='utf-8') as arquivo:
                        arquivo.write(item + '\n')
                        arquivo.close()


if __name__ == '__main__':
    main()
