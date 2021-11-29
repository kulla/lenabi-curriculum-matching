# sachsen

all: output/sachsen-mathematik.json

input/sachsen-mathematik.html: input
	curl "https://www.schulportal.sachsen.de/lplandb/index.php?lplanid=461&lplansc=SPos4aG4oIhjKYDcHVW8&token=57f7bc93ad1833666ec0edf6d147da11#page461_24860" > $@

output/sachsen-%.json: input/sachsen-%.html output
	python3 scraping/sachsen.py < $< > $@

input:
	mkdir $@

output:
	mkdir $@

# bayern

.SECONDEXPANSION:
.PRECIOUS: %.html

H := \#
PREQ = $(shell a=$@; echo $${a%%/*})
NEXT = $(shell a=$@; echo $${a$H*/})

ifndef bundesland
export ROOTDIR := $(CURDIR)
%.html:
	[ -d $(PREQ) ] || mkdir $(PREQ)
	$(MAKE) -C $(PREQ) -f $(ROOTDIR)/Makefile $(NEXT) bundesland=$(PREQ)
else
ifndef fach
%.html:
	[ -d $(PREQ) ] || mkdir $(PREQ)
	$(MAKE) -C $(PREQ) -f $(ROOTDIR)/Makefile $(NEXT) fach=$(PREQ)
else
%.html:
	case "$$bundesland" in \
		bayern) curl -L "https://www.lehrplanplus.bayern.de/fachlehrplan/gymnasium/$*/$(fach)" > $@;; \
		esac
endif
endif

%.json: $$(subst -,/,$$*).html
	python3 scraping/bayern.py $< >$@
