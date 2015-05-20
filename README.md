uruchamianie apliakacji:
1. w app/Rscripts.py w 3 linii nalezy podac sciezke do pliku z danymi testowymi (w fazie robienia jest skrypt bioracy dane z bazy)
2. w R install.packages('arules') (jesli niezainstalowana)
3. uruchamiamy Rserve uruchamiajac skrypt ./start.R (jesli nie dziala wykonywanie skryptow z l.k. sciagnac apt-get install littler)
4. uruchamiamy aplikacje

uruchamianie pyRserve:
1. ściągnij R 

2. ściągnij Rserve

3. ściągnij pyRserve

4. uruchom Rserve (uruchom R poleceniem R, następnie w interpreterze R uruchamiamy wpisujemy Rserve())

5. W pythonie import pyRserve

6. sprawdzamy czy działa: conn = pyRserve.connect()

Aby uruchomić aplikacje:

1. instalujemy biblioteke arules, w R install.packages('arules')

2. w Rscripts dopisujemy w pierwszej linii na zmienną dir2 sciezke do pliku z danymi

ustawianie pythona:

1.  python3.4 i pip (można przez MS web platform installer)
2.  python tools do visual studio
3.  stworzyć projekt djangowy z szablonu w visual studio i dać mu zainstalowac u siebie pakiety do pythona
4.  ściągnąć visual studio 2010 express
5.  easy_install pyodbc (z pipem wiecej klikania)
6.  pip install django-pyodbc-azure

pip freeze
```
Django==1.7.7
South==1.0.2
django-oauth-plus==2.2.6
django-pyodbc-azure==1.2.7
httplib2==0.9
oauth2==1.5.211
pyodbc==3.0.7
requests==2.6.0
```
