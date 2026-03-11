.PHONY: all

all: install gen 2fly

lint:
	python3 script/lint_src.py

install:
	pip3 install -r requirements.txt -q

gen: install
	python3 script/gen_dict.py

2fly: gen
	python3 script/convert_dict.py encoding_method='flypy' output_file_path='../radical_flypy.dict.yaml'

2ms: gen
	python3 script/convert_dict.py encoding_method='mspy' output_file_path='../radical_mspy.dict.yaml'

2py: gen
	python3 script/convert_dict.py encoding_method='py' output_file_path='../radical.dict.yaml'
