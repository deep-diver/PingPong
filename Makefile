test:
	pytest

publish:
	python setup.py bdist_wheel
	twine upload dist/*
	rm -rf dist

clean:
	rm -rf dist