all: tsv

tsv: rdf4discourse
	cd rdf4discourse/discourse-markers/parcor/bibles/;\
	make gazetteers
	ln -s rdf4discourse/discourse-markers/parcor/bibles/gazetteers tsv

# replace by symlink if already installed
rdf4discourse:
	git clone https://github.com/acoli-repo/rdf4discourse
