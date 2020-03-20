lint:
	$(MAKE) $@ -C cli
	$(MAKE) $@ -C api

test:
	$(MAKE) $@ -C cli
	$(MAKE) $@ -C api
