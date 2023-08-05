Manual
++++++

Without PipeStack
=================

There is currently no documentation for using the Mail API without PipeStack
but the tests are well documented so please read them. They can be found in the
``test`` directory of the source distribution.

Using the Mail Pipe
===================

Set up a pipe stack like this:

.. include :: ../../example/bag_mail.py
   :literal:


The ``bag.mail.send()`` function looks like this:

::

    def send(
        message,
        to,
        from_email,
        from_name,
        subject=None,
        type='plain',
        charset=None,
    )

The core config options you can use are:

``sendmail``

    The path to the sendmail program, eg ``/usr/bin/sendmail``. If this is
    specified then sendmail is used to send emails.

``smtp.host``

    The hostname or IP address of the SMTP server to use. If this is specified
    then SMTP is used to send emails. If you are using SMTP you can use the
    following optional options:

    ``smtp.username``
        The SMTP username

    ``smtp.password``
        The SMTP users's password

    ``smtp.port``
        The SMTP port (only needed if it isn't 25)

    ``smtp.starttls``
        Can be specified as ``true`` or ``false``. If ``true`` then TLS will be
        used, defaults to ``false`` if not specified.

    ``smtp.verbose``
        Logs lots of information about any SMTP communication

There are also two options which are very useful when debugging:

``debug_folder``

    This is path to an existing directory where all emails should be stored as
    text files *instead* of being sent. This means you can debug your application
    without the emails actually being sent.

``to_email_override``

    This should be a comma separated list of email addresses where every email
    should be sent to *instead* of the original recipents. This is useful for
    debugging when you want the emails to be sent to a test email address or a set
    of test email addresses.

Setting up Postfix
==================

A common senario you may encounter is having a web server and wanting to send
mail directly from it. The easiest approach is to use the SMTP setup and have
the mail sent from a proper mailserver but if you don't have a mailserver or an
SMTP account you can use, you'll have to install one on your web server. The
difficulty is that you'll only want the web server to be able to send mails,
not recieve them.

A good piece of software for handling mail delivery is Postfix. In Postfix
terminology the setup described above is called a `null client
<http://www.postfix.org/STANDARD_CONFIGURATION_README.html#null_client>`_ and
this is what you'll want to set up.

Here's how to do it on Ubuntu/Debian-based systems:

::

    sudo apt-get install postfix

You'll be shown this screen:

::


    ┌───────────────────────────┤ Postfix Configuration ├───────────────────────────┐
    │ Please select the mail server configuration type that best meets your needs.  │ 
    │                                                                               │ 
    │  No configuration:                                                            │ 
    │   Should be chosen to leave the current configuration unchanged.              │ 
    │  Internet site:                                                               │ 
    │   Mail is sent and received directly using SMTP.                              │ 
    │  Internet with smarthost:                                                     │ 
    │   Mail is received directly using SMTP or by running a utility such           │ 
    │   as fetchmail. Outgoing mail is sent using a smarthost.                      │ 
    │  Satellite system:                                                            │ 
    │   All mail is sent to another machine, called a 'smarthost', for delivery.    │ 
    │  Local only:                                                                  │ 
    │   The only delivered mail is the mail for local users. There is no network.   │ 
    │                                                                               │ 
    │ General type of mail configuration:                                           │ 
    │                                                                               │ 
    │                            No configuration                                   │ 
    │                            Internet Site                                      │ 
    │                            Internet with smarthost                            │ 
    │                            Satellite system                                   │ 
    │                            Local only                                         │ 
    │                                                                               │ 
    │                                                                               │ 
    │                     <Ok>                         <Cancel>                     │ 
    │                                                                               │ 
    └───────────────────────────────────────────────────────────────────────────────┘ 
                                       

Choose ``No configuration``.

The installation whirrs away and leaves you with this advice:

::

    Postfix was not set up.  Start with 
      cp /usr/share/postfix/main.cf.debian /etc/postfix/main.cf
    .  If you need to make changes, edit
    /etc/postfix/main.cf (and others) as needed.  To view Postfix configuration
    values, see postconf(1).
    
    After modifying main.cf, be sure to run '/etc/init.d/postfix reload'.
    
You'll now have a ``/usr/sbin/sendmail`` binary ready for sending mail. You can test it like this:

::

    cat << EOF | sendmail -t
    to:peter@example.net
    from:james@example.com
    subject:Testing 123
    
    EOF

You'll see this error because Postfix isn't setup yet:

::

    sendmail: fatal: open /etc/postfix/main.cf: No such file or directory

Run these commands replacing ``$mydomain`` with the domain name you want your emails to appear to come from:

::

    sudo cp /usr/share/postfix/main.cf.debian /etc/postfix/main.cf
    sudo postconf -e "myorigin = $mydomain"
    sudo postconf -e "relayhost = $mydomain"
    sudo postconf -e "inet_interfaces = loopback-only"
    sudo postconf -e "local_transport = error:local delivery is disabled"

Finally edit ``/etc/postfix/master.cf`` and comment out the local delivery agent entry changing this:

::

    local     unix  -       n       n       -       -       local

To this

::

    #local     unix  -       n       n       -       -       local

Now try again:

::

    cat << EOF | sendmail -t
    to:peter@example.net
    from:james@example.com
    subject:Testing 123

    EOF

You'll get this:

::

    postdrop: warning: unable to look up public/pickup: No such file or directory

That's because you haven't started postfix:

::

    sudo /etc/init.d/postfix start

The mail pipe can now send email in sendmail mode.

I don't really consider myself a Postfix expert yet so if you spot any problems
with the configuration above, please let me know.
