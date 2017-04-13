%{?scl:%scl_package aether-connector-okhttp}
%{!?scl:%global pkg_name %{name}}
%{?java_common_find_provides_and_requires}

%global baserelease 1

%global commit 1b666247f763ed846062b09e5010a5a417cff436
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:           %{?scl_prefix}aether-connector-okhttp
Version:        0.14.0
Release:        3.%{baserelease}%{?dist}
Summary:        OkHttp Aether Connector

# src/main/java/io/tesla/aether/wagon/OkHttpsWagon.java is ASL and EPL
License:        EPL and (ASL 2.0 and EPL)
URL:            https://github.com/tesla/%{pkg_name}
Source0:        https://github.com/tesla/%{pkg_name}/archive/%{commit}/%{pkg_name}-%{version}-%{shortcommit}.tar.gz
Source1:        eclipse-1.0.txt

BuildArch:      noarch

BuildRequires: %{?scl_prefix_java_common}mvn(org.eclipse.jetty:jetty-util)
BuildRequires: %{?scl_prefix_maven}mvn(org.eclipse.sisu:org.eclipse.sisu.plexus)
BuildRequires: %{?scl_prefix_maven}mvn(org.eclipse.sisu:sisu-maven-plugin)
BuildRequires: %{?scl_prefix_maven}mvn(org.codehaus.plexus:plexus-component-annotations)
BuildRequires: %{?scl_prefix}mvn(com.google.guava:guava)
BuildRequires: %{?scl_prefix_java_common}mvn(junit:junit)
BuildRequires: %{?scl_prefix}mvn(com.squareup.okhttp:okhttp)
BuildRequires: %{?scl_prefix_java_common}mvn(javax.inject:javax.inject)
BuildRequires: %{?scl_prefix_java_common}mvn(org.slf4j:slf4j-simple)
BuildRequires: %{?scl_prefix_maven}mvn(org.apache.maven.wagon:wagon-provider-api)
BuildRequires: %{?scl_prefix_maven}maven-local

%description
A repository connector implementation based on Square's OkHttp.

%package javadoc
Summary:        Javadoc for %{pkg_name}

%description javadoc
API documentation for %{pkg_name}.

%prep
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
set -e -x
%setup -q -n %{pkg_name}-%{commit}
cp %{SOURCE1} .

find -name '*.class' -delete
find -name '*.jar' -delete

# Doesn't really need the parent
%pom_remove_parent

# Unbundle SslContextFactory
%pom_add_dep org.eclipse.jetty:jetty-util
rm -r src/main/java/io/takari/aether/okhttp/ssl/
sed -i -e "s/io.takari.aether.okhttp.ssl.SslContextFactory/org.eclipse.jetty.util.ssl.SslContextFactory/" \
    -e "s/scf.setTrustStore(trustStorePath)/scf.setTrustStorePath(trustStorePath)/" \
    src/main/java/io/takari/aether/okhttp/OkHttpAetherClient.java
%{?scl:EOF}


%build
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
set -e -x
# We don't have all test deps (e.g. npn-boot)
%mvn_build --skip-tests
%{?scl:EOF}


%install
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
set -e -x
%mvn_install
%{?scl:EOF}


%files -f .mfiles
%dir %{_javadir}/%{pkg_name}
%doc eclipse-1.0.txt
%doc license-header.txt

%files javadoc -f .mfiles-javadoc
%doc eclipse-1.0.txt

%changelog
* Thu Jan 19 2017 Mat Booth <mat.booth@redhat.com> - 0.14.0-3.1
- Auto SCL-ise package for rh-eclipse46 collection

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jun 16 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Mar 11 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.14.0-1
- Update to upstream version 0.14.0

* Fri Jul 25 2014 Mat Booth <mat.booth@redhat.com> - 0.12.0-4
- Fix failure to build with the latest version of guava

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat May 24 2014 Gerard Ryan <galileo@fedoraproject.org> - 0.12.0-2
- Update to latest upstream version 0.12.0
- RHBZ#1100949: Patch for latest aether api

* Tue Mar 04 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0.0.11-3
- Use Requires: java-headless rebuild (#1067528)

* Wed Feb 5 2014 Gerard Ryan <galileo@fedoraproject.org> - 0.0.11-2
- Initial rpm