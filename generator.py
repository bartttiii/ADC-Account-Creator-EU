import requests, time, random, string, os
from bs4 import BeautifulSoup
from GmailDotEmailGenerator import GmailDotEmailGenerator

basemail = input('Enter prefix of your email\t')

randompass = input('Do you want a random pass? Y for Yes. Any other Key for No\t')
if randompass == 'y' and 'y':
    print('Generating Random passwords.')
else:
    password = input('Enter Desired Password\t')
accountstogen = input('Enter Desired Accounts to be Made\t')
accountstogen = int(accountstogen)
if len(basemail) > 2:
    maxemails = (len(basemail) - 1)** 2
if len(basemail) <= 2:
    maxemails = 2

if maxemails < accountstogen:
    print("You can only generate a max of {} using email {}@gmail.com".format(maxemails,basemail))
    exit()




def account_successfully_created(response):
    try:
        return False if BeautifulSoup(response.text, "html.parser").find('input',
                                                                         {'id': 'resumeURL'}).get('value') == \
                        'https://www.adidas.nl/on/demandware.store/Sites-adidas-NL-Site/nl_NL/MyAccount-CreateOrLogin' \
            else True
    except:
        return True


for email in \
        (GmailDotEmailGenerator(basemail + '@gmail.com').generate())[:accountstogen]:

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36',
        'Accept-Encoding': 'gzip, deflate, sdch, br',
        'Accept-Language': 'en-US,en;q=0.8',
        'Upgrade-Insecure-Requests': '1'
    }
    if randompass == 'y' and 'y':
        length = 13
        chars = string.ascii_letters + string.digits + '$&@?!#%'
        random.seed = (os.urandom(1024))
        password = ''.join(random.choice(chars) for i in range(length))

    s = requests.Session()
    s.headers.update(headers)

    r = s.get('https://cp.adidas.nl/web/eCom/nl_NL/loadcreateaccount')
    csrftoken = BeautifulSoup(r.text, "html.parser").find('input', {'name': 'CSRFToken'}).get('value')

    s.headers.update({
        'Origin': 'https://cp.adidas.nl',
        'Referer': 'https://cp.adidas.nl/web/eCom/nl_NL/loadcreateaccount',
    })
    r = s.post('https://cp.adidas.nl/web/eCom/nl_NL/accountcreate',
               data={
                   'firstName': '###',  ### Set your Name
                   'lastName': '###',  # Set your name
				   'day': '##', # Set your day
				   'month': '09', # Set your month
				   'year': '1999', # Set your year
                   'email': email,
                   'password': password,
                   'confirmPassword': password,
                   '_amf': 'on',
                   'terms': 'true',
                   '_terms': 'on',
                   'metaAttrs[pageLoadedEarlier]': 'true',
                   'app': 'eCom',
                   'locale': 'nl_NL', # Set your locale
                   'domain': '',
                   'consentData1': 'Sign me up for adidas emails, featuring exclusive offers, featuring latest product info, news about upcoming events, and more. See our <a target="_blank" href="https://www.adidas.com/us/help-topics-privacy_policy.html">Policy Policy</a> for details.',
                   'consentData2': '',
                   'consentData3': '',
                   'CSRFToken': csrftoken
               })

    if account_successfully_created(r) == False:
        # print 'ACCOUNT EXISTS'
        print("Username = {0}, Password = {1}, Account EXISTS".format(email, password))
    if account_successfully_created(r) == True:
        print("Created Account : Username = {0}, Password = {1}".format(email, password))
        with open('accounts' + '.txt', 'a') as f:
            f.write(email + ':' + password + '\n')
            f.close()

    time.sleep(5)
