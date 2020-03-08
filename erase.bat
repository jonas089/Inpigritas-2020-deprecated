cd keys
del /f account.pem
del /f private_key.pem
del /f public_key.pem
cd ..
cd src
del /f blockchain.dat
cd ..
ECHO done

@PAUSE
