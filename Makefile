install:
	pip3 install --upgrade pip && pip3 install -r requirements.txt

format:
	black utils/*.py
	black youtube/*.py
	black *.py
