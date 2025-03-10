#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

Summary:	Collection of helpers and mock objects for unit tests and doc tests
Summary(pl.UTF-8):	Zbiór funkcji pomocniczych i obiektów atrap do testów jednostkowych i dokumentacji
Name:		python-testfixtures
# keep 6.x here for python2 support
Version:	6.18.5
Release:	2
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/testfixtures/
Source0:	https://files.pythonhosted.org/packages/source/t/testfixtures/testfixtures-%{version}.tar.gz
# Source0-md5:	e89cfe8325778a8c519a6bf63ae3fe83
URL:		https://pypi.org/project/testfixtures/
%if %{with python2}
BuildRequires:	python-modules >= 1:2.7
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-django < 2
BuildRequires:	python-mock
BuildRequires:	python-pytest >= 3.6
BuildRequires:	python-pytest-cov
BuildRequires:	python-pytest-django
BuildRequires:	python-sybil
BuildRequires:	python-twisted
BuildRequires:	python-zope.component
BuildRequires:	python-zope.interface
%endif
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.6
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-django
BuildRequires:	python3-pytest >= 3.6
BuildRequires:	python3-pytest-cov
BuildRequires:	python3-pytest-django
BuildRequires:	python3-sybil
BuildRequires:	python3-twisted
BuildRequires:	python3-zope.component
BuildRequires:	python3-zope.interface
%endif
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	sphinx-pdg
%endif
Requires:	python-modules >= 1:2.7
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
testfixtures is a collection of helpers and mock objects that are
useful when writing automated tests in Python.

%description -l pl.UTF-8
testfixtures to zbiór funkcji pomocniczych i obiektów atrap,
przydatnych przy pisaniu automatycznych testów w Pythonie.

%package -n python3-testfixtures
Summary:	Collection of helpers and mock objects for unit tests and doc tests
Summary(pl.UTF-8):	Zbiór funkcji pomocniczych i obiektów atrap do testów jednostkowych i dokumentacji
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.6

%description -n python3-testfixtures
testfixtures is a collection of helpers and mock objects that are
useful when writing automated tests in Python.

%description -n python3-testfixtures -l pl.UTF-8
testfixtures to zbiór funkcji pomocniczych i obiektów atrap,
przydatnych przy pisaniu automatycznych testów w Pythonie.

%package apidocs
Summary:	API documentation for Python testfixtures module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona testfixtures
Group:		Documentation

%description apidocs
API documentation for Python testfixtures module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona testfixtures.

%prep
%setup -q -n testfixtures-%{version}

%build
%if %{with python2}
%py_build

%if %{with tests}
# django test fails with "no such table"
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS=pytest_django.plugin \
%{__python} -m pytest testfixtures/tests -k 'not test_django'
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS=pytest_django.plugin \
%{__python3} -m pytest testfixtures/tests
%endif
%endif

%if %{with doc}
PYTHONPATH=$(pwd) \
%{__make} -C docs html
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_postclean
%endif

%if %{with python3}
%py3_install
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc CHANGELOG.rst LICENSE.txt README.rst
%{py_sitescriptdir}/testfixtures
%{py_sitescriptdir}/testfixtures-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-testfixtures
%defattr(644,root,root,755)
%doc CHANGELOG.rst LICENSE.txt README.rst
%{py3_sitescriptdir}/testfixtures
%{py3_sitescriptdir}/testfixtures-%{version}-py*.egg-info
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_static,*.html,*.js}
%endif
