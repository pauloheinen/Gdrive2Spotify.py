# GDRIVE
from __future__ import print_function
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']

# SPOTIFY
import spotify

# SELENIUM
from selenium import webdriver

DUCK = "https://duckduckgo.com/?q={0}"
ASK = "https://www.ask.com/web?q={0}"
GOOGLE = "https://www.google.com/search?q={0}"
YANDEX = "https://yandex.com/search/?text={0}"
YAHOO = "https://search.yahoo.com/search;_ylt=A0geKei5QEZhFKAAL1xDDWVH;_ylc=X1MDMTE5NzgwNDg2NwRfcgMyBGZyAwRmcjIDcDpzLHY6c2ZwLG06c2ItdG9wBGdwcmlkAzJVOExwOFkuU1ZXUG4uazRvTDZHZUEEbl9yc2x0AzAEbl9zdWdnAzAEb3JpZ2luA3NlYXJjaC55YWhvby5jb20EcG9zAzAEcHFzdHIDBHBxc3RybAMwBHFzdHJsAzgxBHF1ZXJ5A0h1bmdyaWElMjBIaXAlMjBIb3AlMjAtJTIwQW1vciUyMGUlMjBGJUMzJUE5JTIwKE9mZmljaWFsJTIwTXVzaWMlMjBWaWRlbyklMjAlMjNDaGVpcm9Eb01hdG8lMjAobXAzY3V0Lm5ldCkubXAzBHRfc3RtcAMxNjMxOTk0MDQ2?p={0}&fr=sfp&fr2=p%3As%2Cv%3Asfp%2Cm%3Asb-top&iscqry="
engines = [DUCK, ASK, YAHOO, YANDEX, GOOGLE]

