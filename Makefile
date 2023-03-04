#################################################################################
# GLOBALS                                                                       #
#################################################################################

PROFILE = default
PROJECT_NAME = Mushroom_Classification

#################################################################################
# COMMANDS                                                                      #
#################################################################################

## Install Python Dependencies
environment: test_environment
  python3 -m venv .venv
	source .venv/bin/activate
	pip install -r requirements-development.txt

## TODO
