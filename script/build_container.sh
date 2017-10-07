#!/usr/bin/env bash
set -ex

apt-get update
apt-get install -y software-properties-common python-software-properties python3-pip
add-apt-repository -y ppa:deadsnakes/ppa
apt-get update && apt-get install -y python3.6 python3.6-dev

export DEBIAN_FRONTEND=noninteractive
apt-get install -y mysql-server-5.7 libmysqlclient-dev
mkdir -p /var/lib/mysql
mkdir -p /var/run/mysqld
mkdir -p /var/log/mysql

sed -i -e "$ a [client]\n\n[mysql]\n\n[mysqld]"  /etc/mysql/my.cnf
sed -i -e "s/\(\[client\]\)/\1\ndefault-character-set = utf8/g" /etc/mysql/my.cnf
sed -i -e "s/\(\[mysql\]\)/\1\ndefault-character-set = utf8/g" /etc/mysql/my.cnf
sed -i -e "s/\(\[mysqld\]\)/\1\ninit_connect='SET NAMES utf8'\ncharacter-set-server = utf8\ncollation-server=utf8_unicode_ci\nbind-address = 0.0.0.0/g" /etc/mysql/my.cnf

apt-get clean

update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.5 1
update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.6 2
ln -sf /usr/bin/python3 /usr/bin/python && ln -s /usr/bin/pip3 /usr/bin/pip
pip install --upgrade pip
