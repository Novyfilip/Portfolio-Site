from flask import Flask, render_template, request, redirect, flash, url_for, abort
import os, json, datetime, requests
print("CWD:", os.getcwd())
print("emplates folder contents:", os.listdir(os.path.join(os.getcwd(), 'templates')))


app = Flask(__name__)
app.secret_key = 'rhododendron'  # Required for flashing messages int he contact form

DATA_FILE = os.path.join(os.path.dirname(__file__), 'data', 'messages.json')

@app.route('/')
def home():
    return render_template('index.html')  # main page

GITHUB_USER = 'Novyfilip'
@app.route('/projects')
def projects():
    resp = requests.get(f'https://api.github.com/users/{GITHUB_USER}/repos')
    repos = resp.json() if resp.ok else []
    projects_list = [
      {"name": r['name'], "desc": r.get('description') or '', "url": r['html_url']}
      for r in repos
    ]
    return render_template('projects.html', projects=projects_list)

@app.route('/projects/<repo_name>')
def project_detail(repo_name):
    # Fetch the repo metadata
    r = requests.get(f'https://api.github.com/repos/{GITHUB_USER}/{repo_name}')
    if not r.ok:
        return abort(404)

    data = r.json()
    return render_template('project_detail.html',
                           name=data['name'],
                           desc=data.get('description',''),
                           url=data['html_url'])

    

#@app.route('/interests')
@app.route('/interests/')
def interests():
    # build lists of image URLs and matching captions
    images = [ url_for('static', filename=f'img/{i}.jpg') for i in range(1,6) ]
    captions = [
      "Board games in Hamburg, Winter",
      "Me in Paris, Winter",
      "Gym PR day, Spring",
      "Running in the kolding Fjord, Spring",
      "My best  steak, Summer",
    ]

    # pass *both* into the template context
    return render_template('interests.html',
                           images=images,
                           captions=captions)

@app.route('/notebooks')
def notebooks():
    # list of (name, filepath) tuples
    nb = [
       ("Car Classification", "Car classification.ipynb")
       #,  
     # will add more
    ]
    return render_template('notebooks.html', notebooks=nb)

@app.route('/contact', methods=['GET','POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        msg  = request.form.get('message')

        if not (name and msg):
            flash("oops, need both name & message")
            return redirect('/contact')

        # build the entry
        entry = {
            "time": datetime.datetime.now().isoformat(),
            "name": name,
            "message": msg
        }

        # load existing, append, save back
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            print("couldn't read JSON, starting fresh:", e)
            data = []

        data.append(entry)

        try:
            with open(DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print("error writing JSON:", e)
            flash("Your message was received but not saved :(")
            return redirect('/contact')

        flash(f"Thanks, {name}! Your message is saved.")
        return redirect('/contact')

    return render_template('contact.html')



#For production, we need to set the FLASK_ENV environment variable to production
if __name__ == '__main__':
    debug = os.environ.get("FLASK_DEBUG", "true") == "true"
    app.run(debug=debug)
