# -*- coding: utf-8 -*-
"""
Created on Mon May 18 17:58:33 2020

@author: qihus
"""
## Git repo : https://github.com/HoussamSlk/FeedCleaner_Regex
import pandas as pd
import datetime
import re
from db_connector import *

#Reading the datafile and storing it in a variable
feed = pd.read_csv("C:/Users/qihus/Downloads/out_2020.06.11 feed file 97.csv")
DR_startups = pd.read_csv("C:/Users/qihus/Desktop/Duplicate_URL Project/companies_20_05_20_1589966891.csv")
DR_investors = pd.read_csv('C:/Users/qihus/Desktop/my Notes/allinvestors 04062020.csv')
###############################################################################
############################################################
#change the form startups are written in
from progressbar import ProgressBar
pbar = ProgressBar()
for i in pbar(range(len(DR_startups))):
    co_name= str(DR_startups.iloc[i,0]) 
    co_name = co_name[0]+co_name[1:len(co_name)].lower()
    DR_startups.iloc[i,0] = co_name
###############################################################################
DR_startups_data = DR_startups 
DR_investors_data = DR_investors
DR_startups = list(DR_startups['NAME'])
DR_investors = list(DR_investors['NAME'])
#############################################################
def is_startup(word):
    return word in DR_startups
##############################################################################
def is_investor(word):
    return word in DR_investors
############################################################
def get_dr_url(startup):
    url_row = DR_startups_data[DR_startups_data.NAME == startup]
    url = url_row['PROFILE URL'].values[0]
    return url
##############################################################
def get_dr_url_investor(investor):
    url_row = DR_investors_data[DR_investors_data.NAME == investor]
    url = url_row['PROFILE URL'].values[0]
    return url
################################################################
def currency_finder(word):
    if '$' in word:
        return 'USD'
    if '€' in word:
        return 'EUR'
    if '£' in word:
        return 'GBP'
    if '₩' in word:
        return 'KRW'
    if ('kronor' or 'SEK') in word:
        return 'SEK'
    if ('euros' or 'euro' or 'EUR') in word:
        return 'EUR'
    if ('dollar' or 'USD') in word:
        return 'USD'
    if 'GBP' in word:
        return 'GBP'
    if 'JPY' in word:
        return 'JPY'
    if 'KRW' in word:
        return 'KRW'
    if 'CNY' in word:
        return 'CNY'
    if 'CHF' in word:
        return 'CHF'
    ############################################################
def nextword(target, source):
    for i, w in enumerate(source):
        if w == target and i<len(source)-1:
            return source[i+1]
        else:
            return ""
      
###############################################################################
def amount_patterns(a_string):
    amount = 0
    amount_M = 0
    pattern_0 =r'\d+\.?\d{0,2} [mM]illion'
    pattern_1 = r'[$€£]{1}\d+\.?\d{0,2}[k]'
    pattern_2 = r'[$€£]{1}\d{1,} million'
    pattern_3 = r'\d{1,} million'
    pattern_4 = r'\d{1,} miljoner kronor'
    pattern_5 = r'[0-9]{6,} euro'
    pattern_6 = r'[$€£]\d+\,\d{0,3}'
    pattern_7 = r'[$€£]{1}\d+\.\d{0,2}'
    pattern_8 = r'[$€£]{1}\d+\.?\d{0,2}[mM]'
    pattern_9 = r'\d{1,},\d{1,} million'
    pattern_10 = r'\d+\.?\d{0,2}\s?[mM][$€£]{1}'
    pattern_11 = r'\d+\.?\d{0,2}\s?[k][$€£]{1}'
    match_0 = re.search(pattern_0, a_string)
    match_1 = re.search(pattern_1, a_string)
    match_2 = re.search(pattern_2, a_string)
    match_3 = re.search(pattern_3, a_string)
    match_4 = re.search(pattern_4, a_string)
    match_5 = re.search(pattern_5, a_string)
    match_6 = re.search(pattern_6, a_string)
    match_7 = re.search(pattern_7, a_string)
    match_8 = re.search(pattern_8, a_string)
    match_9 = re.search(pattern_9, a_string)
    match_10 = re.search(pattern_10, a_string)
    match_11 = re.search(pattern_11, a_string)
    if match_0:
        amount = match_0.group()
        amount_M = amount[:-8]
        return amount_M
    if match_1:
        amount = match_1.group()
        amount = int(amount[1:-1])
        amount_M = amount/1000
        return amount_M 
    if match_2:
        amount = match_2.group()
        amount_M = amount[1:-8]
        return amount_M
    if match_3:
        amount = match_3.group()
        amount_M = amount[:-8]
        return amount_M
    if match_4:
        amount = match_4.group()
        amount_M = amount[:-16]
        return amount_M
    if match_5:
        amount = match_5.group()
        amount = int(amount[:-5])
        amount_M = amount / 1000000
        return amount_M
    if match_6:
        amount = match_6.group()
        amount = amount[1:]
        amount_M = amount.replace(',','.')
        return amount_M
    if match_7:
        amount = match_7.group()
        amount_M = amount[1:]
        return amount_M
    if match_8:
        amount = match_8.group()
        amount_M = amount[1:-1]
        return amount_M
    if match_9:
        amount = match_9.group()
        amount_M = amount[:-8]
        return amount_M
    if match_10:
        amount = match_10.group()
        amount_M = amount[:-2]
        return amount_M
    if match_11:
        amount = match_11.group()
        amount.replace(" ", "")
        amount = int(amount[:-2])
        amount_M = amount/1000
        return amount_M
