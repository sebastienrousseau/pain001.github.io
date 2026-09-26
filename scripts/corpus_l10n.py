#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2023-2026 Sebastien Rousseau
# SPDX-License-Identifier: Apache-2.0 OR MIT
"""Strings for the localized corpus scenario pages.

The scenario pages are generated from the library's provenance
records, so a locale variant costs the strings below and nothing else.
Five locales ship: the ones whose market packs the corpus already
covers (SEPA core). The scenario description and the source titles
are quoted from the record in their original English and labelled as
such, so no page is silently half-translated.

Keys are the page's fixed strings; ``{...}`` placeholders are filled
by the generator. English is the reference and must stay byte-for-byte
what the English pages already say.
"""
from __future__ import annotations

# slug -> (BCP 47 language tag, POSIX locale) as the site's front matter uses them.
CORPUS_LOCALES: dict[str, tuple[str, str]] = {
    "de": ("de", "de_DE"),
    "fr": ("fr", "fr_FR"),
    "es": ("es", "es_ES"),
    "it": ("it", "it_IT"),
    "nl": ("nl", "nl_NL"),
}

STRINGS: dict[str, dict] = {
    "en": {
        "eyebrow": "Example corpus",
        "title": "{sid}: ISO 20022 pain.001 example for {country} ({family})",
        "meta_desc": "{desc} A validated pain.001 sample for {country} on the {family} rail, "
                     "with its ISO 20022 JSON twin and provenance record; run it in the browser.",
        "keywords": "pain.001 example {country}, {family} sample XML, ISO 20022 {country} payment file, "
                    "{sid}, pain001 corpus",
        "desc_label": "",
        "intro": "A payment initiation file for **{country}** on the **{family}** rail, shipped in "
                 "{editions}, generated and checked by pain001 {version}. It is a synthetic example built "
                 "from the public scheme rulebooks: no real party, account or bank guideline behind it.",
        "h_files": "Files",
        "th_edition": "Edition", "th_file": "Payment file",
        "th_twin": "ISO 20022 JSON twin", "th_prov": "Provenance record",
        "no_twin": "None (twins cover pain.001 only)",
        "twin_para": "The twin is the same payment in the ISO 20022 Registration Authority's JSON convention, "
                     "lossless in both directions; its JSON Schema (2020-12) is published per edition: "
                     "{schemas}. An agent can produce a twin that validates against the schema and hand it "
                     "to the library to render the XML.",
        "h_run": "Run it in your browser",
        "run_para": "[Open this scenario in the demo]({url}): the pain001 library loads in a Python runtime "
                    "in your browser, rebuilds the file from the {n} record(s) below, checks it against the "
                    "`{scheme}` rulebook and the official XSD, and shows the JSON twin. Nothing leaves your "
                    "machine.",
        "flat_records": "The flat records the library rebuilds it from (the CSV pipeline's own column names):",
        "h_checked": "How the library checked it",
        "xsd": "Official XSD", "mdr": "ISO message definition rules", "profile": "Rail profile",
        "passed": "passed", "errors": "{n} error(s)", "warnings": "{n} warning(s)",
        "confidence": "Confidence **{level}**: {note}.",
        "levels": {"verified": "verified", "derived": "derived", "assumed": "assumed"},
        "notes": {
            "verified": "checked against a sample the scheme itself published",
            "derived": "built from the public rulebook or implementation guide; "
                       "no published sample was available to compare",
            "assumed": "one detail rests on an assumption the record names; "
                       "treat that detail with care",
        },
        "h_sources": "Where the content comes from",
        "read": "(read {date})",
        "public_only": "Public rulebook content only; see the corpus page for the method.",
        "sha_para": "SHA-256 of each file is in its provenance record. Your bank's own usage guideline is not "
                    "represented here: [apply it privately](/example-corpus/#your-bank-s-guideline) with the "
                    "library's overlay tooling.",
        "back": "Back to the example corpus",
        "all_by_country": "All payment files by country",
        "countries": {
            "BE": "Belgium", "CH": "Switzerland", "DE": "Germany", "ES": "Spain",
            "FR": "France", "GB": "United Kingdom", "IT": "Italy",
            "LU": "Luxembourg", "NL": "Netherlands", "SE": "Sweden",
            "US": "United States",
        },
    },
    "de": {
        "eyebrow": "Beispielkorpus",
        "title": "ISO-20022-pain.001-Beispiel {sid}: {country} ({family})",
        "meta_desc": "{desc} Eine validierte pain.001-Beispieldatei ({country}, Schiene {family}), "
                     "mit ISO-20022-JSON-Zwilling und Provenienzdatensatz; im Browser ausführbar.",
        "keywords": "pain.001 Beispiel {country}, {family} Beispiel-XML, ISO 20022 {country} Zahlungsdatei, "
                    "{sid}, pain001 Korpus",
        "desc_label": "Szenariobeschreibung, zitiert aus dem Provenienzdatensatz (englischer Originaltext):",
        "intro": "Eine Zahlungsinitiierungsdatei (**{country}**, Schiene **{family}**), ausgeliefert "
                 "in {editions}, erzeugt und geprüft von pain001 {version}. Es handelt sich um ein synthetisches "
                 "Beispiel aus den öffentlichen Regelwerken der Zahlungssysteme: keine reale Partei, kein reales "
                 "Konto und keine Bankrichtlinie dahinter.",
        "h_files": "Dateien",
        "th_edition": "Edition", "th_file": "Zahlungsdatei",
        "th_twin": "ISO-20022-JSON-Zwilling", "th_prov": "Provenienzdatensatz",
        "no_twin": "Keiner (Zwillinge gibt es nur für pain.001)",
        "twin_para": "Der Zwilling ist dieselbe Zahlung in der JSON-Konvention der ISO-20022-Registrierungsstelle, "
                     "in beide Richtungen verlustfrei; sein JSON-Schema (2020-12) wird je Edition veröffentlicht: "
                     "{schemas}. Ein Agent kann einen Zwilling erzeugen, der gegen das Schema validiert, und ihn "
                     "der Bibliothek zur XML-Erzeugung übergeben.",
        "h_run": "Im Browser ausführen",
        "run_para": "[Dieses Szenario in der Demo öffnen]({url}): Die pain001-Bibliothek wird in einer "
                    "Python-Laufzeit in Ihrem Browser geladen, baut die Datei aus den unten stehenden Datensätzen "
                    "({n}) neu auf, prüft sie gegen das Regelwerk `{scheme}` und die offizielle XSD und zeigt den "
                    "JSON-Zwilling. Nichts verlässt Ihren Rechner.",
        "flat_records": "Die flachen Datensätze, aus denen die Bibliothek die Datei neu aufbaut "
                        "(die Spaltennamen der CSV-Pipeline):",
        "h_checked": "Wie die Bibliothek die Datei geprüft hat",
        "xsd": "Offizielle XSD", "mdr": "ISO-Nachrichtendefinitionsregeln", "profile": "Schienenprofil",
        "passed": "bestanden", "errors": "{n} Fehler", "warnings": "{n} Warnung(en)",
        "confidence": "Konfidenz **{level}**: {note}.",
        "levels": {"verified": "geprüft", "derived": "abgeleitet", "assumed": "angenommen"},
        "notes": {
            "verified": "gegen ein vom Zahlungssystem selbst veröffentlichtes Muster geprüft",
            "derived": "aus dem öffentlichen Regelwerk oder Implementierungsleitfaden aufgebaut; "
                       "kein veröffentlichtes Muster stand zum Vergleich zur Verfügung",
            "assumed": "ein Detail beruht auf einer Annahme, die der Datensatz benennt; "
                       "behandeln Sie dieses Detail mit Vorsicht",
        },
        "h_sources": "Woher der Inhalt stammt",
        "read": "(gelesen am {date})",
        "public_only": "Nur Inhalte öffentlicher Regelwerke; die Methode steht auf der Korpusseite.",
        "sha_para": "Der SHA-256-Wert jeder Datei steht in ihrem Provenienzdatensatz. Die eigene "
                    "Nutzungsrichtlinie Ihrer Bank ist hier nicht abgebildet: "
                    "[Wenden Sie sie privat an](/example-corpus/#your-bank-s-guideline) mit dem "
                    "Overlay-Werkzeug der Bibliothek.",
        "back": "Zurück zum Beispielkorpus (EN)",
        "all_by_country": "Alle Zahlungsdateien nach Land (EN)",
        "countries": {
            "BE": "Belgien", "CH": "Schweiz", "DE": "Deutschland", "ES": "Spanien",
            "FR": "Frankreich", "GB": "Vereinigtes Königreich", "IT": "Italien",
            "LU": "Luxemburg", "NL": "Niederlande", "SE": "Schweden",
            "US": "Vereinigte Staaten",
        },
    },
    "fr": {
        "eyebrow": "Corpus d'exemples",
        "title": "Exemple pain.001 ISO 20022 {sid} : {country} ({family})",
        "meta_desc": "{desc} Un exemple pain.001 validé ({country}, rail {family}), avec son jumeau JSON "
                     "ISO 20022 et sa fiche de provenance ; exécutable dans le navigateur.",
        "keywords": "exemple pain.001 {country}, XML exemple {family}, fichier de paiement ISO 20022 {country}, "
                    "{sid}, corpus pain001",
        "desc_label": "Description du scénario, citée depuis la fiche de provenance (texte original en anglais) :",
        "intro": "Un fichier d'initiation de paiement (**{country}**, rail **{family}**), livré en {editions}, "
                 "généré et vérifié par pain001 {version}. C'est un exemple synthétique construit à partir des "
                 "règles publiques des schémas de paiement : aucune partie réelle, aucun compte réel, aucune "
                 "directive bancaire derrière lui.",
        "h_files": "Fichiers",
        "th_edition": "Édition", "th_file": "Fichier de paiement",
        "th_twin": "Jumeau JSON ISO 20022", "th_prov": "Fiche de provenance",
        "no_twin": "Aucun (les jumeaux ne couvrent que pain.001)",
        "twin_para": "Le jumeau est le même paiement dans la convention JSON de l'autorité d'enregistrement "
                     "ISO 20022, sans perte dans les deux sens ; son schéma JSON (2020-12) est publié par "
                     "édition : {schemas}. Un agent peut produire un jumeau valide contre le schéma et le "
                     "confier à la bibliothèque pour générer le XML.",
        "h_run": "L'exécuter dans votre navigateur",
        "run_para": "[Ouvrir ce scénario dans la démo]({url}) : la bibliothèque pain001 se charge dans un "
                    "environnement Python de votre navigateur, reconstruit le fichier à partir des {n} "
                    "enregistrement(s) ci-dessous, le vérifie contre les règles `{scheme}` et le XSD officiel, "
                    "puis affiche le jumeau JSON. Rien ne quitte votre machine.",
        "flat_records": "Les enregistrements à plat dont la bibliothèque repart "
                        "(les noms de colonnes du pipeline CSV) :",
        "h_checked": "Comment la bibliothèque l'a vérifié",
        "xsd": "XSD officiel", "mdr": "Règles de définition des messages ISO", "profile": "Profil de rail",
        "passed": "conforme", "errors": "{n} erreur(s)", "warnings": "{n} avertissement(s)",
        "confidence": "Confiance **{level}** : {note}.",
        "levels": {"verified": "vérifié", "derived": "dérivé", "assumed": "supposé"},
        "notes": {
            "verified": "comparé à un échantillon publié par le schéma de paiement lui-même",
            "derived": "construit à partir du règlement public ou du guide d'implémentation ; "
                       "aucun échantillon publié n'était disponible pour comparaison",
            "assumed": "un détail repose sur une hypothèse que la fiche nomme ; "
                       "traitez ce détail avec prudence",
        },
        "h_sources": "D'où vient le contenu",
        "read": "(lu le {date})",
        "public_only": "Contenu des règlements publics uniquement ; la méthode est décrite sur la page du corpus.",
        "sha_para": "Le SHA-256 de chaque fichier figure dans sa fiche de provenance. La directive d'utilisation "
                    "propre à votre banque n'est pas représentée ici : "
                    "[appliquez-la en privé](/example-corpus/#your-bank-s-guideline) avec l'outil d'overlay "
                    "de la bibliothèque.",
        "back": "Retour au corpus d'exemples (EN)",
        "all_by_country": "Tous les fichiers de paiement par pays (EN)",
        "countries": {
            "BE": "Belgique", "CH": "Suisse", "DE": "Allemagne", "ES": "Espagne",
            "FR": "France", "GB": "Royaume-Uni", "IT": "Italie",
            "LU": "Luxembourg", "NL": "Pays-Bas", "SE": "Suède",
            "US": "États-Unis",
        },
    },
    "es": {
        "eyebrow": "Corpus de ejemplos",
        "title": "Ejemplo pain.001 ISO 20022 {sid}: {country} ({family})",
        "meta_desc": "{desc} Una muestra pain.001 validada ({country}, raíl {family}), con su gemelo JSON "
                     "ISO 20022 y su registro de procedencia; ejecútela en el navegador.",
        "keywords": "ejemplo pain.001 {country}, XML de muestra {family}, archivo de pago ISO 20022 {country}, "
                    "{sid}, corpus pain001",
        "desc_label": "Descripción del escenario, citada del registro de procedencia (texto original en inglés):",
        "intro": "Un archivo de iniciación de pagos (**{country}**, raíl **{family}**), entregado en {editions}, "
                 "generado y comprobado por pain001 {version}. Es un ejemplo sintético construido a partir de los "
                 "reglamentos públicos de los esquemas de pago: no hay detrás ninguna parte real, ninguna cuenta "
                 "real ni ninguna guía bancaria.",
        "h_files": "Archivos",
        "th_edition": "Edición", "th_file": "Archivo de pago",
        "th_twin": "Gemelo JSON ISO 20022", "th_prov": "Registro de procedencia",
        "no_twin": "Ninguno (los gemelos solo cubren pain.001)",
        "twin_para": "El gemelo es el mismo pago en la convención JSON de la Autoridad de Registro ISO 20022, "
                     "sin pérdidas en ambos sentidos; su JSON Schema (2020-12) se publica por edición: "
                     "{schemas}. Un agente puede producir un gemelo que valide contra el esquema y entregarlo "
                     "a la biblioteca para generar el XML.",
        "h_run": "Ejecútelo en su navegador",
        "run_para": "[Abrir este escenario en la demo]({url}): la biblioteca pain001 se carga en un entorno "
                    "Python dentro de su navegador, reconstruye el archivo a partir de los {n} registro(s) "
                    "siguientes, lo comprueba contra el reglamento `{scheme}` y el XSD oficial, y muestra el "
                    "gemelo JSON. Nada sale de su máquina.",
        "flat_records": "Los registros planos a partir de los cuales la biblioteca lo reconstruye "
                        "(los nombres de columna del propio pipeline CSV):",
        "h_checked": "Cómo lo comprobó la biblioteca",
        "xsd": "XSD oficial", "mdr": "Reglas de definición de mensajes ISO", "profile": "Perfil de raíl",
        "passed": "superado", "errors": "{n} error(es)", "warnings": "{n} aviso(s)",
        "confidence": "Confianza **{level}**: {note}.",
        "levels": {"verified": "verificado", "derived": "derivado", "assumed": "supuesto"},
        "notes": {
            "verified": "comparado con una muestra publicada por el propio esquema de pago",
            "derived": "construido a partir del reglamento público o de la guía de implementación; "
                       "no había ninguna muestra publicada con la que comparar",
            "assumed": "un detalle se apoya en una suposición que el registro nombra; "
                       "trate ese detalle con cautela",
        },
        "h_sources": "De dónde procede el contenido",
        "read": "(leído el {date})",
        "public_only": "Solo contenido de reglamentos públicos; el método se describe en la página del corpus.",
        "sha_para": "El SHA-256 de cada archivo está en su registro de procedencia. La guía de uso propia de su "
                    "banco no está representada aquí: "
                    "[aplíquela en privado](/example-corpus/#your-bank-s-guideline) con la herramienta de "
                    "overlays de la biblioteca.",
        "back": "Volver al corpus de ejemplos (EN)",
        "all_by_country": "Todos los archivos de pago por país (EN)",
        "countries": {
            "BE": "Bélgica", "CH": "Suiza", "DE": "Alemania", "ES": "España",
            "FR": "Francia", "GB": "Reino Unido", "IT": "Italia",
            "LU": "Luxemburgo", "NL": "Países Bajos", "SE": "Suecia",
            "US": "Estados Unidos",
        },
    },
    "it": {
        "eyebrow": "Corpus di esempi",
        "title": "Esempio pain.001 ISO 20022 {sid}: {country} ({family})",
        "meta_desc": "{desc} Un campione pain.001 validato ({country}, circuito {family}), con il suo gemello "
                     "JSON ISO 20022 e il record di provenienza; eseguibile nel browser.",
        "keywords": "esempio pain.001 {country}, XML di esempio {family}, file di pagamento ISO 20022 {country}, "
                    "{sid}, corpus pain001",
        "desc_label": "Descrizione dello scenario, citata dal record di provenienza (testo originale in inglese):",
        "intro": "Un file di disposizione di pagamento (**{country}**, circuito **{family}**), fornito in "
                 "{editions}, generato e verificato da pain001 {version}. È un esempio sintetico costruito dai "
                 "regolamenti pubblici degli schemi di pagamento: nessuna parte reale, nessun conto reale, "
                 "nessuna linea guida bancaria dietro di esso.",
        "h_files": "File",
        "th_edition": "Edizione", "th_file": "File di pagamento",
        "th_twin": "Gemello JSON ISO 20022", "th_prov": "Record di provenienza",
        "no_twin": "Nessuno (i gemelli coprono solo pain.001)",
        "twin_para": "Il gemello è lo stesso pagamento nella convenzione JSON della Registration Authority "
                     "ISO 20022, senza perdite in entrambe le direzioni; il suo JSON Schema (2020-12) è "
                     "pubblicato per edizione: {schemas}. Un agente può produrre un gemello valido rispetto allo "
                     "schema e consegnarlo alla libreria per generare l'XML.",
        "h_run": "Eseguilo nel tuo browser",
        "run_para": "[Apri questo scenario nella demo]({url}): la libreria pain001 si carica in un runtime "
                    "Python nel tuo browser, ricostruisce il file dai {n} record qui sotto, lo verifica rispetto "
                    "al regolamento `{scheme}` e all'XSD ufficiale e mostra il gemello JSON. Nulla lascia la "
                    "tua macchina.",
        "flat_records": "I record piatti da cui la libreria lo ricostruisce (i nomi di colonna della pipeline CSV):",
        "h_checked": "Come la libreria lo ha verificato",
        "xsd": "XSD ufficiale", "mdr": "Regole di definizione dei messaggi ISO", "profile": "Profilo di circuito",
        "passed": "superato", "errors": "{n} errore/i", "warnings": "{n} avviso/i",
        "confidence": "Confidenza **{level}**: {note}.",
        "levels": {"verified": "verificato", "derived": "derivato", "assumed": "presunto"},
        "notes": {
            "verified": "confrontato con un campione pubblicato dallo schema di pagamento stesso",
            "derived": "costruito dal regolamento pubblico o dalla guida di implementazione; "
                       "nessun campione pubblicato era disponibile per il confronto",
            "assumed": "un dettaglio si basa su un'ipotesi che il record indica; "
                       "tratta quel dettaglio con cautela",
        },
        "h_sources": "Da dove proviene il contenuto",
        "read": "(letto il {date})",
        "public_only": "Solo contenuti di regolamenti pubblici; il metodo è descritto nella pagina del corpus.",
        "sha_para": "Lo SHA-256 di ogni file è nel suo record di provenienza. La linea guida d'uso della tua "
                    "banca non è rappresentata qui: "
                    "[applicala in privato](/example-corpus/#your-bank-s-guideline) con lo strumento di "
                    "overlay della libreria.",
        "back": "Torna al corpus di esempi (EN)",
        "all_by_country": "Tutti i file di pagamento per paese (EN)",
        "countries": {
            "BE": "Belgio", "CH": "Svizzera", "DE": "Germania", "ES": "Spagna",
            "FR": "Francia", "GB": "Regno Unito", "IT": "Italia",
            "LU": "Lussemburgo", "NL": "Paesi Bassi", "SE": "Svezia",
            "US": "Stati Uniti",
        },
    },
    "nl": {
        "eyebrow": "Voorbeeldcorpus",
        "title": "ISO 20022 pain.001-voorbeeld {sid}: {country} ({family})",
        "meta_desc": "{desc} Een gevalideerd pain.001-voorbeeld ({country}, rail {family}), met zijn ISO 20022 "
                     "JSON-tweeling en herkomstrecord; uitvoerbaar in de browser.",
        "keywords": "pain.001 voorbeeld {country}, {family} voorbeeld-XML, ISO 20022 {country} betaalbestand, "
                    "{sid}, pain001 corpus",
        "desc_label": "Scenariobeschrijving, geciteerd uit het herkomstrecord (oorspronkelijke Engelse tekst):",
        "intro": "Een betaalinitiatiebestand (**{country}**, rail **{family}**), geleverd in {editions}, "
                 "gegenereerd en gecontroleerd door pain001 {version}. Het is een synthetisch voorbeeld, "
                 "opgebouwd uit de openbare rulebooks van de betaalschema's: geen echte partij, geen echte "
                 "rekening en geen bankrichtlijn erachter.",
        "h_files": "Bestanden",
        "th_edition": "Editie", "th_file": "Betaalbestand",
        "th_twin": "ISO 20022 JSON-tweeling", "th_prov": "Herkomstrecord",
        "no_twin": "Geen (tweelingen bestaan alleen voor pain.001)",
        "twin_para": "De tweeling is dezelfde betaling in de JSON-conventie van de ISO 20022 Registration "
                     "Authority, verliesvrij in beide richtingen; het JSON Schema (2020-12) wordt per editie "
                     "gepubliceerd: {schemas}. Een agent kan een tweeling maken die tegen het schema valideert "
                     "en die aan de bibliotheek geven om de XML te genereren.",
        "h_run": "Voer het uit in uw browser",
        "run_para": "[Open dit scenario in de demo]({url}): de pain001-bibliotheek laadt in een Python-runtime "
                    "in uw browser, bouwt het bestand opnieuw op uit de {n} record(s) hieronder, controleert "
                    "het tegen het rulebook `{scheme}` en de officiële XSD, en toont de JSON-tweeling. Niets "
                    "verlaat uw computer.",
        "flat_records": "De platte records waaruit de bibliotheek het opnieuw opbouwt "
                        "(de kolomnamen van de CSV-pipeline zelf):",
        "h_checked": "Hoe de bibliotheek het heeft gecontroleerd",
        "xsd": "Officiële XSD", "mdr": "ISO-berichtdefinitieregels", "profile": "Railprofiel",
        "passed": "geslaagd", "errors": "{n} fout(en)", "warnings": "{n} waarschuwing(en)",
        "confidence": "Betrouwbaarheid **{level}**: {note}.",
        "levels": {"verified": "geverifieerd", "derived": "afgeleid", "assumed": "aangenomen"},
        "notes": {
            "verified": "vergeleken met een voorbeeld dat het betaalschema zelf heeft gepubliceerd",
            "derived": "opgebouwd uit het openbare rulebook of de implementatiegids; "
                       "er was geen gepubliceerd voorbeeld om mee te vergelijken",
            "assumed": "één detail berust op een aanname die het record benoemt; "
                       "behandel dat detail met zorg",
        },
        "h_sources": "Waar de inhoud vandaan komt",
        "read": "(gelezen op {date})",
        "public_only": "Alleen inhoud uit openbare rulebooks; de methode staat op de corpuspagina.",
        "sha_para": "De SHA-256 van elk bestand staat in zijn herkomstrecord. De eigen gebruiksrichtlijn van uw "
                    "bank is hier niet weergegeven: "
                    "[pas die privé toe](/example-corpus/#your-bank-s-guideline) met de overlay-tooling van "
                    "de bibliotheek.",
        "back": "Terug naar het voorbeeldcorpus (EN)",
        "all_by_country": "Alle betaalbestanden per land (EN)",
        "countries": {
            "BE": "België", "CH": "Zwitserland", "DE": "Duitsland", "ES": "Spanje",
            "FR": "Frankrijk", "GB": "Verenigd Koninkrijk", "IT": "Italië",
            "LU": "Luxemburg", "NL": "Nederland", "SE": "Zweden",
            "US": "Verenigde Staten",
        },
    },
}


def check() -> list[str]:
    """Every locale carries every English key, with the same placeholders."""
    import re
    problems = []
    en = STRINGS["en"]
    ph = re.compile(r"\{[a-z_]+\}")
    for slug, t in STRINGS.items():
        if set(t) != set(en):
            problems.append(f"{slug}: keys differ: {sorted(set(t) ^ set(en))}")
            continue
        for k, v in en.items():
            if isinstance(v, dict):
                if set(t[k]) != set(v):
                    problems.append(f"{slug}.{k}: keys differ")
            elif set(ph.findall(v)) != set(ph.findall(t[k])):
                problems.append(f"{slug}.{k}: placeholders differ")
    return problems


if __name__ == "__main__":
    import sys
    bad = check()
    print("\n".join(bad) or f"corpus_l10n: {len(STRINGS)} locales consistent")
    sys.exit(1 if bad else 0)
