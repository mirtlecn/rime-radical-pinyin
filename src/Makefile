.PHONY: all lint install gen 2fly 2ms 2py append fix

MAKE_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
FROM_ARG := $(word 1,$(MAKE_ARGS))
TO_ARGS := $(wordlist 2,$(words $(MAKE_ARGS)),$(MAKE_ARGS))

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

append:
	@if [ "$(words $(MAKE_ARGS))" -lt 2 ]; then echo 'Usage: make append "<字>" "<组件>"' >&2; exit 2; fi
	python3 script/replace_error.py -f '$(FROM_ARG)' -t '$(TO_ARGS)' -a

fix:
	@if [ "$(words $(MAKE_ARGS))" -lt 2 ]; then echo 'Usage: make fix "<字>" "<组件>"' >&2; exit 2; fi
	python3 script/replace_error.py -f '$(FROM_ARG)' -t '$(TO_ARGS)'

ifneq ($(filter append fix,$(firstword $(MAKECMDGOALS))),)
%:
	@:
endif
