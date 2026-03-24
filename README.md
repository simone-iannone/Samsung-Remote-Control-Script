# Samsung-Remote-Control-Script
Samsung TV Remote Control via WebSocket

Questo script Python permette di inviare comandi remoti a una TV Samsung compatibile tramite il canale WebSocket sicuro (porta 8002). È utile per automatizzare l’invio di comandi come l’aumento del volume o altri tasti del telecomando digitale.

Caratteristiche principali
Connessione sicura alla TV via WebSocket.
Gestione automatica del token di autorizzazione dopo aver premuto “Consenti” sul popup della TV.
Invio programmabile di comandi remoti (es. KEY_VOLUP, KEY_HOME, ecc.).
Possibilità di inviare ripetutamente comandi (ad esempio aumentare il volume più volte in sequenza), così da ottenere un effetto di “volume spam”, utile in scenari di test: il volume della TV verrà alzato automaticamente più volte finché lo script non termina, anche più velocemente rispetto a un telecomando fisico.
Come funziona
Avvia lo script Python.
Sulla TV apparirà un popup per autorizzare il dispositivo. Premi Consenti.
Lo script riceve il token di autorizzazione e invia i comandi scelti, eventualmente ripetuti più volte per simulare il “volume spam”.

⚠️ Attenzione: usare questa funzionalità solo su dispositivi personali o ambienti di test. Non inviare comandi indesiderati su TV altrui.

Modifica le variabili nella sezione CONFIG:

Note

Ogni volta che lo script viene eseguito è necessario premere Consenti sulla TV.
