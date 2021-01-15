###############
Developer guide
###############

Maintenance of the virtual environment:
- creation: `virtualenv --python python3 venv`
- activation: `source venv/bin/activate`
- installation of dependencies: `pip install -r requirements.txt`
- installation of an experimental dependency: `pip install <dependency>`
- update of the dependency list: `pip freeze > requirements.txt`
- deactivation: `deactivate`