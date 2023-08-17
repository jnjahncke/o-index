#!/usr/bin/env python

import numpy as np
import pandas as pd

import requests
from bs4 import BeautifulSoup
from re import *

# Get PMCID from PMID
def get_pmcid_year(pmid):
    base_url = f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"
    response = requests.get(base_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    date = soup.find_all('span', {'class' : 'cit'})[0].text.strip()
    date = split("\D", date)[0]
    try:
        pmcid = soup.find_all('a', {'class' : 'id-link', 'data-ga-action' : 'PMCID'})[0].text.strip()
    except:
        pmcid = None
    return (pmcid , date)


# Get PMIDs, Openness from author name
def get_pmids_open(author):
    
    # Parse author name, build first+last
    author = author.split()
    if len(author) > 1:
        aname = author[0]
        for name in author[1:]:
            aname += "+" + name
    else:
        aname = author[0]
        
    #find total number of pages
    base_url= f'https://pubmed.ncbi.nlm.nih.gov/?term={aname}&page='
    response = requests.get(base_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    pages = soup.find_all('label', {'class' : 'of-total-pages'})
    p = pages[0].text.strip()
    p = p.split()
    pagenum=int(p[1])
    
    # scrape pubmed
    pmids = []
    entries = []
    for i in range(1,pagenum+1): #change # into max num of pages
        URL = f'https://pubmed.ncbi.nlm.nih.gov/?term={aname}&page={i}'
        response = requests.get(URL)
        soup = BeautifulSoup(response.content, 'html.parser')
        pmids = soup.find_all('span', {'class' : 'docsum-pmid'})
        entries = soup.find_all("div", {'class' : 'docsum-content'})
        titles = soup.find_all("a", {'class' : 'docsum-title'})
        journals = soup.find_all("span", {'class' : 'docsum-journal-citation short-journal-citation'})
    
    # build dictionary of id:pmcid
    ids = {}
    years = {}
    title_dict = {}
    journal_dict = {}
    for id,entry,title,journal in zip(pmids,entries,titles,journals):
        id = id.text.strip()
        pmcid, year = get_pmcid_year(id)
        years[id] = year
        title_dict[id] = title.text.strip()
        journal_dict[id] = split("\d", journal.text.strip())[0].strip()
        if pmcid:
            ids[id] = pmcid
        elif search(r"Free",entry.text.strip()): # use regex to search for "Free" in docsum-content
            ids[id] = "open"
        else:
            ids[id] = "closed"
        
    return ids, years, title_dict, journal_dict

def get_openness(author, api):
    ids, years, titles, journals = get_pmids_open(author)
    
    apikey = open(api, 'r').read()

    # Load keywords and create open-science categories
    keyword_df = pd.read_csv('keywords.csv')
    categoryIDs = np.unique(np.array(keyword_df['category']))
    category_descriptions = keyword_df['category_description']
    category_descriptions = category_descriptions.unique().tolist()
    full_text = 'full_text'
    category_descriptions.append(full_text)
    
    #create df with all the unique categories:
    data = (len(ids), len(category_descriptions))

    #data = (len(ids), len(category_descriptions))
    o_idx_df = pd.DataFrame(np.zeros(data), columns = category_descriptions)
    #deleting the 'code relevant column from the final df
    pmcids = []
    for i, item in enumerate(ids): 
        o_idx_df.loc[[i],['pmid']] = item
        o_idx_df.loc[[i],['year']] = years[item]
        o_idx_df.loc[[i],['journal']] = journals[item]
        o_idx_df.loc[[i],['title']] = titles[item]
        if ids[item] == 'closed':
            pmcids.append(None)
            #if PMCID is unavailable make items in df None type
            o_idx_df.iloc[[i],0:2] = None
            continue
        if ids[item] == 'open':
            pmcids.append(None)
            o_idx_df.loc[[i],['full_text']] = 1
            o_idx_df.iloc[[i],0:2] = None

        else:
            pmcids.append(ids[item])
            o_idx_df.loc[[i],['full_text']] = 1
    db = 'pmc'
    base = 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?'
    for j, pmcid in enumerate(pmcids):
        if pmcid == None:
            continue
        s = '{:s}db={:s}&id={:s}'.format(base, db, pmcid, apikey)
        out = requests.get(s)
        bs = BeautifulSoup(out.content, features="xml")
        # Check if full text is available; if not - move to the next paper
        for cat in categoryIDs:
            found_keyword = False
            # Loop through specific keywords related to each open-science category
            for k, keyword in enumerate(keyword_df['keyword'][keyword_df['category'] == cat]):
                for s in finditer(keyword, out.text, IGNORECASE):
                    #if we are on cat "code relevant" (cat 3) we are testing to see if code is relevant for this paper
                    o_idx_df.iloc[[j],[cat-1]] = keyword_df.loc[k]["weight"]
                    found_keyword = True

                # If one keyword is found, stop with searching for this category
                if found_keyword is True:
                    break
            #if code category is 0, check to see if code is relevant
            if cat == 2 and found_keyword== True:
                break 
            if cat == 3 and found_keyword == False:
                o_idx_df.iloc[[j],[cat-2]] = None
                break    
                
    del o_idx_df['code_relevant']

    o_idx_df.loc[:,'o-score'] = o_idx_df.mean(numeric_only=True, axis=1)

    return o_idx_df

def oindex(df):
    OIndex = df["o-score"].mean()
    return OIndex
    

def main():

    print(get_openness("jennifer jahncke", "apikey.txt"))

if __name__ == '__main__':
    main()
