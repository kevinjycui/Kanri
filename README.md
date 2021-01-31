![](https://challengepost-s3-challengepost.netdna-ssl.com/photos/production/software_photos/001/373/912/datas/gallery.jpg)

## Inspiration
In a time when working from home is the norm, we seek solutions to more efficiently managing businesses and projects online. The key to effective remote collaboration is a management tool to tie it all together. Kanri uses open-source natural language processing libraries from NLTK and Stanford NLP to communicate and direct information amongst a team on Slack.

## What it does
Kanri is a personal bot that keep track of information communicated within a business to manage and stimulate participation amongst a team. It keeps track of schedules by tracking dates and times mentioned in Slack and SMS messages to be reviewed by the team. It learns information as it chats, building a knowledge base of the project to spread to members of the team.

![](https://challengepost-s3-challengepost.netdna-ssl.com/photos/production/software_photos/001/374/001/datas/gallery.jpg)

## How we built it
The core natural language processing uses two libraries. The open-source Python library NLTK uses a Tf-IDF and Cosine Similarity approach to find the most relevant responses to inquiries and conversations with the bot. The open-source Stanza library by the Stanford NLP Group allows for POS tagging in order to identify and store entities from within messages to be relayed in the future, as well as determining whether a message is a question or a statement. Using Flask, ngrok, and the Slack API, these libraries are connected to a Slack App to allow team members to interact with it. Using Twilio, we were able to add SMS implementation as well.

## Challenges we ran into
The toughest challenge was figuring out how the natural language processing algorithms worked and how to implement them into the bot. Being able to identify certain elements with a high enough accuracy was difficult, and sometimes several libraries had to be employed in order to accomplish this.

## Accomplishments that we're proud of
We are proud of building a functioning NLP chatbot despite having no prior experience in machine learning. The bot is able to converse and learn rudimentary information, and link entities to other entities.

## What we learned
We learned the process of natural language processing and one of its applications.

## What's next for Kanri
Making Kanri a functioning chatbot was a huge challenge, and as we were given such a short time to complete it, there is still a lot of potential. New features to further improve the efficiency of a team can be implemented, such as features to conduct routine checkups and standups, as well as improvements in the NLP itself, such as working off of the POS tagging to change tenses in responses (eg. change first-person statements to second-person when used in response).
