test:
	pytest

publish:
	python setup.py bdist_wheel
	twine upload dist/*
	rm -rf dist
	rm -rf src/bingbong.egg-info
	rm -rf build
	
clean:
	rm -rf dist
	rm -rf src/bingbong.egg-info
	rm -rf build