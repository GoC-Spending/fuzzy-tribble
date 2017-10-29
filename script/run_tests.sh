#!/usr/bin/env bash
set -euf -o pipefail

chown -R mysql:mysql /var/lib/mysql /var/run/mysqld /var/log/mysql
service mysql start

pytest tests -vv
