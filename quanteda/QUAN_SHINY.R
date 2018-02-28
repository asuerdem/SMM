library(quanteda)
library(readtext)
library(SnowballC)
library(ggplot2)
library(dplyr)
library("spacyr")

setwd("~/Documents/SMM/quanteda")

#######MAKE A CORPUS######3
#0.0 find a csv  upload template from SHINY
#0.1 read the text into quanteda, availabale formats are:
#(.txt) ; (.csv) ;XML ; JSON; data Facebook API, in JSON ;data from  Twitter API,  
#from a drop down menu, user can select the suitable format
#READ COMMAND: text_field= is where the text is: ie. title, contenet, news etc... 
#hence we need another configuration button after the formatof the corpus is selected: 
#your text is in column: ....
aidata <- readtext("AI_peopleschina.csv", text_field="content") 
#aidata <- aidata[! duplicated( aidata$head), ]
#aidata <- corpus(aidata[-7])

# following command turns the file into a corpus: 
aicorp <- corpus(aidata) #makes a corpus
aicorp <- corpus_trim(aicorp, what = c("sentences", "paragraphs", "documents"), 
                 min_ntoken =4)
#following command creates Metadata about the corpus, ie. description etc..
#a menu item such as: Description and Notes about your corpus: 
metacorpus(aicorp, "notes") <- "This is the description of my corpus........"


#######1. EXPLORE YOUR CORPUS##########
#1.0 this gives a general summary of the corpus and makes a DF for further operations
#1.0.1: calculate readibility: a pulldown menu with configuration: measure= "Flesch.Kincaid" etc.. ; 
#remove_hyphens=T, F; min-max sentence length
fk <- textstat_readability(aicorp, "Flesch.Kincaid")
#add readibility to corpus
docvars(aicorp, "fk") <- fk
# 1.0.2 inspect the corpus summary
tokenInfo <-summary(aicorp, showmeta = T)
#write to an external csv file if needed, make a button: do you want save the summary as external file?
View(tokenInfo)

#1.1 different graphs for exploring the corpus:
#configuartion: x, y, plottype, some plots may require tweaking, as.factor, as.,nteger etc...
ggplot(tokenInfo, aes(x =as.factor(year), y=Tokens)) + geom_boxplot()
#configuartion: x, y, plottype, some plots may require tweaking, as.factor, as.,nteger etc...
ggplot(tokenInfo, aes(x =as.factor(year), y=fk)) + geom_boxplot()
#  to see  the content of any text, beeter done with plotly in an intercative manner, if noT: 
texts(aicorp)[76]

#1.2 corpus_subset
ai16 <- corpus_subset(aicorp, year == 2016)
ai15 <- corpus_subset(aicorp, year == 2015)
#join two corpuses, ie update your corpus, append new elements
aicorp <- aicorp + "newcorp"
aisum <- ai15 + ai16 #this is a working example, 

#1.3 concordance: box: enter your keyword, windows=?
options(width = 200)
scikw <- kwic(aicorp, "science")
kwic(aicorp, "scien", valuetype = "regex")
textplot_xray(scikw, sort=T)
#lexical dispersion plot
textplot_xray(kwic(ai15, "science" ), kwic(ai15, "technology" ), sort = T)+ 
  aes(color = keyword) + scale_color_manual(values = c("blue", "red"))
#subset the kw corpus
KWsubset <- corpus_subset(aicorp, docnames(aicorp)%in% scikw$docname)#subsets the documents of which names match the kwic docs(home)
save(KWsubset, file = "kwsubset.rda")


#2. FEATURE EXTRACTION
#2.0 tOKENIZE
#TOKENIZE: configuration: what: "word", "sentence", "character", "fastestword; 
#remove: symbols, separators, hyphens, twitter, urls, numbers, puntuation
#n-grams? 1L, 2L ...
aitokens <- tokens(aicorp, remove_punct=T, remove_separators = T, remove_numbers = T, remove_url = T)
#remove stopwords configuration: language (english, turkish.... ); case_insensitive, min_nchar, max_nchar
aitokenstp <- tokens_select(aitokens, stopwords("SMART"), "remove", padding = F)
#n-grams
aingr <- tokens_select(tokens(aicorp, remove_punct = T, ngrams = 2), stopwords("english"), "remove")
#to remove the stopwords for n-grams:#COLLOCATIONS: configuration: w or w/o stopwords?
colls <- textstat_collocations(aitokenstp, n = 1500, size = 3)
arrange(colls, desc(count))


###2.1 Parsing the text
spacy_initialize()
parsedtxt <- spacy_parse(aicorp) #configurations:pos;tag;entity; lemma; dependency. refer to help
saveRDS(parsedtxt, file="parsedai.rda")#save the parsed corpus since it takes very long time
parsedai <- readRDS(file="parsedai.rda")#read back
#named entity extraction
entity_extract(parsedai) #entitiy, entity type
#multi-word entities into single "tokens":
consen <- entity_consolidate(parsedtxt)
#you can filter tokens according to their tags: 
per <-filter(consen, entity_type=="EVENT")#change to pos==NOUN or tag ==NN
pers <- group_by(per, lemma)
pers <-summarise(pers)
spacy_finalize()
#some processes for cleaning the parsed corpus needed




