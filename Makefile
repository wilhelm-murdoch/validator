install:
	python setup.py develop

uninstall:
	python setup.py develop --uninstall

test:
	python setup.py nosetests

clean:
	find . -name \*.pyc -exec rm {\} \; ; rm -rf build/ dist/ *.egg-info *.egg