import pandas as pd
from django.contrib.auth.models import User
from backend.models import EventUser,Event


df = pd.read_excel('C:/Users/ste0001/Downloads/Teilnehmerliste_Kartrennen_Stetteldorf_2020.xlsx',sheet_name='Kart2020')
#d1 = df[df.Zusage == 'Ja']

def create_username(first_name,last_name,all_usernames):
    
    count = 0
    while True:
        count += 1
        tmp = str(count)
        tmp = tmp.zfill(4)
        username = '{0}{1}{2}'.format(last_name[:2].lower(),first_name[:1].lower(),tmp) 
        if not username in all_usernames:
            return username
    return False,'cannot assign username'


def load_users_list(dataframe):
    users = []
    all_usernames = [user.username for user in User.objects.all()]
    for id,row in dataframe.iterrows():
        tmp = {}
        tmp['first_name'] = row.Vorname
        tmp['last_name'] = row.Nachname
        tmp['action'] = 'accept' if row.Zusage == 'Ja' else 'reject'
        username = create_username(row.Vorname,row.Nachname,all_usernames)
        all_usernames.append(username)
        tmp['username'] = username
        tmp['password'] = 'Willkommen1'
        users.append(tmp)
    return users

def create_user(event,users):
    for user in users:
        obj = User()
        obj.username = user['username']
        obj.first_name = user['first_name']
        obj.last_name = user['last_name']
        obj.set_password = user['password']
        obj.save()
        EventUser.objects.create(event=event,user=obj,action=user['action'])

if __name__ == "__main__":
    event = Event.objects.all().first()
    d1 = df[df.Zusage == 'Ja']
    users = load_users_list(d1)
    create_user(event,users)