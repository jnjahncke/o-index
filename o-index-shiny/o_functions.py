#!/usr/bin/env python

import numpy as np
import pandas as pd
from collections import defaultdict

import requests
from bs4 import BeautifulSoup
from re import *
import os

# Get PMCID from PMID
def get_pmcid_year(pmid):
    base_url = f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"
    response = requests.get(base_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    date = soup.find_all('span', {'class' : 'cit'})[0].text.strip().split()[0]
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
            aname += "%" + name
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
        pmids += soup.find_all('span', {'class' : 'docsum-pmid'})
        entries += soup.find_all("div", class_='docsum-content')
    
    # build dictionary of id:pmcid
    ids = {}
    years = {}
    for id,entry in zip(pmids,entries):
        pmcid, year = get_pmcid_year(id.text.strip())
        years[id.text.strip()] = year
        if pmcid:
            ids[id.text.strip()] = pmcid
        elif search(r"Free",entry.text.strip()): # use regex to search for "Free" in docsum-content
            ids[id.text.strip()] = "open"
        else:
            ids[id.text.strip()] = "closed"
        
    return ids, years

def get_openness(author, api):
    ids, years = get_pmids_open(author)
    
    apikey = open(api, 'r').read()
    
    # Load keywords and create open-science categories
    terms = pd.read_csv('keywords.csv')
    categories = terms['category']
    category_descriptions = terms['category_description']
    categories_unique = np.unique(np.array(categories))
    category_descriptions = category_descriptions.unique().tolist()
    full_text = 'full_text'
    category_descriptions.append(full_text)
    
    #create df with all the unique categories:
    data = (len(ids), len(category_descriptions))
    o_idx_df = pd.DataFrame(np.zeros(data), columns = category_descriptions)
    
    df_list = [0] * len(category_descriptions)
    pmcids = []
    for i, item in enumerate(ids): 
        o_idx_df.loc[[i],['pmid']] = item
        o_idx_df.loc[[i],['year']] = years[item]
        if ids[item] == 'closed':
            continue
        if ids[item] == 'open':
            o_idx_df.loc[[i],['full_text']] = 1
        else:
            pmcids.append(ids[item])
            o_idx_df.loc[[i],['full_text']] = 1
            
    db = 'pmc'
    base = 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?'
    dict_term = defaultdict(list)
    fulfilled_categories = [0] * len(categories_unique)
    for j, pmcid in enumerate(pmcids):
        s = '{:s}db={:s}&id={:s}'.format(base, db, pmcid, apikey)
        out = requests.get(s)
        bs = BeautifulSoup(out.content, features="xml")
        # Check if full text is available; if not - move to the next paper
        for i, categoryInd in enumerate (categories_unique):
            found_keyword = False
            # Loop through specific keywords related to each open-science category
            for k,term in enumerate(terms['keyword'][terms['category'] == categoryInd]):
                for s in finditer(term, out.text, IGNORECASE):
                    o_idx_df.iloc[[j],[i]] = terms.loc[k]["weight"]
                    found_keyword = True

                # If one keyword is found, stop with searching for this category
                if found_keyword is True:
                    break
    
    return o_idx_df

def main():

    print(get_openness("jennifer jahncke", "apikey.txt"))

if __name__ == '__main__':
    main()
