from flask import render_template, redirect, url_for, g
from . import main_bp
from .forms import AddForm
from .. import mongo
from ..gitdoc import gitdoc
from ..auth import is_logged_in, login_required
from urllib.parse import urlsplit


@main_bp.before_request
def before_request():
    g.is_authenticated = False
    if is_logged_in():
        g.is_authenticated = True


@main_bp.route('/')
@main_bp.route('/index')
@login_required
def index():
    filter = {"name": {"$regex": r"^(?!system\.)"}}
    doc_list = mongo.db.list_collection_names(filter=filter, nameOnly=True)
    return render_template(
        'index.html',
        documents=doc_list
    )


@main_bp.route('/get_document/<path:document_name>')
@login_required
def get_document(document_name):
    if document_name in mongo.db.list_collection_names(nameOnly=True):
        documents = mongo.db[document_name].find()
        return render_template('_article.html', documents=documents)
    reponame = '/'.join(document_name.split('/')[:2])
    documents = mongo.db[reponame].find()
    document = mongo.db[reponame].find_one({'full_name': document_name})
    return render_template(
        '_article.html',
        documents=documents,
        document=document
    )


@main_bp.route('/register_project', methods=['GET', 'POST'])
@login_required
def register_project():
    form = AddForm()
    if form.validate_on_submit():
        git_files = []
        repo_name = urlsplit(form.project.data).path.strip('/')
        git_files = gitdoc.get_files(repo_name)
        md_files = gitdoc.md_files(git_files)
        gitdoc.save_documents(repo_name=repo_name, git_files=md_files)
        return redirect(url_for('main_bp.index'))
    return render_template('register_project.html', form=form)


# @main_bp.route('/register_project_modal', methods=['GET', 'POST'])
# @login_required
# def register_project_modal():
#     form = AddForm()
#     if form.validate_on_submit():
#         git_files = []
#         git_files = gitdoc.get_files(form.project.data)
#         md_files = gitdoc.md_files(git_files)
#         for md_file in md_files:
#             text = md_file.decoded_content.decode("utf-8")
#             project = Document(
#                 repo=form.project.data,
#                 name=md_file.name,
#                 file_path=md_file.path,
#                 full_name='/'.join([form.project.data, md_file.path]),
#                 body_raw=text,
#                 body_html=markdown(text, extensions=[
#                     'fenced_code', 'tables', 'nl2br', 'sane_lists'
#                 ]),
#                 last_modified=md_file.last_modified
#             )
#             db.session.add(project)
#             db.session.commit()
#         return redirect(url_for('main_bp.index'))
#     return render_template('register_project_modal.html', form=form)


@main_bp.route('/update_documents')
@login_required
def update_documents():
    gitdoc.check_update()
    return redirect(url_for('main_bp.index'))
