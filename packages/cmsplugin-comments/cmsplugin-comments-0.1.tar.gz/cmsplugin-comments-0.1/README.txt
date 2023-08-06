To install cmsplugin-comments

pip install cmsplugin-comments

Add url(r'^comments/', include('django.contrib.comments.urls')), to urls.py
Add 'cmsplugin_comments' to INSTALLED_APPS

To Enable captcha

Add url(r'^captcha/',  include('captcha.urls')), to urls.py
Add 'capcha' to INSTALLED_APPS
Add COMMENTS_APP = 'cmsplugin_comments' to settings

To Enable emailing of new messages to admins add the following to settings

EMAIL_HOST=
EMAIL_PORT=
EMAIL_HOST_USER='my@email.com'
EMAIL_HOST_PASSWORD='xxx'
EMAIL_USE_TLS=True

Add a comment_notification_email.txt template to {project-home}/templates/comments

finally:

manage.py syncdb
manage.py migrate
