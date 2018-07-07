STARDICT_TOOLS_DIR=~/stardict/tools/src/
STARDICT_SANSKRIT_BIN=~/stardict-sanskrit/bin

# Let the URL not end with /.
URL=https://github.com/sanskrit-coders/stardict-malayalam/raw/master/ml-head/$(shell pwd|sed -e s/.*[/]//)/tars

# make all DICTS=xyz
DICTS=.*

.PHONY: all stardict tars

all:final_babylon stardict tars

final_babylon:
	bash $(STARDICT_SANSKRIT_BIN)/babylon_add_optitrans.sh DICTS=$(DICTS)

stardict:
	bash $(STARDICT_SANSKRIT_BIN)/tsv_to_stardict.sh DICTS=$(DICTS)

tars:
	bash $(STARDICT_SANSKRIT_BIN)/make_tarballs.sh $(URL) DICTS=$(DICTS)

mkfile_path := $(abspath $(lastword $(MAKEFILE_LIST)))
current_dir := $(dir $(mkfile_path))
# Let the URL not end with /.
tarlist:
	bash $(STARDICT_SANSKRIT_BIN)/update_tars_md.sh $(current_dir)tars $(URL)
