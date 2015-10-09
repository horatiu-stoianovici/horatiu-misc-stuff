In order to activate this periodical job:
1. sudo crontab -e
2. Add the line:
* * * * * sh _path-to-this-directory_/script.sh > _path-to-this-directory_/logs/cronlog 2>&1
3. Save the file opened with the crontab command and edit script.sh to cd in the current directory