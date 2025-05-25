from flask import Flask, render_template, request, redirect, flash, url_for, abort
import os, json, datetime, requests, random, traceback
from markdown import markdown  # used for rendering readmes, so don't remove
from urllib.parse import quote  # for creating safe binder URLs

print("CWD:", os.getcwd())
print("Templates folder contents:", os.listdir(os.path.join(os.getcwd(), 'templates')))

app = Flask(__name__)
app.secret_key = 'rhododendron'  # required for flash() in contact form


@app.route('/')
def home():

    return render_template('index.html') 

GITHUB_USER = 'Novyfilip'

@app.route('/projects')
def projects():
    # Grab public repos using the GitHub API
    resp = requests.get(f'https://api.github.com/users/{GITHUB_USER}/repos')
    repos = resp.json() if resp.ok else []

    # Return trimmed info
    projects_list = [
        {"name": r['name'], "desc": r.get('description') or '', "url": r['html_url']}
        for r in repos
    ]
    return render_template('projects.html', projects=projects_list)


@app.route('/projects/<repo_name>')
def project_detail(repo_name):
    # Grabs basic metadata
    r = requests.get(f'https://api.github.com/repos/{GITHUB_USER}/{repo_name}')
    if not r.ok:
        return abort(404)
    data = r.json()

    # finds a notebook file if present
    contents = requests.get(f'https://api.github.com/repos/{GITHUB_USER}/{repo_name}/git/trees/main?recursive=1')
    notebook_file = None

    if contents.ok:
        tree = contents.json().get("tree", [])
        for f in tree:
            if f['path'].endswith('.ipynb') and not f['path'].startswith('.ipynb_checkpoints/'):
                notebook_file = f['path']
                break  # takes the first valid one

    binder_url = None
    if notebook_file:
        filepath = quote(notebook_file)
        binder_url = f"https://mybinder.org/v2/gh/{GITHUB_USER}/{repo_name}/main?filepath={filepath}"

    # tries grabbing a README in either casing
    readme_html = ''
    readme_req = requests.get(f"https://raw.githubusercontent.com/{GITHUB_USER}/{repo_name}/main/README.md")
    if not readme_req.ok:
        readme_req = requests.get(f"https://raw.githubusercontent.com/{GITHUB_USER}/{repo_name}/main/readme.md")
    if readme_req.ok:
        readme_html = markdown(readme_req.text)
    print("README preview (first 500 chars):", readme_html[:500])
    #debugging
    return render_template('project_detail.html',
                           name=data['name'],
                           desc=data.get('description', ''),
                           url=data['html_url'],
                           binder_url=binder_url,
                           readme=readme_html)  # now to pass it in


@app.route('/interests/')
def interests():
    # used for my hobby slideshow
    images = [url_for('static', filename=f'img/{i}.jpg') for i in range(1, 6)]
    captions = [
        "Board games in Hamburg, Winter",
        "Me in Paris, Winter",
        "Gym PR day, Spring",
        "Running in the Kolding Fjord, Spring",
        "My best steak, Summer",
    ]

    return render_template('interests.html', images=images, captions=captions)


@app.route('/notebooks')
def notebooks():
    # manually linked notebooks here if needed
    nb = [
        ("Car Classification", "Car classification.ipynb")
        # add more if necessary
    ]
    return render_template('notebooks.html', notebooks=nb)

def get_random_motd():
    try:
        with open(os.path.join(os.path.dirname(__file__), 'data', 'motd.json'), 'r', encoding='utf-8') as f:
            messages = json.load(f)
        if messages:
            return random.choice(messages)
    except Exception as e:
        print("MOTD error:", e)
    return None
DATA_FILE = os.path.join(os.path.dirname(__file__), 'data', 'messages.json')
MOTD_FILE = os.path.join(os.path.dirname(__file__), 'data', 'motd.json')
print("Resolved MOTD path:", MOTD_FILE)

def get_random_motd():
    try:
        with open(MOTD_FILE, 'r', encoding='utf-8') as f:
            messages = json.load(f)
        if messages:
            return random.choice(messages)
    except Exception as e:
        print("MOTD load error:", e)
    return None

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    motd = get_random_motd()  # Uses the helper now
    print("Contact MOTD selected:", motd)
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        msg = request.form.get('message')

        if not (name and email and msg):
            flash("Oops, all fields are required!")
            return redirect('/contact')

        entry = {
            "time": datetime.datetime.now().isoformat(),
            "name": name,
            "email": email,
            "message": msg
        }

        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except:
            data = []

        data.append(entry)

        try:
            with open(DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
        except:
            flash("Message received but saving failed.")
            return redirect('/contact')

        flash(f"Thanks, {name}! Your message is saved.")
        return redirect('/contact')

    return render_template('contact.html', motd=motd)





# For production on Render, thats why debug mode is off
if __name__ == '__main__':
    debug = os.environ.get("FLASK_DEBUG", "true") == "true"
    app.run(debug=debug)
