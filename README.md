# FLASH CARD
#### Video Demo:  https://youtu.be/DzFZrWlqFC4?si=EcWTT1ibY0aalPdj
#### Description:

Hello CS50,

Here is my final project. In this project, I have created a web app where users can create and manage flashcards, and we can review these flashcards using the spaced repetition technique. Let me explain what I have done in this project.

This web app allows users to register and log in with accounts. Once logged in, users can create and delete folders. These folders serve as containers for flashcards, and each flashcard holds the information you want to retain and review.

It also features functions to manage and edit the flashcards. Newly created cards are initially placed in Box 1. After studying a flashcard, you have three options: "hard," "normal," and "easy." If you choose "easy," the card will be moved to Box 5 and will be reviewed again after 2 weeks. If you choose "normal," it will be advanced to the next box. If you click "hard," the card will be reset to Box 1 and will be reviewed daily.

Alright, let's explore how I applied the learned knowledge to create it.

First is the app.py, where I wrote the logic for the website. This is where I handle routes and where data flow is processed. In app.py, I import a pre-written function file called helper.py, which has been very helpful for me in processing data access in the flashcard.db database. This database contains tables for users to manage users, decks to manage folders, and decks and cards used to manage the flashcards.

And I have also created some HTML files to build the web interface. First is login.html, this page is for users to log in. If you don't have an account, you will need to register on the register.html page. After you have registered and logged in, you can freely create, delete, and open decks which are displayed as folders in index.html. If you click "Open," you will be redirected to the insidedeck.html page.

Upon entering insidedeck.html, you will see five boxes. Box 1 contains cards that need to be reviewed daily, Box 2 is for every once a day, Box 3 for every three days, Box 4 for every seven days, and Box 5 for every fourteen days. Cards are automatically sorted within the boxes, and the boxes increment after each study session. If the specified days pass, the cards will appear for review when you study.

When you open a box, you will see a list of cards within that box. You can also delete and edit cards.

There are other files like apology.html and congra.html that I've created to inform users when they input something incorrectly or when they've completed a lesson. Then, there's layout.html, which I designed to create a navigation bar for the entire website.

This is my first project, even though it contains numerous mistakes and many parts that I'm not satisfied with, I am truly proud of it. It's my first time creating a product, setting up challenges for myself, and solving them. There were many difficulties throughout the process of building this website, and I went online to research and gather much-needed knowledge to equip myself further.

After the course, I realized that what CS50 provided me with is more than just programming knowledge. It taught me how to handle problems and the ability to learn on my own. Looking back a few months ago, I see that I didn't even know how a website truly works. I'm genuinely proud of how far I've come.


I sincerely thank CS50 as well.