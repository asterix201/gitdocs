from app import create_app
# from app.models import Document


app = create_app()


# @app.shell_context_processor
# def make_shell_context():
#     return {'Document': Document}


if __name__ == '__main__':
    app.run(use_debugger=False, use_reloader=False, passthrough_errors=True)
