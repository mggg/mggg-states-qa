install:
	pip3 install --upgrade pip && \
	python3 setup.py bdist_wheel && \
	pip3 install dist/*.whl

clean:
	rm -rf build dist *.egg*