######3. DFM  #######
#3.0 raw DFM
#Constructing a document-frequency matrix; this is a quick and dirty solution, needs to be done after careful feature selection
ai.dfm <- dfm(aicorp, remove = stopwords("SMART"), stem = T, remove_punct = T, remove_numbers = T)
ai.dfmw <- dfm_weight(ai.dfm, type ="tfidf" )#"frequency", tf = relfreq, relmaxfreq, logfreq, tfidf
ai.trm <- dfm_trim(ai.dfmw, min_count = 100, max_count = 300,  verbose = T)

topfeatures((ai.dfmw))
# TF (relfreq), term frequency/allterms in a doc;
#"relmaxfreq" feature counts/highest feature count in a document
#3.1 Graphs
#wordcloud; configureations:
#min.freq, max.words, scale (if too big or small)

textplot_wordcloud(ai.trm, max.words =Inf,  random.order = FALSE,
                   rot.per = .25, scale = c(2, 0.01), 
                   colors = RColorBrewer::brewer.pal(8,"Dark2"))
#Frequency table; configure n(number of terms) accordingly
aifr <- textstat_frequency(ai.dfmw, n = 100)
ggplot(aifr, aes(x = feature, y = frequency)) +
  geom_point() + 
  theme(axis.text.x = element_text(angle = 90, hjust = 1))


#3.2 Grouping
ai.grp <- dfm(aicorp, groups = "year", remove = stopwords("SMART"), remove_punct = TRUE)
#show most freq words by year
dfm_sort(ai.grp)[, 1:20]
#3.2.1 wordcloud
textplot_wordcloud(ai.grp, comparison = T)
textplot_wordcloud(ai.grp, random.color = TRUE, rot.per = .25, 
                   colors = sample(colors()[2:128], 5))
#3.2.2 Baloonplot f
aigr.trm <- dfm_trim(ai.grp, min_count = 500, verbose = T)
dt <- as.table(as.matrix(aigr.trm))
library("gplots")
balloonplot(t(dt), main ="Words", xlab ="", ylab="",
            label = FALSE, show.margins = FALSE)

#3.2.3 plot the freq of a term in groups
freq_grouped <- textstat_frequency(ai.dfmw,
                                   groups = "year")
# Filter the term "musk"
fregr <- subset(freq_grouped, feature %in% "musk") 
ggplot(fregr,  aes(group, frequency)) +
  geom_point()+
  theme(axis.text.x = element_text(angle = 90, hjust = 1))


#3.2.4 do for most frequent 10 each year
freq_grouped <- textstat_frequency(ai.dfmw, n=10,
                                   groups = "year")
ggplot(data = freq_grouped, aes(x = nrow(freq_grouped):1, y = frequency)) +
  geom_point() +
  facet_wrap(~ group, scales = "free") +
  coord_flip() +
  scale_x_continuous(breaks = nrow(freq_grouped):1,
                     labels = freq_grouped$feature) +
  labs(x = NULL, y = "Relative frequency")

# 3.2.5 calculate keyness reference to a group (disciminates the key words according to groups)
#Only select speeches for a group(year, person etc..)
ai.sub <- corpus_subset(aicorp, 
                             year %in% c("2015", "2016"))
# Create a dfm grouped by president
ai.subdfm <- dfm(ai.sub, groups = "year", remove = stopwords("english"), 
                remove_punct = TRUE)
# Calculate keyness and determine Trump as target group
result_keyness <- textstat_keyness(ai.subdfm, target = "2016")
# Plot estimated word keyness
textplot_keyness(result_keyness) 


#####DFM from dictionary categories, this can go to beginning or separate 
#make a dictionary
myDict <- dictionary(list(science = c("technology", "scien*", "invent*"),
                          economy = c("jobs", "economy", "business", "grow", "work")))

#or use an external dictionary
myDict <- dictionary(file= "moral foundations dictionary.dic", format = "LIWC")
# set the file location to the correct location on your computer.
#DFM
ai.dict <- dfm(aicorp, groups = "year",  remove = stopwords("english"), remove_punct = TRUE, dictionary =myDict)
topfeatures(ai.dict)
#Baloonplot for , but can alos add other plots
dt <- as.table(as.matrix(ai.dict))
library("gplots")
balloonplot(t(dt), main ="Words", xlab ="", ylab="",
            label = FALSE, show.margins = FALSE)



#4. KNOWLEDGE DISCOVERY: SIMILARITIES
ai2016 <- corpus_subset(aicorp, year==2016)
ai2016dfm <- dfm(ai2016, stem = T, remove = stopwords("english"), remove_punct=T)
d <- textstat_simil(dfm_weight(ai2016dfm, "tfidf"), margin="features", method="cosine")
textstat_dist(dfm_weight(ai2016dfm, "tfidf"), margin="documents", method="euclidean")


##FEATURES

ai.trm <- dfm_trim(ai.dfmw, min_count = 100, max_count = 200,  verbose = T)
d <- textstat_simil(dfm_weight(ai.trm, "tfidf"), margin="features", method="cosine")

#CLUSTERING
library(dendextend)
hc_res <- hclust(d, method = "ward.D")
dend <- as.dendrogram(hc_res)
plot(dend, 
     horiz =  TRUE,  nodePar = list(cex = .007))

