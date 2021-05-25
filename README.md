# Our Lockdown Reads

![our lockdown books logo file](static/images/our-lockdown-reads-logo.png)

Our Lockdown reads is a community driven site where users can come to 
review books they have read during lockdown and read other members reviews of other books.
The website will build a database of the books our users have read and provide links to purchase 
the books should our users choose to.


## Table of contents

## UX 

### Project Goals

The Goal of this project is to create a user friendly interface so users can submit the books that 
they have read through lockdown and being able to read other users reviews , this goal will be achieved by 
building a database and providing functionality to the users to create , read update and delete their posts.
there will also be links to the books reviewed so if a user likes a book they can follow the link and 
purchase he book for themselves.

### User Goals 

- Create a Profile upon registering

- Create a book review

- Read other users reviews

- Be able to purchase a book I liked 

-  See which book reviews are most liked 

### User Stories

As a first time user of the website I would like to:

- Register and create my profile

- Leave a review for a book I read during lockdown

- Read other users reviews

- Be able to follow a link to purchase a book whose review I liked

As a returning user I would like to:

- Edit or Update my profile

- Edit or Delete my book reviews

- See if any other users liked my reviews

- See if there is any new reviews since my last visit 

### Site Owner Goals 

As the site owner I would like to: 

- Build a database of all the books my users read during lockdown.

- Be able to see which books were most liked so as to see what book I might read next

- With affiliate links to online book stores the website could work as a business model where 
I could generate revenue through my users purchasing books through the links provided in the reviews

### User Requirements and Expectations

- Well layed out UX design which is user friendly, easy to navigate,
accessable and responsive

- The user should be able to navigate easily throughout the site, this could easily be attained with theuse of a fixed navbar

- The site should be able to handle, access, store and present back the data to the user 
in clear , strucured way

- The user should be the only one able to edit and delete his/her reviews while all users should be able to read the reviews

- Editing and deleting of reviews and creating new reviews should be granted to users by the principles of C-R-U-D functionality

## Structure Of The Project

The main focus of the website is being able to utilize the database and display the correct conents to the user.
I have used mongodb to create 3 collections for storing the data , they are users for 
storing our registered users passwords and username to access their profile and create, update and delete their reviews. All users registered 
or not can read all reviews.
the next collection is labelled Books and this will store all the data
for the book in which a user has reviewed and willbe stored under the following keys

- _id
- book_name
- book_author
- genre 
- rating 
- review_title
- review
- reviewed_by
- image_url
- purchase_link

with the data that has been input to the fields we should be able to create 
an informative site hat is pleasing to the eye.

Lastly I hav created a collection for genres which will relate to the genre 
field of the previous database, this will help to organize the books by genre 
and I will be able to add more genres if or split an over subscribed genre into 
2 seperate genres.

## Design Choices 

### Fonts

### Colour Scheme

### Icons

### Wireframing

### Features

### Technologies Used

- HTML

- CSS

- JAVASCRIPT 

- JQUERY

- PYTHON 

- MONGODB

- PYMONGO 

- FLASK


### Testing

### Bugs / Fixes

### Deployment

### Credits

- [randomkeygen.com](https://randomkeygen.com/) for allowing me to create a secure secret key.

- [canva.com](https://www.canva.com/) for the free pro trial which allowed me to create my logo.

- 