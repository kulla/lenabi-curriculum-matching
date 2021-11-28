
all: output/sachsen-mathematik.json

input/sachsen-mathematik.html:
	curl "https://www.schulportal.sachsen.de/lplandb/index.php?lplanid=461&lplansc=SPos4aG4oIhjKYDcHVW8&token=57f7bc93ad1833666ec0edf6d147da11#page461_24860" > $@

output/sachsen-%.json: input/sachsen-%.html
	python3 scraping/sachsen.py < $< > $@
