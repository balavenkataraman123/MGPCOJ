# Cs50w final project documentation

The application I created is a website for students to practice math and compete. I was inspired to make this by the numerous competitive programming websites with thousands of problems of varying levels and leaderboards where users can compete with each other, like DMOJ and codeforces.

## Distinctiveness and complexity

This is distinct from all the other projects done previously in the course, as it is a competitive problem-solving platform where users compete to solve problems (even though I originally designed it for math problems it can be used for any subject)

It is complex because it has 3 models, one for users, one for problems and one for submissions. It actually has functionality and practical use, and it fulfils all the requirements. It has 250 lines of views, 75 lines of models, about 50 lines of js, and 9 HTML files

Users who are set as problem setters by the website admin can create problems, and other users get points for solving them. While making a problem you provide the title of the problem, the text of the problem, the answer, the solution, the level and the XP earned from solving it. Optionally you can provide the URL of an image for the question and solution. Most hosting services have limited storage, so it will be better for the users to upload the images to a free 3rd party image hosting service like imgbb.com and provide the URL rather than having it fill up the hard drives of the server.

How to run: just make migrations and run the server
To add problems log in with an admin user (python manage.py createsuperuser) and click on the user profile and check the box ‘isproblemsetter’. A link to make problems appears in the navbar, clicking on it takes you to the page to make a problem

Clicking on ‘problems’ in the navbar shows a list of all the problems, with their level, point value, category and link. You can search problems, or order them by any property. From a problem’s page, you can solve it. If you get the answer correct on the first try, you get the full XP, if you get it correct on the second try, you get half the points. You cant get more than 2 tries, to stop people from trying every possible answer to a question. If you’ve got it correct or got it wrong both tries, it shows a button to reveal the solution and a link to get other similar problems, based on the level and category

Clicking on the Leaderboard link in the navbar shows the list of all users, which you can sort by name, points or problems solved. There is also a link to the user profile where you can see the user’s description (like what school they are from)

This platform aims to make learning and practicing more fun and competitive. I am also going to add the functionality to make live contests soon, with a timer and a live leaderboard.
