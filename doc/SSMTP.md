# Set Up SSMTP for PHP

First, edit `/etc/ssmtp/ssmtp.conf`:

    # File: /etc/ssmtp/ssmtp.conf                                    
    
    # The user that gets all the mails (UID < 1000, usually the admin)
    root=noreply@hk-tippspiel.com
    
    # The mail server (where the mail is sent to), both port 465 or 587 should be acceptable
    # See also https://support.google.com/mail/answer/78799
    mailhub=smtp.strato.de:587
    
    # The address where the mail appears to come from for user authentication.
    rewriteDomain=hk-tippspiel.com
    
    # The full hostname.  Must be correctly formed, fully qualified domain name or GMail will reject connect$
    hostname=hk-tippspiel.com
    
    # Use SSL/TLS before starting negotiation
    UseTLS=Yes
    UseSTARTTLS=Yes
    
    # Username/Password
    AuthUser=noreply@hk-tippspiel.com
    AuthPass=PASSWORD
    AuthMethod=LOGIN
    
    # Email 'From header's can override the default domain?
    FromLineOverride=yes

Then edit `/etc/ssmtp/revaliases`

    # File: /etc/ssmtp/revaliases    
    #
    # sSMTP aliases
    # 
    # Format:	local_account:outgoing_address:mailhub
    #
    # Example: root:your_login@your.domain:mailhub.your.domain[:port]
    # where [:port] is an optional port number that defaults to 25.
    
    root:noreply@tippspiel.krumreyh.com:smtp.strato.de:465
    mainuser:noreply@tippspiel.krumreyh.com:smtp.strato.de:465
    
Test configuration with:

    echo test | mail -v -s "testing ssmtp setup" hermann@krumreyh.com