# bot-FUNDvoiculescu
Cum să faci farm la voturi pentru că sunt un leneș.
## Long story short
Deci. Dirigu a zis pe grup ca "Va rog sa votați... Contorizați voturile ...fiecare... La final îmi trimiteți" și eu CRED ca o sa dea un plus sau un 10 la cel care va avea cele mai multe voturi. Având în vedere că cunostintele mele la matematica sunt lowkey la **fund** (wink wink), vreau plusu sau nota de 10 pe cand incepe scoala. 

## Care e faza cu mizeria asta de cod?
Well, să stau să dau click-uri manual toată noaptea ca sclavul e ceva ce eu NU pot face, așa ca am decis sa imi folosesc my big brain abilities si sa fac un bot care sa faca asta in locul meu. Nici măcar nu e codat de mine, da asta nu mai zicem la nimeni. Base-ul a fost generat cu un LLM local în Ollama (a trebuit să-i dau un pic de jailbreak ca să nu-mi țină predici de etică când i-am zis să facă un bot de spam voturi), iar după aia i-am dat feed în Grok ca să-l facă mai bun și să-l optimizeze la sânge (pentru ca aparent Grok nu are masuri bune de "user intent") . Poate ca nu e cel mai bun cod (avand in vedere ca e vibecoded), dar își face treaba perfect (sa zicem).

## Features (dacă le pot numi așa)
Codul e o mizerie care se bazeaza pe timp de sleep random ca sa nu ne detecteze cloudflare, dar automatizează tot ca să nu rămânem cu **fund**ul gol:

* **Mail.tm bypass:** Face conturi fake behind the scenes și citește codul de confirmare direct din json-ul mail-ului. E lowkey amuzant sa vezi ca o "oficialitate" din asta nu s-a gandit la mail check-ing.
* **Undetected Chromedriver:** Grok mi-a zis să bag asta în loc de Selenium normal, ca să nu ne luăm ban în secunda doi și să ajungem direct în **fund**ul clasamentului (butt jokes haha). 
* **Human simulation behavior:** Are niște `random_sleep()` aruncate complet haotic prin cod. Zici că e un om care de abia ține mouse-ul în mână când completează formularul.
* **Auto-Restart Memory Saver:** Chrome-ul mănâncă RAM de rupe. Dacă nu-i dădeam kill la fiecare 10 voturi, pica memoria în **fund** și crăpa PC-ul (i guess nu stiu, asa mi a zis aiul so yea, fact check me idc).
* **JSON Logging:** Salvează tot ce mișcă în `votes_log.json`. Dacă dirigu intreaba de unde am 2000 de voturi over night, literally tot ce trebuie sa fac ii sa ii arat fisierul.

## Cum îi dai run ((pentru noobi (dw nici eu n-am stiut neaparat))
Disclaimer din start: don't DM me for tech support. Dacă nu vă merge, google it or yk, use ai i guess.

1. Aveți nevoie de Python. Dacă nu știți să-l instalați, skill issue.
2. Deschideți un terminal și băgați comanda asta ca să luați pachetele (fiti siguri ca aveti un venv in acelasi folder ca si fisierul cu programul, adica unde este .py-ul):
   `pip install undetected_chromedriver requests selenium`
3. Dacă vreți să farmați pentru alt candidat, schimbați `CANDIDATE_NAME` din script desi ma rog nu recomand.
4. Dați-i run:
   `python vot_fundvoiculescu.py`
5. Lăsați-l în **fund**al să-și facă treaba și băgați-vă la nani.

## Gandaci si alte probleme
Dacă pică site-ul de la **fund**ație din cauza noastră, lowkey nu mă prea interesează, aia e problema lor ca nu s in stare de nimic. Dacă bot-ul dă un random error la 4 dimineața... iarăși, not my problem, modify the code at your own wishes. Dați-i un restart, optimize it, idc. Codul ăsta există doar din pura disperare pt plus sau nota deci daca se intampla ceva rau, e vina lu dirigu nu a mea. Use ts at your own discretion but be careful. 
