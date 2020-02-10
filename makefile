# Find out the operating system
UNAME := $(shell uname)

all: py_scripts preprocessor toros.conf.yaml

ifeq ($(UNAME), Linux)
preprocessor: preprocessord.service
uninstall: uninstall_linux
services=preprocessord.service
service_dir=/etc/systemd/system
endif
ifeq ($(UNAME), Darwin)
preprocessor: org.toros.preprocessor.plist
uninstall: uninstall_osx
services=org.toros.preprocessor.plist
service_dir=/Library/LaunchAgents
endif
conf_dir=/etc/toros

.PHONY: all preprocessor py_scripts install uninstall clean

py_scripts: $(wildcard *.py)
	pip install .

%d.service: templates/%d.service.template torosmanager/%.py
# sed is needed to replace the absolute path of the scheduler script in the .service file
	sed 's,scriptname,$(shell which $(*)),' $< > $@

org.toros.%.plist: templates/org.toros.%.plist.template
# sed is needed to replace the absolute path of the scheduler script in the .service file
	sed 's,scriptname,$(shell which $(*)),' $< > $@

$(conf_dir):
	mkdir -p $@

toros.conf.yaml:
	cp templates/toros.conf.yaml.template $@

install: $(service_dir) $(conf_dir) preprocessor toros.conf.yaml
	cp $(services) $(service_dir)
	cp toros.conf.yaml $(conf_dir)/toros.conf.yaml

uninstall_linux:
	-systemctl stop preprocessord
	-pip uninstall -y torosmanager
	-rm $(service_dir)/preprocessord.service
	rm -r $(conf_dir)

uninstall_osx:
	-launchctl unload $(service_dir)/org.toros.*.plist
	-pip uninstall -y torosmanager
	-rm $(service_dir)/org.toros.*.plist
	rm -r $(conf_dir)

clean:
	-rm *.service
	-rm *.plist
	-rm toros.conf.yaml
