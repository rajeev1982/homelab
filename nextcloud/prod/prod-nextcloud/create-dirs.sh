#!/bin/bash

root_folder=.

# rm -rf 		                ${root_folder}
# mkdir -p                    ${root_folder}

mkdir 				        ${root_folder}/apps ${root_folder}/config ${root_folder}/html ${root_folder}/data
chown -R www-data:www-data	${root_folder}/apps ${root_folder}/config ${root_folder}/html ${root_folder}/data
chmod -R 0770			    ${root_folder}/apps ${root_folder}/config ${root_folder}/html ${root_folder}/data

mkdir 				        ${root_folder}/mariadb ${root_folder}/redis
chown -R www-data:www-data	${root_folder}/mariadb ${root_folder}/redis
chmod -R 0777			    ${root_folder}/mariadb ${root_folder}/redis