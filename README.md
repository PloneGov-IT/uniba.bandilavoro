uniba.bandilavoro
=================

Add-on Plone per la gestione della pubblicazione dei bandi per la selezione di personale prodotti dai dipartimenti universitari (ad es. cococo).

Questo prodotto nasce dall'esigenza di avere un sistema per la pubblicazione delle procedure concorsuali dei Dipartimenti di ricerca dell'Università degli Studi di Bari Aldo Moro.  
*Uniba.bandilavoro* **non è un gestionale** ma una "compilazione guidata" alla pubblicazioni delle informazioni relative a bandi per il reclutamento.

Si è partiti dall'idea che un bando debba raccogliere le informazioni principali, mentre quelle di dettaglio appartengono all'entità "Profilo" (uno o più) ricercato. Inoltre esiste la necessità di tener traccia delle rettifiche apportate con apposito decreto ai bandi di concorso, e per questo è previsto un oggetto apposito.

**Questo prodotto non è usato a pieno regime. E' da considerarsi in beta-version.**

Architettura
------------
Il pacchetto è quindi costituito, fondamentalmente, da tre nuovi "tipi" di oggetto (archetypes):

  - Bando
  - Profilo
  - Rettifica

Tutti e tre questi oggetti sono di tipo *Folderish*, ovvero sono contenitori. *Profilo* e *Rettifica* non possono essere aggiunti se non nella cartella-oggetto *Bando*. Questo si rende necessario poichè un Bando può avere più Profili ricercati, e le Rettifiche possono riguardare (e quindi aggiunte) sia il Bando sia il Profilo.

Esempio di architettura base di un bando:

• DD.89/2013 per la ricerca di personale

––––––• Rettifica ai dati del Bando con DD. 90/2013

––––––• Profilo "Tecnico di Laboratorio biochimico"

–––––––––• Rettifica al profilo per mero errore materiale DD. 91/2013

––––––• Profilo "Assistente di laboratorio"



Con questo esempio si è ipotizzato un bando pubblicato per la ricerca di 2 profili professionali. In seguito sono state apportate due rettifiche: una per i dati del bando, la secondo per i dati strettamente legati al profilo (ad esempio il compenso).

Installazione
-------------
Questo pacchetto è progettato per versioni di Plone 4.x. Il pacchetto è da installare con metodo canonico tramite aggiunta nella lista degli *eggs* del buildout.

Una volta installato, apparirà una nuova voce di menu nel "Pannello di controllo": qui vanno settati i dipartimenti, le tipologie contrattuali e i tipi di profilo.


TO-DO
=====
+ Internazionalizzazione tramite utilizzo di 18n
+ Automatizzare la modifica dell'oggetto Bando/Profilo una volta aggiunta una Rettifica
+ Ottimizzazione del meccanismo di rettifica/annotazione
+ Compilazione guidata degli allegati
+ Test

##  Autore
+ Vito Falco - Università degli Studi di Bari Aldo Moro, vito.falco@uniba.it

Meenzione d'onore a 
+ Alessandro Ceglie - Università degli Studi di Bari Aldo Moro, alessandro.ceglie@uniba.it

