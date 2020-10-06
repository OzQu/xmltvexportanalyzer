# xmltvexportanalyzer
Simple python script, which analyzes xmltvexport if there is channels with too much empty time without program

# usage
xmltvexportanalyzer.py -i <inputFile> -c <channelId> -s <max separation seconds>

# example
```bash
>>> python xmltvexportanalyzer.py -i xmltvexport.xml -s 5 -c 17 -l fi
---    arguments    ---
inputFile: xmltvexport.xml
channelId: 17
separation: 5
--- start analyzing ---
channelId: 17 | separation: 0:00:10 | Program: Halv sju ( 2020-10-12 06:30:00 - 2020-10-12 07:00:00 ) | Next program: The Royal (12) ( 2020-10-12 07:00:10 - 2020-10-12 07:49:00 )
```
