#
# $Id: Makefile,v 3d0f4ea94c86 2010/06/09 10:49:38 vsevolod $
#

all: build

arch:
	cp -f PKGBUILD PKGBUILD.local
	sed -i -e 's/_hgroot=.*/_hgroot=../' PKGBUILD.local
	makepkg -p PKGBUILD.local

build:
	python setup.py sdist

pypi:
	python setup.py register

pypiup:
	# can`t work via proxy ?
	python setup.py sdist upload

test:
	nosetests

clean:
	rm -rf build dist *.egg-info *.pyc *.tar.?z *.orig *~ pkg src PKGBUILD.local
