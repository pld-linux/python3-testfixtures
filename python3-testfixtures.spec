#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests
%bcond_without	django	# django tests

Summary:	Collection of helpers and mock objects for unit tests and doc tests
Summary(pl.UTF-8):	Zbiór funkcji pomocniczych i obiektów atrap do testów jednostkowych i dokumentacji
Name:		python3-testfixtures
Version:	10.0.0
Release:	1
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/testfixtures/
Source0:	https://files.pythonhosted.org/packages/source/t/testfixtures/testfixtures-%{version}.tar.gz
# Source0-md5:	47d7c2f5026e0b7212d152cb487e6f40
URL:		https://pypi.org/project/testfixtures/
BuildRequires:	python3-modules >= 1:3.11
BuildRequires:	python3-setuptools
BuildRequires:	python3-setuptools_git
%if %{with tests}
%{?with_django:BuildRequires:	python3-django}
BuildRequires:	python3-pytest >= 7.1
BuildRequires:	python3-pytest-cov
%{?with_django:BuildRequires:	python3-pytest-django}
BuildRequires:	python3-sybil >= 6
BuildRequires:	python3-twisted
BuildRequires:	python3-zope.component
BuildRequires:	python3-zope.interface
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	python3-furo
BuildRequires:	sphinx-pdg-3
%endif
Requires:	python3-modules >= 1:3.11
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
testfixtures is a collection of helpers and mock objects that are
useful when writing automated tests in Python.

%description -l pl.UTF-8
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
%py3_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS=%{?with_django:pytest_django.plugin} \
%{__python3} -m pytest testfixtures/tests %{!?with_django:--ignore testfixtures/tests/test_django}
%endif

%if %{with doc}
PYTHONPATH=$(pwd) \
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGELOG.rst LICENSE.txt README.rst
%{py3_sitescriptdir}/testfixtures
%{py3_sitescriptdir}/testfixtures-%{version}-py*.egg-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_static,*.html,*.js}
%endif
