PYTHON=python

.PHONY : buildout clean distclean release 

buildout: .installed.cfg

.installed.cfg: bin buildout.cfg
		bin/buildout

bin:
		$(PYTHON) bootstrap.py --distribute

clean:
		rm -rf _trial_temp build dist *.egg-info
		find . \( -name "*.pyc" -o -name "*.pyo" \) -exec rm -f {} \;

distclean: clean
		rm -rf bin eggs develop-eggs .installed.cfg parts

release: clean buildout
		[ "" == "`hg status`" ] || ( echo "Working copy must be clean in order to perform a release." ; exit 1 )
		bin/testunits 
		bin/integrationtests
		bin/buildout install releaser
		bin/fullrelease
