import requests, threading, speech_recognition, random, string, os, time, colorama



def getProxies():
    with open('proxies.txt', 'r') as proxies:
        proxies = proxies.read().splitlines()
    return proxies
    # try:
    #   proxies = ''
    #   for chunk in requests.get('https://bit.ly/2Or38Z5').iter_content(
    #           chunk_size=10000):
    #       if chunk:
    #           chunk = chunk.decode()
    #           proxies = proxies + chunk
    #   proixes = proxies.splitlines()
    # except:
    #   with open('proxies.txt', 'r') as proxies:
    #     proxies = proxies.read().splitlines()
    # return proxies


proxies= getProxies()

def getCaptcha():
    for i in range(1):
        try:
            with requests.session() as session:
                captchaToken = session.post('https://client-api.arkoselabs.com/fc/gt2/public_key/E5554D43-23CC-1982-971D-6A2262A2CA24', data={'public_key':'E5554D43-23CC-1982-971D-6A2262A2CA24', 'rnd':f'0.{random.randint(1000,100000)}', 'userbrowser':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36 Edg/89.0.774.57', 'site':'https://www.twitch.tv', 'language':'en'}, proxies={'http':random.choice(proxies), 'https':random.choice(proxies)}, timeout=20)
            threading.Thread(target=create_account,args=(captchaToken.json()['token'],)).start()
        except:
            pass

def getClient():
    with requests.session() as session:
        client = session.get('https://www.twitch.tv/').text.split('"Client-ID":"')[1].split('",')[0]
    return [client, session.cookies]

success = 0
fail = 0
created = 0

def count():
    while True:
        os.system(f'title S = {success}/ F = {fail} / C = {created}')
        time.sleep(1)

def create_account(token):
    global success, fail, created
    try:
        with requests.session() as session:
            session.get('https://www.twitch.tv/')
            client_id = getClient()
            session.cookies = client_id[1]
            client_id = client_id[0]
            password = 'nab0rsbotslol3'
            username = f'nab0rs{random.randint(1,100005)}'
            session_token = token.split('|')[0]
            captcha = session.get(f'https://client-api.arkoselabs.com/fc/get_audio/?session_token={session_token}&analytics_tier=40&r=us-west-2&language=en', proxies={'http':random.choice(proxies), 'https':random.choice(proxies)})
            ffname = f'captchas\{random.randint(1,100000)}.wav'
            with open(ffname, 'wb') as ff:
                ff.write(captcha.content)
            regon = speech_recognition.Recognizer()
            with speech_recognition.AudioFile(ffname) as ff2:
                rec = regon.record(ff2)
                raw = regon.recognize_google(rec)
                answ = ''
                for x in raw:
                    if x.isdigit():
                        answ = answ + x
            sovled = session.post('https://client-api.arkoselabs.com/fc/audio/', data={'session_token':session_token, 'language':'en', 'r':'us-west-2', 'audio_type':2, 'response':answ, 'analytics_tier':40}, proxies={'http':random.choice(proxies), 'https':random.choice(proxies)})
            if sovled.json()['response'] == 'correct':
                success += 1
                for i in range(10):
                    try:
                        reg = session.post('https://passport.twitch.tv/register', headers={'accept-language''origin':'https://www.twitch.tv','sec-fetch-dest':'empty', 'sec-fetch-mode':'cors', 'sec-fetch-site':'same-site','referer':'https://www.twitch.tv/','user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36 Edg/89.0.774.57' ,'content-type':'text/plain;charset=UTF-8', 'accept-encoding':'gzip, deflate, br'},json={"username":username,"password":password,"email":f"{username}@gmail.com","birthday":{"day":21,"month":9,"year":1999},"client_id":client_id,"include_verification_code":True,"arkose":{"token":f"{session_token}|r=us-west-2|metabgclr=transparent|guitextcolor=%23000000|metaiconclr=%23757575|meta=3|lang=en|pk=E5554D43-23CC-1982-971D-6A2262A2CA24|at=40|sup=1|rid=25|atp=2|cdn_url=https://cdn.arkoselabs.com/fc|lurl=https://audio-us-west-2.arkoselabs.com|surl=https://client-api.arkoselabs.com"}}, proxies={'http':random.choice(proxies), 'https':random.choice(proxies)})
                        print(reg.text)
                        with open('cookies.txt', 'a') as cookies:
                            tokenc = reg.json()['access_token']
                            cookies.write(f'{username}:{password}:{tokenc} \n')
                            created += 1
                            print(f'Account created: {username}:{tokenc}')
                            break
                    except:
                        pass
            else:
                fail += 1
    except:
        pass
threading.Thread(target=count,).start()


def handle():
    while True:
        getCaptcha()

for x in range(250):
    threading.Thread(target=handle,).start()



