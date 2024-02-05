import requests


def get_user_languages(username, token):
    """Gets programming languages and sorts them"""
    url = 'https://api.github.com/users/{}/repos'
    headers = {'Authorization': f'token {token}'}

    response = requests.get(url.format(username), headers=headers)

    if response.status_code == 200:
        repositories = response.json()
        languages = {}

        for repo in repositories:
            language = repo.get("language")
            if language:
                languages[language] = languages.get(language, 0) + 1

        # Trier les langages par nombre d'occurrences (en ordre décroissant)
        sorted_languages = dict(sorted(languages.items(),
                                key=lambda x: x[1], reverse=True))

        # Sélectionner les trois langages les plus utilisés
        top_languages = dict(list(sorted_languages.items())[:3])

        return top_languages

    else:
        print(f"Error: {response.status_code}")
        return None


def get_user_coding_activity(username, token):

    events_list = ["PushEvent", "PullRequestEvent", "CreateEvent"]
    url = f"https://api.github.com/users/{username}/events"
    headers = {'Authorization': f'token {token}'}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        events = response.json()
        activity_count = 0

        for event in events:
            # Check for events related to code (PushEvent,
            # PullRequestEvent, etc.)
            if event.get("type") in events_list:
                activity_count += 1

        return activity_count

    else:
        print(f"Error: {response.status_code}")
        return None


def get_repos_without_issues(username, token):
    # GitHub API endpoint to get user's repositories
    repositories_url = f'https://api.github.com/users/{username}/repos'
    headers = {'Authorization': f'token {token}'}

    try:
        # Make a request to get the user's repositories
        response = requests.get(repositories_url, headers=headers)

        if response.status_code == 200:
            repositories = response.json()

            # Count repositories without issues
            no_issues_repos = sum(
                1 for repo in repositories
                if not repo.get('has_issues')
            )

            return no_issues_repos

        else:
            print(f"Error: {response.status_code}")
            return None

    except Exception as e:
        print(f"Error: {e}")
        return None


def get_repos_without_readme(username, token):
    # GitHub API endpoint to get user's repositories
    repositories_url = f'https://api.github.com/users/{username}/repos'
    headers = {'Authorization': f'token {token}'}

    try:
        # Make a request to get the user's repositories
        response = requests.get(repositories_url, headers=headers)

        if response.status_code == 200:
            repositories = response.json()

            # Count repositories without README.md
            repositories_without_readme = sum(
                1 for repo in repositories
                if not has_readme(username, repo['name'], token)
            )

            return repositories_without_readme

        else:
            print(f"Error: {response.status_code}")
            return None

    except Exception as e:
        print(f"Error: {e}")
        return None


def has_readme(username, repo, token):
    # GitHub API endpoint to get repository contents
    url = f'https://api.github.com/repos/{username}/{repo}/contents'
    headers = {'Authorization': f'token {token}'}

    # Make a request to get the repository contents
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        repository_contents = response.json()
        return (
            any(
                file['name'].lower() == 'readme.md'
                for file in repository_contents
            )
        )

    else:
        print(f"Error: {response.status_code}")
        return False  # Assume no README.md if there's an error


def get_team_projects_count(username, token):
    # GitHub API endpoint to get user's repositories
    repositories_url = f'https://api.github.com/users/{username}/repos'
    headers = {'Authorization': f'token {token}'}

    try:
        # Make a request to get the user's repositories
        response = requests.get(repositories_url, headers=headers)

        if response.status_code == 200:
            repositories = response.json()

            # Count repositories that can be considered as team projects
            team_projects_count = sum(
                1 for repo in repositories
                if is_team_project(repo)
            )

            return team_projects_count

        else:
            print(f"Error: {response.status_code}")
            return None

    except Exception as e:
        print(f"Error: {e}")
        return None


def is_team_project(repository):
    # Check if the repository has certain characteristics
    # indicating it's a team project
    return (
        repository.get('archived', False) is False
        and repository.get('fork', False) is False
    )
