distro: register clean build upload

init:
	pip install -r requirements.txt

init-dev:
	pip install -r requirements-dev.txt

doc:
	pandoc --from=markdown --to=rst --output="README.rst" "README.md"

clean:
	rm dist/* || true
	rm -fr __pycache__ || true
	rm -fr hashfile/__pycache__ || true
	rm -fr build || true

build:
	python3 setup.py sdist
	python3 setup.py bdist_wheel

upload:
	twine upload dist/hashfile*

register:
	python setup.py register

distro: register clean build upload