##############################################################################
def round_type(a_string):
    acquisition = ['acquires', 'acquired', 'buys', 'bought', 'akquisitionen', 'übernimmt',\
                   'sväljer', 'köper', 'säljer', 'overname', 'neem', 'nam', 'overgenomen', \
                       'koopt', 'gekocht', 'verkoopt', 'verkocht','purchased']
    series_a = ['series a', 'Series A']
    series_b = ['series b', 'Series B']
    series_c = ['series c', 'Series C']
    series_d = ['series d', 'Series D']
    series_e = ['series e', 'Series E']
    series_f = ['series f', 'Series F']
    series_g = ['series g', 'Series G']
    series_h = ['series h', 'Series H']
    series_i = ['series i', 'Series I']
    ipo = ['IPO', 'public offering', 'to list', 'floats']
    grant = ['grant','Grant']
    seed = ['seed','SEED']
    if any(word in a_string for word in acquisition):
        return 'ACQUISITION'
    if any(word in a_string for word in series_a):
        return 'SERIES A'
    if any(word in a_string for word in series_b):
        return 'SERIES B'
    if any(word in a_string for word in series_c):
        return 'SERIES C'
    if any(word in a_string for word in series_d):
        return 'SERIES D'
    if any(word in a_string for word in series_e):
        return 'SERIES E'
    if any(word in a_string for word in series_f):
        return 'SERIES F'
    if any(word in a_string for word in series_g):
        return 'SERIES G'
    if any(word in a_string for word in series_h):
        return 'SERIES H'
    if any(word in a_string for word in series_i):
        return 'SERIES I'
    if any(word in a_string for word in ipo):
        return 'IPO'
    if any(word in a_string for word in grant):
        return 'GRANT'
    if any(word in a_string for word in seed):
        return 'SEED'
###############################################################################
def round_type_by_amount(amount):
    if (type(amount) == str)and (amount == ''): #if amount if empty
        return 'EARLY VC'
    else:
        amount = float(amount)
        if (amount == 0)  or  ((amount >= 1)and (amount < 10)):
            return 'EARLY VC'
        if amount < 1:
            return 'SEED'
        if amount >= 10:
            return 'LATE VC'
###############################################################################
def round_exists(startup_name,month,year,amount,currency):
    #API function
    return 0 
    
###############################################################################
def filling_report(df):
    filesize = len(df)
    filled_startups = len(df[df.Out_name !=''])
    filled_investors = len(df[df.Out_investors !=''])
    print("file processed successfully ...")
    print('Total size is {0} '.format(filesize))
    print('{0} % of start-ups names were identified total of {1} rows'\
          .format(filled_startups/filesize*100,filled_startups))
    print('{0} % of investors were identified total of {1} rows'\
          .format(filled_investors/filesize*100,filled_investors))
