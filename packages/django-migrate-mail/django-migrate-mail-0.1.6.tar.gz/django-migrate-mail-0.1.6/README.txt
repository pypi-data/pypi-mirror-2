Copy Gmail mailbox contents to another Gmail mailbox.
https://bitbucket.org/msayapin/gmailcopy

Please install gdata by:
pip install -e hg+https://gdata-python-client.googlecode.com/hg/@7e1465f46ef6162ec27bf8712eddd046c257c58a#egg=gdata

USAGE
=====

pip install django-migrate-mail

Add `migrate_mail` to INSTALLED_APPS, include the url pattern:

    (r'^url/to/migrate/', include('migrate_mail.urls')),

Run syncdb --migrate to apply database migrations.