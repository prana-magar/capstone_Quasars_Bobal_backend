# How to create encrypted password for data-config?
	1. create a temporary file pwd.txt with db actual password.(use echo -n 'password'> pwd.txt)
	2. run "openssl enc -aes-128-cbc -a -salt -in pwd.txt" . It will ask for encrypt/decrypt key.
	3. create a file encryptionkey and insert encrypt/decrypt key used in step 2. (use echo -n 'key'> enryptionkey)
		NOTE: use -n in echo so it doesnt enter new line. This is critical and may fail decryption process.
	4.change data-config to added new encrypted password (instead of plain password ) and 
		include encryptionkey file path in param encryptKeyFile
 	5. further info: https://lucene.apache.org/solr/guide/7_3/uploading-structured-data-store-data-with-the-data-import-handler.html#encrypting-a-database-password
