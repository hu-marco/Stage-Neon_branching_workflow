# Stage - Branching Workflows di Neon

## 1. Introduzione

Questa repository nasce dallo stage per l'analisi sul Branching Workflows del Postgres di Neon.
Il programma presente è solo un prototipo estremamente grezzo e non completo.
È stato scelto come lingaggio di programmazione Python.

## 2. Obiettivo

L'obiettivo finale è studiare come integrare il database branching possa essere integrato in una pipeline DevOper per rendere le modifiche al database più affidabili.

## 3. Struttura del progetto

La repository può essere diverso in diverse parti:

* ** API ** : di cui useremo FastAPI, un famoso moderno framework in Python per costruire i API.
* ** Migrazioni ** : useremo Alembic, uno strumento per la gestione dei database in Python.
* ** Database** : l'argomento principale è proprio il Postgres di Neon (neon.com)
* ** Pipeline ** : useremo  Github Actions di Github.
* ** Test ** : useremo pytest, una funzione di Python.
* ** Sito web ** : viene utilizzato HTML linguaggio usato per la creazione le pagine web, CSS usato per l'estetica e Javascript responsabile per rendere le pagine interattive.

### 3.1 API

Dal punto di vista di API, utilizziamo FastAPI per creare dei file Python all'interno della cartella ** routers ** che dispongono delle funzioni per la comunicazione di dati tra il database e il software.

### 3.2 Migrazioni

Le migrazioni sono cambiamenti o trasferimenti di dati delle tabelle o database.
Ciò che usiamo, Alembic, rende la creazione e gestione delle migrazioni in modo semplice e facilmente comprensibile.
Nella cartella ** migrations ** dove sono presenti le migrazioni.


### 3.3 Database

Dal lato del database, utilizzeremo SQLAlchemy e Pydantic per gestire il database.
Anche in questo vengono suddivice in diverse parti per gestire i diversi compiti:
- ** models.py ** e ** schemas.py **: vengono definiti i modelli delle tabelle e facilita la creazione o recupero dell'informazioni.
- ** database.py **: vengono creati le tabelle e inserite i primi dati randomici
- ** branch.py ** : contiene le funzioni per la creazione del branch, mentre ** branch_command.py ** e ** setup_branch.py ** sono necessari nei GitHub Actions


### 3.4 Pipeline

Pipeline DevOps è un insieme di processi e strumenti automatizzati che consente ai sviluppatori di collaborare.
Nel nostro caso, viene utilizzato Github Actions, di cui a seconda dell'uso può essere gratuito o fornisce un limito uso.
In ** .github/workflows ** contiene tutti i actions per la verifica e test.


### 3.5 Test

Sono stati effettuati diversi test di integrazione e end-to-end per verificare l'assenza di errori.

### 3.6 Sito Web

Il sito web è estremamente semplice e grezzo. Essendo un prototipo, dà un idea di un possibile prodotto finito.
Essendo uno scheletro esso contiene il minimo dei controlli.

## 4. Note

Per il corretto funzionamento dei workflows, devo essere salvati in secrets della repository i seguenti dati:

- **DATABASE_NAME**: nome del database
- **DATABASE_ROLE**: ruolo sul database (esempio. proprietario)
- **NEON_API_KEY**: il punto di accesso al database (usato per la creazione dei branch)
- **NEON_PROJECT_ID**: id del progetto
- **SHARED_DATABASE_URL**: url di un database condiviso (in questo caso ho usato un branch)

Inoltre la correttezza dei test è basato al contenuto del mio database, quindi la generazione di nuovi dati può comportare errori