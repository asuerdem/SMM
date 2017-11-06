cd ~/Documents/newscrawler
year=$(date +'%H')
year=$(( year - 2 ))
if [[ $year -lt 10 ]]; then
	year=200$year
else
	year=20$year
fi
echo "today's menu is $year \n"

scrapy crawl hurriyetcolumn -a yearmonth="$year-01" -o dataout/hurriyetcolumn$year-01.json -t json
python sleeper.py
scrapy crawl hurriyetcolumn -a yearmonth="$year-02" -o dataout/hurriyetcolumn$year-02.json -t json
python sleeper.py
scrapy crawl hurriyetcolumn -a yearmonth="$year-03" -o dataout/hurriyetcolumn$year-03.json -t json
python sleeper.py
scrapy crawl hurriyetcolumn -a yearmonth="$year-04" -o dataout/hurriyetcolumn$year-04.json -t json
python sleeper.py
scrapy crawl hurriyetcolumn -a yearmonth="$year-05" -o dataout/hurriyetcolumn$year-05.json -t json
python sleeper.py
scrapy crawl hurriyetcolumn -a yearmonth="$year-06" -o dataout/hurriyetcolumn$year-06.json -t json
python sleeper.py
scrapy crawl hurriyetcolumn -a yearmonth="$year-07" -o dataout/hurriyetcolumn$year-07.json -t json
python sleeper.py
scrapy crawl hurriyetcolumn -a yearmonth="$year-08" -o dataout/hurriyetcolumn$year-08.json -t json
python sleeper.py
scrapy crawl hurriyetcolumn -a yearmonth="$year-09" -o dataout/hurriyetcolumn$year-09.json -t json
python sleeper.py
scrapy crawl hurriyetcolumn -a yearmonth="$year-10" -o dataout/hurriyetcolumn$year-10.json -t json
python sleeper.py
scrapy crawl hurriyetcolumn -a yearmonth="$year-11" -o dataout/hurriyetcolumn$year-11.json -t json
python sleeper.py
scrapy crawl hurriyetcolumn -a yearmonth="$year-12" -o dataout/hurriyetcolumn$year-12.json -t json


echo "hurriyet $year is finished \n"
