import os
import discord
from keep_alive import keep_alive
import requests
from requests_html import HTMLSession
import csv
import pandas as pd
import statistics

client = discord.Client()
my_secret = os.environ['token']


def getInput(inputMoney):
    input_money = inputMoney.strip()
    name = (input_money + " kaç tl").strip()
    url = "https://www.google.com.tr/search?q=" + name

    return url


def startSession(queryUrlInput):
    try:
        session = HTMLSession()
        response = session.get(queryUrlInput)

    except requests.exceptions.RequestException as e:
        print(e)

    return response


def findCurrencyValue(sessionInput):
    css_identifier_query_name = ".wDYxhc"
    css_identifier_input_money = ".vk_sh"
    css_identifier_output_value = ".dDoNo"

    result = sessionInput.html.find(css_identifier_query_name)[0]

    item = {'input_money': "Invalid Currency", 'output_value': "Invalid Currency"}
    try:
        item = {
            'input_money': result.find(css_identifier_input_money, first=True).text,
            'output_value': result.find(css_identifier_output_value, first=True).text
        }
    except:
        pass

    return item


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    msg = message.content

    if message.author == client.user:
        return

    msg_arap_check = str(message.content).split(" ")[0]
    if msg_arap_check == "sa":
        await message.channel.send("arap mısın amkkk")

    if msg.startswith('!money'):
        money = str(msg).split(" ")[1]
        queryUrl = getInput(money)
        session = startSession(queryUrl)
        money = findCurrencyValue(session)

        await message.channel.send("Currently value is: " + (money['output_value']))

        value = money['output_value'].split(" ")[0]

        with open('values.csv', 'a', newline='') as f:
            thewriter = csv.writer(f, delimiter=' ')
            thewriter.writerow(value)
    if msg.startswith('!stability'):
        csvSterlin = pd.read_csv("normalized_sterlin.csv", sep=";")
        csvUsd = pd.read_csv("normalized_usd.csv", sep=";")
        csvEuro = pd.read_csv("normalized_euro.csv", sep=";")

        sd_sterlin = statistics.stdev(list(csvSterlin.loc[:, "sterlin"]))
        sd_usd = statistics.stdev(list(csvUsd.loc[:, "usd"]))
        sd_euro = statistics.stdev(list(csvEuro.loc[:, "euro"]))
        mostStable = ""
        if (sd_sterlin < sd_usd) and (sd_sterlin < sd_euro):
            mostStable = "Sterlin"
        if (sd_usd < sd_euro) and (sd_usd < sd_sterlin):
            mostStable = "Usd"
        if (sd_euro < sd_sterlin) and (sd_euro < sd_usd):
            mostStable = "Euro"
        await message.channel.send(mostStable + " is the most stable currency.")


keep_alive()
client.run(os.getenv('token'))
