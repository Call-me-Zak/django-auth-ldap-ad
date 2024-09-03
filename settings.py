import ldap3
from django_auth_ldap.config import LDAPSearch, GroupOfNamesType


####### added (this was what was working) THIS IS THE ONE BEING USED UPPER ONE IS USELESS
LDAP_SERVER = 'ldap://tested-this-against-my-ldap-server' #replace with your LDAP server address aka AD
LDAP_USER = 'ZakAuth' #this is your log on username from AD 
 ##### got invalid credentials when I tried with zak (reason : incorrect permissions, ZakAuth has correct permissions set on AD server)
LDAP_PASSWORD = 'insert-the-AD-account-password' ##change this
BASE_DN = 'dc=your_domain,dc=com' # base domain name, replace with your domain name e.g: google.com dc=google, dc=com 
SEARCH_FILTER = '(objectClass=person)'

server = ldap3.Server(LDAP_SERVER)
conn = ldap3.Connection(server, user=LDAP_USER, password=LDAP_PASSWORD, auto_bind=True)
##perform a search
conn.search(search_base=BASE_DN,
            search_filter=SEARCH_FILTER,
            search_scope=ldap3.SUBTREE,
            attributes=['cn','sn','mail']) #specify what to retrieve

for entry in conn.entries:
    print(entry)

conn.unbind() #unbind

############# new ends here
# define ldap search for users
AUTH_LDAP_USER_SEARCH = LDAPSearch(
    "CN=Users, DC=ye, DC=net",
    ldap3.SUBTREE,
    "(sAMAccountName=%(user)s)"
)

# define user flags by group
AUTH_LDAP_USER_FLAGS_BY_GROUP = {
    "is_active": "CN=Active Users, CN=Users, DC=ye, DC=net"
}

# define ldap search for groups
AUTH_LDAP_GROUP_SEARCH = LDAPSearch(
    "CN=Groups, DC=ye, DC=net",
    ldap3.SUBTREE, 
    "(objectClass=group)"
)

# define group types
AUTH_LDAP_GROUP_TYPE = GroupOfNamesType()
# mirror groups
AUTH_LDAP_MIRROR_GROUPS = True

# this broke my code and I can't be bothered to fix it as it's not a necessity for me atm, you can uncomment and set to {0} if you want
#AUTH_LDAP_CONNECTION_OPTIONS = {'timeout': 30}

#'myapp.backends.LDAPBackend', (was inside the list) (this was my initial LDAP backend, rewrote it to fit ldap3)
AUTHENTICATION_BACKENDS = [
    'myapp.backends.ActiveDirectoryBackend', # custom AD backedn
    'django.contrib.auth.backends.ModelBackend', #default backend
]



import logging
# Enable logging for ldap
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('django_auth_ldap')
logger.setLevel(logging.DEBUG)
