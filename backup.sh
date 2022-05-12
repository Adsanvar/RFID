# Boilerplate for crontabe backups
# Note: add a .my.config with [mysqldump] user and pass
# Author Adrian Sandoval
ts=$(date +"%m_%d_%Y")
mysqldump -u root dbname > destination/db_dump_"${ts}".sql