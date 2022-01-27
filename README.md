# LoginAuthentication

I have used django to create a website login system.

It has a many different kinds of templates. 

First is login.html which requires username and passoword to login and also has forget passowrd link.
Furthermore , fortgetpwd.html will ask you to enter registered email and then will send the otp to the provided email.
After 1 min, the reset otp link will be activate and when clicked on it, otp will send on your email id again.
Then after validating the otp if it is correct thhen it will redirect you to resetpwd.html where you can reset your password.


Once eveything is valid , you will be render to index.html.
Index page also contain logout link which onclicked will logout you from the website.
Logout page has link which will again take you to login page.

This is a simple but versatile login system with validation at each stage.

Feel free to use this repository in your website.
