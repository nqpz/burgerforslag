# burgerforslag

Gå ind på http://burgerforslag.dk/ og kig rundt omkring!


## Opsætning

Kør `get_missing_borgerforslag && update` en gang om dagen for at hente
alle borgerforslag og generere nye burgerforslag.  Kør `update` for at
generere nye burgerforslag uden at undersøge om der er nye
borgerforslag.

Peg din webserver til `serve`-mappen.  Noget i den her dur:

```
server_name burgerforslag.dk www.burgerforslag.dk;

root /path/to/burgerforslag/serve;
index index.html;

location / {
    try_files $uri $uri/ =404;
}

location /se-og-stoet-forslag {
    try_files $uri "${uri}_${args}.html" =404;
}
```

Afhængigheder: Python 3 og Python 3-pakken `pyquery`.


## Udvikling

Det interessante foregår i `rødløg`.


## Kontakt

Lav en GitHub-issue eller skriv til `Niels G. W. Serup
<tomatketchup@burgerforslag.dk>`