###############################################################################        
###########DF Related functions################################################
###########functions that takes DF and returns a news DF with results #########
###############################################################################
def company_name (df):
    data = df #store input dataframe in a variable  
    titles = list(df['TITLE'])
    skip_word = ['Funding' , 'Collective' , 'Round' , 'Count' , 'Provider',\
             'Amazon','Facebook','The', 'Engine', 'Data','Note', 'Young', \
            'Healthcare','Foundation', 'New' ,'Now' , 'This', 'Million', 'Open' , \
                'Teams','After' ,'Capital' , '39', '100' , '54' , 'Acquire', \
                    'Air','Raise', 'Ceo','Company', 'Daily','Extra',\
                        'Startup','Top','Up','Vc','With','Venture','Saas', \
                            'Initial','Inc','United','rais','Parent','Takes',\
                            'Artificial','Tv','Electric','Emerging','South','Run',\
                                'Property','Clean','Tech','Ok','Special','Voice','Energy',\
                                    'Facility','Gas','Virtual','Android','Jeff']
    pbar = ProgressBar()
    for title in pbar(titles):
        title = str(title)
        startup_name = startup_dr_url =  ""
        for word in title.split():
            next_word = nextword(word,title.split())
            word = word[0]+word[1:len(word)].lower()
            if word in skip_word or word.isdigit():
                continue
            if word[0].isupper() or word[0].isdigit():
                if (is_startup(word)):
                    if (startup_name == ""):
                        startup_name = word
                        startup_dr_url = get_dr_url(startup_name)
                if '.' in word and startup_name == "":
                    splited_word=word.split('.')
                    splited_word=splited_word[0]
                    if (is_startup(splited_word)):
                        startup_name = splited_word
                        startup_dr_url = get_dr_url(startup_name)
                    #some companies with two words we have them in our database as one word
                    splited_word=word.split('.')
                    splited_word=splited_word[0]+' '+splited_word[1]
                    if (is_startup(splited_word)):
                        startup_name = splited_word
                        startup_dr_url = get_dr_url(startup_name)
                if startup_name == "":
                    two_words = word+' '+next_word
                    two_words = two_words[0]+two_words[1:len(two_words)].lower()
                    if(is_startup(two_words)):
                        startup_name = two_words
                        startup_dr_url = get_dr_url(two_words)
    
        data.loc[data.TITLE == title, 'Out_name'] = startup_name
        data.loc[data.TITLE == title, 'Out_url'] = startup_dr_url
        if data.loc[data.TITLE == title, 'Out_name'].item() == '':
            startup_name_list = [word for word in DR_startups if word in title]
            startup_name_list = [x for x in startup_name_list if x not in skip_word ]
            if startup_name_list:
                max_name = max(startup_name_list, key=len)
                if (re.search(r'\b({0})\b'.format(max_name),title) and len(max_name)>2 \
                    and max_name not in skip_word):
                    startup_name = max_name
                    startup_dr_url = get_dr_url(startup_name)
                    data.loc[data.TITLE == title, 'Out_name'] = startup_name
                    data.loc[data.TITLE == title, 'Out_url'] = startup_dr_url
    return data
    
###############################################################################
def get_date(df):
    data = df
    data['Out_year'] = pd.DatetimeIndex(data['DATE']).year
    data['Out_month'] = pd.DatetimeIndex(data['DATE']).month
    return data
###############################################################################
def get_currency(df):
    data = df #store input dataframe in a variable  
    titles = list(df['TITLE'])
    pbar = ProgressBar()
    for title in pbar(titles):
        title = str(title)
        currency =  ""
        if(currency_finder(title)):
            currency = currency_finder(title)
            
        data.loc[data.TITLE == title, 'Out_currency'] = currency
    contents = list(df['CONTENT'])
    pbar = ProgressBar()
    for content in pbar(contents):
        content = str(content)
        currency =  ""
        if len(data.loc[(data.CONTENT == content) & (data.Out_currency=='')]) != 0:
            currency = currency_finder(content)
            data.loc[data.CONTENT == content, 'Out_currency'] = currency
    return data

################################################################################
def get_amount(df):
    data = df
    titles = list(df['TITLE'])
    pbar = ProgressBar()
    for title in pbar(titles):
        title = str(title)
        amount = ""
        if(amount_patterns(title)):
            amount = amount_patterns(title)
        data.loc[data.TITLE == title, 'Out_amount'] = amount
    contents = list(df['CONTENT'])
    pbar = ProgressBar()
    for content in pbar(contents):
        content = str(content)
        amount = ""
        if len(data.loc[(data.CONTENT == content) & (data.Out_amount=='')]) != 0:
               amount = amount_patterns(content)
               data.loc[data.CONTENT == content, 'Out_amount'] = amount
    return data
