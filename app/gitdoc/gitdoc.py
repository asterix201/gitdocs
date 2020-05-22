from github import Github
from flask import current_app
from markdown import markdown
import pathlib
from datetime import datetime
from .. import mongo
from ..import scheduler

GIT_TIME_FORMAT = '%a, %d %b %Y %H:%M:%S %Z'


def get_files(git_repo):
    """Get all of the contents of the repository recursively"""
    github_token = current_app.config['GITHUB_TOKEN']
    github = Github(github_token)
    repo = github.get_repo(git_repo)
    contents = repo.get_contents("")
    file_list = []
    while contents:
        file_content = contents.pop()
        if file_content.type == "dir":
            contents.extend(repo.get_contents(file_content.path))
        else:
            file_list.append(file_content)
    return file_list


# filter_md_files = list(filter(
#     lambda git_file: pathlib.Path(git_file.name).suffix == ".md",
#     get_files("asterix201/test-web")
# ))


def md_files(file_list):
    """Get list of markdown files from the repository file list"""
    md_files = []
    while file_list:
        git_file = file_list.pop()
        if pathlib.Path(git_file.name).suffix == ".md":
            md_files.append(git_file)
    return md_files


def save_documents(repo_name, git_files):
    project_collection = mongo.db[repo_name]
    for each_file in git_files:
        text = each_file.decoded_content.decode("utf-8")
        document = {
                'repo': each_file.repository.full_name,
                'name': each_file.name,
                'file_path': each_file.path,
                'full_name': '/'.join(
                    [each_file.repository.full_name, each_file.path]
                ),
                'body_raw': text,
                'body_html': markdown(text, extensions=[
                    'fenced_code', 'tables', 'nl2br', 'sane_lists'
                ]),
                'last_modified': each_file.last_modified,
                'last_modified_utc': datetime.strptime(
                        each_file.last_modified, GIT_TIME_FORMAT
                    ),
                'last_sync': datetime.utcnow()
            }
        if project_collection.find_one({'file_path': each_file.path}):
            project_collection.replace_one(
                {'file_path': each_file.path}, document
            )
            continue
        project_collection.insert(document)


def update_document(git_file):
    collection = git_file.repository.full_name
    text = git_file.decoded_content.decode("utf-8")
    document = {
            'repo': git_file.repository.full_name,
            'name': git_file.name,
            'file_path': git_file.path,
            'full_name': '/'.join(
                [git_file.repository.full_name, git_file.path]
            ),
            'body_raw': text,
            'body_html': markdown(text, extensions=[
                'fenced_code', 'tables', 'nl2br', 'sane_lists'
            ]),
            'last_modified': git_file.last_modified,
            'last_modified_utc': datetime.strptime(
                    git_file.last_modified, GIT_TIME_FORMAT
                ),
            'last_sync': datetime.utcnow()
        }
    find_doc = mongo.db[collection].find_one({'file_path': git_file.path})
    if not find_doc:
        mongo.db[collection].insert_one(document)
        return print(f'document {document.get("full_name")} added')
    if datetime.strptime(
        find_doc.get('last_modified'), GIT_TIME_FORMAT
    ) < datetime.strptime(
        git_file.last_modified, GIT_TIME_FORMAT
    ):
        mongo.db[collection].find_one_and_replace(
                {'file_path': git_file.path}, document
            )
        return print(f'document {document.get("full_name")} updated')


@scheduler.task('interval', id='check_update', minutes=5, misfire_grace_time=900)
def check_update():
    with scheduler.app.app_context():
        filter = {"name": {"$regex": r"^(?!system\.)"}}
        docs_list = mongo.db.list_collection_names(filter=filter, nameOnly=True)
        for document in docs_list:
            git_files = get_files(document)
            git_docs = md_files(git_files)
            for git_doc in git_docs:
                update_document(git_doc)
