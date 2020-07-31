import  requests
import hashlib
import sys

'''
using Api of "https://haveibeenpwned.com/Passwords" and sending only first 5 characters
of SHA1 geenrated hash key for our password "password123"
SHA1 hash key for "password123" is "CBFDAC6008F9CAB4083784CBD1874F76618D2A97"
'''


'''
Response [200] is OKAY,so we have passed only 5 char so API gives all the possible output which matches
these 5 char, then we have compare our hash key with this database in local machine to find it hacked or not.
'''
def request_api_data(SHA1_hash_key):
    url = 'https://api.pwnedpasswords.com/range/' + SHA1_hash_key
    response = requests.get(url)
    if response.status_code !=200:
        raise RuntimeError(f'error fetching: {res.status_code},check api and try again ')
    return response

def get_password_leaks_count(hashes, hash_to_check):
    '''
    hashes is the response stored in object,so hashes.text will convert response into text
    as list of keys found with their count
    '''
    hashes = (lines.split(':') for lines in hashes.text.splitlines())
    for h,count in hashes:
        if h==hash_to_check:
            return count
    return 0


def pwned_api_check(password):

    # generates SHA1 hash key for any password and string is encoded to utf-8 format
    
    sha1_password = hashlib.sha1(password.encode('utf=8')).hexdigest().upper()
    first5_char, tail_char = sha1_password[:5], sha1_password[5:]
    response = request_api_data(first5_char)
    return get_password_leaks_count(response, tail_char)

def main(args):
    for password in args:
        count = pwned_api_check(password)
        if count:
            print(f'{password} has been found {count} of times..so probably change the password')
        else:
            print(f'{password} has not been found..continue with same password!')
    return 'Password checking completed!'
    
'''
Run through terminal by passing any number of passwords
as arguments
'''

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
