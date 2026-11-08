import pymysql
pymysql.install_as_MySQLdb()

from django.db.backends.mysql.features import DatabaseFeatures

# Forzar la desactivación de RETURNING para MariaDB 10.4
DatabaseFeatures.can_return_rows_from_insert = False
DatabaseFeatures.can_return_rows_from_bulk_insert = False
DatabaseFeatures.can_return_generated_columns = False
DatabaseFeatures.can_return_columns_from_insert = False