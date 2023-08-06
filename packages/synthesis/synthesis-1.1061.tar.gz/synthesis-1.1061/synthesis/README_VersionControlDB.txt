
This process assumes that you have VirtualEnv installed.

The reason for this is to implement version control into an existing (us) or new database that is under the control of
sqlalchemy.  This will allow for schema maintenance of the database.

# easy_install
easy_install sqlalchemy-migrate

# Create the repository
migrate create Synthesis_Repository "Synthesis Project"

# Put the DB under Version Control
migrate version_control postgres://(your username):(your pass)@localhost:5432/coastaldb_test Synthesis_Repository

# which creates a table in the database called
migrate_version