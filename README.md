# Caucab

## About
This is a social network project I'm building just because it construction is full of things I can learn from. 

## Status
The project is in a early stage but I've decided to share it because it may help to someone. The database provided in this repo has 3 users. Admin who is a superuser, "facebook" and "twitter". All have the same password "ISaPASSword"

## Characteristics
This social network shares the message system of twitter and the circles of google plus. You can share a message and all the people following you will see it. Also you can add people to circles, the idea is that in circles you add the people you read the most or you want to be updated about.

Also you can create hashtags and make mentions.

## Things I've cared about

* Mentions and hashtags are clickeable. That means that when they are rendered a templatetag makes them links.
* Circles can be customized by colors specified in the models.py
* You can't insert html code in the messages.

## To do
In short time I want to:
* Builb view to list all messages by hastags.
* Create page to manage circles. Now you have to do it from the admin-panel.
* Be able to insert clickeable links.
* Change views from using functions to classes.
* Create a rest api.

Not near but I want:
* Integrate channels

