# ----------------------------------------------------------------------------------#
# author: https://github.com/fla-pi/                                                #
# gli url valgono per sei siti di quotidiani, e sono:                               # 
# corriere.it ; lastampa.it ; repubblica.it ; ilgiornale.it; ilfattoquotidiano.it ; #
# ilmessaggero.it .                                                                 #
# Non è capace di gestire url di altri siti, ma è possibile adattare il codice      #
# alle pagine html di altri siti, con le adeguate modifiche.                        #
#-----------------------------------------------------------------------------------#


import os
import sys
import time
import json
import re
import random
from time import sleep
import ssl

import requests as rq
from bs4 import BeautifulSoup as bs
from newspaper import Article
import nltk



def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()

dates = []
links = []
link_dict = dict()
downlink =[]
xx = 0

def corr(s):
    articles= s.findAll('a')
    for article in articles:
        try:
            if article != None:
                #title and link
                if article.findAll('href') != None:
                    link = article.get('href')
                    link1 = link[43:]
                    reg = re.search("www.corriere.it/[a-z]+/[0-9]",link1)
                    if "http:"  not in link1 and "https:" not in link1:
                        link1 = "http:" + link1
            else:
                title = 'N/A'
                link1 = 'N/A'
            if reg and ('13_agosto_29' not in link1):
                if link1 not in links and ('#commentFormAnchor' not in link1):
                    links.append(link1)
                    date_n = date[0:4]
                    if date_n not in link_dict:
                        link_dict[date_n] = list()
                    link_dict[date_n].extend((link1,))
                    print(link1)
        except:
            pass

def gior(s):
    articles= s.findAll('a')
    for article in articles:
        
        try:
            if article != None:
                
                if article.findAll('href') != None:
                    link = article.get('href')
                    if link[:3] == 'http':
                        link1 = link[44:]
                    else:
                        link1 = link[20:]
                    if "https://www.ilgiornale.it" not in link1:
                        link1 = "https://www.ilgiornale.it"+link1
                    ex = "www.ilgiornale.it/news"
                    
            else:
                title = 'N/A'
                link1 = 'N/A'
            if ex in link1:
                if link1 not in links and ("https://www.ilgiornale.it/" in link1):
                    links.append(link1)
                    date_n = date[0:4]
                    if date_n not in link_dict:
                        link_dict[date_n] = list()
                    link_dict[date_n].extend((link1,))
                    print(link1)
        except:
            print('error')

def fatto(s):
    articles= s.findAll('a')
    for article in articles:
        try:
            if article != None:
                
                if article.findAll('href') != None:
                    link = article.get('href')
                    link1 = link[43:]
                    reg = re.search("www.ilfattoquotidiano.it/[0-9]+/[0-9]",link1)
                    link1 = link1+'amp'
            else:
                title = 'N/A'
                link1 = 'N/A'
            if reg:
                if link1 not in links and '#disqus_thread' not in link1 and ('#c' not in link1) and ('mailto' not in link1):
                    links.append(link1)
                    date_n = date[0:4]
                    if date_n not in link_dict:
                        link_dict[date_n] = list()
                    link_dict[date_n].extend((link1,))
                    print(link1)
        except:
            pass

def stampa(s):
    articles= s.findAll('a')
    for article in articles:
        try:
            if article != None:
        
                if article.findAll('href') != None:
                    link = article.get('href')
                    link1 = link[43:]
                    if '?ref' in link1:
                        link1 = re.sub(r'?ref.+', '/amp', link1)
                    if "https://www.lastampa.it/" not in link1:
                        link1 = "https://www.lastampa.it/" + link1
                    if '/amp' not in link[-7:]:
                        link1 = link1+'/amp'
                    reg = re.search("www.lastampa.it/[a-z]+/[0-9]+",link1)
                    reg2 = re.search("www.lastampa.it/[0-9]+/[0-9]+/[0-9]+/[a-z]+",link1)
            else:
                title = 'N/A'
                link1 = 'N/A'
            if reg or reg2:
                if link1 not in links and ('premium.html/amp' not in link1) and ('primapagina' not in link1) and ('tuttolibri' not in link1) and ('utility' not in link1):
                    links.append(link1)
                    date_n = date[0:4]
                    if date_n not in link_dict:
                        link_dict[date_n] = list()
                    link_dict[date_n].extend((link1,))
                    print(link1)
        except:
            pass

