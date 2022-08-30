#!/usr/bin/env sh
isort *.py cogs/*.py || echo "Error running isort, make sure you have it installed."
black *.py cogs/*.py || echo "Error running black, make sure you have it installed."
