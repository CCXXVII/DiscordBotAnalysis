import pandas as pd
import statistics


csvSterlin = pd.read_csv("normalized_sterlin.csv",sep=";")
csvUsd = pd.read_csv("normalized_usd.csv",sep=";")
csvEuro = pd.read_csv("normalized_euro.csv",sep=";")


sd_sterlin = statistics.stdev(list(csvSterlin.loc[:,"sterlin"]))
print(sd_sterlin)


sd_usd = statistics.stdev(list(csvUsd.loc[:,"usd"]))
print(sd_usd)


sd_euro = statistics.stdev(list(csvEuro.loc[:,"euro"]))
print(sd_euro)









