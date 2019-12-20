dev:
	source env/bin/activate; watchmedo shell-command ./src/ --wait --drop --recursive --command="python compile.py; osascript -e 'tell application \"Google Chrome\" to tell the active tab of its first window to reload'"
