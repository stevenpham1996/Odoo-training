#!/bin/bash
set -e
set -o pipefail
LANG=en_US.UTF-8
TARGETARCH=${1:-$(dpkg --print-architecture)}

# Install some deps, lessc and less-plugin-clean-css, and wkhtmltopdf
sudo apt-get update
sudo apt-get upgrade
sudo apt install -f
sudo dpkg --configure -a

sudo apt install wkhtmltopdf


# sudo DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends ca-certificates curl dirmngr fonts-noto-cjk gnupg libssl-dev node-less npm python3-magic python3-num2words python3-odf python3-pdfminer python3-pip python3-phonenumbers python3-pyldap python3-qrcode python3-renderpm python3-setuptools python3-slugify python3-vobject python3-watchdog python3-xlrd python3-xlwt xz-utils
# WKHTMLTOPDF_ARCH=${TARGETARCH}
# case ${TARGETARCH} in
# "amd64") WKHTMLTOPDF_ARCH=amd64 && WKHTMLTOPDF_SHA=967390a759707337b46d1c02452e2bb6b2dc6d59  ;;
# "arm64")  WKHTMLTOPDF_SHA=90f6e69896d51ef77339d3f3a20f8582bdf496cc  ;;
# "ppc64le" | "ppc64el") WKHTMLTOPDF_ARCH=ppc64el && WKHTMLTOPDF_SHA=5312d7d34a25b321282929df82e3574319aed25c  ;;
# esac

# wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6.1-2/wkhtmltox_0.12.6.1-2.bullseye_amd64.deb
# echo ${WKHTMLTOPDF_SHA} wkhtmltox_0.12.6.1-2.bullseye_amd64.deb 
# sudo apt install -y --no-install-recommends ./wkhtmltox_0.12.6.1-2.bullseye_amd64.deb
# sudo rm -rf /var/lib/apt/lists/* wkhtmltox_0.12.6.1-2.bullseye_amd64.deb

sudo DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends ca-certificates curl dirmngr fonts-noto-cjk gnupg libssl-dev node-less npm python3-magic python3-num2words python3-odf python3-pdfminer python3-pip python3-phonenumbers python3-pyldap python3-qrcode python3-renderpm python3-setuptools python3-slugify python3-vobject python3-watchdog python3-xlrd python3-xlwt xz-utils
WKHTMLTOPDF_ARCH=${TARGETARCH}
case ${TARGETARCH} in
"amd64") WKHTMLTOPDF_ARCH=amd64 && WKHTMLTOPDF_SHA=967390a759707337b46d1c02452e2bb6b2dc6d59  ;;
"arm64")  WKHTMLTOPDF_SHA=90f6e69896d51ef77339d3f3a20f8582bdf496cc  ;;
"ppc64le" | "ppc64el") WKHTMLTOPDF_ARCH=ppc64el && WKHTMLTOPDF_SHA=5312d7d34a25b321282929df82e3574319aed25c  ;;
esac

sudo curl -o wkhtmltox.deb -sSL https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6.1-3/wkhtmltox_0.12.6.1-3.jammy_${WKHTMLTOPDF_ARCH}.deb
echo ${WKHTMLTOPDF_SHA} wkhtmltox.deb | sha1sum -c -
sudo apt-get install -y --no-install-recommends ./wkhtmltox.deb
sudo rm -rf /var/lib/apt/lists/* wkhtmltox.deb

# install latest postgresql-client
sudo apt update
sudo apt install postgresql postgresql-contrib


# install pip & python dependencies
sudo apt-get install build-essential
sudo apt-get install libsasl2-dev python3.11-dev libldap2-dev libssl-dev libpq-dev libffi-dev
python -m pip install --upgrade setuptools
python -m pip install -r odoo/requirements.txt
# python debugger
python -m pip install ipdb

# start and set up postgresql database
sudo service postgresql start
sudo su - postgres -c "createuser --createdb --username postgres --no-createrole --no-superuser --pwprompt odoo17"
