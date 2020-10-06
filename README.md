# xmltvexportanalyzer
Simple python script, which analyzes xmltvexport if there is channels with too much empty time without program

# usage
xmltvexportanalyzer.py -i <inputFile> -c <channelId> -s <max separation seconds> -l <lang defaults to fi> -h

# example
```bash
>>> python xmltvexportanalyzer.py -i xmltvexport.xml -s 5 -c 17
---    arguments    ---
inputFile: xmltvexport.xml
channelId: 17
separation: 5
lang:
--- start analyzing ---
channelId: 17 | separation: 0:00:10 | Program: Puoli seitsemän ( 2020-10-12 06:30:00 - 2020-10-12 07:00:00 ) | Next program: Kyläsairaala (12) ( 2020-10-12 07:00:10 - 2020-10-12 07:49:00 )
```
