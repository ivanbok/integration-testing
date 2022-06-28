# General
brew install mysql
mysql -h <endpoint> -P 3306 -u <mymasteruser> -p
CREATE DATABASE <your_database_name>;
python manage.py makemigrations
python manage.py migrate

# Example
brew install mysql
mysql -h mysql-test2.ckwl7smelju6.ap-southeast-1.rds.amazonaws.com -P 3306 -u admin -p
CREATE DATABASE djangodatabase;
python manage.py makemigrations
python manage.py migrate