"""anonymous registration form and views

:organization: Logilab / SecondWeb
:copyright: 2009-2010 LOGILAB S.A. (Paris, FRANCE), license is LGPL v2.
:contact: http://www.logilab.fr/ -- mailto:contact@logilab.fr
:license: GNU Lesser General Public License, v2.1 - http://www.gnu.org/licenses
"""
__docformat__ = "restructuredtext en"

from logilab.common.decorators import clear_cache

from yams.schema import role_name

from cubicweb import mail, crypto
from cubicweb.view import StartupView
from cubicweb.web import Redirect, ValidationError, ProcessFormError
from cubicweb.web import controller, form, captcha
from cubicweb.web import formwidgets as fw, formfields as ff
from cubicweb.web.views import forms, basecomponents, urlrewrite

def qname(attr):
    return role_name(attr, 'subject')


class RegistrationForm(forms.FieldsForm):
    __regid__ = 'registration'
    domid = 'registrationForm'
    form_buttons = [fw.SubmitButton()]

    @property
    def action(self):
        return self._cw.build_url(u'registration_sendmail')

    # properly name fields according to validation errors that may be raised by
    # Repository.register_user
    login = ff.StringField(widget=fw.TextInput(), role='subject',
                           # we don't want to see 'authenticate'
                           label=_('i18n_register_login'),
                           required=True)
    upassword = ff.StringField(widget=fw.PasswordInput(), role='subject',
                               required=True)
    address = ff.StringField(widget=fw.TextInput(), role='subject',
                               required=True)
    firstname = ff.StringField(widget=fw.TextInput(), role='subject')
    surname = ff.StringField(widget=fw.TextInput(), role='subject')
    captcha = ff.StringField(widget=captcha.CaptchaWidget(), required=True,
                             label=_('captcha'),
                             help=_('please copy the letters from the image'))


class RegistrationFormView(form.FormViewMixIn, StartupView):
    __regid__ = 'registration'

    def call(self):
        form = self._cw.vreg['forms'].select('registration', self._cw)
        self.w(form.render(display_progress_div=False))

class RegistrationSendMailController(controller.Controller):
    __regid__ = 'registration_sendmail'
    content = _(u'''
Hello %(firstname-subject)s %(surname-subject)s,

thanks for registering on %(base_url)s.

Please click on the link below to activate your account :
%(url)s.

See you soon on %(base_url)s !
''')
    subject = _(u'Confirm your registration on %(base_url)s')

    def publish(self, rset=None):
        data = self.checked_data()
        recipient = data[qname('address')]
        msg = self.build_email(recipient, data)
        self._cw.vreg.config.sendmails([(msg, (recipient,))])
        raise Redirect(self.success_redirect_url())

    def checked_data(self):
        '''only basic data check here (required attributes and password
        confirmation check)
        '''
        form = self._cw.vreg['forms'].select('registration', self._cw)
        form.formvalues = {} # init fields value cache
        data = {}
        errors = {}
        for field in form.fields:
            try:
                for field, value in field.process_posted(form):
                    if value is not None:
                        data[field.role_name()] = value
            except ProcessFormError, exc:
                errors[field.role_name()] = unicode(exc)
        if errors:
            raise ValidationError(None, errors)
        return data

    def build_email(self, recipient, data):
        activationurl = self.activation_url(data) # build url before modifying data
        data.setdefault(qname('firstname'), '')
        data.setdefault(qname('surname'), '')
        if not (data.get(qname('firstname')) or data.get(qname('surname'))):
            data[qname('firstname')] = data[qname('login')]
        data.update({'base_url': self._cw.vreg.config['base-url'],
                     'url': activationurl})
        content = self._cw._(self.content) % data
        subject = self._cw._(self.subject) % data
        return mail.format_mail({}, [recipient], content=content,
                                subject=subject, config=self._cw.vreg.config)

    def activation_url(self, data):
        data.pop(qname('upassword') + '-confirm', None)
        key = crypto.encrypt(data, self._cw.vreg.config['registration-cypher-seed'])
        return self._cw.build_url('registration_confirm', key=key)

    def success_redirect_url(self):
        msg = self._cw._(u'Your registration email has been sent. Follow '
                         'instructions in there to activate your account.')
        return self._cw.build_url('', __message=msg)


class RegistrationConfirmController(controller.Controller):
    __regid__ = 'registration_confirm'

    def publish(self, rset=None):
        req = self._cw
        try:
            data = crypto.decrypt(req.form['key'],
                                  req.vreg.config['registration-cypher-seed'])
            login = data[qname('login')]
            password = data.pop(qname('upassword'))
        except:
            msg = req._(u'Invalid registration data. Please try registering again.')
            raise Redirect(req.build_url(u'register', __message=msg))
        req.form = data # hijack for proper validation error handling
        self.appli.repo.register_user(login, password,
                                      email=data.get(qname('address')),
                                      firstname=data.get(qname('firstname')),
                                      surname=data.get(qname('surname')))
        # force new authentication (anon until there)
        clear_cache(req, 'get_authorization')
        req.form['__login'] = login
        req.form['__password'] = password
        if req.cnx:
            req.cnx.close()
        req.cnx = None
        try:
            self.appli.session_handler.set_session(req)
        except Redirect:
            pass
        assert req.user.login == login
        raise Redirect(self.success_redirect_url(data))

    def success_redirect_url(self, data):
        msg = self._cw._(u'Congratulations, your registration is complete. '
                         'Welcome %(firstname-subject)s %(surname-subject)s !')
        return self._cw.build_url('', __message=msg%data)


class UserLink(basecomponents.UserLink):
    def anon_user_link(self):
        super(UserLink, self).anon_user_link()
        self.w(u'&nbsp;[<a class="logout" href="%s">%s</a>]' % (
            self._cw.build_url('register'), self._cw._('i18n_register_user')))

## urls #######################################################################

class RegistrationSimpleReqRewriter(urlrewrite.SimpleReqRewriter):
    rules = [
        ('/register', dict(vid='registration')),
        ]

def registration_callback(vreg):
    vreg.register_all(globals().values(), __name__, (UserLink,))
    vreg.register_and_replace(UserLink, basecomponents.UserLink)
