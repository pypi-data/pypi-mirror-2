Example
+++++++

The ``bag_mail.py`` example sets up a pipe stack with a mail pipe. It should be
run from the command line like this:

::

    python bag_mail.py <config>

You'll need to have the dependencies such as ``BareNecessities`` installed or
you will get a complaint that ``MailPipe`` couldn't be imported.

Each time the example is run you will be prompted for an email address to
recieve the test message. The way that email is actually sent will be
determined by the settings in the config file.

There are a number of different config files as examples:

``smtp.conf``
    The email is sent via SMTP. You'll need to entere your own SMTP server
    details in the config file.

``sendmail.conf``

    The email is sent via SMTP. You may need to check a sendmail-compatible
    binary is installed and update the path to that binary. Postfix is a good
    choice if you don't have any mail software.

``debug_folder.conf``
    In this case no emails are sent at all. Whatever the settings the emails
    all get stored as files in the debug folder. Very handy for debuging live
    data without irritating lots of users.

``to_email_override.conf``
    As an alternative debug method you can instead specify the
    ``to_email_override`` field which will send emails, but will send them to the
    list of emails specified and not to the real recipents. You'll need to update
    the config file with your own email addresses for the example to work.