def rep(s):
    articles= s.findAll('a')
    for article in articles:
        try:
            if article != None:
        
                if article.findAll('href') != None:
                    link = article.get('href')
                    link1 = link[43:]
                    if '?ref' in link1:
                        link1 = re.sub(r'?ref.+', 'amp/', link1)
                    else:
                        link1 = link1 +'amp'
                    reg = re.search("www.repubblica.it/[a-z]+/[0-9]+/[0-9]+/[0-9]+/news",link1)
                    #reg2 = re.search("www.lastampa.it/[a-z]+/[a-z]+/[0-9]+",link1)
            else:
                title = 'N/A'
                link1 = 'N/A'
            if reg:
                if link1 not in links and  ('#commenta' not in link1):
                    links.append(link1)
                    date_n = date[0:4]
                    if date_n not in link_dict:
                        link_dict[date_n] = list()
                    link_dict[date_n].extend((link1,))
                    print(link1)
                    
        except:
            pass

def mess(s):
    articles= s.findAll('a')
    for article in articles:
        try:
            if article != None:
        
                if article.findAll('href') != None:
                    link = article.get('href')
                    link1 = link[43:]
                    if "://www.ilmessaggero.it/" not in link1:
                        link1 = "https://www.ilmessaggero.it/" + link1
                    reg = re.search("www.ilmessaggero.it/[a-z]+/[a-z]+/[a-z]+",link1)
                    
            else:
                title = 'N/A'
                link1 = 'N/A'
            if reg:
                if link1 not in links and  (('video' or 'fotogallery' or '#commenti') not in link1):
                    links.append(link1)
                    date_n = date[0:4]
                    if date_n not in link_dict:
                        link_dict[date_n] = list()
                    link_dict[date_n].extend((link1,))
                    print(link1)
        except:
            pass
        
inp1 = input('Url del sito: ')
inp2 = input('Da data (scrivi aaaammgg,es: 20190705): ')
inp3 = input('Fino a data (scrivi aaaammgg,es: 20190705): ')
#url = 'http://web.archive.org/cdx/search/cdx?url=corriere.it&collapse=digest&from=20170107&to=20190431&output=json'
url = 'http://web.archive.org/cdx/search/cdx?url='+inp1+'&collapse=digest&from='+inp2+'&to='+inp3+'&output=json'
urls = rq.get(url).text
parse_url = json.loads(urls) 
url_list = []

for i in range(1,len(parse_url)):
    orig_url = parse_url[i][2]
    tstamp = parse_url[i][1]
    waylink = tstamp+'/'+orig_url
    url_list.append(waylink)

l = len(url_list)
i = 0
printProgressBar(0, l, prefix = 'Progress:', suffix = 'Completi: '+ str(i) + '/'+ str(l) +'''
 ''', length = 100)
for url in url_list:
    try:
        final_url = 'https://web.archive.org/web/'+url
        date = final_url[28:36]
        i+=1
        if date not in dates:
            dates.append(date)
            print(date)
            req = rq.get(final_url).text
            # parse html using beautifulsoup and store in soup
            soup = bs(req,'html.parser')
            if 'corriere' in inp1:
                corr(soup)
            elif 'giornale' in inp1:
               gior(soup)
            elif 'fattoquotidiano' in inp1:
               fatto(soup)
            elif 'lastampa' in inp1:
               stampa(soup)
            elif 'repubblica' in inp1:
                rep(soup)
            elif 'messaggero' in inp1:
                mess(soup)
            time.sleep(0.1)
            printProgressBar(i, l, prefix = 'Progress:', suffix = 'Completi: '+ str(i) + '/'+ str(l) +'''
''', length = 100)
    except:
        time.sleep(5)
        
        pass
