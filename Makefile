
deploy:
	rsync -r . --exclude .git $(shell ~/uwplse/getdir)

.PHONY: deploy
