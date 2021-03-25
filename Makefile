all: runget

runget_lin: coinbase_get.py
	python3 coinbase_get.py&

runget_win: coinbase_get.py
	python coinbase_get.py&
