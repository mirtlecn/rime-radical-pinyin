.PHONY: all

all: clean schema install dict 2fly

clean:
	rm -rf gen && mkdir -p gen

schema: clean
	cp radical*.schema.yaml gen/

install:
	pip install -r requirements.txt -q

dict: clean install
	python gen.py

2fly:
	python convert.py encoding_method='flypy'

2ms:
	python convert.py encoding_method='mspy'

2py:
	python convert.py encoding_method='py'
