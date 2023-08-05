Stirimango is an anagram for "migrations"

Database migrations solve the painful process of dealing with updates to the
schema of a database.  The concept is not new, as the authors originally were
introduced the concept working with Ruby on Rails.  Stirimango is a Python
implementation of migrations.  Stirimango is unlike newer versions of Rails in
that it does not provide an ORM layer -- it deals only in raw SQL.

More specifically, Stirimango uses the :mod:`psycopg2` module to manipulate the
PostgreSQL RDBMS.  With little modification, Stirimango could be used with other
database systems; however, the author only uses PostgreSQL.
