# Motivation
I decided to make a personal portfolio as the topic of my project because it brings me the most personal utility. I don’t currently have a job and I’m hoping this will help me find one. I’ve bought a domain (filipnovy.dk) to host it on too.
# Features
## HTML and Styling
The website has a light and dark theme, switchable with 🌙☀️ emojis. There is a navbar leading to sites about my projects, interests and a contact page. The header and footer are a gradient. The grid is present in my Projects site; they are projects automatically pulled from my Github account, with the repo name and description rendered there. Contact includes a form that checks valid email format and whether it’s full. It gives an error message if not.
## CSS Responsive Design
The site adjusts to screen size dynamically. Most features on the site have a css-defined custom appearance.
Javascript User interaction
There are buttons to change theme and font size. The form gives a message upon successful/unsuccessful validation. In my Interests page, there is an image slider that changes both automatically and with arrows. If you mouse over the picture, it provides a description.
## Backend/Server Processing
 If the contact form is filled successfully, the message is saved in a json file. Furthermore, the Contact page loads a random data science related insight from a json file upon every refresh. Also, I use github API to display repo names (hypertext link to the repo), description, Read Me and if the repo contains a notebook, one can open it with a button live using the Binder library. One can also download my CV from the main page.

## Structure

- `app.py`: The main Flask backend routing.
- `templates/`: Contains HTML pages using Jinja2 templating (`base.html` layout).
- `static/`: Includes `style.css` for styling and `script.js` for interactivity.
- `data/`: includes a place to store messages, json that loads random insights
