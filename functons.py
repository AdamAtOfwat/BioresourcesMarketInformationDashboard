  
import pandas as pd
import requests
import sqlite3


def auto_download():
    company_links = {
        'ANH': r'https://www.anglianwater.co.uk/siteassets/household/about-us/bioresources-market-information-2020-tables-1-5.xlsx',
        'HDD': r'https://www.hdcymru.co.uk/content/dam/hdcymru/regulatory-documents/2020-bioresources-market-information-HD-appendix1.xlsx',
        'NES': r'https://www.nwg.co.uk/globalassets/corporate-images/news-and-press/northumbrian-water-bioresources-market-information-2019-20.pdf',
        'SRN': r'https://www.southernwater.co.uk/media/3646/rc-20-rcfl-016-bioresources-market-information-completed.xlsm',
        'SVE': r'https://www.stwater.co.uk/content/dam/stw/regulatory-library/2020-bioresources-market-information-stw-appendix1.xlsx',
        'SWB': r'https://www.southwestwater.co.uk/siteassets/commercial/bioresources-market-information-2019-20.xlsx',
        'TMS': r'https://www.thameswater.co.uk/media-library/home/about-us/responsibility/managing-sewage-sludge/bioresources-locations-and-successful-contract-market-info-2019-20.xlsx',
        'UUW': r'https://www.unitedutilities.com/globalassets/z_corporate-site/about-us-pdfs/annual-performance-report-2020/bioresources-platform-2020.xlsx',
        'WSH': r'https://corporate.dwrcymru.com/-/media/Project/Files/Page-Documents/Corporate/Library/Annual-Performance-Reports/2019-2020/Dwr-Cymru-Bioresources-market-information-for-publication-2019-20.ashx',
         'WSX': r'https://www.wessexwater.co.uk/-/media/files/wessexwater/corporate/strategy-and-reports/bioresources-market-information-2020.xlsx',
        'YKY': r'https://www.yorkshirewater.com/media/2585/yky-bioresources-market-information-2020.xlsx'
        }

    for key in company_links:
        r = requests.get(company_links[key])
        with open(fr'inputs\{key}.xlsx', 'wb') as f:
            f.write(r.content)


def data_mung(df, headers, company):
    """This function mungs a dataframe into the right format. """
    df.columns = headers.iloc[0, :].tolist()
    df.set_index(pd.MultiIndex.from_product([[company], df.index]), inplace=True)
    df.dropna(thresh=5, inplace=True)
    df['Company'] = company
    return df



def Concat():
    """This function concatenates key elements of all the three files from the main database tables."""
    conn = sqlite3.connect(r'Outputs\bioresources.db')
    df_small = pd.read_sql("""SELECT 
                                 Company, 
                                "Company Name", 
                                "WwTW site name" AS "Site Name",
                                "WwTW location (grid ref latitude)" AS "Latitide",
                                "WwTW location (grid ref longitude)" AS "Longitude",
                                "Volume of raw sludge produced per year" AS "Sludge production",
                                "WwTW classification" AS "Site classification"
                              FROM small""", conn)

    df_small['Type'] = 'Small WwTW'


    df_WwTW = pd.read_sql("""SELECT 
                                Company,
                                "Company Name", 
                                "WwTW site name" AS "Site Name",
                                "WwTW location grid ref latitude" AS "Latitide",
                                "WwTW location grid ref longitude" AS "Longitude",
                                "Volume of raw sludge produced per year" AS "Sludge production"
                            FROM WwTW""", conn)

    df_WwTW['Type'] = 'WwTW'

    df_STC = pd.read_sql("""SELECT 
                                Company,
                                "Company Name",
                                "Sludge Treatment Centre (STC) name" AS 'Site Name',
                                "STC location (grid ref latitude)" AS "Latitide",
                                "STC location (grid ref longitude)" AS "Longitude",
                                "End product volume per year" AS "Sludge production",
                                "Type of site"
                            FROM STC""", conn)

    df_STC['Type'] = 'STC'

    df = pd.concat([df_small, df_WwTW], join="inner")
    df = pd.concat([df, df_STC], join="outer")
    df['Company_Type'] = df.Company + ': ' + df.Type
    df.reset_index(inplace=True, drop=True)
    df['Type of site'].fillna(value='Wastewater Treatment Works', inplace=True)
    return df

