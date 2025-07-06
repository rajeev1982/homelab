#!/bin/bash

root_folder=.

# rm -rf 		                ${root_folder}
# mkdir -p                    ${root_folder}

mkdir 				        ${root_folder}/apps ${root_folder}/config ${root_folder}/data ${root_folder}/html
chown -R www-data:www-data	${root_folder}/apps ${root_folder}/config ${root_folder}/data ${root_folder}/html
chmod -R 0770			    ${root_folder}/apps ${root_folder}/config ${root_folder}/data ${root_folder}/html

mkdir 				        ${root_folder}/mariadb ${root_folder}/redis
chown -R www-data:www-data	${root_folder}/mariadb ${root_folder}/redis
chmod -R 0777			    ${root_folder}/mariadb ${root_folder}/redis