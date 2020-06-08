#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 25 12:31:46 2020

@author: alexhawat
"""


import requests
from requests.auth import HTTPBasicAuth
import json
import pandas as pd


def get_all_fields():
    """ Get all fields available to use in fields_string of get_companies_bulk
    
    Returns: 
    
    list of string elements, each element a field
   
    Example:
    
    my_fields=get_all_fields()
     
    """
    
    fields_string='id,name,path,tagline,about,url,website_url,twitter_url,facebook_url,linkedin_url,google_url,crunchbase_url,angellist_url,playmarket_app_id,appstore_app_id,images,employees,employees_latest,industries,sub_industries,corporate_industries,service_industries,technologies,income_streams,growth_stage,traffic_summary,hq_locations,tg_locations,client_focus,revenues,tags,payments,achievements,delivery_method,launch_year,launch_month,has_strong_founder,has_super_founder,total_funding,total_funding_source,last_funding,last_funding_source,company_status,last_updated,last_updated_utc,facebook_likes_chart,alexa_rank_chart,twitter_tweets_chart,twitter_followers_chart,twitter_favorites_chart,employees_chart,similarweb_3_months_growth_unique,similarweb_3_months_growth_percentile,similarweb_3_months_growth_relative,similarweb_3_months_growth_delta,similarweb_6_months_growth_unique,similarweb_6_months_growth_percentile,similarweb_6_months_growth_relative,similarweb_6_months_growth_delta,similarweb_12_months_growth_unique,similarweb_12_months_growth_percentile,similarweb_12_months_growth_relative,similarweb_12_months_growth_delta,app_3_months_growth_unique,app_3_months_growth_percentile,app_3_months_growth_relative,pp_6_months_growth_unique,app_6_months_growth_percentile,app_6_months_growth_relative,app_12_months_growth_unique,app_12_months_growth_percentile,app_12_months_growth_relative,employee_3_months_growth_unique,employee_3_months_growth_percentile,employee_3_months_growth_relative,employee_3_months_growth_delta,employee_6_months_growth_unique,employee_6_months_growth_percentile,employee_6_months_growth_relative,employee_6_months_growth_delta,employee_12_months_growth_unique,employee_12_months_growth_percentile,employee_12_months_growth_relative,employee_12_months_growth_delta,kpi_summary,team,investors,fundings,traffic,similarweb_chart'
    
    
    return fields_string.split(',')

def get_companies_bulk(fields_string='id,name,website_url', must_dict={}, must_not_dict=[]):
    """ Get data about companies in bulk with filtering and selection of returned fields
    
   
    Parameters:
   
    fields_string (string): fields to be returned for data points (default: 'id,name,website_url' )
    
    must_dict (dict): inclusion filter for data points (default: {})
    
    must_not_dict (dict): exclusion filter for data points (default: {})
    
    
    Returns: 
    
    Pandas DataFrame when data is available, False in case of error
    
    Example:
        
    my_df=get_companies_bulk('id,name,website_url,industries,investors', { 'hq_locations': ['Amsterdam'],'tags': ['banking']})    
    if my_df == False:
        print("error loading data")

    """
    
    
    next_page_id = ""
    items = []
    
    while True:    
       
        data = {
        "form_data": {
            "must":must_dict,
            "must_not":must_not_dict
            },
        "fields": fields_string,
        "next_page_id": next_page_id,
        "limit": 100
        }    
        
        headers = {
            'Authorization': 'Basic MTExZGVhbHJvb21UZXN0aW5nfmVudjo=',
            'Content-Type': 'application/json'
            }
        r = requests.post(url="https://api.dealroom.co/api/v1/companies/bulk", data=json.dumps(data), headers=headers)
        res = json.loads(r.text)
        #print(res) 
        next_page_id = res['next_page_id']
        
        if 'error' in res.keys():
            print("error code: ",res['code'])
            print("error message: ",res['message'])
            return False
        
        res=res['items'] 
        items=items+res
        if next_page_id == None:
           break
   


    return pd.DataFrame(items)
    

 

