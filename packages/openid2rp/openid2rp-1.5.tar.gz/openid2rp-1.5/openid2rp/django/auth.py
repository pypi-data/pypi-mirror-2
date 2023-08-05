""" 
Written by Peter Troeger <peter@troeger.eu>.

A small Django authentication backend for OpenID, based on the openid2rp package.
It is automatically installed together with openid2rp. 

In order to get the Django database magic right, you need to add 'openid2rp.django' to your 
INSTALLED_APPS list in setup.py. You also need to add 'openid2rp.django.auth.Backend' to the
list of authentication backends. Example:

INSTALLED_APPS = (
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.sites',
	'django.contrib.admin',
	'openid2rp.django',
	'<yourapp>.front'
)

AUTHENTICATION_BACKENDS = (
	'django.contrib.auth.backends.ModelBackend',
	'openid2rp.django.auth.Backend'
)

The database is extended with one table for the	 OpenID identifier storage. 
Therefore, make sure that you call "python manage.py syncdb" ones 
after installing this package.

In contrast to most other Django OpenID authentication packages, this one
does not try to cover any view aspects. It also keeps the nature of openid2rp
by assuming that you know how OpenID works. 

Since the Django authentication framework is not prepared for a multi-step auth scenario with several 
inputs and outputs, you need to call a preparation function ("preAuthenticate") from the module
before you can use the Django authenticate() method. make sure that you use the correct keyword
arguments in the authenticate() call.

Session storage is based on a module-scope variable. I was to lazy to decode the openid2rp session dict
for the database storing and lifetime checking. There is also no Nonce checking so far.

The explicit modeling of each exceptional case hopefully allows you to realize an according 
reaction in your view rendering. 

"""

from django.conf import settings
from django.contrib.auth.models import User
from openid2rp.django.models import UserOpenID
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth.models import AnonymousUser
import openid2rp

AX = openid2rp.AX
sessions=[]

class IncorrectURI(Exception):
	pass

class IncorrectClaim(Exception):
	pass
	
class MissingSession(Exception):
	pass

class AuthenticationError(Exception):
	pass

class IncompleteAnswer(Exception):
	pass
	
class MultipleClaimUsage(Exception):
	pass
	
def storeOpenID(user, openid):
	claim=UserOpenID(user=user, uri=openid)
	claim.save()

def getOpenIDs(user):
	return UserOpenID.objects.filter(user=user).values_list('uri', flat=True)

def preAuthenticate(uri, answer_url, 
					sreg = (('nickname', 'email'), ()),
					ax = ((openid2rp.AX.email, openid2rp.AX.first, openid2rp.AX.last), ())):
	"""
	Initializes the OpenID authentication. 
	The input are the OpenID URI the user wants to be authorized with. You get
	that from your login screen. The answer_url is the one the provider should call when 
	finished, and the sreg / ax parameters as with the original openid2rp.request_authentication() call. 
	In the view for the answer_url, you will call then "authenticate".

	The output are two values: response and claim.
	The first value is the HttpResponse object with the neccessary redirect to the providers
	login site. You just return that from your view.
	The second value is the (normalized) claim URI from the original URI. 
	You need that later in the authenticate call, so store it somewhere in the session.
	
	If something goes wrong, one of the following errors is raised: IncorrectURI, IncorrectClaim
	"""
	global sessions

	try:
		kind, claimedId = openid2rp.normalize_uri(uri)			
	except Exception, e:
		raise IncorrectURI(str(e))
	res = openid2rp.discover(claimedId)
	if res != None:
		services, url, op_local = res
		session = openid2rp.associate(services, url)
		sessions.append(session)
		redirect_url=openid2rp.request_authentication( services, url, session['assoc_handle'], answer_url, claimedId, op_local, sreg=sreg, ax=ax )
		response=HttpResponse()
		response['Location']=redirect_url
		response.status_code=307
		return response, claimedId
	else:
		raise IncorrectClaim()

class Backend:	
	def get_user(self, user_id):
		try:
			return User.objects.get(pk=user_id)
		except User.DoesNotExist:
			return None

	def authenticate(self, **credentials):
		"""
		This finalizes the OpenID authentication. Input kwargs parameters:
		- request: Django request object, which has all the GET parameters being given by the OpenID provider
		- claim: Output from the preAuthenicate() call we asked you to store somewhere.
		
		The result of this call is either:
		- A User object with additional attributes.
		- A AnonymousUser object with additional attributes, in case the OpenID authentication was
		  good, but no matching user could be found.
		- One of the exceptions.

		The additional attributes are:
		- openid_email: The eMail address, or None.
		- openid_claim: The real claimId string for this user. You might want to use that in the storeID() call.
		- openid_sreg: A dictionary of received SREG values.
		- openid_ax: A dictionary of received AX values.
	
		If you get an AnonymousUser object as result, you need to assign the returned claim string first to some
		existing Django user. This backend will not create the according User object for you,
		since this is application-specific. You can use the AX / SREG data to pre-fill some registration
		form. If you somehow came to a Django user object for the returned claim string, use the storeID() call.
		
		Possible errors: MissingSession, AuthenticationError, IncompleteAnswer, MultipleClaimUsage
		"""

		global sessions

		if not ("request" in credentials and "claim" in credentials):
			raise TypeError
		
		request=credentials['request']
		claimedId=credentials['claim']
		
		query=request.META['QUERY_STRING']
		handle = request.GET['openid.assoc_handle']
		for session in sessions:
			if session['assoc_handle'] == handle:
				break
		else:
			session=None
		if not session:
			raise MissingSession
		try:
			signed=openid2rp.authenticate(session, query)
		except Exception, e:
			raise AuthenticationError(str(e))
		# provider-based auth returns claim id, OpenID not (if I got that right) - in this case we take the original value
		if 'openid.claimed_id' in request.GET:
			if 'claimed_id' not in signed:
				raise IncompleteAnswer()
			claimedId = request.GET['openid.claimed_id']
		else:
			if 'identity' not in signed:
				raise IncompleteAnswer()
		# look up OpenID claim string in local database
		idrecord=UserOpenID.objects.filter(Q(uri=claimedId))
		if len(idrecord)>1:
			# more than one user has this claimID, which is definitly wrong
			raise MultipleClaimUsage()
		elif len(idrecord)<1:
			# No user has this OpenID claim string assigned
			user = AnonymousUser()
		else:
			user=idrecord[0].user
		# inactive users are handled by the later login() method, so we can return them here too
		user.openid_claim = claimedId
		user.openid_ax = openid2rp.get_ax(query, openid2rp.get_namespaces(query), signed)
		user.openid_sreg = openid2rp.get_sreg(query, signed)
		user.openid_email = openid2rp.get_email(query)
		return user
		
