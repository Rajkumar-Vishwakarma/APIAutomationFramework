import requests
import json


def main():
    response = requests.get("https://datausa.io/api/data?drilldowns=Nation&measures=Population")
    
    json_obj = response.json()
    data_source = json_obj["source"][0]["annotations"]["source_name"]
    
    nations_json_obj = json_obj["data"]
    no_of_years = len(nations_json_obj)-1
    initial_yr = None
    final_yr = None
    previous_population = 0
    dictionary_prcnt_yr = {}
    
    for i in range(len(nations_json_obj)):
        data_nation = nations_json_obj[i]
        population = data_nation["Population"]
        prcnt_change = float(0)
        
        if previous_population == 0:
            previous_population = population
        else:
            prcnt_change = float((((previous_population - population) / population) * 100))
            dictionary_prcnt_yr[nations_json_obj[i-1]["Year"]] = prcnt_change
     
        if i == 0:
            final_yr = data_nation["Year"][2:]
            
        if i == len(nations_json_obj)-1:
            initial_yr = data_nation["Year"][2:]
    
    peak_population_prcnt = get_max_prcnt(dictionary_prcnt_yr)
    lowest_population_prcnt = get_min_prcnt(dictionary_prcnt_yr)
    peak_population_yr = get_year(peak_population_prcnt, dictionary_prcnt_yr)[2:];
    lowest_population_yr = get_year(lowest_population_prcnt, dictionary_prcnt_yr)[2:];
    
    print("According to {}, in {} years from 20{} to 20{}, peak population growth was {}% in 20{} and lowest population increase was {}% in 20{}.".
          format(data_source,no_of_years,initial_yr,final_yr,peak_population_prcnt,peak_population_yr,lowest_population_prcnt,lowest_population_yr))

def get_max_prcnt(dictionary_prcnt_yr):
    max_prcnt = element_prcnt = float(0)
    for value in dictionary_prcnt_yr.values():
        element_prcnt = value
        if max_prcnt < element_prcnt:
            max_prcnt = element_prcnt
    return max_prcnt
    
def get_min_prcnt(dictionary_prcnt_yr):
    min_prcnt = element_prcnt = float(0)
    if len(dictionary_prcnt_yr) > 0:
        min_prcnt = list(dictionary_prcnt_yr.values())[0]
    for value in dictionary_prcnt_yr.values():
        element_prcnt = value
        if min_prcnt > element_prcnt:
            min_prcnt = element_prcnt
    return min_prcnt

def get_year(population_prcnt, dictionary_prcnt_yr):
    year = None
    prcnt = float(0)
    for prcnt_value in dictionary_prcnt_yr.values():
        prcnt = prcnt_value
        if prcnt_value == population_prcnt:
            break
    
    for year_value in dictionary_prcnt_yr.keys():
        if dictionary_prcnt_yr[year_value] == prcnt:
            year = year_value
            break
    
    return year
            
main()