with open('link_articoli.csv', 'w') as f:
    for key in link_dict.keys():
        f.write("%s,%s\n"%(key,link_dict[key]))
print(len(links), 'articoli scaricati') 
def text():
    inp4 = input('Quanti articoli vuoi estrarre? (Se ci sono articoli da anni diversi, il numero sarà diviso tra gli anni presenti) ')
    if int(inp4) > len(links):
        print('Gli articoli collezionati non sono abbastanza')
        text()
    else:
        try:
            num_samp = int(inp4)//len(link_dict.keys())
            for key,value in link_dict.items():
                if len(value) >= num_samp:
                    link_text = random.sample(value, num_samp)
                else:
                    link_text = value
                if isinstance(link_text, list):
                    for i in link_text:
                        downlink.append(i)
            print(downlink)
        except Exception as e: print(e)
        def scrape(download):
            outpath = inp1[:-3]+'/'
            inp5 = input('Vuoi creare i txt nella cartella ' + outpath + '? (Y/N) ')
            if inp5 != 'Y' and inp5 != 'y':
                if inp5 == 'N' or inp5 == 'n':
                    inp6 = input('Digita un nome per la nuova cartella: ')
                    outpath = inp6+'/'
                else:
                    scrape(downlink)
            
            
            if os.path.exists(outpath):
                print(' La cartella esiste già, cambia il nome')
                scrape(downlink)
            try:
                os.mkdir(outpath)
            except Exception as e:
                print(e)
                scrape(downlink)
            j = 0
            l = len(download)
            printProgressBar(0, l, prefix = 'Progress:', suffix = 'Completi: '+ str(j) + '/'+ str(l) +'''
    ''', length = 100)
            for i in download:
                url = i
                a= Article(url, language='it')
                try:
                    req = rq.get(url).text
                    soup = bs(req,'html.parser')
                except:
                    try:
                        url = 'https' + url[4:]
                        req=  rq.get(url).text
                        soup = bs(req,'html.parser')
                    except:
                        pass
                

                if 'repubblica' in url:

                    for y in soup.findAll("aside", attrs ={'class':'inline-article'}): 
                        y.decompose()
                    for x in soup.findAll("footer", attrs = {'class':'main-footer'}):
                        x.decompose()
                    for x in soup.findAll("figcaption"):
                        x.decompose()
                    for y in soup.findAll("aside"): 
                        y.decompose()
                    for y in soup.findAll("h2"): 
                        y.decompose()
                    for y in soup.findAll("blockquote"): 
                        y.decompose()
                    try:
                        title = soup.find('h1').get_text()
                    except:
                        title = ' '
                    for y in soup.findAll("h1"): 
                        y.decompose()


                            
                    article = soup.findAll('div',attrs ={'subscriptions-section':'content'})

                    try:
                        sub = soup.find('p', attrs ={'class':'subheading'}).get_text()
                    except:
                        sub = ''
                        pass
                    tit_art = re.sub('[^A-Za-z0-9]+', '', title)
                    output = outpath+tit_art[:20]+'.txt'
                    if os.path.exists(output):
                        print('Esiste già un file con questo nome, elimino il file esistente')
                        os.remove(output)
                    art = title+ '\n'+ sub+ '\n'
                    f = open(output, "w", encoding="utf-8")
                    f.write(art)
                    f.close()
                    for i in article:
                        b = i.get_text()
                        f_txt= open(output,"a", encoding="utf-8")
                        f_txt.write(b)
                        f_txt.write("\n")
                        f_txt.close()
                    j += 1
                    time.sleep(0.1)
                    printProgressBar(j, l, prefix = 'Progress:', suffix = 'Completi: '+ str(j) + '/'+ str(l) +'''
''', length = 100)
                elif 'stampa.it' in url:
                    for y in soup.findAll("aside"): 
                        y.decompose()
                    for y in soup.findAll("a"):
                        y.decompose()
                    for x in soup.findAll("footer", attrs = {'class':'main-footer'}):
                        x.decompose()
                    for y in soup.findAll("blockquote"): 
                        y.decompose()
                    #for y in soup.findAll("span"): 
                        #y.decompose()
                    span = soup.findAll('span')
                    try:
                        title = soup.find('h1', attrs={'class':'entry__title'}).get_text()
                        p = re.match('[a-zA-Z]',title)
                        if not p :
                            title = soup.find('h1').get_text()
                    except:
                        try:
                            title = soup.find('h1').get_text()
                        except:
                            title = ' '
                    if 'topnews' not in url:
                        for y in span:
                            yt = str(y)
                            if '<span>"' in yt:
                            
                                pass
                            else:
                                y.decompose()
                    for y in soup.findAll("h1"): 
                        y.decompose()
                    for y in soup.findAll('div', attrs ={'class':'inline-embed'}):
                        y.decompose()
                    article = soup.findAll('div',attrs ={'class':'entry__content'})

                    text = ''
                    for i in article:
                        a = i.get_text()
                        text = text + a + '\n'
                    
                    p = re.match('[a-zA-Z]',text)
                    if not p :
                        article = soup.findAll('div',attrs ={'class':'article-body'})
                        text = ''
                        for i in article:
                            a = i.get_text()
                            text = text + a + '\n'
                        p = re.match('[a-zA-Z]',text)
                    if not p :
                        article = soup.findAll('p')
                        text = ''
                        for i in article:
                            a = i.get_text()
                            text = text + a + '\n'
                    
                    try:
                        subtitle = soup.find('p', attrs={'class':'entry__subtitle'}).get_text()

                    except:
                       subtitle = ' '
                    
                    pos1 = text.find('...\n')
                    if pos1 != -1:
                        pos_n = pos1+3
                        text = text[pos_n:]
                        
                    
                    tit_art = re.sub('[^A-Za-z0-9]+', '', title)
                    output = outpath+tit_art[:20]+'.txt'
                    if os.path.exists(output):
                        print('Esiste già un file con questo nome, elimino il file esistente')
                        os.remove(output)
                    art = title+ '\n'
                    try:
                        art = art+ subtitle+ '\n'
                    except:
                        pass
                    art = art + text
                    f = open(output, "w", encoding="utf-8")
                    f.write(art)
                    f.close()
                    j += 1
                    time.sleep(0.1)
                    printProgressBar(j, l, prefix = 'Progress:', suffix = 'Completi: '+ str(j) + '/'+ str(l) +'''
''', length = 100)
        
                elif 'corriere.it' in url:
                    a.download()
                    a.parse()
                    for y in soup.findAll("aside", attrs ={'class':'inline-article'}): 
                        y.decompose()
                    for y in soup.findAll("aside"): 
                        y.decompose()
                    for y in soup.findAll("a"): 
                        y.decompose()
                    for x in soup.findAll("footer"):
                        x.decompose()
                    for y in soup.findAll("h5"): 
                        y.decompose()
                    for y in soup.findAll("blockquote"): 
                        y.decompose()
                    span = soup.findAll('span')
                    try:
                        title = soup.find('h1').get_text()
                    except:
                        title = ' '
                    try:
                        aut = soup.find('h3', attrs = {'class':'article-signature'} ).get_text()
                    except:
                        pass
                    
                    for y in soup.findAll("h3"): 
                        y.decompose()
                    for y in span:
                        yt = str(y)
                        if 'class="bold"' in yt:
                            pass
                        else:
                            y.decompose()
                    article = soup.findAll('div', attrs ={'class':'chapter'})
                    text = ' '
                    for i in article:
                        b = i.get_text()
                        text = text + b + '\n'
                    try:
                        subtitle = soup.find('p', attrs={'class':'subheading'}).get_text()
                    except:
                        subtitle = ''
                    tit_art = re.sub('[^A-Za-z0-9]+', '', title)
                    output = outpath+tit_art[:20]+'.txt'
                    if os.path.exists(output):
                        print('Esiste già un file con questo nome, elimino il file esistente')
                        os.remove(output)
                    art = title+ '\n'
                    try:
                        art = art+ subtitle+ '\n'
                    except:
                        pass
                    try:
                        art = art+ aut+ '\n'
                    except:
                        pass
                    t = a.text
                    art = art + t
                    f = open(output, "w", encoding="utf-8")
                    f.write(art)
                    f.close()
                    j += 1
                    time.sleep(0.1)
                    printProgressBar(j, l, prefix = 'Progress:', suffix = 'Completi: '+ str(j) + '/'+ str(l) +'''
''', length = 100)
                elif 'fattoquotidiano' in url:
                    for y in soup.findAll("aside"): 
                        y.decompose()
                    for y in soup.findAll("a"):
                        y.decompose()
                    for x in soup.findAll("footer", attrs = {'class':'main-footer'}):
                        x.decompose()
                    for y in soup.findAll("blockquote"): 
                        y.decompose()
                    for y in soup.findAll('div', attrs = {'class':'subscription-wrapper'}):
                        y.decompose()
                    for y in soup.findAll('div', attrs = {'class': 'content footer'}):
                        y.decompose()
                    span = soup.findAll('span')
                    for y in soup.findAll('div', attrs = {'class':'article-ifq-bottom-pro-sostenitore-wrapper'}):
                        y.decompose()
                    for y in soup.findAll('div', attrs = {'class':'disquis'}):
                        y.decompose()
                    for y in soup.findAll('div', attrs = {'class':'footer-copyright'}):
                        y.decompose()
                    try:
                        title = soup.find('h1', attrs={'class':'title-article'}).get_text()
                        p = re.match('[a-zA-Z]',title)
                        if not p :
                            title = soup.find('h1').get_text()
                    except:
                        try:
                            title = soup.find('h1').get_text()
                        except:
                            title = ' '
                    

                    text = ''

                    article = soup.findAll('section',attrs ={'class':'article-content'})
                    try:
                       subtitle = soup.find('div', attrs={'class':'catenaccio'}).get_text()

                    except:
                        pass
                    text = ''
                    for i in article:
                        a = i.get_text()
                        text = text + a + '\n'
                    p = re.match('[a-zA-Z]',text)
                    if not p :
                        article = soup.findAll('p')
                        text = ''
                        for i in article:
                            a = i.get_text()
                            text = text + a + '\n'
                        subtitle = ' '
                    pos1 = text.find('[…]\n')
                    if pos1 != -1:
                        pos_n = pos1+3
                        text = text[pos_n:]
                    tit_art = re.sub('[^A-Za-z0-9]+', '', title)
                    output = outpath+tit_art[:20]+'.txt'
                    if os.path.exists(output):
                        print('Esiste già un file con questo nome, elimino il file esistente')
                        os.remove(output)
                    art = title+ '\n'
                    try:
                        art = art+ subtitle+ '\n'
                    except:
                        pass
                    art = art + text
                    f = open(output, "w", encoding="utf-8")
                    f.write(art)
                    f.close()
                    j += 1
                    time.sleep(0.1)
                    printProgressBar(j, l, prefix = 'Progress:', suffix = 'Completi: '+ str(j) + '/'+ str(l) +'''
''', length = 100)
                elif 'ilgiornale' in url:
                    try:
                        aut = soup.find('span', attrs = {'class':'author-ref'}).get_text()
                    except:
                        pass
                    for y in soup.findAll("aside"): 
                        y.decompose()
                    for y in soup.findAll("a"):
                        y.decompose()
                    for x in soup.findAll("footer", attrs = {'class':'main-footer'}):
                        x.decompose()
                    for y in soup.findAll("blockquote"): 
                        y.decompose()
                    for y in soup.findAll('div', attrs = {'class':'subscription-wrapper'}):
                        y.decompose()
                    for y in soup.findAll('div', attrs = {'class': 'content footer'}):
                        y.decompose()
                    span = soup.findAll('span')
                    try:
                        title = soup.find('h1', attrs={'class':'title-article'}).get_text()
                        p = re.match('[a-zA-Z]',title)
                        if not p :
                            title = soup.find('h1').get_text()
                    except:
                        try:
                            title = soup.find('h1').get_text()
                        except:
                            title = ' '
                    try:
                        aut = soup.find('span', attrs = {'class':'author-ref'}).get_text()
                    except:
                        aut = ' '
                    text = ''

                    article = soup.findAll('section',attrs ={'class':'article-content'})
                    try:
                       subtitle = soup.find('div', attrs={'class':'catenaccio'}).get_text()

                    except:
                        pass
                    text = ''
                    for i in article:
                        a = i.get_text()
                        text = text + a + '\n'
                    p = re.match('[a-zA-Z]',text)
                    if not p :
                        article = soup.findAll('p')
                        text = ''
                        for i in article:
                            a = i.get_text()
                            text = text + a + '\n'
                        subtitle = ' '
                    tit_art = re.sub('[^A-Za-z0-9]+', '', title)
                    output = outpath+tit_art[:20]+'.txt'
                    if os.path.exists(output):
                        print('Esiste già un file con questo nome, elimino il file esistente')
                        os.remove(output)
                    art = title+ '\n'
                    try:
                        art = art+ subtitle+ '\n'
                    except:
                        pass
                    try:
                        art = art+ aut+ '\n'
                    except:
                        pass
                    art = art + text
                    f = open(output, "w", encoding="utf-8")
                    f.write(art)
                    f.close()
                    j += 1
                    time.sleep(0.1)
                    printProgressBar(j, l, prefix = 'Progress:', suffix = 'Completi: '+ str(j) + '/'+ str(l) +'''
''', length = 100)
                elif 'ilmessaggero' in url:

                    for y in soup.findAll("aside"): 
                        y.decompose()
                    for y in soup.findAll("div", attrs =  {'class':'link_snippet'}):
                        y.decompose()
                    for y in soup.findAll("div", attrs =  {'class':'snippet_titolo'}):
                        y.decompose()
                    for y in soup.findAll("a", attrs =  {'class':'link_item'}):
                        y.decompose()
                    for x in soup.findAll("footer", attrs = {'class':'main-footer'}):
                        x.decompose()
                    for y in soup.findAll("blockquote"): 
                        y.decompose()
                    for y in soup.findAll('div', attrs = {'class':'subscription-wrapper'}):
                        y.decompose()
                    for y in soup.findAll('div', attrs = {'class': 'content footer'}):
                        y.decompose()
                    
                    try:
                        title = soup.find('h1', attrs={'class':'title-article'}).get_text()
                        p = re.match('[a-zA-Z]',title)
                        if not p :
                            title = soup.find('h1').get_text()
                    except:
                        try:
                            title = soup.find('h1').get_text()
                        except:
                            title = ' '
                    text = ''

                    article = soup.findAll('div',attrs ={'class':'body-text'})
                    
                    text = ''
                    for i in article:
                        a = i.get_text(separator=' ')
                        text = text + a + '\n'
                    p = re.match('[a-zA-Z]',text)
                    if not p :
                        article = soup.findAll('p')
                        text = ''
                        for i in article:
                            a = i.get_text(separator = ' ').strip()
                            text = text + a + '\n'
                    tit_art = re.sub('[^A-Za-z0-9]+', '', title)
                    output = outpath+tit_art[:20]+'.txt'
                    if os.path.exists(output):
                        print('Esiste già un file con questo nome, elimino il file esistente')
                        os.remove(output)
                    art = title+ '\n' + text
                    f = open(output, "w", encoding="utf-8")
                    f.write(art)
                    f.close()
                    j += 1
                    time.sleep(0.1)
                    printProgressBar(j, l, prefix = 'Progress:', suffix = 'Completi: '+ str(j) + '/'+ str(l) +'''
''', length = 100)
                else:
                    pass
            print("Operazione completata! I file verranno rinominati col numero di token all'inizio")
            try:
                from nltk.probability import FreqDist
                
                w = 0
                le = len(os.listdir(outpath))
                printProgressBar(0, le, prefix = 'Progress:', suffix = 'Completi: '+ str(w) + '/'+ str(le) +'''
''', length = 100)
                
                for file in os.listdir(outpath):
                    if file.endswith(".txt"):    
                        raw_txt = open(outpath+'/'+file, encoding = 'utf-8').read()
                        tokenized = nltk.word_tokenize(raw_txt, language = 'italian')
                        fdist = FreqDist(tokenized)
                        num = str(int((fdist.N())))                
                        os.rename(outpath+file, outpath+num+'_'+file)
                        w +=1
                        time.sleep(0.1)
                        printProgressBar(w, le, prefix = 'Progress:', suffix = 'Completi: '+ str(w) + '/'+ str(le) +'''
''', length = 100)
            except:
                print('''

Per contare i token, scarica "book" dalla finestra (Nltk downloader) che si è aperta!!! (NON E' NECESSARIO SE LO HAI GIA' FATTO UNA VOLTA)
Per andare avanti, al termine del download, chiudi la finestra Nltk Downloader

''')
                try:
                    _create_unverified_https_context = ssl._create_unverified_context
                except AttributeError:
                    pass
                
                else:
                    ssl._create_default_https_context = _create_unverified_https_context
                nltk.download()
                from nltk.probability import FreqDist
                try:
                    w = 0
                    le = len(os.listdir(outpath))
                    printProgressBar(0, le, prefix = 'Progress:', suffix = 'Completi: '+ str(w) + '/'+ str(le) +'''
''', length = 100)
                except:
                    pass
                for file in os.listdir(outpath):
                    if file.endswith(".txt"):    
                        raw_txt = open(outpath+'/'+file, encoding = 'utf-8').read()
                        tokenized = nltk.word_tokenize(raw_txt, language = 'italian')
                        fdist = FreqDist(tokenized)
                        num = str(int(fdist.N()))                
                        os.rename(outpath+file, outpath+num+'_'+file)
                        w +=1
                        time.sleep(0.1)
                        printProgressBar(w, le, prefix = 'Progress:', suffix = 'Completi: '+ str(w) + '/'+ str(le) +'''
''', length = 100)
            
            print('Controllo i file che potrebbero contenere elementi da pulire (verranno rinominati con ATTENTO all\'inizio')
            prog = 0
            leng = len(os.listdir(outpath))
            printProgressBar(0, leng, prefix = 'Progress:', suffix = 'Completi: '+ str(w) + '/'+ str(le) +'''
''', length = 100)
            count = 1
            path = outpath
            for file in os.listdir(outpath):
                if file.endswith(".txt"):    
                    f = open(path+'/'+file, encoding = 'utf-8')
                    text = f.read()
                    if 'LEGGI' in text:
                        print(count, file)
                        f.close()
                        os.rename(path+file, path+'ATTENTO'+'_'+file)
                        count +=1
                        prog +=1
                    elif 'Leggi anche' in text:
                        
                        print(count, file)
                        f.close()
                        os.rename(path+file, path+'ATTENTO'+'_'+file)
                        count +=1
                        prog +=1
                    elif 'Leggi ' in text:
                        
                        print(count, file)
                        f.close()
                        os.rename(path+file, path+'ATTENTO'+'_'+file)
                        count +=1
                        prog +=1
                    elif 'Guarda ' in text:
                        
                        print(count, file)
                        f.close()
                        os.rename(path+file, path+'ATTENTO'+'_'+file)
                        count +=1
                        prog +=1
                    elif 'GUARDA' in text:
                        print(count, file)
                        f.close()
                        os.rename(path+file, path+'ATTENTO'+'_'+file)
                        count +=1
                        prog +=1
                    elif 'REP' in text:
                        print(count, file)
                        f.close()
                        os.rename(path+file, path+'ATTENTO'+'_'+file)
                        count +=1
                        prog +=1
                    elif 'FOTO' in text:
                        print(count, file)
                        f.close()
                        os.rename(path+file, path+'ATTENTO'+'_'+file)
                        count +=1
                        prog +=1
                    elif '--»»' in text:
                        print(count, file)
                        f.close()
                        os.rename(path+file, path+'ATTENTO'+'_'+file)
                        count +=1
                        prog +=1
                    elif 'INTERVISTA'in text:
                        print(count, file)
                        f.close()
                        os.rename(path+file, path+'ATTENTO'+'_'+file)
                        count +=1
                        prog +=1
                    elif 'VIDEO' in text:
                        print(count, file)
                        f.close()
                        os.rename(path+file, path+'ATTENTO'+'_'+file)
                        count +=1
                        prog +=1
                    elif 'APPROFONDIMENT' in text:
                        print(count, file)
                        f.close()
                        os.rename(path+file, path+'ATTENTO'+'_'+file)
                        count +=1
                        prog +=1
                    elif 'ISCRIVITI' in text:
                        print(count, file)
                        f.close()
                        os.rename(path+file, path+'ATTENTO'+'_'+file)
                        count +=1
                        prog +=1
                    elif 'Iscriviti' in text:
                        print(count, file)
                        f.close()
                        os.rename(path+file, path+'ATTENTO'+'_'+file)
                        count +=1
                        prog +=1
                    elif 'GRAFICI' in text:
                        print(count, file)
                        f.close()
                        os.rename(path+file, path+'ATTENTO'+'_'+file)
                        count +=1
                        prog +=1
                    elif 'GRAFICO' in text:
                        
                        print(count, file)
                        f.close()
                        os.rename(path+file, path+'ATTENTO'+'_'+file)
                        count +=1
                        prog +=1
                    elif 'SCHED' in text:
                        print(count, file)
                        f.close()
                        os.rename(path+file, path+'ATTENTO'+'_'+file)
                        count +=1
                        prog +=1
                    elif 'SEGUI' in text:
                        print(count, file)
                        f.close()
                        os.rename(path+file, path+'ATTENTO'+'_'+file)
                        count +=1
                        prog +=1
                    elif 'CALCOLA' in text:
                        print(count, file)
                        f.close()
                        os.rename(path+file, path+'ATTENTO'+'_'+file)
                        count +=1
                        prog +=1
                    elif 'ECCO' in text:
                        print(count, file)
                        f.close()
                        os.rename(path+file, path+'ATTENTO'+'_'+file)
                        count +=1
                        prog +=1
                    elif 'TABELLE'in text:
                        print(count, file)
                        f.close()
                        os.rename(path+file, path+'ATTENTO'+'_'+file)
                        count +=1
                        prog +=1
                    elif 'LE PREVISIONI ' in text:
                        print(count, file)
                        f.close()
                        os.rename(path+file, path+'ATTENTO'+'_'+file)
                        count +=1
                        prog +=1
                    else:
                        prog +=1
                    time.sleep(0.1)
                    printProgressBar(prog, leng, prefix = 'Progress:', suffix = 'Completi: '+ str(w) + '/'+ str(le) +'''
''', length = 100)
            sys.exit()
        scrape(downlink)
text()
