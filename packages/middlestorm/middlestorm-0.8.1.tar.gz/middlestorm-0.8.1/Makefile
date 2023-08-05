#
# $Id: Makefile,v 74e3e6109a58 2010/04/19 09:30:45 vsevolod $
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

clean:
	rm -rf build dist *.egg-info *.pyc *.tar.gz *.orig *~ pkg src PKGBUILD.local
	rm -f tests/*.pyc tests/*.orig tests/*~

