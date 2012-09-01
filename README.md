facebook-moods
==============

A console Python application to categorize the moods of Facebook posts using the Klassif.io cloud machine learning algorithm.

This application runs using the public classifier I created with id 5. It accepts the following categories: happy, sad, in_love, and angry. The program will skip a post if you type none.

It supports auto mode which pulls down a batch of Facebook posts that match the search query you provide. You will be presented with each post and you can classify each as happy, sad, in_love, or none. 

The second mode is manual, in which you enter the text of the facebook post (or other source if it is similar, such as a twitter post) and then you will be prompted to categorize it. Each categorization is immediately uploaded to Klassif.io.
