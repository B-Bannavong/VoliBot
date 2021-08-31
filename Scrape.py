CLIENT_ID = 'kOUB-9yoTlH7vNtmDDcMPw'
SECRET_KEY = 'fG_oxXT93FZLxMVmN-Bpmpq8j30yyQ'
from pandas.core.frame import DataFrame
import requests
from requests.auth import HTTPBasicAuth
import spacy
from spacy import displacy
import pandas as pd
with open('pw.txt', 'r') as f:
    pw = f.read()

data = {
    'grant_type': 'password',
    'username': 'Eccccca',
    'password': pw
}
subs = ['https://oauth.reddit.com/r/wallstreetbets/hot', 'https://oauth.reddit.com/r/smallstreetbets', 'https://oauth.reddit.com/r/investing']
headers = {'User-Agent' : 'MyAPI/0.0.1'}
res = requests.post('https://www.reddit.com/api/v1/access_token',
auth=HTTPBasicAuth(CLIENT_ID, SECRET_KEY), data=data, headers=headers)
TOKEN = res.json()['access_token']
headers['Authorization'] = f'bearer {TOKEN}'


def main(reddit_url):
    for url in reddit_url:
        res = requests.get(url,
        headers=headers, params={'limit' : '50'}) #We can add 'after' : [id]' to get all posts after the specified ID

        df = pd.DataFrame()
        nlp = spacy.load('en_core_web_sm')
        for post in res.json()['data']['children']:
            df = df.append({
                'Subreddit' : post['data']['subreddit'],
                'Type' : post['kind'] + '_' + post['data']['id'],
                'Flair' : post['data']['link_flair_text'],
                'Title' : post['data']['title'],
                'Post_Text' : post['data']['selftext'],       
                'Upvotes' : post['data']['ups'],
                'Downvotes' : post['data']['downs'],
                'Ratio' : post['data']['upvote_ratio'],
            }, ignore_index=True)

        options = ['DD', 'YOLO', 'Gain', 'Technical Analysis']
        df_result = df[df['Flair'].isin(options)]

        BLACKLIST = ['otm', 'itm', 'yolo', 'ath']


        df_result['Tickers'] = df_result['Title'].apply(get_tckr)
        print(df_result)

def get_tckr(text):
    doc = nlp(text)
    #displacy.render(doc, style='ent')
    tckr_list = []
    for entity in doc.ents:
        if entity.label_ == 'ORG' and entity.text.lower() not in BLACKLIST:
            tckr_list.append(entity.text)
    return (tckr_list)
if __name__ == "__main__":
    main(subs)


#print(post['data'].keys()) #(call this for list of possible keys)
# print(displacy.render(doc, style='ent'))