###############################################################################
def get_round_type(df):
    data = df
    titles = list(df['TITLE'])
    pbar = ProgressBar()
    for title in pbar(titles):
        title = str(title)
        content = str(data.loc[data.TITLE == title, 'CONTENT'].item())
        roundtype = "EARLY VC"
        if(round_type(title)):
            roundtype = round_type(title)
            data.loc[data.TITLE == title, 'Out_RoundType'] = roundtype   
        elif(round_type(content)):
            roundtype = round_type(content)
            data.loc[data.TITLE == title, 'Out_RoundType'] = roundtype
        else:
            amount = data.loc[data.TITLE == title, 'Out_amount'].item()
            if not amount:
                data.loc[data.TITLE == title, 'Out_RoundType'] = roundtype 
                continue
            amount = float(amount)
            roundtype = round_type_by_amount(amount)
            data.loc[data.TITLE == title, 'Out_RoundType'] = roundtype  
    return data
###############################################################################
def investor_name (df):
    data = df #store input dataframe in a variable  
    titles = list(df['TITLE'])
    skip_word = ['Investment','Class','Facebook','Get','ring','Raise',\
                 'VI','Late','Fintech','Science','3m','Impact','Virtu','M F','dsp',\
                         'Twitter','eir','iri','Win','Service','Tag','Ista' ,'Q4','FinSMEs',\
                             'Certain','MKB','Aer','Apple','Global','SAAS','Google',\
                                 'Amazon','Property','Kong','Join',\
                                     'Youtube','LinkedIn','Forbes','D', 'Investo']
    pbar = ProgressBar()
    for title in pbar(titles):
        title = str(title)
        content = str(data.loc[data.TITLE == title, 'CONTENT'].item())
        investors = []
        investors_url =[]
        investors_title = [word for word in DR_investors \
                     if word in title]
        investors_content = [word for word in DR_investors \
                             if word in content]
        investors = set([*investors_title, *investors_content])
        investors = [x for x in investors if x not in skip_word ]
        for investor in investors:
            investor_url = get_dr_url_investor(investor)
            investors_url.append(investor_url)
        investors = ','.join(map(str,investors))
        investors_url = '\n'.join(map(str,investors_url))
        
        data.loc[data.TITLE == title, 'Out_investors'] = investors
        data.loc[data.TITLE == title, 'Out_investors_url'] = investors_url
        
    return data
    
###############################################################################
def remove_duplicates(df):
    data = df 
    #preprocessing : removing rows with empty fields of company name , currency & amount
    #dropduplicates in pandas treat NAs are similar (duplicates) so to avoid removing rows 
    #that are not duplicates this step is essential  
    empty_fields = data.loc[(data.Out_name == '') | (data.Out_name.isna())]
    #to do : remove empty_fields from data
    data = data.drop_duplicates(subset=['Out_name', 'Out_currency','Out_amount'], keep='first')
    #possible_dup = data[data.duplicated(subset=['Out_name'],keep=False)]
    #possible_dup.to_csv("possible_dup.csv",index=False)
    data = data.append(empty_fields)
    data = data.drop_duplicates(subset ="ID", keep = 'first') 
    return data
## add colomun with 'duplicates to check'
###############################################################################

#NEW CODE INSIDE A FUNCTION
    #test function here : 
    
    #input_df = feed.copy()
    output = company_name(feed)
    output = get_date(output)
    output = get_currency(output)
    output = get_amount(output)
    output = get_round_type(output)
    output = investor_name(output)
    ##before report # function to flag the (not funding) T/F 
    ## articles that are not funding ; hint use col U V 
    report = filling_report(output)
    report = filling_report(input_df,output)
    cleaned = remove_duplicates(output)
    cleaned.to_csv("clean_out_2020.06.11 feed file 97.csv",index=False)
    output.to_csv("out_out_2020.06.11 feed file 97.csv",index=False)
    #run remove duplication here 
    #save result here , have two files 

