.PHONY: clean dist

clean:
	find . -name '*.pyc' -type f -delete
	find . -name '__pycache__' -type d -delete

dist: clean
	rm -rf dist
	mkdir -p dist/rabbithole
	cp -R docs dist/rabbithole
	cp -R modules dist/rabbithole
	cp -R rh dist/rabbithole
	cp rabbithole.py dist/rabbithole
	cp rabbithole.cfg.defaults dist/rabbithole
	cp rabbithole.cfg.sample dist/rabbithole
	cp LICENSE.md dist/rabbithole
	cp README.md dist/rabbithole
	tar -czf dist/release.tar.gz -C dist rabbithole
