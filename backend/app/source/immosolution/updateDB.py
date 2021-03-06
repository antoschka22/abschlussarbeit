from dao.db import get_db_cursor

def updateDatabase():
    def checkTables():
        """
            überprüft ob alle bereits Tabelle existieren
        """
        with get_db_cursor() as cursor:
            cursor.execute("""SELECT count(*) as amountoftables
                            FROM pg_catalog.pg_tables
                            WHERE schemaname != 'pg_catalog' AND 
                            schemaname != 'information_schema';
                            """)
            return cursor.fetchone()

    def checkDBVersionTableExists():
        """
            überprüft ob die Tabelle db_version in der Datenbank existiert
        """
        with get_db_cursor() as cursor:
            cursor.execute("""SELECT *
                            FROM INFORMATION_SCHEMA.TABLES
                            WHERE TABLE_SCHEMA = 'public'
                            AND TABLE_NAME = 'db_version'; 
                            """)
            return cursor.fetchone()
    if not checkDBVersionTableExists():
        """
            erstellt die Tabelle db_version, falls sie nicht funktioniert
        """
        with get_db_cursor() as cursor:
            cursor.execute("""
                            CREATE TABLE db_version (
                            id FLOAT(5) PRIMARY KEY,
                            comment VARCHAR(255) NOT NULL);
                            """)
    def latestVersion():
        """
            Get the current version of the db
        """
        with get_db_cursor() as cursor:
            cursor.execute("select max(id) from db_version")
            return cursor.fetchone()

    def addVersion(version, comment):
        """
            add next new version with a comment
        """
        with get_db_cursor() as cursor:
            cursor.execute("""
                            insert into db_version (id, comment)
                            values(%s, %s)""", [version, comment])

    checkAllTheTables = checkTables()
    lastVersionId = latestVersion()
    if checkAllTheTables['amountoftables'] == 1:
        if lastVersionId["max"] != 0.1:
            addVersion(0.1, 'test')
    if lastVersionId["max"] < 0.2:
        with get_db_cursor() as cursor:
            cursor.execute("""
                CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
                CREATE TABLE IF NOT EXISTS Infos( 
                    id UUID DEFAULT uuid_generate_v4 () UNIQUE,
                    angebot VARCHAR(65535) NOT NULL,
                    gruedung VARCHAR(65535) NOT NULL,
                    referenzprojekte VARCHAR(65535) NOT NULL,
                    mitarbeiter VARCHAR(65535) NOT NULL,
                    privatkunden VARCHAR(65535) NOT NULL,
                    PRIMARY KEY (id)
                );
                CREATE TABLE IF NOT EXISTS Kunden(
                    firmenname VARCHAR(65535) NOT NULL,
                    PLZ VARCHAR(65535) NOT NULL,
                    ort VARCHAR(65535) NOT NULL,
                    strasse VARCHAR(65535) NOT NULL,
                    PRIMARY KEY (firmenname)
                );
                CREATE TABLE IF NOT EXISTS Projekte(
                    projektname VARCHAR(65535) NOT NULL UNIQUE,
                    herzeigeprojekte BOOLEAN NOT NULL,
                    kunden_kundenname VARCHAR(65535),
                    PRIMARY KEY (projektname),
                    FOREIGN KEY (kunden_kundenname) REFERENCES Kunden(firmenname) ON DELETE CASCADE
                );
                CREATE TABLE IF NOT EXISTS Bilder(
                    id UUID DEFAULT uuid_generate_v4 () UNIQUE,
                    projektbilder VARCHAR(65535),
                    projekt_id VARCHAR(65535) NOT NULL,
                    PRIMARY KEY (id),
                    FOREIGN KEY (projekt_id) REFERENCES Projekte(projektname) ON DELETE CASCADE
                );
                CREATE TABLE IF NOT EXISTS Leistungen(
                    leistung VARCHAR(65535),
                    PRIMARY KEY (Leistung)
                );
                CREATE TABLE IF NOT EXISTS Arbeit(
                    id UUID DEFAULT uuid_generate_v4 () UNIQUE,
                    beschreibung VARCHAR(65535) NOT NULL,
                    leistungen_leistung VARCHAR(65535),
                    PRIMARY KEY (id),
                    FOREIGN KEY (leistungen_leistung) REFERENCES Leistungen(leistung) ON DELETE CASCADE
                );
                INSERT INTO Infos(angebot, gruedung, referenzprojekte, mitarbeiter, privatkunden)
                VALUES ('Als kompetentes und motiviertes Unternehmen bieten wir all unseren Kunden sorgsam abgestimmte Lösungen im Bereich Gebäudemanagement und Gebäudetechnik an. Daher liegen unsere Kernkompetenzen in der Planung und Installation sowie im Betrieb und in der Wartung von gebäudetechnischen Anlagen in den Bereichen Heizung, Kälte/Klima, Lüftung und Sanitär.', 
                'Seit der Gründung des Unternehmens im Jahr 2002 steht Immosolution für Service und Dienstleistungen in Handschlagqualität. Als junges und dynamisches Team, werden wir nun seit Anfang 2020 in neuer Konstellation erfolgreich den gewohnten Ansprüchen aller Bestands- und Neukunden gerecht', 
                'Referenzprojekte sind immer der beste und zuverlässigste Beweis für die Leistungsfähigkeit eines Unternehmens. Einige ausgewählte Beispiele zeigen unsere umgesetzten Projekte, die das Ergebnis intensiver, professioneller und kundenorientierte Arbeit darstellen.',
                'Ein Unternehmen ist nur so gut wie seine Mitarbeiter, weshalb bei uns fachliche Qualifikation und hohes persönliches Leistungs- und Qualitätsbewusstsein an erster Stelle stehen. ', 
                'Neben Privatkunden betreuen wir auch diverse Industrie- und Gewerbeunternehmen wie Hotels und Gastronomie-Betriebe. Gerade deshalb stehen unsere Kunden als Mensch und Geschäftspartner im Mittelpunkt.');

                INSERT INTO Leistungen (leistung)
                VALUES 
                ('Gebäudemanagement'),
                ('Gebäudetechnik');

                INSERT INTO Arbeit (beschreibung, leistungen_leistung)
                VALUES 
                ('Neuinstallationen & Sanierungen', 'Gebäudemanagement'),
                ('Wartungen & Reparaturen', 'Gebäudemanagement'),
                ('technische Dokumentationen und Befunde', 'Gebäudemanagement'),
                ('Kälte- & Klimatechnische Anlagen', 'Gebäudetechnik'),
                ('Heizungs- & Lüftungstechnische Anlagen', 'Gebäudetechnik'),
                ('Sanitär- & Gastechnische Anlagen', 'Gebäudetechnik'),
                ('Solartechnik und nachhaltige Wärmetechnik', 'Gebäudetechnik');
                """)
        addVersion(0.2, 'basic tables creation')
        
    if lastVersionId["max"] < 0.3:
        with get_db_cursor() as cursor:
            cursor.execute("""
                INSERT INTO Kunden (firmenname, plz, ort, strasse)
                VALUES  
                ('Fleck Elektroinstallationen GmbH', '1120', 'Wien', 'Wienerbergstraße 25B'),
                ('WEVIG Wohnungseigentumsverwaltungs- und Immobilientreuhand GmbH', '1150', 'Wien', 'Märzstraße 1'),
                ('WIEBE Wiener Bauträger- und EntwicklungsgesmbH', '1150', 'Wien', 'Märzstraße 1'),
                ('Familienwohnbau gemeinnützige Bau- und Siedlungsgesellschaft m.b.H.', '1150', 'Wien', 'Märzstraße 1'),
                ('Hottinger Bruel & Kjaer Austria GmbH', '1230', 'Wien', 'Lemböckgasse 63/2'),
                ('Institut für medizinische u. chemische Labordiagnostik Gesellschaft m.b.H', 'diverse Labore', 'diverse Labore', 'diverse Labore'),
                ('BHB Boutique Hotel Betriebs GmbH THE GUEST HOUSE VIENNA', '1010', 'Wien', 'Führichgasse 10'),
                ('Zentralverband der Hausbesitzer – Hausbesitzerhilfsverein', '1010', 'Wien', 'Landesgerichtsstraße 6'),
                ('Hofer Richard GmbH', '7423', 'Pinkfeld', 'Julius-Raab-Straße 11'),
                ('DG-Ausbau', '1010', 'Wien', 'Stubenring 22'),
                ('Manner Shop', '1010', 'Wien', 'Stephansplatz 7'),
                ('iSi Automotive Austria GmbH', '1210', 'Wien', 'Scheydgasse 30-32'),
                ('Wohnhausanlage samt Solar/Heizung', '1210', 'Wien', 'Donaufelderstraße 91'),
                ('Wohnhausanlage Vöslauerstraße 74', '2500', 'Baden', 'Vöslauerstraße 74'),
                ('Sanierung eines Privathauses', '5084', 'Großgmain', 'Großgmain 487'),
                ('Bankfilialen (Raiffeisenbank)', 'Österreich', 'Österreich', 'Österreich'),
                ('Hotel König von Ungarn GmbH', '1010', 'Wien', 'Schulerstraße 10'),
                ('Meininger Hotel Wien', '1020', 'Wien', 'Rembrandtstraße 21'),
                ('Hotel Landhaus Moserhof GmbH', '2352', 'Gumpodslkirchen', 'Wienerstraße 53'),
                ('Electronic Partner Austria GmbH', '2351', 'Wiener Neudorf', 'Industriezentrum NÖ-SÜD'),
                ('Privatstiftung zur Unterstützung und Bildung von Arbeitnehmer/Innen', '1060', 'Wien', 'Kaunitzgasse 2/8'),
                ('Brix Zaun + Tor GmbH', '7201', 'Neudörfl', 'Fabriksgelände'),
                ('Diverse Ordinationen und Apotheken', 'Wien und Niederösterreich', 'Wien und Niederösterreich', 'Wien und Niederösterreich');
            """)
        addVersion(0.3, 'Kunden implementiert')
        
    if lastVersionId["max"] < 0.4:
        with get_db_cursor() as cursor:
            cursor.execute("""
                DROP TYPE IF EXISTS rolesENUM;
                CREATE TYPE rolesENUM AS enum('ADMIN');
                CREATE TABLE IF NOT EXISTS users(
                    username VARCHAR(255) UNIQUE NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    role rolesENUM,
                    PRIMARY KEY (username)
                );
                INSERT INTO users (username, password, role)
                VALUES ('admin', '$2a$10$EuMetZvSiZfX.TI33ohhhuqvld6WLby2LXqDIKU37EvmNbXiNi9oK', 'ADMIN');
            """)
        addVersion(0.4, 'create users table')
    
    if lastVersionId["max"] < 0.5:
        with get_db_cursor() as cursor:
            cursor.execute("""
                INSERT INTO projekte (projektname, herzeigeprojekte, kunden_kundenname)
                VALUES 
                ('Austausch der Kältetechnischen Anlage in einer großen Schokoladenmanufaktur in der Wiener Innenstadt', true, 'Fleck Elektroinstallationen GmbH'),
                ('Eigenheim Sanierung samt Errichtung der haustechnischen anlagen in Salzburg', true, 'WEVIG Wohnungseigentumsverwaltungs- und Immobilientreuhand GmbH'),
                ('Errichtung der kältetechnischen Anlage für ein Bürogebäude am Wiener Neubaugürtel', true, 'WIEBE Wiener Bauträger- und EntwicklungsgesmbH'),
                ('Errichtung einer Solaranlage auf dem Dach einer Wohnhausanlage in Wien Donaustadt', true, 'Familienwohnbau gemeinnützige Bau- und Siedlungsgesellschaft m.b.H.'),
                ('Montage einer Fußbodenheizung in einer Wohnung in Simmering', true, 'Hottinger Bruel & Kjaer Austria GmbH'),
                ('Sanierung Zinshaus samt Dachgeschossausbau am Ring', true, 'Institut für medizinische u. chemische Labordiagnostik Gesellschaft m.b.H'),
                ('Neu Errichtung einer Wohnhausanlage mit 19 Wohneinheiten in Hernals', false, 'BHB Boutique Hotel Betriebs GmbH THE GUEST HOUSE VIENNA'),
                ('Sanierung von 5 Operationssälen im Militärkrankenhaus in Ulaanbaatar', false, 'Zentralverband der Hausbesitzer – Hausbesitzerhilfsverein'),
                ('Umbau der gasbetriebenen Heizhausanlage auf Fernwärmeversorgung einer Wohnhausanlage in Baden bei Wien', false, 'Hofer Richard GmbH'),
                ('Zubau am Bürogebäude der Firma Fleck', false, 'DG-Ausbau');
            """)
        addVersion(0.5, 'insert all the images')
    if lastVersionId["max"] < 0.6:
        with get_db_cursor() as cursor:
            cursor.execute("""
                INSERT INTO bilder (projektbilder, projekt_id)
                VALUES 
                ('1.jpg', 'Austausch der Kältetechnischen Anlage in einer großen Schokoladenmanufaktur in der Wiener Innenstadt'),
                ('2.jpg', 'Austausch der Kältetechnischen Anlage in einer großen Schokoladenmanufaktur in der Wiener Innenstadt'),
                ('3.jpg', 'Austausch der Kältetechnischen Anlage in einer großen Schokoladenmanufaktur in der Wiener Innenstadt'),
                ('4.jpg', 'Austausch der Kältetechnischen Anlage in einer großen Schokoladenmanufaktur in der Wiener Innenstadt'),
                ('5.jpg', 'Austausch der Kältetechnischen Anlage in einer großen Schokoladenmanufaktur in der Wiener Innenstadt'),
                ('6.jpg', 'Austausch der Kältetechnischen Anlage in einer großen Schokoladenmanufaktur in der Wiener Innenstadt'),
                ('7.jpg', 'Austausch der Kältetechnischen Anlage in einer großen Schokoladenmanufaktur in der Wiener Innenstadt'),
                ('1.jpg', 'Eigenheim Sanierung samt Errichtung der haustechnischen anlagen in Salzburg'),
                ('2.jpg', 'Eigenheim Sanierung samt Errichtung der haustechnischen anlagen in Salzburg'),
                ('5.jpg', 'Eigenheim Sanierung samt Errichtung der haustechnischen anlagen in Salzburg'),
                ('6.jpg', 'Eigenheim Sanierung samt Errichtung der haustechnischen anlagen in Salzburg'),
                ('7.jpg', 'Eigenheim Sanierung samt Errichtung der haustechnischen anlagen in Salzburg'),
                ('8.jpg', 'Eigenheim Sanierung samt Errichtung der haustechnischen anlagen in Salzburg'),
                ('9.jpg', 'Eigenheim Sanierung samt Errichtung der haustechnischen anlagen in Salzburg'),
                ('10.jpg', 'Eigenheim Sanierung samt Errichtung der haustechnischen anlagen in Salzburg'),
                ('11.jpg', 'Eigenheim Sanierung samt Errichtung der haustechnischen anlagen in Salzburg'),
                ('12.jpg', 'Eigenheim Sanierung samt Errichtung der haustechnischen anlagen in Salzburg'),
                ('13.jpg', 'Eigenheim Sanierung samt Errichtung der haustechnischen anlagen in Salzburg'),
                ('14.jpg', 'Eigenheim Sanierung samt Errichtung der haustechnischen anlagen in Salzburg'),
                ('15.jpg', 'Eigenheim Sanierung samt Errichtung der haustechnischen anlagen in Salzburg'),
                ('2.jpg', 'Errichtung der kältetechnischen Anlage für ein Bürogebäude am Wiener Neubaugürtel'),
                ('4.jpg', 'Errichtung der kältetechnischen Anlage für ein Bürogebäude am Wiener Neubaugürtel'),
                ('6.jpg', 'Errichtung der kältetechnischen Anlage für ein Bürogebäude am Wiener Neubaugürtel'),
                ('7.jpg', 'Errichtung der kältetechnischen Anlage für ein Bürogebäude am Wiener Neubaugürtel'),
                ('8.jpg', 'Errichtung der kältetechnischen Anlage für ein Bürogebäude am Wiener Neubaugürtel'),
                ('9.jpg', 'Errichtung der kältetechnischen Anlage für ein Bürogebäude am Wiener Neubaugürtel'),
                ('10.jpg', 'Errichtung der kältetechnischen Anlage für ein Bürogebäude am Wiener Neubaugürtel'),
                ('11.jpg', 'Errichtung der kältetechnischen Anlage für ein Bürogebäude am Wiener Neubaugürtel'),
                ('12.jpg', 'Errichtung der kältetechnischen Anlage für ein Bürogebäude am Wiener Neubaugürtel'),
                ('13.jpg', 'Errichtung der kältetechnischen Anlage für ein Bürogebäude am Wiener Neubaugürtel'),
                ('14.jpg', 'Errichtung der kältetechnischen Anlage für ein Bürogebäude am Wiener Neubaugürtel'),
                ('15.jpg', 'Errichtung der kältetechnischen Anlage für ein Bürogebäude am Wiener Neubaugürtel'),
                ('1.jpg', 'Errichtung einer Solaranlage auf dem Dach einer Wohnhausanlage in Wien Donaustadt'),
                ('2.jpg', 'Errichtung einer Solaranlage auf dem Dach einer Wohnhausanlage in Wien Donaustadt'),
                ('3.jpg', 'Errichtung einer Solaranlage auf dem Dach einer Wohnhausanlage in Wien Donaustadt'),
                ('4.jpg', 'Errichtung einer Solaranlage auf dem Dach einer Wohnhausanlage in Wien Donaustadt'),
                ('5.jpg', 'Errichtung einer Solaranlage auf dem Dach einer Wohnhausanlage in Wien Donaustadt'),
                ('6.jpg', 'Errichtung einer Solaranlage auf dem Dach einer Wohnhausanlage in Wien Donaustadt'),
                ('1.jpg', 'Montage einer Fußbodenheizung in einer Wohnung in Simmering'),
                ('2.jpg', 'Montage einer Fußbodenheizung in einer Wohnung in Simmering'),
                ('3.jpg', 'Montage einer Fußbodenheizung in einer Wohnung in Simmering'),
                ('4.jpg', 'Montage einer Fußbodenheizung in einer Wohnung in Simmering'),
                ('5.jpg', 'Montage einer Fußbodenheizung in einer Wohnung in Simmering'),
                ('6.jpg', 'Montage einer Fußbodenheizung in einer Wohnung in Simmering'),
                ('7.jpg', 'Montage einer Fußbodenheizung in einer Wohnung in Simmering'),
                ('1.jpg', 'Sanierung Zinshaus samt Dachgeschossausbau am Ring'),
                ('2.jpg', 'Sanierung Zinshaus samt Dachgeschossausbau am Ring'),
                ('3.jpg', 'Sanierung Zinshaus samt Dachgeschossausbau am Ring'),
                ('4.jpg', 'Sanierung Zinshaus samt Dachgeschossausbau am Ring'),
                ('5.jpg', 'Sanierung Zinshaus samt Dachgeschossausbau am Ring'),
                ('6.jpg', 'Sanierung Zinshaus samt Dachgeschossausbau am Ring'),
                ('7.jpg', 'Sanierung Zinshaus samt Dachgeschossausbau am Ring'),
                ('8.jpg', 'Sanierung Zinshaus samt Dachgeschossausbau am Ring'),
                ('9.jpg', 'Sanierung Zinshaus samt Dachgeschossausbau am Ring'),
                ('1.jpg', 'Neu Errichtung einer Wohnhausanlage mit 19 Wohneinheiten in Hernals'),
                ('2.jpg', 'Neu Errichtung einer Wohnhausanlage mit 19 Wohneinheiten in Hernals'),
                ('3.jpg', 'Neu Errichtung einer Wohnhausanlage mit 19 Wohneinheiten in Hernals'),
                ('4.jpg', 'Neu Errichtung einer Wohnhausanlage mit 19 Wohneinheiten in Hernals'),
                ('5.jpg', 'Neu Errichtung einer Wohnhausanlage mit 19 Wohneinheiten in Hernals'),
                ('1.jpg', 'Sanierung von 5 Operationssälen im Militärkrankenhaus in Ulaanbaatar'),
                ('2.jpg', 'Sanierung von 5 Operationssälen im Militärkrankenhaus in Ulaanbaatar'),
                ('3.jpg', 'Sanierung von 5 Operationssälen im Militärkrankenhaus in Ulaanbaatar'),
                ('4.jpg', 'Sanierung von 5 Operationssälen im Militärkrankenhaus in Ulaanbaatar'),
                ('1.jpg', 'Umbau der gasbetriebenen Heizhausanlage auf Fernwärmeversorgung einer Wohnhausanlage in Baden bei Wien'),
                ('2.jpg', 'Umbau der gasbetriebenen Heizhausanlage auf Fernwärmeversorgung einer Wohnhausanlage in Baden bei Wien'),
                ('1.jpg', 'Zubau am Bürogebäude der Firma Fleck'),
                ('2.jpg', 'Zubau am Bürogebäude der Firma Fleck');
            """)
        addVersion(0.6, 'insert all the images')
    
    if lastVersionId["max"] < 0.7:
        with get_db_cursor() as cursor:
            cursor.execute("""
                ALTER TABLE projekte
                ADD manuellerPost BOOLEAN DEFAULT false;
            """)
        addVersion(0.7, 'check if the project was created manually(true) or with postgres(false)')
        
    if lastVersionId["max"] < 0.8:
        with get_db_cursor() as cursor:
            cursor.execute("""
                ALTER TABLE users
                ADD instagram_AT VARCHAR(255) DEFAULT 'IGQVJYblMzSVB5RjZAXUWVRUkZAhU0ZAtNUNVVGIzS2NIc3FiQ3VTOVgwY2E5YThuRkZAMZAHJBTUhmc1RFWFJ3c09acjViS1Vwc0RCS1NaQXEwMTdWQkM5U0FWSTBWbUZADTWptYlJYbmNB';
            """)
        addVersion(0.8, 'add instagram access token column')
        
    if lastVersionId['max'] < 0.9:
        with get_db_cursor() as cursor:
            cursor.execute("""
                SET standard_conforming_strings = on;
                
                ALTER TABLE infos
                ADD ankuendigung VARCHAR(65535) NOT NULL DEFAULT 'Unser Betrieb ist über die Weihnachtsfeiertage vom 24.12.2021 bis inkl. 09.01.2022 geschlossen. Wir wünschen frohe Weihnachten und einen guten Rutsch ins neue Jahr!'              
            """)
        addVersion(0.9, "add the table Ankündigung")
    
    if lastVersionId['max'] < 1.0:
        with get_db_cursor() as cursor:
            cursor.execute("""
                ALTER TABLE infos
                ADD SwitchAnkuendigung BOOLEAN NOT NULL DEFAULT false;
            """)
        addVersion(1.0, "add Ankündigung an/aus")
        
    if lastVersionId['max'] < 1.1:
        with get_db_cursor() as cursor:
            cursor.execute("""
                ALTER TABLE infos
                ADD ankuendigung_image VARCHAR(65535) NOT NULL DEFAULT 'bg-picture-4.5.jpg',
                ADD ueberuns_image VARCHAR(65535) NOT NULL DEFAULT 'parallax-5.jpg',
                ADD team_image VARCHAR(65535) NOT NULL DEFAULT 'parallax-2.jpg',
                ADD projekte_image VARCHAR(65535) NOT NULL DEFAULT 'parallax-6.jpg';
            """)
        addVersion(1.1, "add images to the infos")
        
    if lastVersionId['max'] < 1.2:
        with get_db_cursor() as cursor:
            cursor.execute("""
                ALTER TABLE projekte
                DROP CONSTRAINT projekte_kunden_kundenname_fkey,
                DROP COLUMN kunden_kundenname;
                
                DROP TABLE kunden;
            """)
        addVersion(1.2, "delete Kundenname")
        
    if lastVersionId['max'] < 1.3:
        with get_db_cursor() as cursor:
            cursor.execute("""
                ALTER TABLE projekte
                DROP COLUMN manuellerpost;
            """)
        addVersion(1.3, "delete manueller Post, because we actually dont need it")
        
    if lastVersionId["max"] < 1.4:
        with get_db_cursor() as cursor:
            cursor.execute("""
                ALTER TABLE projekte
                ADD manuellerPost BOOLEAN DEFAULT false;
            """)
        addVersion(1.4, 'if brauche doch den manuellen Post')
        
    if lastVersionId["max"] < 1.5:
        with get_db_cursor() as cursor:
            cursor.execute("""
                ALTER TABLE bilder
                DROP CONSTRAINT bilder_projekt_id_fkey,
                ADD CONSTRAINT bilder_projekt_id_fkey
                FOREIGN KEY (projekt_id) REFERENCES projekte(projektname) ON DELETE CASCADE ON UPDATE CASCADE
            """)
        addVersion(1.5, 'foreign key ändern, damit er geupdatet wird, wenn sich der Name des Projekts ändert')
        
    if lastVersionId["max"] < 1.6:
        with get_db_cursor() as cursor:
            cursor.execute("""
                ALTER TABLE projekte
                ADD COLUMN foldername SERIAL
                
            """)
        addVersion(1.6, 'foldername is stored, auto increment value')
        
    if lastVersionId['max'] < 1.7:
        with get_db_cursor() as cursor:
            cursor.execute("""
                ALTER TABLE projekte
                DROP COLUMN manuellerpost;
            """)
        addVersion(1.7, "delete manueller Post, because we actually dont need it")

    if lastVersionId['max'] < 1.8:
        with get_db_cursor() as cursor:
            cursor.execute("""
                UPDATE projekte SET foldername = 1 WHERE projektname = 'Errichtung der kältetechnischen Anlage für ein Bürogebäude am Wiener Neubaugürtel';
                UPDATE projekte SET foldername = 2 WHERE projektname = 'Errichtung einer Solaranlage auf dem Dach einer Wohnhausanlage in Wien Donaustad';
                UPDATE projekte SET foldername = 3 WHERE projektname = 'Montage einer Fußbodenheizung in einer Wohnung in Simmering';
                UPDATE projekte SET foldername = 4 WHERE projektname = 'Sanierung Zinshaus samt Dachgeschossausbau am Ring';
                UPDATE projekte SET foldername = 5 WHERE projektname = 'Neu Errichtung einer Wohnhausanlage mit 19 Wohneinheiten in Hernals';
                UPDATE projekte SET foldername = 6 WHERE projektname = 'Sanierung von 5 Operationssälen im Militärkrankenhaus in Ulaanbaatar';
                UPDATE projekte SET foldername = 7 WHERE projektname = 'Umbau der gasbetriebenen Heizhausanlage auf Fernwärmeversorgung einer Wohnhausanlage in Baden bei Wien';
                UPDATE projekte SET foldername = 8 WHERE projektname = 'Zubau am Bürogebäude der Firma Fleck';
                UPDATE projekte SET foldername = 9 WHERE projektname = 'Austausch der Kältetechnischen Anlage in einer großen Schokoladenmanufaktur in der Wiener Innenstadt';
                UPDATE projekte SET foldername = 11 WHERE projektname = 'Eigenheim Sanierung samt Errichtung der haustechnischen anlagen in Salzburg';
            """)
        addVersion(1.8, "give specific foldername")

    if lastVersionId['max'] < 1.9:
        with get_db_cursor() as cursor:
            cursor.execute("""

                ALTER TABLE projekte
                DROP COLUMN foldername;

                ALTER TABLE projekte
                ADD COLUMN foldername INT UNIQUE NULL;

                UPDATE projekte SET foldername = 1 WHERE projektname = 'Errichtung der kältetechnischen Anlage für ein Bürogebäude am Wiener Neubaugürtel';
                UPDATE projekte SET foldername = 2 WHERE projektname = 'Errichtung einer Solaranlage auf dem Dach einer Wohnhausanlage in Wien Donaustadt';
                UPDATE projekte SET foldername = 3 WHERE projektname = 'Montage einer Fußbodenheizung in einer Wohnung in Simmering';
                UPDATE projekte SET foldername = 4 WHERE projektname = 'Sanierung Zinshaus samt Dachgeschossausbau am Ring';
                UPDATE projekte SET foldername = 5 WHERE projektname = 'Neu Errichtung einer Wohnhausanlage mit 19 Wohneinheiten in Hernals';
                UPDATE projekte SET foldername = 6 WHERE projektname = 'Sanierung von 5 Operationssälen im Militärkrankenhaus in Ulaanbaatar';
                UPDATE projekte SET foldername = 7 WHERE projektname = 'Umbau der gasbetriebenen Heizhausanlage auf Fernwärmeversorgung einer Wohnhausanlage in Baden bei Wien';
                UPDATE projekte SET foldername = 8 WHERE projektname = 'Zubau am Bürogebäude der Firma Fleck';
                UPDATE projekte SET foldername = 9 WHERE projektname = 'Austausch der Kältetechnischen Anlage in einer großen Schokoladenmanufaktur in der Wiener Innenstadt';
                UPDATE projekte SET foldername = 11 WHERE projektname = 'Eigenheim Sanierung samt Errichtung der haustechnischen anlagen in Salzburg';

            """)
        addVersion(1.9, "fix bug")      