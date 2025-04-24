# Sim Server Log

Skript mis imiteerib serveri tööd kirjutades serveri tegevusi logi faili. Lisaks teeb kausta suvalisel hetkel 
mõngingaid teenuste logi faile mida siis ka ära kustutab. 

# Paigaldus PyCharmiga
1. Tee PyCharmiga uus projekt läbi versiooni kontrolli (_Version Control_) File -> New Project from Version Control
2. URL reale kleebi Githubi .git link (ja nupule **Clone**)
   * Usalda projekti (Trust Project)
   * Ava endale sobivas aknas
3. Seadista Python Interpreter -> Add New Interpreter -> Add Local Interpreter -> OK
   * Kui küsib kas installida requirements võib lubada, kuid järgmist punkti ära tee ning käivita PyCharm uuesti
4. Kui eelmise punkti * ei teinud, siis peale seda võta PyCharmis terminal (Alt + F12) ning kirjuta **````pip install -r requirements.txt````**
   * See paigaldab [Faker](https://faker.readthedocs.io/en/master/) mooduli ja mooduli sõltuvused
5. Järgnevaks saad käivitada skripti **run_server.py**

# Paigaldus käsureal
1. Paigalda [Python](https://www.python.org/), kui pole.
   * Vaata, et installil oleks PATH märkeruut valitud
2. Paigalda [Git for Windows](https://git-scm.com/downloads/win), kui pole
3. Peale installe tee restart 
4. Ava terminal (Powershell sobib)
5. Liigu kausta kuhu soovid antud rakenduse allalaadida
6. Klooni rakendus:
    * ````git clone https://github.com/OkramL/SimServerLog.git````
7. Liigu kausta SimServerLog
    * ````cd SimServerLog````
8. Installi Pythoni virtuaal keskkond
    * ````pip install virtualenv````
9. Loo projekti kausta virtuaalkeskkond (_Virtual Enviroment_) nimega **.venv**
    * ````python -m venv .venv````
10. Aktiveeri virtuaalkeskkond
    * ````.\.venv\Scripts\activate````
11. Paigalda [Faker](https://pypi.org/project/Faker/) moodul ja vajalikud mooduli sõltuvused
    * ````pip install -r .\requirements.txt````
12. Käivita rakendus: ````python run_server.py```` või ````python run_server.py no-gz````

Kui juhuslikult terminali kinni paned, siis
1. Ava terminal (PowerShell sobib)
2. Liigu kausta SimServerLog ````cd KETAS:\KAUST\KAUST\SimServerLog````
3. Aktiveeri virtuaalkeskkond ````.\.venv\Scripts\activate````
4. Käivita rakendus ````python run_server.py```` või ````python run_server.py no-gz````

# Töötamine
Käivitades skripti jääb see lõputult tööle kirjutades iga 1-5 sekundi tagant logi faili mingi tegevuse. Samal ajal seda 
ka konosoli näidates. Logi tehakse **c:\Temp** kausta nimega **application.log**. Kui logi fail on saavutanud skriptis määratud 
mahu (10kB), siis tehakse sellest eraldi fail mille lõppu lisatakse .1 (application.log.1) ning logi kirjutamist 
jätkatakse jälle application.log faili. Kõige vanem logi fail on .9 lõpuga ja kõige uuem .log ehk hetkel kasutatav fail. 
Kõik see on juhul, kui võtit **no-gz** mitte kasutada käsureal. Vaata 14.01.2025 ja 20.01.2025 täiendusi.

Igakord kui skript uuesti käivitatakse kustutatakse eelnevad logid ära ja alustatakse uuesti logide loomist. Kõik on juhuslik!

# 14.01.2025 - täiendused

1. Vanad failid pakitakse kokku .gz ning lisatakse lõppu .1 kuni .9 (näiteks: **application.gz.3**)
2. Lisatud on käsurea argument **no-gz**, mis tähendab, et vanu faile kokku ei pakita. Näiteks **application.log.6**
3. Aktiivne fail kuhu kirjutatakse on **application.log** 

# 20.01.2025 - täiendused
1. Kokkupakitud faili malli on muudetud. See on **application.log.NUMBER.gz**, kus NUMBER ON ikka 1-9 ja vanim on 
suurima numbriga.

# 23.04.2025 - täiendused
1. Täiendatud README.md faili **Paigaldus käsureal** osaga

# ÜLESANDE TEGIJAD
1. Kui teed esimest ülesannet käivita käsurealt skript: **````py run_server.py no-gz````**
2. Kui teed teist ülesannet (esimene on valmis) käivita käsurealt skript **````py run_server````**

Kui terminal või cmd on käivitatud õiges kaustas, siis on vaja Pythoni Virtual Enviroment ka aktiveerida. Selleks kirjuta: ````.venv\Script\activate````
**NB! Kasuta selleks TAB'i, et näpukaid poleks ja asi oleks õige.**
