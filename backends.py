from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
from ldap3 import Server, Connection, ALL, NTLM
from Crypto.Hash import MD4
import logging

 

# Set up logging configuration

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

 
class ActiveDirectoryBackend(BaseBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        logging.debug(f"Incoming login request: username={username}, password={password}")


   
        if not username or not password:
            return None  

            # Attempt AD authentication

        if self.ad_authenticate(username, password):

                try:

                    # Try to find or create the user in Django

                    user, created = User.objects.get_or_create(username=username)

                    # We no longer set the password here
                    # feel free to remove the logging function if you want

                    if created:

                        logging.info(f"User {username} created in Django but no password is stored.")

                    return user

                except Exception as e:

                    logging.error(f"Error during user retrieval or creation: {e}")

                    return None

        
        else:
            logging.info(f"AD authentication failed for username={username}")


       

        return None

 

    def get_user(self, user_id):

        try:

            return User.objects.get(pk=user_id)

        except User.DoesNotExist:

            return None


    def ad_authenticate(self, username, password):

            # AD server settings

        AD_SERVER = 'tested-this-against-my-server => works as intended'

        AD_USER_DOMAIN = 'google.com' #full domain here #method 1

        AD_USER_BASE_DN = 'DC=google,DC=com'  # DC=google,DC=com' #method 2 

        #keep only one and adjust your variables accordingly, I pref the first one, but you can use whichever one you like

   

         # Construct the user DN

        user_dn = f'{AD_USER_DOMAIN}\\{username}'

   

        try:

            logger.debug(f"Connecting to AD server: ldap://{AD_SERVER}")

        # Create the server and connection

            server = Server(AD_SERVER, get_info=ALL)

            conn = Connection(server, user=user_dn, password=password, authentication=NTLM)

       

        # Bind (authenticate) to the server

            if conn.bind():

                logger.info(f"AD bind successful for user_dn={user_dn}")

                return True

            else:

                return False

        except Exception as e:

            logging.error(f"AD authentication error: {e}")

            return False

        finally:

        # Always unbind (close) the connection

            if conn:

                conn.unbind()