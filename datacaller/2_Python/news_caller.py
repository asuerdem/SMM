import pandas as pd
from sqlalchemy import create_engine

engine  = create_engine('sqlite:///hurriyet.db')

def convert_to_like(word):
    word = u"'%" + word + u"%'"
    # word = word.decode("utf-8")
    return word

def convert_tuples(w_tuple):
    if len(w_tuple) == 1:
        out = convert_to_like(w_tuple[0])
        out = [out]
    else:
        opt1 = "'%" + w_tuple[0] + " % " + w_tuple[1] + "%'"
        opt2 = "'%" + w_tuple[1] + " % " + w_tuple[0] + "%'"
        out = [opt1.decode("utf-8"),opt2.decode("utf-8")]
    #
    return out


word_list = [u"'% Barış süre%'", u"'% Çözüm süre%'", u"'% Kürt Açılımı%'", u"'% Demokratik açılım%'", u"'% Milli birlik ve kardeşlik projesi %'"]


dat_num = 10
begin = "2009-01-01"
end   = "2015-01-01"
word_list = [("Demokratik Bölgeler Partisi",), ("DBP",)]


