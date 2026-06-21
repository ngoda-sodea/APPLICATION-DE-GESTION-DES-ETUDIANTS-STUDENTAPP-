# nom de l'application : studentApp
import os

# ========== DÉFINITION DES CLASSES ==========

class Etudiant:
    """Classe représentant un étudiant"""
    def __init__(self, id_etudiant, nom, prenom, date_naissance, niveau, filiere, groupe_td="", groupe_tp=""):
        self.id_etudiant = id_etudiant
        self.nom = nom
        self.prenom = prenom
        self.date_naissance = date_naissance
        self.niveau = niveau
        self.filiere = filiere
        self.groupe_td = groupe_td
        self.groupe_tp = groupe_tp
    
    def afficher(self):
        """Affiche les informations de l'étudiant"""
        return f"ID:{self.id_etudiant} | {self.nom} {self.prenom} | {self.niveau} - {self.filiere} | TD:{self.groupe_td} TP:{self.groupe_tp}"


class Matiere:
    """Classe représentant une matière / UE"""
    def __init__(self, id_matiere, intitule, credits, semestre):
        self.id_matiere = id_matiere
        self.intitule = intitule
        self.credits = credits
        self.semestre = semestre
        self.enseignants = []  # Liste des enseignants pour cette matière
    
    def ajouter_enseignant(self, enseignant):
        """Ajoute un enseignant à la matière"""
        self.enseignants.append(enseignant)
    
    def afficher(self):
        """Affiche les informations de la matière"""
        enseignants_noms = ", ".join([f"{e.prenom} {e.nom}" for e in self.enseignants]) if self.enseignants else "Aucun"
        return f"{self.id_matiere} | {self.intitule} | Crédits:{self.credits} | S{self.semestre} | Enseignants: {enseignants_noms}"


class Enseignant:
    """Classe représentant un enseignant"""
    def __init__(self, id_enseignant, nom, prenom, departement):
        self.id_enseignant = id_enseignant
        self.nom = nom
        self.prenom = prenom
        self.departement = departement
    
    def afficher(self):
        return f"ID:{self.id_enseignant} | {self.prenom} {self.nom} ({self.departement})"


class Note:
    """Classe représentant une note obtenue par un étudiant dans une matière"""
    def __init__(self, id_etudiant, id_matiere, valeur, session="normale"):
        self.id_etudiant = id_etudiant
        self.id_matiere = id_matiere
        self.valeur = valeur
        self.session = session


# ========== CLASSE PRINCIPALE DE GESTION ==========

