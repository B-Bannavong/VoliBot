from pandas.core.frame import DataFrame
import requests
from requests.auth import HTTPBasicAuth
import spacy
from spacy import displacy
import pandas as pd
from globals import *



class scraper:
    
    def __init__ (self, *args, **kwargs):
        self.res = requests.post('https://www.reddit.com/api/v1/access_token',
        auth = HTTPBasicAuth(CLIENT_ID, SECRET_KEY), data=data, headers=headers)
        self.TOKEN = self.res.json()['access_token']
        headers['Authorization'] = f'bearer {self.TOKEN}'
        self.df = pd.DataFrame()
        self.nlp = spacy.load('en_core_web_sm')
        self.count = 0
        self.ticker_type = 'ORG'
        
        return super().__init__(*args, **kwargs)

    def run(self,reddit_url):
        for url in reddit_url:
            res = requests.get(url,
            headers=headers, params={'limit' : '50'}) #We can add 'after' : [id]' to get all posts after the specified ID

            for post in res.json()['data']['children']:
                self.df = self.df.append({
                    'Subreddit' : post['data']['subreddit'],
                    'Type' : post['kind'] + '_' + post['data']['id'],
                    'Flair' : post['data']['link_flair_text'],
                    'Title' : post['data']['title'],
                    'Post_Text' : post['data']['selftext'],       
                    'Upvotes' : post['data']['ups'],
                    'Downvotes' : post['data']['downs'],
                    'Ratio' : post['data']['upvote_ratio'],
                }, ignore_index=True)


            if url != 'https://oauth.reddit.com/r/investing/hot':
                df_result = self.df[self.df['Flair'].isin(options)]
                df_result['Tickers'] = df_result['Title'].apply(self.get_tckr)
                self.data_to_html(df_result)
                print(df_result)
               
            else:
                self.df['Tickers'] = self.df['Title'].apply(self.get_tckr)
                self.data_to_html(self.df)
                print(self.df)
                
            df_result = df_result[0:0]
            self.df = self.df[0:0]
     
    def data_to_html(self,result):
        result.to_html(CWD + f'\Reddit Data\Scraped-{subNames[self.count]}.html')
        self.count = self.count + 1
        

    def get_tckr(self,text):
        doc = self.nlp(text)
        displacy.render(doc, style='ent')
        tckr_list = [entity.text for entity in doc.ents if entity.label_ == self.ticker_type and entity.text.lower() not in BLACKLIST]
        return (tckr_list)


if __name__ == "__main__":
    scrape = scraper()
    scrape.run(subs)



