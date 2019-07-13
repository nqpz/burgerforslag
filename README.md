# burgerforslag

Gå ind på http://burgerforslag.dk/ og kig rundt omkring!


## Udvikling

Det interessante foregår i scriptet [rist_løg](rist_løg).  Kør for
eksempel `./rist_løg borgerforslag/00005.json` for at generere et
burgerforslag på standard out (kræver at du har kørt
`./get_missing_borgerforslag`).

Afhængigheder: Python 3 og Python 3-pakken `pyquery`.


## Opsætning af selve siden

Kør `get_missing_borgerforslag && update` en gang om dagen for at hente
alle borgerforslag og generere nye burgerforslag.

Kør `github-web-hook` ved boot som mappens ejer, så siden bliver
opdateret ved gitskub.

Peg din webserver til `serve`-mappen.  Noget i den her dur hvis du
bruger nginx:

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

location /github-web-hook {
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_pass http://localhost:44033;
}
```


## Kontakt

Lav en GitHub-issue eller skriv en email til Niels G. W. Serup på
<tomatketchup@burgerforslag.dk>


## Licens (fri software)

Burgerforslag-koden er copyright (C) 2019 Niels G. W. Serup og
tilgængelig under [GNU Affero General Public License, udgave
3](https://www.gnu.org/licenses/agpl-3.0.en.html) eller en senere
udgave.
