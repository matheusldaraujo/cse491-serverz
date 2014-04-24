# Shell script to automatically create imageapp.db
#!/bin.sh
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
IMG_PATH=$DIR"/imageapp.db"
test -f $IMG_PATH && rm $IMG_PATH
echo "Creating new imageapp.db database."
sqlite3 $IMG_PATH "CREATE TABLE images(id INTEGER PRIMARY KEY AUTOINCREMENT, image BLOB, thumb TEXT, user_id INTEGER, name TEXT );"
echo "Database created."