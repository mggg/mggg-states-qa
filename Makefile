# For easily keeping the directory clean for testing and installation

install:
	pip3 install --upgrade pip
	python3 setup.py bdist_wheel
	pip3 install dist/*.whl

tester:
	pip3 install --upgrade pip
	python3 setup.py test
	pytest

clean:
	rm -rf build dist *.egg*