#  login into Google Drive
def LoginGDrive():
    creds = None
    if os.path.exists('../Tokens/token.json'):  # if you're already logged sometime
        creds = Credentials.from_authorized_user_file('../Tokens/token.json', SCOPES)  # load the credentials

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:  # if you havent logged or isnt valid credentials
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('../Tokens/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open('../Tokens/token.json', 'w') as token:
            token.write(creds.to_json())
    drive = build('drive', 'v3', credentials=creds)
    return drive


def savetxt(items, filename):  # list items [] // filename of the savefile.txt
    filePath = filename + '-GDrive.txt'
    ask = input("\nSave items into a file? (Y/N) ").lower()
    if ask.isascii():
        if ask == 'y' or ask == 'n':
            if ask == 'y':
                if os.path.exists(filePath):  # if the file already exists
                    os.remove(filePath)  # delete it
                with open(filePath, 'a', encoding='utf-8') as arquivo:  # open the file or create
                    for item in items:  # write every item on it
                        arquivo.write(item + '\n')
                print("Files saved!")
        else:
            savetxt(items, filename)
    else:
        savetxt(items, filename)  # recursive call


def all(drive, sp, txtname, folderID):  # this function is called to retrieve data from GDrives folder, could be all data or from a specific folder
    listaItens = []
    count = 0
    query_str = "mimeType='audio/mpeg' and trashed != true"
    if folderID is not None:  # folderID
        query_str = "mimeType='audio/mpeg' and trashed != true and parents in \'{}\'".format(folderID)
    page_token = None

    while True:
        results = drive.files().list(q=query_str, corpora='user', pageSize=500, spaces='drive',
                                     fields='nextPageToken, *', pageToken=page_token).execute()
        for index, item in enumerate(results.get('files', []), count + 1):
            count += 1
            listaItens.append(item.get('name') + ' ' + item.get('id'))
            print('{} {}'.format(index, item.get('name')))

        page_token = results.get('nextPageToken', None)
        if page_token is None:
            break
    savetxt(listaItens, txtname)
    if folderID is None:
        addQuestion(listaItens, sp)
    return listaItens


def folderOnly(drive, sp):  # shows up the folders with audio/mpeg content and provides access to it
    parentslist = []  # parents id of folders
    count = 0
    query_str = "mimeType='audio/mpeg' and trashed != true"  # standard query to be send
    page_token = None

    while True:
        results = drive.files().list(q=query_str, corpora='user', pageSize=500, spaces='drive',
                                     fields='nextPageToken, *', pageToken=page_token).execute()
        for index, item in enumerate(results.get('files', []), count):  # for each file in files[]
            for parents in item.get('parents'):  # for each item in sublist of files[]
                if not parentslist.__contains__(parents):  # if parents[] not contains musics -> parentsID
                    parentslist.append(parents)  # add into
                    count += 1  # +1 item

        page_token = results.get('nextPageToken', None)
        if page_token is None:
            break

    while True:
        index = 0
        print("\nThis could take a while...\n'0' = Voltar\nPastas:")

        for item in parentslist:  # for each item in parentslist
            index += 1
            print(str(index) + ' ' + search(drive, item).get('name'))  # print index and item name
        choice = int(input("\nAcessar: "))  # choose what folder you want
        choice -= 1
        if choice == -1:
            break

        elif 0 <= choice < len(parentslist):
            listaItens = all(drive, sp, search(drive, parentslist[choice]).get('name'), parentslist[choice])
            addQuestion(listaItens, sp)


def addQuestion(listaItens, sp):
    ask = input("\nAdicionar ao Spotify esses itens? (Y/N) ").lower()
    if ask.isascii():
        if ask == 'y' or ask == 'n':
            if ask == 'y':
                configBrowser(listaItens, sp)
        else:
            addQuestion(listaItens, sp)
    else:
        addQuestion(listaItens, sp)


def search(drive, parentsid):  # search exactly one item from GDrive
    page_token = None

    while True:
        results = drive.files().list(q="trashed != true", corpora='user', pageSize=500, spaces='drive',
                                     fields='nextPageToken, *', pageToken=page_token).execute()
        for item in results.get('files', []):  # for each file in files[]
            if item.get('id') == parentsid:
                return item
        page_token = results.get('nextPageToken', None)
        if page_token is None:
            break


def main():
    sp = spotify.sp  # spotify.py
    drive = LoginGDrive()  # GDrive services
    while True:
        print("\n[1] Search for all musics\n[2] search for musics in a specific folder\n[3] Quit")
        choice = input("Opção: ")
        if choice == '1':
            all(drive, sp, "Allmusics", None)
        elif choice == '2':
            folderOnly(drive, sp)
        elif choice == '3':
            break


def configBrowser(lista, sp):
    # options and config
    options = webdriver.ChromeOptions()
    count = 0
    opcao = sp.playlists()
    key = 'https://open.spotify.com/track/'

    # setting up configs
    options.add_argument('--headless')
    options.add_argument('--disable-extensions')
    options.add_argument('--profile-directory=Default')
    options.add_argument("--incognito")
    options.add_argument("--disable-plugins-discovery")
    options.add_argument("--start-maximized")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    # connection
    driver = webdriver.Chrome(executable_path='chromedriver.exe', options=options)

    for item in lista:
        count += 1
        q = "spotify track " + item
        q.replace(' ', '')

        Browser(driver, sp, opcao, q, engines[0], key, item, count)


def Browser(driver, sp, opcao, q, SE, key, item, count):
    driver.get(SE.format(q))  # starts the chrome and searches the query
    if driver.current_url == "https://www.google.com/sorry/index?continue=":  # if the Google block the IP
        engines.pop(engines.index(SE))  # remove it from the list
        Browser(driver, sp, opcao, q, engines[engines.index(SE) + 1], key, item, count)  # uses another search engine
    else:
        tags = driver.find_elements_by_xpath("//a[@href]")  # find <a </a>
        tagcounter = 0

        # filtering information
        for tag in tags:  # for every tag in tags[]
            tagcounter += 1
            tag = tag.get_attribute("href")  # i want only href in <a </a>

            if tag.startswith(key):  # if that url start with the key that i want to
                driver.get(tag)
                tag = driver.current_url
                tag.strip('https://open.spotify.com/track/')
                sp.add(item=tag, opcao=opcao)
                break

            elif len(tags) == tagcounter:  # if it is at the end of tags[] then
                if (engines.index(SE) + 1) >= len(engines):  # if has ended the search engines[]
                    print("I couldnt find " + item)
                    with open('Failed-list.txt', 'a', encoding='utf-8') as arquivo:
                        arquivo.write(item + '\n')
                        arquivo.close()
                        break
                else:  # if hasn't ended search engines[]
                    Browser(driver, sp, opcao, q, engines[engines.index(SE) + 1], key, item,
                            count)  # uses another search engine


if __name__ == '__main__':
    main()
