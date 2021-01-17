###########
About LoAFi
###########
LoAFi stands for Log Analysis Filter and intends to support interactive
analysis of log files (or any text files). The tool supports identification of
interesting patterns to radically filter all non-matching lines with the idea
to quickly understand the structure of the relevant information.

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

To run the tests, call `make test`.

To build the documentation, invoke `make html`.