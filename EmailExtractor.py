import tkinter
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

universal_links = set()
universal_emails = set()
primary_link = []

def url_correction(url, status):
    global primary_link
    global universal_links
    url2 = ""
    if status == 1:
        if "http" not in url or "https" not in url:
            if "www." not in url:
                url2 = 'https://' + 'www.' + url
                url = 'https://' + url
            else:
                url = 'https://' + url

        else:
            if "www." not in url:
                url2 = 'www.' + url

        universal_links.add(url)
        universal_links.add(url2)
        primary_link.append(url)
        primary_link.append(url2)
        return True, url

    if status == 2:
        base_url = urlparse(url).netloc
        if base_url != "":
            if base_url in primary_link:
                return True, url
            else:
                return False, url
        elif url.startswith('/'):
            url = primary_link[0]+url
            return True, url



def crawler():
    global universal_links
    global universal_emails
    if len(universal_emails) > 0:
        for link in universal_links:
            try:
                html = requests.get(link).content
                bsObj = BeautifulSoup(html, features='html.parser')
            except:
                continue
            all_link = set(a.get('href') for a in bsObj.find_all('a'))

            for link in all_link:
                try:
                    if "mailto:" in link and '@' in link:
                        universal_emails.add(link[7:])
                except:
                    continue

    if len(universal_emails) > 0:
        for email in universal_emails:
            emailBox.insert('end', email)
    else:
        lblMSG.configure(text="No email found!", fg='red')


def link_set(url:str):
    global universal_links
    try:
        result, url = url_correction(url, 1)
        if result:
            html = requests.get(url).content
            bsObj = BeautifulSoup(html, features='html.parser')
        else:
            lblMSG.configure(text="An error happened!", fg='red')
    except:
        pass

    all_link = [
    a.get('href') for a in bsObj.find_all('a')
    if a.get('href') != "" and a.get('href') != "/" and a.get('href') != "#" and '#' not in a.get('href') and 'javascript' not in a.get('href') and ';' not in a.get('href')
    ]

    try:
        for link in all_link:

            result, url = url_correction(link, 2)
            if result:
                if url not in universal_links:
                    universal_links.add(url)
                else:
                    continue
            else:
                continue
    except:
        pass

    crawler()


def txt_check(user_input:str):
    if user_input != "":
        return True
    else:
        return False

def emailExtractor():
    result = txt_check(txtBox.get())
    if result:
        link_set(txtBox.get().strip())
    else:
        lblMSG.configure(text="Please fill in teh field", fg='red')


main = tkinter.Tk()
main.geometry("300x300")
main.title("Email finder")

txtBox = tkinter.Entry(main)
txtBox.pack()

btnSearch = tkinter.Button(main, text="Search!", command=emailExtractor)
btnSearch.pack()

lblMSG = tkinter.Label(main, text="")
lblMSG.pack()

lblSpace1 = tkinter.Label(main, text="")
lblSpace1.pack()

frame = tkinter.Frame(main)
frame.pack()

emailBox = tkinter.Listbox(frame, width=40)
emailBox.pack(side='left')

scrollbar = tkinter.Scrollbar(frame, orient='vertical')
scrollbar.pack(side='right', fill='y')

emailBox.config(yscrollcommand=scrollbar.set)


main.mainloop()