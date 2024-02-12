import requests
from pprint import pprint
from flask import Flask, render_template, request, redirect, url_for
from functions import *
from fileStorage import FileStorage


app = Flask(__name__)
app.config['DEBUG'] = True


GITHUB_TOKEN = ''
user_datas = {}
storage = FileStorage()
all_users_datas = storage.load_data()

@app.route('/')
@app.route('/presentation', strict_slashes=False)
def presentation():
    """Render presentation page"""
    
    return render_template('presentation.html')


@app.route('/developers', strict_slashes=False, methods=['GET', 'POST'])
def developers():
    """Render developers page"""
    
    pprint(all_users_datas)

    if request.method == 'POST':
        if request.form['btn'] == 'All':
            return render_template(
                'developers.html', all_users_datas=all_users_datas, total=storage.count_data()
            )
        elif request.form['btn'] == 'Refresh':
            pass
        elif request.form['btn'] == 'Profile':
            pass
    else:
        return render_template('layoutdevs.html')

@app.route('/mystats', strict_slashes=False, methods=['GET', 'POST'])
def mystats():
    """Gets somes information about a user githubhub"""

    typed_username = None
    if request.method == 'POST':
        typed_username = request.form.get('username')
        if not typed_username:
            render_template('layout.html')
        else:
            global matched
            isin = False
            for data in all_users_datas:
                if data['login'].lower() == typed_username.lower():
                    matched = data
                    isin = True 

            print(isin)
                
            if isin:
                return render_template('mystats.html', user_datas=matched)
            else:
                url = 'https://api.github.com/users/{}'
                headers = {'Authorization': f'token {GITHUB_TOKEN}'}


                response = requests.get(url.format(typed_username),
                                    headers=headers)
                if response.ok:
                    response = response.json()
                    user_datas = {
                        'profile_pic': response['avatar_url'],
                        'created_at': response['created_at'],
                        'login': response['login'],
                        'html_url': response['html_url'],
                        'public_repo_count': response.get('public_repos', 0),
                        'top_languages': get_user_languages
                        (typed_username, GITHUB_TOKEN),
                        'activity_count': get_user_coding_activity
                        (typed_username, GITHUB_TOKEN),
                        'r_without_issues': get_repos_without_issues
                        (typed_username, GITHUB_TOKEN),
                        'no_readme': get_repos_without_readme
                        (typed_username, GITHUB_TOKEN),
                        'total_team_project': get_team_projects_count
                        (typed_username, GITHUB_TOKEN)
                    }
                
                    storage.append_data(user_datas)
                
                    return render_template('mystats.html', user_datas=user_datas)


    return render_template('layout.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, threaded=True)
