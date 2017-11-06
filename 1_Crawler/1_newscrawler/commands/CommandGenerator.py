from __future__ import division
from random import shuffle

# Command generator generates commands to be written into terminal. Its example usage is:

# cg = HurriyetGenerator()
# cg.execute("hurriyet",2005,2005,1)
# cg.execute("hurriyet",2006,2006,1)
# cg.execute("hurriyet",2007,2007,1)
# cg.execute("hurriyet",2008,2008,1)
# cg.execute("hurriyet",2009,2009,1)
# cg.execute("hurriyet",2010,2010,1)

# cg = WiredGenerator()
# cg.execute("wired",1,20000,3)
#
# cg = CumhuriyetGenerator()
# cg.execute("cumhuriyet",1,20000,200)
#
# cg = YenisafakGenerator()
# cg.execute("yenisafak",1,20000,200)

class CommandGenerator:
    source = ""
    sample = "scrapy crawl " + source + " -a yearmonth=%s -o dataout/" + source + "%s.json -t json"

    def writer(self,source,begin,end,dat):
        fh = open("commands_" + source + str(begin) + "to" + str(end) + ".txt","w")
        fh.write("cd .\Documents\\newscrawler\n")
        for s in dat:
            out = self.sample % s +'\n'
            fh.write(out)
            # fh.write("python sleeper.py\n")

        fh.close()
    def execute(self,source,begin,end,freq):
        d = self.generate(source,begin,end,freq)
        self.writer(source,begin,end,d)




class HurriyetGenerator(CommandGenerator):
    source = "hurriyet"
    sample = "scrapy crawl " + source + " -a yearmonth=%s -o dataout/" + source + "%s.json -t json"

    def generate(self,source,begin,end,freq):
        months = [str(m/10).replace(".","") for m in range(1,13)]
        years  = range(begin,end + 1)
        strs   = [[str(y) + "-" + m for m in months] for y in years]
        strs   = sum(strs,[])
        strs   = [('"' + s + '"', s.replace("-","_")) for s in strs]
        return strs

class WiredGenerator(CommandGenerator):
    source = "wired"
    sample = "scrapy crawl " + source + " -a begin=%s -a end=%s -o dataout/" + source + "%s.json -t json"

    def generate(self,source,begin,end,freq):
        months = [str(m/10).replace(".","") for m in range(1,13,3)]
        months2= [str((((m+(freq-1)) + 1 % 12) - 1)/10).replace(".","") for m in range(1,13,freq)]
        years  = range(begin,end + 1)
        strs   = [[str(y) + "-" + m for y in years] for m in months]
        strs   = sum(strs,[])
        strs_t = [[str(y) + "-" + m for y in years] for m in months2]
        strs_t   = sum(strs_t,[])
        strs   = [('"' + strs[i] + '"', '"' + strs_t[i] + '"', strs[i].replace(".","")) for i in range(len(strs))]
        return strs


class CumhuriyetGenerator(CommandGenerator):
    source = "cumhuriyet"
    sample = "scrapy crawl " + source + " -a begin=%s -a end=%s -o dataout/" + source + "%s.json -t json"

    def generate(self,source,begin,end,freq):
        index  = [str(m) for m in range(begin,end,freq)]
        index2 = [str(m+(freq-1)) for m in range(begin,end,freq)]
        order = range(len(index))
        shuffle(order)
        strs   = [('"' + index[i] + '"', '"' + index2[i] + '"', index[i]) for i in order]
        return strs

class YenisafakGenerator(CommandGenerator):
    source = "yenisafak"
    sample = "scrapy crawl " + source + " -a begin=%s -a end=%s -o dataout/" + source + "%s.json -t json"

    def generate(self,source,begin,end,freq):
        index  = [str(m) for m in range(begin,end,freq)]
        index2 = [str(m+(freq-1)) for m in range(begin,end,freq)]
        order = range(len(index))
        shuffle(order)
        strs   = [('"' + index[i] + '"', '"' + index2[i] + '"', index[i]) for i in order]
        return strs


cg = HurriyetGenerator()
cg.execute("hurriyet",2005,2005,1)
cg.execute("hurriyet",2006,2006,1)
cg.execute("hurriyet",2007,2007,1)
cg.execute("hurriyet",2008,2008,1)
cg.execute("hurriyet",2009,2009,1)
cg.execute("hurriyet",2010,2010,1)

# cg = WiredGenerator()
# cg.execute("wired",1,20000,3)
#
# cg = CumhuriyetGenerator()
# cg.execute("cumhuriyet",1,20000,200)
#
# cg = YenisafakGenerator()
# cg.execute("yenisafak",1,20000,200)
