## Popis projektu
This project is focused on data scraping from Web Page presenting the results of Czech legislative election held on 20th and 21st October 2017.
Link to web-page:

https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103

## Installation of Python Packages
Python packages which are referenced in the main python file are listed in requirements.txt.
Before their installation is recommended to set up virtual environment and to define Python interpreter. 
Python packages can be installed as follows:

 pip install -r requirements.txt

## Initialization of Web Scraper Tool
Main Python file is named as "election_scraper.py" and is configured to be started in terminal´s command line. 

Example - How to execute the main python file:
python .\election_scraper.py <argument_1> <argument_2>

argument_1 = URL link to webpage.  
argument_2 = name of the CSV file to save collected data. 

## Example:
Election results for District named "Plzen-mesto" can be extracted as follows:

python .\election_scraper.py "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=4&xnumnuts=3203" "vysledky_Plzen.csv"

### Election Scraper output when executed:

Stahuji data z URL: https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=4&xnumnuts=3203 .
Ukladam data do souboru...
Ukončuji Web Scraper.

Data saved in the destination file:

Cislo obce,Nazev obec,Volici v seznamu,Vydane obalky,Volebni ucast v %,Odevzdane obalky,Platne hlasy,Občanská demokratická strana,Řád národa - Vlastenecká unie,CESTA ODPOVĚDNÉ SPOLEČNOSTI,Česká str.sociálně demokrat.,Radostné Česko,STAROSTOVÉ A NEZÁVISLÍ,Komunistická str.Čech a Moravy,Strana zelených,"ROZUMNÍ-stop migraci,diktát.EU",Strana svobodných občanů,Blok proti islam.-Obran.domova,Občanská demokratická aliance,Česká pirátská strana,OBČANÉ 2011-SPRAVEDL. PRO LIDI,Referendum o Evropské unii,TOP 09,ANO 2011,SPR-Republ.str.Čsl. M.Sládka,Křesť.demokr.unie-Čs.str.lid.,Česká strana národně sociální,REALISTÉ,SPORTOVCI,Dělnic.str.sociální spravedl.,Svob.a př.dem.-T.Okamura (SPD),Strana Práv Občanů,-
558851,Dýšina,1349,860,"63,75",858,853,114,0,0,48,0,52,41,10,5,16,1,2,119,0,3,45,269,5,34,0,3,2,1,80,3,-
558966,Chrást,1429,1002,"70,12",1002,999,151,1,1,51,1,31,63,8,4,15,1,2,111,1,1,45,354,1,24,0,11,5,2,114,1,-
...