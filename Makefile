all: runget

runget_lin: coinbase_get.py
	python3 coinbase_get.py 0 & >& ./linux_log.txt 

runget_win: coinbase_get.py
	python coinbase_get.py 1 >> ./win_log.txt &