class GestionEtudiants:
    """Système de gestion des étudiants"""
    
    def __init__(self):
        self.etudiants = []      # Liste des étudiants
        self.matieres = []       # Liste des matières
        self.enseignants = []    # Liste des enseignants
        self.notes = []          # Liste des notes
        self.next_id_etudiant = 1
        self.next_id_enseignant = 1
        self.next_id_matiere = 1
    
    # ========== GESTION DES ÉTUDIANTS ==========
    
    def ajouter_etudiant(self):
        """Ajoute un nouvel étudiant avec saisie utilisateur"""
        print("\n--- AJOUT D'UN ÉTUDIANT ---")
        nom = input("Nom : ").strip().upper()
        prenom = input("Prénom : ").strip().capitalize()
        date_naissance = input("Date de naissance (JJ/MM/AAAA) : ")
        niveau = input("Niveau (L1, L2, L3, M1, M2) : ").strip().upper()
        filiere = input("Filière (Informatique, Maths, etc.) : ").strip().capitalize()
        groupe_td = input("Groupe TD (ex: TD1, laisser vide si non défini) : ").strip().upper()
        groupe_tp = input("Groupe TP (ex: TP-A, laisser vide si non défini) : ").strip().upper()
        
        etudiant = Etudiant(
            self.next_id_etudiant, nom, prenom, date_naissance,
            niveau, filiere, groupe_td, groupe_tp
        )
        self.etudiants.append(etudiant)
        print(f"\n✓ Étudiant ajouté avec succès ! ID attribué : {self.next_id_etudiant}")
        self.next_id_etudiant += 1
        input("\nAppuyez sur Entrée pour continuer...")
    
    def lister_etudiants(self):
        """Affiche la liste de tous les étudiants"""
        if not self.etudiants:
            print("\n⚠ Aucun étudiant enregistré.")
            return
        
        print("\n" + "="*90)
        print("LISTE DES ÉTUDIANTS")
        print("="*90)
        print(f"{'ID':<5} {'NOM':<15} {'PRENOM':<15} {'NIVEAU':<8} {'FILIERE':<20} {'TD':<6} {'TP':<6}")
        print("-"*90)
        for e in self.etudiants:
            print(f"{e.id_etudiant:<5} {e.nom:<15} {e.prenom:<15} {e.niveau:<8} {e.filiere:<20} {e.groupe_td:<6} {e.groupe_tp:<6}")
        print("="*90)
        input("\nAppuyez sur Entrée pour continuer...")
    
    def rechercher_etudiant(self, id_etudiant=None, nom=None):
        """Recherche un étudiant par ID ou par nom"""
        if id_etudiant:
            for e in self.etudiants:
                if e.id_etudiant == id_etudiant:
                    return e
        if nom:
            resultats = [e for e in self.etudiants if nom.upper() in e.nom or nom.lower() in e.prenom.lower()]
            return resultats
        return None
    
    def modifier_etudiant(self):
        """Modifie les informations d'un étudiant existant"""
        if not self.etudiants:
            print("\n⚠ Aucun étudiant à modifier.")
            return
        
        self.lister_etudiants()
        try:
            id_modif = int(input("\nEntrez l'ID de l'étudiant à modifier : "))
            etudiant = self.rechercher_etudiant(id_etudiant=id_modif)
            
            if not etudiant:
                print("\n❌ Étudiant non trouvé !")
                input("Appuyez sur Entrée pour continuer...")
                return
            
            print(f"\nModification de : {etudiant.nom} {etudiant.prenom}")
            print("Laissez vide pour conserver la valeur actuelle.\n")
            
            nouveau_nom = input(f"Nom [{etudiant.nom}] : ").strip().upper()
            if nouveau_nom:
                etudiant.nom = nouveau_nom
            
            nouveau_prenom = input(f"Prénom [{etudiant.prenom}] : ").strip().capitalize()
            if nouveau_prenom:
                etudiant.prenom = nouveau_prenom
            
            nouvelle_date = input(f"Date de naissance [{etudiant.date_naissance}] : ")
            if nouvelle_date:
                etudiant.date_naissance = nouvelle_date
            
            nouveau_niveau = input(f"Niveau [{etudiant.niveau}] : ").strip().upper()
            if nouveau_niveau:
                etudiant.niveau = nouveau_niveau
            
            nouvelle_filiere = input(f"Filière [{etudiant.filiere}] : ").strip().capitalize()
            if nouvelle_filiere:
                etudiant.filiere = nouvelle_filiere
            
            nouveau_td = input(f"Groupe TD [{etudiant.groupe_td}] : ").strip().upper()
            if nouveau_td:
                etudiant.groupe_td = nouveau_td
            
            nouveau_tp = input(f"Groupe TP [{etudiant.groupe_tp}] : ").strip().upper()
            if nouveau_tp:
                etudiant.groupe_tp = nouveau_tp
            
            print("\n✓ Informations mises à jour avec succès !")
            
        except ValueError:
            print("\n❌ ID invalide !")
        
        input("\nAppuyez sur Entrée pour continuer...")
    
    def supprimer_etudiant(self):
        """Supprime un étudiant"""
        if not self.etudiants:
            print("\n⚠ Aucun étudiant à supprimer.")
            return
        
        self.lister_etudiants()
        try:
            id_suppr = int(input("\nEntrez l'ID de l'étudiant à supprimer : "))
            etudiant = self.rechercher_etudiant(id_etudiant=id_suppr)
            
            if etudiant:
                confirmation = input(f"\nConfirmez-vous la suppression de {etudiant.nom} {etudiant.prenom} ? (o/N) : ")
                if confirmation.lower() == 'o':
                    self.etudiants = [e for e in self.etudiants if e.id_etudiant != id_suppr]
                    # Supprimer aussi ses notes
                    self.notes = [n for n in self.notes if n.id_etudiant != id_suppr]
                    print("\n✓ Étudiant supprimé avec succès !")
                else:
                    print("\n❌ Suppression annulée.")
            else:
                print("\n❌ Étudiant non trouvé !")
        except ValueError:
            print("\n❌ ID invalide !")
        
        input("\nAppuyez sur Entrée pour continuer...")
    
    # ========== GESTION DES MATIÈRES ==========
    
    def creer_matiere(self):
        """Crée une nouvelle matière"""
        print("\n--- CRÉATION D'UNE MATIÈRE ---")
        intitule = input("Intitulé de la matière : ").strip().capitalize()
        
        try:
            credits = int(input("Nombre de crédits ECTS : "))
            semestre = int(input("Semestre (1, 2, 3, 4, 5, 6) : "))
            
            id_matiere = f"UE{self.next_id_matiere:03d}"
            matiere = Matiere(id_matiere, intitule, credits, semestre)
            
            # Ajout des enseignants
            print("\n--- AJOUT DES ENSEIGNANTS POUR CETTE MATIÈRE ---")
            while True:
                print("\n1. Ajouter un enseignant existant")
                print("2. Créer un nouvel enseignant")
                print("3. Terminer l'ajout des enseignants")
                choix = input("Votre choix : ")
                
                if choix == '1':
                    self.lister_enseignants()
                    try:
                        id_ens = int(input("ID de l'enseignant : "))
                        enseignant = self.rechercher_enseignant(id_ens)
                        if enseignant:
                            matiere.ajouter_enseignant(enseignant)
                            print(f"✓ {enseignant.prenom} {enseignant.nom} ajouté à la matière")
                        else:
                            print("❌ Enseignant non trouvé")
                    except ValueError:
                        print("❌ ID invalide")
                
                elif choix == '2':
                    self.ajouter_enseignant(matiere)
                
                elif choix == '3':
                    break
                
                else:
                    print("❌ Choix invalide")
            
            self.matieres.append(matiere)
            self.next_id_matiere += 1
            print(f"\n✓ Matière '{intitule}' créée avec succès ! ID: {id_matiere}")
            
        except ValueError:
            print("\n❌ Erreur : Veuillez entrer des nombres valides pour les crédits et le semestre.")
        
        input("\nAppuyez sur Entrée pour continuer...")
    
    def lister_matieres(self):
        """Affiche la liste des matières"""
        if not self.matieres:
            print("\n⚠ Aucune matière enregistrée.")
            return
        
        print("\n" + "="*90)
        print("LISTE DES MATIÈRES")
        print("="*90)
        for m in self.matieres:
            print(m.afficher())
        print("="*90)
        input("\nAppuyez sur Entrée pour continuer...")
    
    def rechercher_matiere(self, id_matiere):
        """Recherche une matière par son ID"""
        for m in self.matieres:
            if m.id_matiere == id_matiere:
                return m
        return None
    
    # ========== GESTION DES ENSEIGNANTS ==========
    
    def ajouter_enseignant(self, matiere=None):
        """Ajoute un nouvel enseignant (optionnellement lié à une matière)"""
        print("\n--- AJOUT D'UN ENSEIGNANT ---")
        nom = input("Nom : ").strip().upper()
        prenom = input("Prénom : ").strip().capitalize()
        departement = input("Département : ").strip().capitalize()
        
        enseignant = Enseignant(self.next_id_enseignant, nom, prenom, departement)
        self.enseignants.append(enseignant)
        
        if matiere:
            matiere.ajouter_enseignant(enseignant)
            print(f"✓ Enseignant {prenom} {nom} ajouté à la matière {matiere.intitule}")
        else:
            print(f"✓ Enseignant ajouté avec succès ! ID: {self.next_id_enseignant}")
        
        self.next_id_enseignant += 1
        return enseignant
    
    def ajouter_enseignant_libre(self):
        """Ajoute un enseignant sans l'associer à une matière immédiatement"""
        self.ajouter_enseignant()
        input("\nAppuyez sur Entrée pour continuer...")
    
    def lister_enseignants(self):
        """Affiche la liste des enseignants"""
        if not self.enseignants:
            print("\n⚠ Aucun enseignant enregistré.")
            return
        
        print("\n" + "="*70)
        print("LISTE DES ENSEIGNANTS")
        print("="*70)
        for e in self.enseignants:
            print(e.afficher())
        print("="*70)
    
    def rechercher_enseignant(self, id_enseignant):
        """Recherche un enseignant par son ID"""
        for e in self.enseignants:
            if e.id_enseignant == id_enseignant:
                return e
        return None
    
    def ajouter_enseignant_a_matiere(self):
        """Ajoute un enseignant existant à une matière"""
        if not self.matieres:
            print("\n⚠ Aucune matière disponible. Créez d'abord une matière.")
            return
        
        self.lister_matieres()
        id_matiere = input("\nEntrez l'ID de la matière : ").strip()
        matiere = self.rechercher_matiere(id_matiere)
        
        if not matiere:
            print("\n❌ Matière non trouvée !")
            input("Appuyez sur Entrée pour continuer...")
            return
        
        self.lister_enseignants()
        try:
            id_ens = int(input("\nEntrez l'ID de l'enseignant à ajouter : "))
            enseignant = self.rechercher_enseignant(id_ens)
            
            if enseignant:
                matiere.ajouter_enseignant(enseignant)
                print(f"\n✓ {enseignant.prenom} {enseignant.nom} ajouté à la matière {matiere.intitule}")
            else:
                print("\n❌ Enseignant non trouvé !")
        except ValueError:
            print("\n❌ ID invalide !")
        
        input("\nAppuyez sur Entrée pour continuer...")
    
    # ========== GESTION DES NOTES ==========
    
    def attribuer_note(self):
        """Attribue une note à un étudiant dans une matière"""
        if not self.etudiants:
            print("\n⚠ Aucun étudiant. Veuillez d'abord ajouter des étudiants.")
            return
        
        if not self.matieres:
            print("\n⚠ Aucune matière. Veuillez d'abord créer des matières.")
            return
        
        print("\n--- ATTRIBUTION D'UNE NOTE ---")
        
        # Sélection de l'étudiant
        self.lister_etudiants()
        try:
            id_etudiant = int(input("\nEntrez l'ID de l'étudiant : "))
            etudiant = self.rechercher_etudiant(id_etudiant=id_etudiant)
            
            if not etudiant:
                print("\n❌ Étudiant non trouvé !")
                input("Appuyez sur Entrée pour continuer...")
                return
            
            # Sélection de la matière
            print(f"\nAttribution d'une note pour : {etudiant.nom} {etudiant.prenom}")
            self.lister_matieres()
            id_matiere = input("\nEntrez l'ID de la matière : ").strip()
            matiere = self.rechercher_matiere(id_matiere)
            
            if not matiere:
                print("\n❌ Matière non trouvée !")
                input("Appuyez sur Entrée pour continuer...")
                return
            
            # Saisie de la note
            try:
                valeur = float(input(f"Note sur 20 pour {matiere.intitule} : "))
                if valeur < 0 or valeur > 20:
                    print("\n❌ La note doit être comprise entre 0 et 20 !")
                    input("Appuyez sur Entrée pour continuer...")
                    return
                
                session = input("Session (normale/rattrapage) [normale] : ").strip().lower()
                if session not in ["normale", "rattrapage"]:
                    session = "normale"
                
                # Vérifier si une note existe déjà
                note_existante = None
                for note in self.notes:
                    if note.id_etudiant == id_etudiant and note.id_matiere == id_matiere and note.session == session:
                        note_existante = note
                        break
                
                if note_existante:
                    confirmation = input(f"Une note existe déjà ({note_existante.valeur}/20). Voulez-vous la remplacer ? (o/N) : ")
                    if confirmation.lower() == 'o':
                        note_existante.valeur = valeur
                        print("\n✓ Note mise à jour avec succès !")
                    else:
                        print("\n❌ Modification annulée.")
                else:
                    nouvelle_note = Note(id_etudiant, id_matiere, valeur, session)
                    self.notes.append(nouvelle_note)
                    print("\n✓ Note attribuée avec succès !")
                
            except ValueError:
                print("\n❌ Note invalide !")
                
        except ValueError:
            print("\n❌ ID étudiant invalide !")
        
        input("\nAppuyez sur Entrée pour continuer...")
    
    def afficher_releve_etudiant(self):
        """Affiche le relevé de notes d'un étudiant"""
        if not self.etudiants:
            print("\n⚠ Aucun étudiant.")
            return
        
        self.lister_etudiants()
        try:
            id_etudiant = int(input("\nEntrez l'ID de l'étudiant : "))
            etudiant = self.rechercher_etudiant(id_etudiant=id_etudiant)
            
            if not etudiant:
                print("\n❌ Étudiant non trouvé !")
                input("Appuyez sur Entrée pour continuer...")
                return
            
            print("\n" + "="*80)
            print(f"RELEVÉ DE NOTES - {etudiant.nom} {etudiant.prenom}")
            print(f"Niveau: {etudiant.niveau} | Filière: {etudiant.filiere}")
            print("="*80)
            
            notes_etudiant = [n for n in self.notes if n.id_etudiant == id_etudiant]
            
            if not notes_etudiant:
                print("Aucune note enregistrée pour cet étudiant.")
            else:
                total_pondere = 0
                total_credits = 0
                
                for note in notes_etudiant:
                    matiere = self.rechercher_matiere(note.id_matiere)
                    if matiere:
                        print(f"{matiere.intitule} ({matiere.id_matiere}): {note.valeur}/20 (Crédits: {matiere.credits}) - Session: {note.session}")
                        total_pondere += note.valeur * matiere.credits
                        total_credits += matiere.credits
                
                if total_credits > 0:
                    moyenne = round(total_pondere / total_credits, 2)
                    print("-"*80)
                    print(f"MOYENNE GÉNÉRALE PONDÉRÉE: {moyenne}/20")
            
            print("="*80)
            
        except ValueError:
            print("\n❌ ID invalide !")
        
        input("\nAppuyez sur Entrée pour continuer...")
    
    def statistiques_generales(self):
        """Affiche des statistiques générales"""
        print("\n" + "="*80)
        print("STATISTIQUES GÉNÉRALES")
        print("="*80)
        print(f"📊 Nombre total d'étudiants : {len(self.etudiants)}")
        print(f"📚 Nombre total de matières : {len(self.matieres)}")
        print(f"👨‍🏫 Nombre total d'enseignants : {len(self.enseignants)}")
        print(f"📝 Nombre total de notes attribuées : {len(self.notes)}")
        
        # Calcul de la moyenne générale de tous les étudiants
        if self.etudiants and self.notes:
            print("\n--- MOYENNES PAR ÉTUDIANT ---")
            for etudiant in self.etudiants:
                notes_etudiant = [n for n in self.notes if n.id_etudiant == etudiant.id_etudiant]
                if notes_etudiant:
                    total = 0
                    credits_total = 0
                    for note in notes_etudiant:
                        matiere = self.rechercher_matiere(note.id_matiere)
                        if matiere:
                            total += note.valeur * matiere.credits
                            credits_total += matiere.credits
                    if credits_total > 0:
                        moyenne = round(total / credits_total, 2)
                        print(f"  {etudiant.nom} {etudiant.prenom}: {moyenne}/20")
        
        print("="*80)
        input("\nAppuyez sur Entrée pour continuer...")

    # Ajoutez ces méthodes à la classe GestionEtudiants

    # ========== GESTION DES FICHIERS CSV ==========
    
    def importer_etudiants_csv(self):
        """Importe une liste d'étudiants depuis un fichier CSV"""
        print("\n--- IMPORTATION D'ÉTUDIANTS DEPUIS UN FICHIER CSV ---")
        
        # Demander le nom du fichier
        nom_fichier = input("Nom du fichier CSV à importer (ex: etudiants.csv) : ").strip()
        
        if not os.path.exists(nom_fichier):
            print(f"\n❌ Le fichier '{nom_fichier}' n'existe pas !")
            input("\nAppuyez sur Entrée pour continuer...")
            return
        
        try:
            import csv
            compteur = 0
            erreurs = 0
            
            with open(nom_fichier, 'r', encoding='utf-8') as fichier:
                lecteur_csv = csv.reader(fichier)
                
                # Ignorer l'en-tête si présent
                premiere_ligne = next(lecteur_csv, None)
                if premiere_ligne and premiere_ligne[0].lower() in ['id', 'nom', 'prenom']:
                    print("✓ En-tête détecté et ignoré")
                
                # Parcourir les lignes du fichier
                for ligne in lecteur_csv:
                    try:
                        # Format attendu: nom, prenom, date_naissance, niveau, filiere, groupe_td, groupe_tp
                        if len(ligne) >= 5:
                            nom = ligne[0].strip().upper() if ligne[0] else ""
                            prenom = ligne[1].strip().capitalize() if len(ligne) > 1 else ""
                            date_naissance = ligne[2].strip() if len(ligne) > 2 else "01/01/2000"
                            niveau = ligne[3].strip().upper() if len(ligne) > 3 else "L1"
                            filiere = ligne[4].strip().capitalize() if len(ligne) > 4 else "Informatique"
                            groupe_td = ligne[5].strip().upper() if len(ligne) > 5 else ""
                            groupe_tp = ligne[6].strip().upper() if len(ligne) > 6 else ""
                            
                            # Créer l'étudiant
                            etudiant = Etudiant(
                                self.next_id_etudiant, nom, prenom, date_naissance,
                                niveau, filiere, groupe_td, groupe_tp
                            )
                            self.etudiants.append(etudiant)
                            self.next_id_etudiant += 1
                            compteur += 1
                            print(f"✓ Importé: {nom} {prenom}")
                        else:
                            erreurs += 1
                            print(f"⚠ Ligne ignorée (format incorrect): {ligne}")
                    except Exception as e:
                        erreurs += 1
                        print(f"⚠ Erreur lors de l'import d'une ligne: {e}")
            
            print(f"\n{'='*50}")
            print(f"📊 RÉSUMÉ DE L'IMPORTATION")
            print(f"{'='*50}")
            print(f"✓ Étudiants importés avec succès: {compteur}")
            if erreurs > 0:
                print(f"⚠ Lignes ignorées/erreurs: {erreurs}")
            print(f"📚 Nombre total d'étudiants maintenant: {len(self.etudiants)}")
            
        except Exception as e:
            print(f"\n❌ Erreur lors de la lecture du fichier: {e}")
        
        input("\nAppuyez sur Entrée pour continuer...")
    
    def exporter_etudiants_csv(self):
        """Exporte la liste des étudiants vers un fichier CSV"""
        if not self.etudiants:
            print("\n⚠ Aucun étudiant à exporter !")
            input("\nAppuyez sur Entrée pour continuer...")
            return
        
        print("\n--- EXPORTATION DES ÉTUDIANTS VERS UN FICHIER CSV ---")
        
        # Proposer un nom de fichier par défaut
        nom_defaut = f"etudiants_export_{len(self.etudiants)}_eleves.csv"
        nom_fichier = input(f"Nom du fichier CSV (Enter pour '{nom_defaut}') : ").strip()
        
        if not nom_fichier:
            nom_fichier = nom_defaut
        
        if not nom_fichier.endswith('.csv'):
            nom_fichier += '.csv'
        
        try:
            import csv
            
            with open(nom_fichier, 'w', newline='', encoding='utf-8') as fichier:
                # Écrire l'en-tête
                entetes = ['ID', 'NOM', 'PRENOM', 'DATE_NAISSANCE', 'NIVEAU', 'FILIERE', 'GROUPE_TD', 'GROUPE_TP']
                writer = csv.writer(fichier)
                writer.writerow(entetes)
                
                # Écrire les données des étudiants
                for etudiant in self.etudiants:
                    writer.writerow([
                        etudiant.id_etudiant,
                        etudiant.nom,
                        etudiant.prenom,
                        etudiant.date_naissance,
                        etudiant.niveau,
                        etudiant.filiere,
                        etudiant.groupe_td,
                        etudiant.groupe_tp
                    ])
            
            print(f"\n✓ Exportation réussie !")
            print(f"📁 Fichier créé: {nom_fichier}")
            print(f"📊 Nombre d'étudiants exportés: {len(self.etudiants)}")
            
            # Option pour exporter aussi les notes
            if self.notes:
                print("\n--- OPTION D'EXPORTATION SUPPLÉMENTAIRE ---")
                exporter_notes = input("Voulez-vous aussi exporter les notes ? (o/N) : ").strip().lower()
                
                if exporter_notes == 'o':
                    self.exporter_notes_csv()
            
        except Exception as e:
            print(f"\n❌ Erreur lors de l'exportation: {e}")
        
        input("\nAppuyez sur Entrée pour continuer...")
    
    def exporter_notes_csv(self):
        """Exporte les notes vers un fichier CSV séparé"""
        if not self.notes:
            print("⚠ Aucune note à exporter")
            return
        
        nom_fichier = f"notes_export_{len(self.notes)}_notes.csv"
        
        try:
            import csv
            
            with open(nom_fichier, 'w', newline='', encoding='utf-8') as fichier:
                entetes = ['ID_ETUDIANT', 'NOM_ETUDIANT', 'PRENOM_ETUDIANT', 'ID_MATIERE', 'MATIERE', 'NOTE', 'SESSION']
                writer = csv.writer(fichier)
                writer.writerow(entetes)
                
                for note in self.notes:
                    # Récupérer les infos de l'étudiant
                    etudiant = self.rechercher_etudiant(id_etudiant=note.id_etudiant)
                    nom_etudiant = etudiant.nom if etudiant else "Inconnu"
                    prenom_etudiant = etudiant.prenom if etudiant else "Inconnu"
                    
                    # Récupérer les infos de la matière
                    matiere = self.rechercher_matiere(note.id_matiere)
                    nom_matiere = matiere.intitule if matiere else "Inconnue"
                    
                    writer.writerow([
                        note.id_etudiant, nom_etudiant, prenom_etudiant,
                        note.id_matiere, nom_matiere, note.valeur, note.session
                    ])
            
            print(f"✓ Notes exportées avec succès vers {nom_fichier}")
            
        except Exception as e:
            print(f"❌ Erreur lors de l'exportation des notes: {e}")
    
    def vider_liste_etudiants(self):
        """Vide complètement la liste des étudiants (avec confirmation)"""
        if not self.etudiants:
            print("\n⚠ La liste des étudiants est déjà vide !")
            input("\nAppuyez sur Entrée pour continuer...")
            return
        
        print("\n--- VIDAGE DE LA LISTE DES ÉTUDIANTS ---")
        print(f"⚠ ATTENTION : Cette action va supprimer TOUS les {len(self.etudiants)} étudiants de la base.")
        print("   Les notes associées seront également supprimées.")
        
        # Demander confirmation multiple
        confirmation = input("\nTapez 'CONFIRMER' pour valider la suppression définitive : ").strip().upper()
        
        if confirmation == "CONFIRMER":
            # Compter avant suppression
            nb_etudiants = len(self.etudiants)
            nb_notes = len([n for n in self.notes if n.id_etudiant in [e.id_etudiant for e in self.etudiants]])
            
            # Vider les listes
            self.etudiants.clear()
            self.notes.clear()  # Supprime aussi toutes les notes
            
            # Réinitialiser l'ID counter (optionnel)
            reponse = input("Voulez-vous aussi réinitialiser le compteur d'ID ? (o/N) : ").strip().lower()
            if reponse == 'o':
                self.next_id_etudiant = 1
                print("✓ Compteur d'ID réinitialisé")
            
            print(f"\n{'='*50}")
            print(f"✓ VIDAGE EFFECTUÉ AVEC SUCCÈS !")
            print(f"{'='*50}")
            print(f"🗑️ Étudiants supprimés : {nb_etudiants}")
            print(f"🗑️ Notes supprimées : {nb_notes}")
            print(f"📚 Liste maintenant vide : {len(self.etudiants)} étudiant(s)")
        else:
            print("\n❌ Opération annulée. Aucune donnée n'a été supprimée.")
        
        input("\nAppuyez sur Entrée pour continuer...")
    
    def vider_liste_matieres(self):
        """Vide la liste des matières (optionnel)"""
        if not self.matieres:
            print("\n⚠ La liste des matières est déjà vide !")
            return
        
        print("\n--- VIDAGE DE LA LISTE DES MATIÈRES ---")
        print(f"⚠ ATTENTION : Cela va supprimer TOUTES les {len(self.matieres)} matières.")
        
        confirmation = input("Tapez 'CONFIRMER' pour valider : ").strip().upper()
        
        if confirmation == "CONFIRMER":
            nb_matieres = len(self.matieres)
            self.matieres.clear()
            print(f"\n✓ {nb_matieres} matière(s) supprimée(s)")
        else:
            print("❌ Opération annulée")
    
    def vider_toutes_listes(self):
        """Vide toutes les listes (étudiants, matières, enseignants, notes)"""
        print("\n--- VIDAGE COMPLET DU SYSTÈME ---")
        print("⚠ ATTENTION : Cela va supprimer TOUTES les données !")
        print(f"   - Étudiants: {len(self.etudiants)}")
        print(f"   - Matières: {len(self.matieres)}")
        print(f"   - Enseignants: {len(self.enseignants)}")
        print(f"   - Notes: {len(self.notes)}")
        
        confirmation = input("\nTapez 'VIDER_TOTAL' pour confirmer la suppression définitive : ").strip().upper()
        
        if confirmation == "VIDER_TOTAL":
            self.etudiants.clear()
            self.matieres.clear()
            self.enseignants.clear()
            self.notes.clear()
            self.next_id_etudiant = 1
            self.next_id_enseignant = 1
            self.next_id_matiere = 1
            
            print("\n" + "="*50)
            print("✓ SYSTÈME COMPLÈTEMENT VIDÉ !")
            print("="*50)
            print("Toutes les listes sont maintenant vides.")
        else:
            print("\n❌ Opération annulée")
