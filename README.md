# fsnd-p2-mublog
A multi-user blog for Udacity FSND project 2

This blog uses the webapp2 framework and jinja2 templates.

The current templates use basscss for style.

A running demo site can be found at: [demo site](tbd)

## instructions for running this project

## should have punch-list

### from hw set 1
list page with list of posts:
  - [ ] titles of the posts
  - [ ] dates of the posts
  - [ ] authors of the posts
  - [ ] each title links to permalinks

new post form with:
  - [ ] route /newpost
  - [ ] 'subject' title input
  - [ ] 'content' blog textarea
  - [ ] submit button
  - [ ] * cancel button that clears form
  - [ ] redirect to permalink on submit

blog posts with:
  - [ ] Permalinks like '/blog/1001'
  - [ ] title, content, author, date, * likes
  - [ ] if logged in update, delete
  - [ ] like button

### from hw set 2
create new user with:
  - [ ] route /signup
  - [ ] username unique required input
  - [ ] password unique required input
  - [ ] verify password required input
  - [ ] email optional input
  - [ ] set a valid cookie
  - [ ] redirect to welcome if (secure) cookie present
  - [ ] * hash pass
  - [ ] * link to login if there is an account

welcome page for new accounts with:
  - [ ] route /welcome
  - [ ] message saying Welcome, {username}!
  - [ ] * link to /newpost
  - [ ] * link to logout
  - [ ] * list of own posts with update & delete links

login page
  - [ ] route /login
  - [ ] username required input
  - [ ] password required input
  - [ ] valid cookie on login
  - [ ] redirect to welcome if cookie present
  - [ ] *link to signup

logout route
  - [ ] route /logout
  - [ ] clears all cookies
  - [ ] redirects to signup page

### other  

update own post form for each post with:
  - [ ] 'subject' title input
  - [ ] 'content' blog textarea
  - [ ] submit button
  - [ ] cancel button that clears form
  - [ ] delete button that deletes post
  - [ ] redirect to permalink on submit

delete own posts with:
  - [ ] route permalink/delete

like-ability:
  - [ ] logged in users can like stuff
  - [ ] only one like per user
  - [ ] can't self love

template:
  - [ ] site navigation


### in progress
  - [ ] template chopping rough
  - [ ] static site_data schema

