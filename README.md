Venmom 0.01 by Larry Gadea <trivex@gmail.com>.

This script will transfer your Venmo balance to your real bank account. It should be 
safe to put this on a nightly cron.

Venmo (venmo.com) is a service like PayPal, except better about fees, features and 
general attitude towards the customer. They're really great.


BRIEF BACKGROUND
----------------

Venmo, although it's an awesome service, is also not FDIC insured. Since they're
just a startup, it's very possible that if they go bankrupt, they might be forced to 
take your money down with them. Until they get FDIC, using a script like this will 
ensure that your money stays where it's safest -- in your bank account.


QUICK START
-----------

1.  Download the .py file and edit the USERNAME and PASSWORD constants
2.  Run it using `python venmom.py`
3.  After you're satisfied, add it to your crontab
4.  Have a lovely day


LEGAL
-----

Please send your cease and desist to trivex@gmail.com. Otherwise, I'd love to hear 
comments/suggestions too!

Oh and btw, I cannot be held liable for whatever the script decides to do. There's no
warranty here folks, so run it at your own risk. If by some chance it does blow up on
you, consider fixing it and sending me the patch. :)

This code is unlicensed. Feel free to tell all your friends that you wrote it (though
I have no idea why you'd want to do that)

Thanks!