# ========== INTERFACE UTILISATEUR ==========

def afficher_menu():
    """Affiche le menu principal"""
    print("\n" + "="*60)
    print("SYSTÈME DE GESTION DES ÉTUDIANTS")
    print("="*60)
    print("1.  Ajouter un étudiant")
    print("2.  Lister les étudiants")
    print("3.  Modifier un étudiant")
    print("4.  Supprimer un étudiant")
    print("-"*60)
    print("5.  Créer une matière")
    print("6.  Lister les matières")
    print("7.  Ajouter un enseignant (libre)")
    print("8.  Ajouter un enseignant à une matière")
    print("9.  Lister les enseignants")
    print("-"*60)
    print("10. Attribuer une note à un étudiant")
    print("11. Afficher le relevé de notes d'un étudiant")
    print("12. Statistiques générales")
    print("-"*60)
    print("13. importer une liste d'etudiants")
    
    print("14. exporter la liste ")

    print("15. vider la liste")
    print("0.  Quitter")
    print("="*60)
    

def main():
    """Fonction principale - Interface utilisateur"""
    
    gestion = GestionEtudiants()
    
    # Données de démonstration pour faciliter les tests
    print("\n📌 BONJOUR ET BIENVENUE DANS LE SYSTÈME DE GESTION DES ÉTUDIANTS")
    print("   Des données de démonstration ont été chargées pour vous permettre de tester.")
    
    # Création d'étudiants de démonstration
    demo_etudiants = [
        (1, "MARTIN", "Sophie", "15/03/2003", "L1", "Informatique", "TD1", "TP-A"),
        (2, "BERNARD", "Thomas", "22/07/2002", "L1", "Informatique", "TD1", "TP-B"),
        (3, "PETIT", "Emma", "10/11/2003", "L1", "Maths", "TD2", "TP-A"),
    ]
    for e in demo_etudiants:
        gestion.etudiants.append(Etudiant(*e))
        gestion.next_id_etudiant = 4
    
    # Création d'enseignants de démonstration
    demo_enseignants = [
        (1, "DUPONT", "Jean", "Informatique"),
        (2, "LEFEBVRE", "Marie", "Mathématiques"),
        (3, "MOREAU", "Pierre", "Informatique"),
    ]
    for ens in demo_enseignants:
        gestion.enseignants.append(Enseignant(*ens))
        gestion.next_id_enseignant = 4
    
    # Création de matières de démonstration
    matiere1 = Matiere("INF101", "Programmation Python", 6, 1)
    matiere1.ajouter_enseignant(gestion.enseignants[0])
    matiere1.ajouter_enseignant(gestion.enseignants[2])
    
    matiere2 = Matiere("INF102", "Bases de données", 6, 1)
    matiere2.ajouter_enseignant(gestion.enseignants[0])
    
    matiere3 = Matiere("MATH101", "Mathématiques discrètes", 4, 1)
    matiere3.ajouter_enseignant(gestion.enseignants[1])
    
    gestion.matieres.extend([matiere1, matiere2, matiere3])
    gestion.next_id_matiere = 4
    
    # Notes de démonstration
    demo_notes = [
        Note(1, "INF101", 15.5), Note(1, "INF102", 14.0), Note(1, "MATH101", 12.0),
        Note(2, "INF101", 12.0), Note(2, "INF102", 11.0), Note(2, "MATH101", 14.5),
        Note(3, "INF101", 18.0), Note(3, "INF102", 16.5), Note(3, "MATH101", 13.5),
    ]
    gestion.notes.extend(demo_notes)
    
    print("\n✓ Données de démonstration chargées :")
    print(f"  - {len(gestion.etudiants)} étudiants")
    print(f"  - {len(gestion.enseignants)} enseignants")
    print(f"  - {len(gestion.matieres)} matières")
    print(f"  - {len(gestion.notes)} notes")
    
    # Boucle principale
    
    while True:
        afficher_menu()
        choix = input("\nVotre choix : ")
        
        if choix == '1':
            gestion.ajouter_etudiant()
        elif choix == '2':
            gestion.lister_etudiants()
        elif choix == '3':
            gestion.modifier_etudiant()
        elif choix == '4':
            gestion.supprimer_etudiant()
        elif choix == '5':
            gestion.creer_matiere()
        elif choix == '6':
            gestion.lister_matieres()
        elif choix == '7':
            gestion.ajouter_enseignant_libre()
        elif choix == '8':
            gestion.ajouter_enseignant_a_matiere()
        elif choix == '9':
            gestion.lister_enseignants()
            input("\nAppuyez sur Entrée pour continuer...")
        elif choix == '10':
            gestion.attribuer_note()
        elif choix == '11':
            gestion.afficher_releve_etudiant()
        elif choix == '12':
            gestion.statistiques_generales()
        elif choix == '13':
            gestion.importer_etudiants_csv()  # NOUVEAU
        elif choix == '14':
            gestion.exporter_etudiants_csv()  # NOUVEAU
        elif choix == '15':
            gestion.vider_liste_etudiants()   # NOUVEAU
        elif choix == '0':
            print("\n👋 Au revoir !")
            break
        else:
            print("\n❌ Choix invalide. Veuillez réessayer.")
            input("Appuyez sur Entrée pour continuer...")



if __name__ == "__main__":
    main()
os.system("pause")