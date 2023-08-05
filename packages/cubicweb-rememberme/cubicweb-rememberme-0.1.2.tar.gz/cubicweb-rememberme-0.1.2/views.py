"""rememberme components: plug authentication retreiver

:organization: Logilab
:copyright: 2009-2010 LOGILAB S.A. (Paris, FRANCE), license is LGPL v2.
:contact: http://www.logilab.fr/ -- mailto:contact@logilab.fr
:license: GNU Lesser General Public License, v2.1 - http://www.gnu.org/licenses
"""
from datetime import date, timedelta
from random import randint

from cubicweb.selectors import implements
from cubicweb.web import uicfg, formfields as ff, formwidgets as fw
from cubicweb.web.views import (authentication, basecontrollers, basetemplates,
                                autoform, actions)

_pvs = uicfg.primaryview_section
_pvs.tag_object_of(('CWAuthCookie', 'auth_cookie_for_user', 'CWUser'), 'hidden')

_abaa = uicfg.actionbox_appearsin_addmenu
_abaa.tag_object_of(('CWAuthCookie', 'auth_cookie_for_user', 'CWUser'), False)

MAX_MAGIC_NUMBER = (2 ** 31) - 1 # XXX ** 128

# web authentication info retreiver ############################################

class AuthCookieRetreiver(authentication.WebAuthInfoRetreiver):
    """authenticate by a magic number stored a cookie on the client host
    """
    __regid__ = 'magicnumauth'
    order = 0

    def __init__(self, vreg):
        # XXX make lifetime configurable
        self.cookie_lifetime = timedelta(days=30)

    def authentication_information(self, req):
        """retreive authentication information from the given request, raise
        NoAuthInfo if expected information is not found:

        return info from long lived authentication cookie if any
        """
        cookie = req.get_cookie()
        try:
            authcookie = cookie['__cw_auth_cookie'].value
        except KeyError:
            raise authentication.NoAuthInfo()
        try:
            login, magic = authcookie.split(';__magic=', 1)
        except ValueError:
            req.remove_cookie(cookie, '__cw_auth_cookie')
            raise authentication.NoAuthInfo()
        return login, {'magicnumber': magic}

    def authenticated(self, req, cnx, retreiver):
        """callback when return authentication information have opened a
        repository connection successfully:

        set authentication cookie for the next time
        """
        if not (retreiver is self or '__setauthcookie' in req.form):
            return
        if cnx.anonymous_connection:
            return
        req.form.pop('__setauthcookie', None)
        user = cnx.user()
        authentity = req.create_entity('CWAuthCookie',
                                       magicnumber=randint(0, MAX_MAGIC_NUMBER),
                                       lifetime=self.cookie_lifetime,
                                       auth_cookie_for_user=user.eid)
        # we've to commit here, else cookie may be rollbacked by errors while
        # trying to set last_login_time in the CookieSessionHandler (eg for ldap
        # user at least).
        req.cnx.commit()
        magicnum = authentity.magicnumber
        cookie = req.get_cookie()
        cookie['__cw_auth_cookie'] = '%s;__magic=%s' % (user.login, magicnum)
        req.set_cookie(cookie, '__cw_auth_cookie', maxage=None,
                       expires=date.today() + self.cookie_lifetime)
        cnx.authinfo['magicnumber'] = magicnum


# add remember me checkbox on the login form ###################################

basetemplates.LogForm.append_field(
    ff.BooleanField('__setauthcookie', choices=[(_('remember me'), True)],
                    label=None, widget=fw.CheckBox({'class': 'data'}))
    )


# deactivate manual addition/edition ###########################################

class UneditableCWAuthCookieEdition(autoform.AutomaticEntityForm):
    __select__ = implements('CWAuthCookie')
    def __init__(self, *args, **kwargs):
        raise Unauthorized()

actions.ModifyAction.__select__ = actions.ModifyAction.__select__ & ~implements('CWAuthCookie')
actions.MultipleEditAction.__select__ = actions.MultipleEditAction.__select__ & ~implements('CWAuthCookie')



class LogoutController(basecontrollers.LogoutController):

    def publish(self, rset=None):
        """logout from the instance"""
        cookie = self._cw.get_cookie()
        if '__cw_auth_cookie' in cookie:
            self._cw.remove_cookie(cookie, '__cw_auth_cookie')
        try:
            # removing all existing auth cookie entities, not only the currently
            # used one, doesn't seem like a bad idea
            self._cw.execute('DELETE CWAuthCookie X '
                             'WHERE X auth_cookie_for_user U, U eid %(u)s',
                             {'u': self._cw.user.eid}, 'u')
            self._cw.cnx.commit()
        except:
            import traceback
            traceback.print_exc()
        return super(LogoutController, self).publish(rset)


def registration_callback(vreg):
    vreg.register_all(globals().values(), __name__, (LogoutController,))
    vreg.register_and_replace(LogoutController, basecontrollers.LogoutController)
