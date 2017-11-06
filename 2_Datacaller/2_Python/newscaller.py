import pandas as pd
import re
from sqlalchemy import create_engine

archive_path = "C:/Users/fuadcan/Documents/newscrawler/"
engine = create_engine('sqlite:///' + archive_path + 'archive.db')

query = """SELECT source,date_time,category,link,content FROM News
WHERE (date_time BETWEEN 2009-01-01 AND 2009-01-31)"""

query = """SELECT source,date_time,category,link,content FROM News
LIMIT 5 AND content LIKE '%etti%'"""

dat = pd.read_sql_query(query,engine)
