import requests
from pprint import pprint
from flask import Flask, render_template, request, flash, redirect, url_for
from functions import *
from fileStorage import FileStorage


app = Flask(__name__)
app.config['DEBUG'] = True
app.secret_key = "secret key"


GITHUB_TOKEN = ''
user_datas = {}
storage = FileStorage()
all_users_datas = storage.load_data()

# Filter options to display __start__
prog_langs = ['Programming Languages', '__________  All  __________']
coding_freq = ['Coding frequency', '__________  All  __________']
countries = ['Country', '__________  All  __________']

for user_infos in all_users_datas:
    if user_infos['top_languages']:
        for lang in user_infos['top_languages'].keys():
            if lang not in prog_langs:
                prog_langs.append(lang)
            else:
                pass

    location = user_infos['location']
    if location and location not in countries:
        countries.append(location)

coding_freq = coding_freq + ['Low', 'Medium', 'High']
filter_options = [prog_langs, coding_freq, countries]
# Filter options to display __end__


@app.route('/')
@app.route('/presentation', strict_slashes=False)
def presentation():
    """Render presentation page"""

    return render_template('presentation.html')


@app.route('/developers', strict_slashes=False, methods=['GET', 'POST'])
def developers():
    """Render developers page"""
    all_users_datas = storage.load_data()

    # pprint(all_users_datas)

    if request.method == 'POST':
        if request.form['btn'] == 'All':
            return render_template(
                'developers.html',
                filter_options=filter_options,
                all_users_datas=all_users_datas,
                total=storage.count_data()
            )
        elif request.form['btn'] == 'Refresh':
            # Filter users __start__
            # all_users_datas = []
            filters = {}
            prog_lang_selected = request.form.get('prog_lang')
            coding_freq_selected = request.form.get('coding_frequency')
            country_selected = request.form.get('Country')

            if prog_lang_selected:
                filters['prog_lang'] = prog_lang_selected

            if coding_freq_selected:
                filters['coding_freq'] = coding_freq_selected

            if country_selected:
                filters['country'] = country_selected

            # pprint(filters)

            all_users_datas = storage.filterby(filters)
            # pprint(all_users_datas)
            # Filter users __end__
            """
            flash('Not already implemented!')
            flash('Try the button "All"')
            return render_template(
                'layoutdevs.html', filter_options=filter_options
            )
            """

            return (
                render_template(
                    'developers.html',
                    filter_options=filter_options,
                    all_users_datas=all_users_datas,
                    total=len(all_users_datas)
                )
            )
    else:
        return render_template(
            'layoutdevs.html', filter_options=filter_options
        )


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

                response = requests.get(
                    url.format(typed_username), headers=headers
                )
                if response.ok:
                    response = response.json()
                    user_datas = {
                        'profile_pic': response['avatar_url'],
                        'created_at': response['created_at'],
                        'login': response['login'],
                        'html_url': response['html_url'],
                        'location': response['location'],
                        'email': response['email'],
                        'twitter': response['twitter_username'],
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

                    return (
                        render_template('mystats.html', user_datas=user_datas)
                    )
                else:
                    flash('User doesn\'t exist!')
                    flash('Try another username!')

    return render_template('layout.html')


@app.route(
        '/profile/<username>', strict_slashes=False, methods=['GET', 'POST']
)
def profile(username):
    """Render user profile"""
    all_users_datas = storage.load_data()

    if request.method == 'POST':
        if request.form['btn'] == 'Profile':
            for data in all_users_datas:
                if data['login'].lower() == username.lower():
                    matched = data
            return render_template('profile.html', user_datas=matched)
        elif request.form['btn'] == 'Back':
            return render_template(
                'developers.html',
                filter_options=filter_options,
                all_users_datas=all_users_datas,
                total=storage.count_data()
            )
    else:
        for data in all_users_datas:
            if data['login'].lower() == username.lower():
                matched = data
        return render_template('profile.html', user_datas=matched)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, threaded=True)
