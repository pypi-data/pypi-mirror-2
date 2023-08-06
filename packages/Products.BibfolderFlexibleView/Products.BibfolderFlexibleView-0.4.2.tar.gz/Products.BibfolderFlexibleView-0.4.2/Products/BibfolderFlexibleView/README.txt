BibfolderFlexibleView

Beschreibung des Produkts
  
  Das Produkt BibfolderFlexibleView stellt eine dynamische Ansicht für die Bib-
  liographieverwaltung CMFBibliographyAT bereit. Sie erlaubt dem Besucher der 
  Webseite, sich nur Publikationen eines bestimmten Typs oder eines bestimmten
  Autors anzeigen zu lassen und ermöglicht es dem Betreiber der Seite, das Er-
  scheinungsbild der Liste und den Stil der Bibliographieeinträge (welche Felder
  sollen in welcher Reihenfolge erscheinen) sehr frei anzupassen, ohne dass dafü
  Templates von Hand geändert werden müssten.
  
  Das Produkt ermöglicht es zudem, andere Plone-Objekte (Links, PDFs, ...) mit 
  möglichst geringem Aufwand mit Bibliographieeinträgen zu verknüpfen.

Benoetigt:

  * CMFBibliographyAT 1.1 or higher
  * Plone 4.0 or higher
  
Installation

  Zunächst ins Products Verzeichnis der Zope Instanz entpacken, dann über 
  portal_quickinstaller im ZMI oder Plone Setup -> Add/Remove Products instal-
  lieren.
  
  *Achtung:* Wenn CMFBibliography auf der Instanz schon zuvor benutzt wurde,
  d.h. schon Bibliographie-Referenzobjekte existieren, empfiehlt es sich, ein 
  Update des portal_catalog durchzuführen (ZMI: portal_catalog -> Advanced ->
  Update Catalog), da - falls nicht vorhanden - die Felder 'publication_url'
  und 'absolute_url' zum Catalog hinzugefügt werden (Grund siehe Dokumentation)
  und diese sonst nicht automatisch mit Inhalt gefüllt werden.
  Da ein Update des Catalog einiges an Zeit in Anspruch nehmen kann, ist leider
  IMO keine Option, das bei der Installation (ungefragt) durchzuführen.

Was genau wird installiert? (was laueft unter der Haube?)

XXX auf aktuellen stand bringen!

  * Tool portal_bibliography_flexible_view wird installiert
  
  * Skins werden installiert
  
  * ControlPanel-Seite wird installiert
  
  * unser Template wird in die view_methods von portal_types.BibliographyFolder
    geschrieben
  
  * (Folder-weite) Konfiguration des Templates wird als neue Action von
    portal_types.BibliographyFolder installiert
  
  * view-action von portal_types.BibliographyFolder wird auf "" statt
    auf "base_view" gesetzt (sonst wuerde unser Template, auch wenns bei "Display"
    gesetzt ist, bei klicken auf "view" ignoriert)

TODO - was ich noch plane oder fuer sinnvoll halte

  * Uebersetzung von

  *  diesem Dokument

  *  allen Texten im Produkt

  *  Quellcodekommentaren
    
    ins Englische (im Hinblick darauf, dass das im Idealfall auch der
    (HU-externen) Community zugaenglich sein sollte
  
  * im Hinblick darauf auch: GPL-Lizenzvermerke ueberall dran
  
  * gescheite Dokumentation
  
  * stellenweise ausfuehrliche Beschreibungstexte bei der Konfiguration
  
  * Sortierung konfigurierbar machen: Es moechte ja wahrscheinlich nicht jeder  
    diese Gruppierung nach Jahren
  
  * Auflisten der Ergebnisse auf mehreren Seiten (unproblematisch machbar)
  
  * moeglich machen: vorhandene PDFs *in* den Referenzen als assoziertes Objekt
    anzeigen
  
  * wuenschenswert, aber schwer elegant/ohne Performanceverlust durch
    Extrawuerste zu realisieren: Moeglichkeit, z.b. (eds.) zur Maske
    hinzuzufuegen, *wenn* editors-feld gesetzt. statt hier am ende aufwaendige
    loesungen zu stricken, vielleicht lieber darum bemuehen, dass das Tool mit den
    ATBiblioList-Styles klarkommt (was aber sicher Performancemaessig eher noch
    happiger wird)
  
  * ? Button: Einstellungen auf Instanz-Default zuruecksetzen in
    Ordnereinstellungen
  
  * Template-Kopf (die suche nach den objekten, Filtern, Typen etc.)
    entschlacken, Filtern Performancemaessig verbessern ? (is aber nich der
    Flaschenhals)
  
  * ? validatoren und aehnliches schickes zueg fuer die konfig-seiten? (niedrige
    prioritaet!)

Original author

  Felix Droste, HU Berlin
