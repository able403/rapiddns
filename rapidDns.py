import requests
from bs4 import BeautifulSoup
import argparse
import datetime
parser = argparse.ArgumentParser(description=f"a simple python client for rapiddns.io")
import pathlib
dt = datetime.datetime.now()
import time 
import random
import os
from rich.progress import track

def getdata(domain):
    if (domain.find("/")):
        url = f"https://rapiddns.io/s/{domain}?full=1&down=1"
    items = []
    try:
        response = requests.get(url,timeout=30,headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0"})
        html = response.content
    except Exception as e:
        print("can't connect to rapiddns.io")
    try:
        soup = BeautifulSoup(html, "html.parser")
        table = soup.find("table", id="table")
        rows = table.findAll("tr")
        items = []
        for row in rows:
            cells = row.findAll("td")
            items.append([value.text.strip() for value in cells])
    except Exception as e:
        print(e)
        print("can't get data from rapiddns.io")
        with open("addfailt.txt","a+")as f:
            f.write(domain+"\n")
    return items[1:]


def main():
    try:
        parser.add_argument(
            "--subdomains",
            "-d",
            action="store",
            help="domain name",
            required=False,
        )
        parser.add_argument(
            "--file",
            "-f",
            action="store",
            help="file name",
            required=False,
    )
        args = parser.parse_args()
        arg_subdomains = args.subdomains
        arg_files = args.file
        if (arg_subdomains or arg_files) is None:
            parser.error('parameter --subdomains or --file is required')
        if arg_subdomains is not None:
            time.sleep(random.randint(5,10))
            for line in getdata(arg_subdomains):
                print(",".join(line))
        elif  arg_files is not None:
            try:
                domains = open(arg_files).read().split("\n")
                items_all =""
                failt =""
                for domain in track(domains):
                    time.sleep(random.randint(5,10))
                    items = ""    
                    if domain == "":
                        continue
                    print(domain)
                    for line in getdata(domain):
                        lines =",".join(line)
                        items += lines + "\n"
                    domain = domain.replace("/","-")
                    arg_ofile ="./result/"+domain+".txt"

                    with open(arg_ofile,"a+") as f:
                        f.write(items)
                        f.close()
                    if (os.path.getsize(arg_ofile))== 0:
                        failt +=domain+"\n"
                    items_all += items + "\n"
                allfile ="./result/"+ str(dt.strftime('%Y%m%d%H'))+".txt"
                with open(allfile,"a+") as f:
                    f.write(items_all)
                fail = "fail-"+str(dt.strftime('%Y%m%d%H'))+".txt"
                with open("failt.txt","a+") as f:
                    f.write(failt)                      
            except Exception as e:
                print(e)

    except Exception as e:
        print(e)


if __name__ == "__main__":
    pathlib.Path('./result').mkdir(parents=True, exist_ok=True) 
    main()
