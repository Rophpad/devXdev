import requests
from flask import Flask, render_template, request
from functions import *
from db import *


app = Flask(__name__)
app.config['DEBUG'] = True


session = Session()

GITHUB_TOKEN = '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'
user_datas = {}

@app.route('/')
@app.route('/presentation', strict_slashes=False)
def presentation():
    """Render presentation page"""
    
    return render_template('presentation.html')


@app.route('/developers', strict_slashes=False)
def developers():
    """Render developers page"""
    all_users = session.query(ghUser).all()

    print(all_users)

    return render_template('developers.html')


@app.route('/mystats', strict_slashes=False, methods=['GET', 'POST'])
def mystats():
    """Gets somes information about a user githubhub"""

    typed_username = None
    if request.method == 'POST':
        typed_username = request.form.get('username')
        if not typed_username:
            render_template('layout.html')
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

                # Database feature       
                new_user = ghUser(
                                        username=typed_username,
                                        profile_pic=user_datas['profile_pic'],
                                        login=user_datas['login'],
                                        html_url=user_datas['html_url'],
                                        public_repo_count=user_datas['public_repo_count'],
                                        top_languages=', '.join(user_datas['top_languages'].keys()),
                                        activity_count=user_datas['activity_count'],
                                        r_without_issues=user_datas['r_without_issues'],
                                        no_readme=user_datas['no_readme'],
                                        total_team_project=user_datas['total_team_project']
                                        )
                session.add(new_user)
                session.commit

                global all_users 
                all_users = session.query(ghUser).all()
                print(all_users)
                print(repr(new_user))
                print(new_user.top_languages)

                #session.close()
                # end database feature

                return render_template('mystats.html', user_datas=user_datas)


    return render_template('layout.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, threaded=True)
