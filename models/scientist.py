from pymongo import MongoClient
from bson import ObjectId
import json
import os

# Connexion à MongoDB
# Utilisez une variable d'environnement pour l'URI de connexion ou une valeur par défaut
MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/')
DB_NAME = os.environ.get('DB_NAME', 'learnball')

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
scientists_collection = db.scientists


class Scientist:
    @staticmethod
    def get_all(category=None):
        """
        Récupère tous les scientifiques, éventuellement filtrés par catégorie.
        Retourne une version simplifiée sans quiz/exam/experiment.
        """
        query = {}
        if category and category != "tous":
            query["category"] = category

        # Projection pour exclure les champs détaillés
        projection = {
            "quiz": 0,
            "exam": 0,
            "experiment": 0
        }

        scientists = list(scientists_collection.find(query, projection))

        # Convertir ObjectId en string pour la sérialisation JSON
        for scientist in scientists:
            scientist["_id"] = str(scientist["_id"])

        return scientists

    @staticmethod
    def search_scientists(query):
        """
        Recherche des scientifiques par nom ou domaine.
        """
        search_query = {
            "$or": [
                {"name": {"$regex": query, "$options": "i"}},
                {"field": {"$regex": query, "$options": "i"}},
                {"category": {"$regex": query, "$options": "i"}}
            ]
        }

        # Projection pour exclure les champs détaillés
        projection = {
            "quiz": 0,
            "exam": 0,
            "experiment": 0
        }

        scientists = list(scientists_collection.find(search_query, projection))

        # Convertir ObjectId en string pour la sérialisation JSON
        for scientist in scientists:
            scientist["_id"] = str(scientist["_id"])

        return scientists

    @staticmethod
    def get_by_id(scientist_id):
        """
        Récupère les détails complets d'un scientifique par son ID.
        """
        try:
            scientist = scientists_collection.find_one({"_id": ObjectId(scientist_id)})
            if scientist:
                scientist["_id"] = str(scientist["_id"])
            return scientist
        except:
            return None

    @staticmethod
    def get_categories():
        """
        Récupère toutes les catégories disponibles avec le nombre de scientifiques.
        """
        pipeline = [
            {"$group": {"_id": "$category", "count": {"$sum": 1}}},
            {"$sort": {"_id": 1}}
        ]

        categories = list(scientists_collection.aggregate(pipeline))

        # Ajouter la catégorie "tous"
        total_count = scientists_collection.count_documents({})
        categories.insert(0, {"_id": "tous", "count": total_count})

        return categories

    @staticmethod
    def get_quiz(scientist_id):
        """
        Récupère uniquement les questions de quiz pour un scientifique.
        """
        try:
            scientist = scientists_collection.find_one(
                {"_id": ObjectId(scientist_id)},
                {"_id": 1, "name": 1, "quiz": 1}
            )
            if scientist:
                scientist["_id"] = str(scientist["_id"])
            return scientist
        except:
            return None

    @staticmethod
    def get_exam(scientist_id):
        """
        Récupère uniquement les informations d'examen pour un scientifique.
        """
        try:
            scientist = scientists_collection.find_one(
                {"_id": ObjectId(scientist_id)},
                {"_id": 1, "name": 1, "exam": 1}
            )
            if scientist:
                scientist["_id"] = str(scientist["_id"])
            return scientist
        except:
            return None

    @staticmethod
    def get_experiment(scientist_id):
        """
        Récupère uniquement les informations d'expérience pour un scientifique.
        """
        try:
            scientist = scientists_collection.find_one(
                {"_id": ObjectId(scientist_id)},
                {"_id": 1, "name": 1, "experiment": 1}
            )
            if scientist:
                scientist["_id"] = str(scientist["_id"])
            return scientist
        except:
            return None

    @staticmethod
    def initialize_db():
        """
        Initialise la base de données avec des données de test si elle est vide.
        """
        if scientists_collection.count_documents({}) == 3:
            # Base de données étendue avec 20 scientifiques
            scientists_data = [
                {
                    "name": "Albert Einstein",
                    "field": "Physique Théorique",
                    "category": "physique",
                    "years": "1879-1955",
                    "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3e/Einstein_1921_by_F_Schmutzer_-_restoration.jpg/220px-Einstein_1921_by_F_Schmutzer_-_restoration.jpg",
                    "description": "Physicien théorique allemand, développeur de la théorie de la relativité, l'une des deux piliers de la physique moderne avec la mécanique quantique.",
                    "discoveries": [
                        "Théorie de la relativité restreinte (1905)",
                        "Théorie de la relativité générale (1915)",
                        "Explication de l'effet photoélectrique (Prix Nobel 1921)",
                        "Équation masse-énergie E=mc²"
                    ],
                    "quiz": [
                        {
                            "question": "Quelle est la célèbre équation d'Einstein reliant masse et énergie ?",
                            "options": ["E=mc", "E=mc²", "E=m²c", "E=2mc"],
                            "answer": 1,
                            "explanation": "E=mc² est l'équation la plus célèbre d'Einstein, montrant l'équivalence masse-énergie."
                        },
                        {
                            "question": "En quelle année Einstein a-t-il publié la théorie de la relativité restreinte ?",
                            "options": ["1905", "1915", "1920", "1925"],
                            "answer": 0,
                            "explanation": "La théorie de la relativité restreinte a été publiée en 1905, dans l'annus mirabilis d'Einstein."
                        },
                        {
                            "question": "Pour quelle découverte Einstein a-t-il reçu le Prix Nobel de Physique en 1921 ?",
                            "options": ["Relativité", "Effet photoélectrique", "E=mc²", "Mouvement brownien"],
                            "answer": 1,
                            "explanation": "Einstein a reçu le Prix Nobel pour son explication de l'effet photoélectrique, et non pour sa théorie de la relativité."
                        },
                        {
                            "question": "Quelle théorie Einstein a-t-il publiée en 1915 ?",
                            "options": ["Théorie quantique", "Relativité restreinte", "Relativité générale", "Mécanique classique"],
                            "answer": 2,
                            "explanation": "Einstein a publié la théorie de la relativité générale en 1915, une extension de la relativité restreinte incluant la gravitation."
                        },
                        {
                            "question": "Quelle nationalité Einstein a-t-il obtenue après avoir quitté l'Allemagne nazie ?",
                            "options": ["Française", "Suisse", "Américaine", "Autrichienne"],
                            "answer": 2,
                            "explanation": "Einstein a quitté l'Allemagne en 1933 pour les États-Unis, où il a obtenu la nationalité américaine en 1940."
                        }
                    ],
                    "exam": {
                        "title": "Dilatation du temps et contraction des longueurs",
                        "problem": "Un vaisseau spatial se déplace à une vitesse v = 0,8c par rapport à la Terre. Une horloge à bord du vaisseau mesure un temps propre de 1 heure. Calculez le temps mesuré par un observateur sur Terre. De plus, le vaisseau a une longueur propre de 100 mètres. Quelle est sa longueur mesurée par l'observateur terrestre ?",
                        "solution": "Pour la dilatation du temps : Δt = Δt₀/√(1-v²/c²) = 1/√(1-(0,8)²) = 1/√(1-0,64) = 1/√0,36 = 1/0,6 = 1,67 heures.\\n\\nPour la contraction des longueurs : L = L₀√(1-v²/c²) = 100 × √(1-(0,8)²) = 100 × √0,36 = 100 × 0,6 = 60 mètres."
                    },
                    "experiment": {
                        "videoUrl": "https://www.youtube.com/embed/Xc4xYacTu-E",
                        "title": "Démonstration de l'équivalence masse-énergie",
                        "description": "Cette vidéo explique et démontre le concept d'équivalence masse-énergie d'Einstein.",
                        "context": "L'équation E=mc² est l'une des découvertes les plus importantes d'Einstein. Elle montre que la masse peut être convertie en énergie et vice versa. Cette équation a des implications profondes en physique nucléaire et en astrophysique.",
                        "keyPoints": [
                            "Observer comment l'énergie peut être convertie en masse",
                            "Comprendre les implications pour la physique nucléaire",
                            "Noter les applications pratiques comme l'énergie nucléaire"
                        ]
                    }
                },
                {
                    "name": "Marie Curie",
                    "field": "Physique et Chimie",
                    "category": "chimie",
                    "years": "1867-1934",
                    "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c8/Marie_Curie_c._1920s.jpg/220px-Marie_Curie_c._1920s.jpg",
                    "description": "Physicienne et chimiste polonaise naturalisée française, pionnière dans l'étude de la radioactivité. Elle est la première personne à avoir reçu deux prix Nobel dans des disciplines scientifiques différentes.",
                    "discoveries": [
                        "Découverte des éléments polonium et radium",
                        "Développement de la théorie de la radioactivité",
                        "Techniques pour isoler les isotopes radioactifs",
                        "Applications médicales des rayons X pendant la Première Guerre mondiale"
                    ],
                    "quiz": [
                        {
                            "question": "Quels éléments Marie Curie a-t-elle découverts ?",
                            "options": ["Uranium et thorium", "Polonium et radium", "Plutonium et américium", "Radon et actinium"],
                            "answer": 1,
                            "explanation": "Marie Curie a découvert le polonium (nommé d'après son pays natal) et le radium en 1898."
                        },
                        {
                            "question": "Dans quels domaines Marie Curie a-t-elle reçu des prix Nobel ?",
                            "options": ["Physique et chimie", "Chimie et médecine", "Physique et paix", "Chimie et littérature"],
                            "answer": 0,
                            "explanation": "Marie Curie a reçu le prix Nobel de physique en 1903 (partagé avec Pierre Curie et Henri Becquerel) et le prix Nobel de chimie en 1911."
                        },
                        {
                            "question": "Quel terme Marie Curie a-t-elle inventé pour décrire l'émission de rayons par certains éléments ?",
                            "options": ["Radioactivité", "Ionisation", "Fission", "Fusion"],
                            "answer": 0,
                            "explanation": "Marie Curie a inventé le terme 'radioactivité' pour décrire le phénomène d'émission de rayons par certains éléments."
                        },
                        {
                            "question": "Combien de fois Marie Curie a-t-elle reçu le prix Nobel ?",
                            "options": ["Une fois", "Deux fois", "Trois fois", "Jamais"],
                            "answer": 1,
                            "explanation": "Marie Curie est la seule personne à avoir reçu deux prix Nobel dans des disciplines scientifiques différentes."
                        },
                        {
                            "question": "Quelle unité de mesure de la radioactivité porte le nom de Marie Curie ?",
                            "options": ["Le becquerel", "Le curie", "Le roentgen", "Le gray"],
                            "answer": 1,
                            "explanation": "Le curie (Ci) est une unité de mesure de l'activité radioactive nommée en l'honneur de Marie Curie."
                        }
                    ],
                    "exam": {
                        "title": "Décroissance radioactive",
                        "problem": "Un échantillon de radium-226 a une demi-vie de 1600 ans. Si vous commencez avec 10 grammes de radium-226, quelle masse restera après 4800 ans ? Exprimez votre réponse en grammes et en pourcentage de la masse initiale.",
                        "solution": "Après 4800 ans, soit 3 demi-vies (4800/1600 = 3), la masse restante sera de 10 × (1/2)³ = 10 × 1/8 = 1,25 grammes, soit 12,5% de la masse initiale."
                    },
                    "experiment": {
                        "videoUrl": "https://www.youtube.com/embed/hMEXuQGLeh0",
                        "title": "Démonstration de la radioactivité",
                        "description": "Cette vidéo montre comment détecter la radioactivité et explique les travaux de Marie Curie.",
                        "context": "Marie Curie a passé des années à isoler des éléments radioactifs à partir de tonnes de pechblende, un minerai d'uranium. Son travail a jeté les bases de la radiochimie moderne.",
                        "keyPoints": [
                            "Observer le fonctionnement d'un compteur Geiger",
                            "Comprendre les différents types de rayonnement (alpha, bêta, gamma)",
                            "Noter les précautions de sécurité lors de la manipulation de matériaux radioactifs"
                        ]
                    }
                },
                {
                    "name": "Isaac Newton",
                    "field": "Physique et Mathématiques",
                    "category": "physique",
                    "years": "1643-1727",
                    "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/39/GodfreyKneller-IsaacNewton-1689.jpg/220px-GodfreyKneller-IsaacNewton-1689.jpg",
                    "description": "Physicien, mathématicien, astronome, philosophe et alchimiste anglais. Figure emblématique de la révolution scientifique du XVIIe siècle, il a établi les fondements de la mécanique classique.",
                    "discoveries": [
                        "Lois du mouvement et gravitation universelle",
                        "Développement du calcul infinitésimal",
                        "Théorie de la lumière et des couleurs",
                        "Télescope réflecteur newtonien"
                    ],
                    "quiz": [
                        {
                            "question": "Combien de lois du mouvement Newton a-t-il formulées ?",
                            "options": ["Deux", "Trois", "Quatre", "Cinq"],
                            "answer": 1,
                            "explanation": "Newton a formulé trois lois du mouvement qui sont à la base de la mécanique classique."
                        },
                        {
                            "question": "Quelle est la formule de la force gravitationnelle selon Newton ?",
                            "options": ["F = ma", "F = G(m₁m₂)/r²", "E = mc²", "F = kx"],
                            "answer": 1,
                            "explanation": "La loi de la gravitation universelle de Newton s'exprime par F = G(m₁m₂)/r², où G est la constante gravitationnelle."
                        },
                        {
                            "question": "Quel livre Newton a-t-il publié en 1687 ?",
                            "options": ["Opticks", "Principia Mathematica", "De Revolutionibus", "Dialogue"],
                            "answer": 1,
                            "explanation": "Les Principia Mathematica (1687) contiennent les lois du mouvement et la loi de la gravitation universelle."
                        },
                        {
                            "question": "Quelle découverte Newton a-t-il faite en décomposant la lumière blanche ?",
                            "options": ["Les couleurs du spectre", "Les ondes électromagnétiques", "La diffraction", "La polarisation"],
                            "answer": 0,
                            "explanation": "Newton a découvert que la lumière blanche est composée de toutes les couleurs du spectre visible."
                        },
                        {
                            "question": "Avec qui Newton a-t-il eu une controverse sur l'invention du calcul infinitésimal ?",
                            "options": ["Galilée", "Leibniz", "Descartes", "Euler"],
                            "answer": 1,
                            "explanation": "Newton et Leibniz ont développé indépendamment le calcul infinitésimal, ce qui a mené à une controverse sur la priorité."
                        }
                    ],
                    "exam": {
                        "title": "Application des lois de Newton",
                        "problem": "Un bloc de 2 kg est placé sur un plan incliné à 30° par rapport à l'horizontale. Le coefficient de frottement statique entre le bloc et le plan est μₛ = 0,3. Le bloc est-il en équilibre ou va-t-il glisser ? Calculez l'accélération du bloc s'il glisse.",
                        "solution": "La composante de la force de gravité parallèle au plan est F_parallèle = mg·sin(30°) = 2 × 9,8 × 0,5 = 9,8 N.\\nLa force normale est F_normale = mg·cos(30°) = 2 × 9,8 × 0,866 = 16,97 N.\\nLa force de frottement maximale est F_frottement = μₛ × F_normale = 0,3 × 16,97 = 5,09 N.\\nComme F_parallèle > F_frottement (9,8 N > 5,09 N), le bloc va glisser.\\nL'accélération est a = (F_parallèle - μₛ × F_normale) / m = (9,8 - 5,09) / 2 = 2,36 m/s²."
                    },
                    "experiment": {
                        "videoUrl": "https://www.youtube.com/embed/JvgpDTx1AZ0",
                        "title": "Démonstration des lois de Newton",
                        "description": "Cette vidéo illustre les trois lois du mouvement de Newton à travers des expériences simples.",
                        "context": "Les lois de Newton constituent le fondement de la mécanique classique et expliquent comment les objets se déplacent sous l'influence de forces.",
                        "keyPoints": [
                            "Observer l'inertie (première loi)",
                            "Noter la relation entre force, masse et accélération (deuxième loi)",
                            "Identifier les paires action-réaction (troisième loi)"
                        ]
                    }
                },
                {
                    "name": "Charles Darwin",
                    "field": "Biologie Évolutionniste",
                    "category": "biologie",
                    "years": "1809-1882",
                    "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2e/Charles_Darwin_seated_crop.jpg/220px-Charles_Darwin_seated_crop.jpg",
                    "description": "Naturaliste britannique qui a proposé la théorie de l'évolution par sélection naturelle, révolutionnant notre compréhension de la vie sur Terre.",
                    "discoveries": [
                        "Théorie de l'évolution par sélection naturelle",
                        "Origine commune de toutes les espèces",
                        "Mécanisme de la sélection sexuelle",
                        "Études sur les îles Galápagos"
                    ],
                    "quiz": [
                        {
                            "question": "Quel livre Darwin a-t-il publié en 1859 ?",
                            "options": ["L'Origine des espèces", "La Descendance de l'homme", "Le Voyage du Beagle", "L'Expression des émotions"],
                            "answer": 0,
                            "explanation": "L'Origine des espèces (1859) présente la théorie de l'évolution par sélection naturelle."
                        },
                        {
                            "question": "Sur quelles îles Darwin a-t-il fait des observations cruciales ?",
                            "options": ["Îles Canaries", "Îles Galápagos", "Îles Falkland", "Îles Hawaï"],
                            "answer": 1,
                            "explanation": "Les observations de Darwin aux îles Galápagos, notamment sur les pinsons, ont été cruciales pour sa théorie."
                        },
                        {
                            "question": "Quel mécanisme Darwin a-t-il proposé pour expliquer l'évolution ?",
                            "options": ["Hérédité des caractères acquis", "Sélection naturelle", "Mutation dirigée", "Création spéciale"],
                            "answer": 1,
                            "explanation": "Darwin a proposé la sélection naturelle comme mécanisme principal de l'évolution."
                        },
                        {
                            "question": "Combien d'années Darwin a-t-il passées à bord du HMS Beagle ?",
                            "options": ["3 ans", "5 ans", "7 ans", "10 ans"],
                            "answer": 1,
                            "explanation": "Darwin a passé 5 ans (1831-1836) à bord du HMS Beagle lors de son voyage autour du monde."
                        },
                        {
                            "question": "Qui a développé une théorie similaire à celle de Darwin en même temps ?",
                            "options": ["Lamarck", "Mendel", "Alfred Russel Wallace", "Thomas Huxley"],
                            "answer": 2,
                            "explanation": "Alfred Russel Wallace a développé indépendamment une théorie de l'évolution par sélection naturelle."
                        }
                    ],
                    "exam": {
                        "title": "Sélection naturelle et adaptation",
                        "problem": "Dans une population de papillons, 60% sont de couleur claire et 40% de couleur sombre. Après une pollution industrielle qui noircit les arbres, la prédation change : les oiseaux capturent 80% des papillons clairs mais seulement 20% des papillons sombres. Calculez la composition de la population après sélection et expliquez le mécanisme évolutif en jeu.",
                        "solution": "Population initiale : 60% clairs, 40% sombres.\\nAprès prédation : Clairs survivants = 60% × 20% = 12%, Sombres survivants = 40% × 80% = 32%.\\nTotal survivants = 44%.\\nNouvelle composition : Clairs = 12%/44% = 27%, Sombres = 32%/44% = 73%.\\nCeci illustre la sélection naturelle : l'environnement modifié favorise les individus sombres, mieux camouflés."
                    },
                    "experiment": {
                        "videoUrl": "https://www.youtube.com/embed/0SCjhI86grU",
                        "title": "Évolution en action : les pinsons de Darwin",
                        "description": "Cette vidéo montre comment les pinsons des Galápagos illustrent l'évolution par sélection naturelle.",
                        "context": "Les pinsons des Galápagos ont des becs adaptés à leur régime alimentaire spécifique, démontrant comment la sélection naturelle façonne les espèces.",
                        "keyPoints": [
                            "Observer la diversité des formes de becs",
                            "Comprendre la relation entre forme et fonction",
                            "Noter l'adaptation à différents environnements"
                        ]
                    }
                },
                {
                    "name": "Gregor Mendel",
                    "field": "Génétique",
                    "category": "biologie",
                    "years": "1822-1884",
                    "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/ba/Gregor_Mendel_Monk.jpg/220px-Gregor_Mendel_Monk.jpg",
                    "description": "Moine et botaniste austro-hongrois, considéré comme le père de la génétique moderne grâce à ses expériences sur l'hérédité chez les petits pois.",
                    "discoveries": [
                        "Lois de l'hérédité (lois de Mendel)",
                        "Concept de gènes dominants et récessifs",
                        "Principe de ségrégation des allèles",
                        "Loi d'assortiment indépendant"
                    ],
                    "quiz": [
                        {
                            "question": "Sur quelle plante Mendel a-t-il principalement travaillé ?",
                            "options": ["Haricots", "Petits pois", "Tournesols", "Maïs"],
                            "answer": 1,
                            "explanation": "Mendel a choisi les petits pois (Pisum sativum) pour ses expériences sur l'hérédité."
                        },
                        {
                            "question": "Combien de lois de l'hérédité Mendel a-t-il établies ?",
                            "options": ["Deux", "Trois", "Quatre", "Cinq"],
                            "answer": 1,
                            "explanation": "Mendel a établi trois lois : uniformité, ségrégation, et assortiment indépendant."
                        },
                        {
                            "question": "Qu'est-ce qu'un allèle dominant selon Mendel ?",
                            "options": ["Un allèle qui s'exprime toujours", "Un allèle plus fréquent", "Un allèle bénéfique", "Un allèle muté"],
                            "answer": 0,
                            "explanation": "Un allèle dominant s'exprime même en présence d'un allèle récessif."
                        },
                        {
                            "question": "Quel ratio Mendel a-t-il observé en F2 pour un croisement monohybride ?",
                            "options": ["1:1", "2:1", "3:1", "9:3:3:1"],
                            "answer": 2,
                            "explanation": "Le ratio 3:1 (dominant:récessif) est caractéristique de la F2 d'un croisement monohybride."
                        },
                        {
                            "question": "Pourquoi les travaux de Mendel ont-ils été ignorés de son vivant ?",
                            "options": ["Ils étaient incorrects", "La génétique n'existait pas encore", "Il n'a pas publié", "Ils étaient trop complexes"],
                            "answer": 1,
                            "explanation": "Les concepts de gènes et d'hérédité n'étaient pas encore établis à l'époque de Mendel."
                        }
                    ],
                    "exam": {
                        "title": "Croisements mendéliens",
                        "problem": "Chez les petits pois, la couleur jaune (J) est dominante sur la couleur verte (j), et la forme lisse (L) est dominante sur la forme ridée (l). Effectuez un croisement dihybride entre deux individus hétérozygotes (JjLl × JjLl). Donnez les génotypes et phénotypes de la descendance avec leurs proportions.",
                        "solution": "Croisement JjLl × JjLl\\nGametes possibles : JL, Jl, jL, jl (pour chaque parent)\\nTableau de Punnett 4×4 donne 16 combinaisons\\nPhénotypes : 9 jaune-lisse : 3 jaune-ridé : 3 vert-lisse : 1 vert-ridé\\nGénotypes : 1 JJLL : 2 JJLl : 2 JjLL : 4 JjLl : 1 JJll : 2 Jjll : 1 jjLL : 2 jjLl : 1 jjll"
                    },
                    "experiment": {
                        "videoUrl": "https://www.youtube.com/embed/Mehz7tCxjSE",
                        "title": "Les expériences de Mendel avec les petits pois",
                        "description": "Cette vidéo reconstitue les expériences historiques de Mendel sur l'hérédité.",
                        "context": "Mendel a méthodiquement croisé des variétés de petits pois pendant 8 ans, établissant les bases de la génétique moderne.",
                        "keyPoints": [
                            "Observer la méthodologie rigoureuse de Mendel",
                            "Comprendre l'importance des croisements contrôlés",
                            "Noter la quantification statistique des résultats"
                        ]
                    }
                },
                {
                    "name": "Antoine Lavoisier",
                    "field": "Chimie",
                    "category": "chimie",
                    "years": "1743-1794",
                    "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/ed/David_-_Portrait_of_Monsieur_Lavoisier_and_His_Wife.jpg/220px-David_-_Portrait_of_Monsieur_Lavoisier_and_His_Wife.jpg",
                    "description": "Chimiste français considéré comme le père de la chimie moderne. Il a établi la loi de conservation de la masse et révolutionné la nomenclature chimique.",
                    "discoveries": [
                        "Loi de conservation de la masse",
                        "Découverte du rôle de l'oxygène dans la combustion",
                        "Nomenclature chimique moderne",
                        "Composition de l'eau (H₂O)"
                    ],
                    "quiz": [
                        {
                            "question": "Quelle loi fondamentale Lavoisier a-t-il énoncée ?",
                            "options": ["Conservation de l'énergie", "Conservation de la masse", "Conservation de la charge", "Conservation du mouvement"],
                            "answer": 1,
                            "explanation": "Lavoisier a énoncé la loi de conservation de la masse : 'Rien ne se perd, rien ne se crée, tout se transforme'."
                        },
                        {
                            "question": "Quel gaz Lavoisier a-t-il nommé 'oxygène' ?",
                            "options": ["Air déphlogistiqué", "Air inflammable", "Air fixe", "Air nitreux"],
                            "answer": 0,
                            "explanation": "Lavoisier a nommé 'oxygène' (générateur d'acide) le gaz que Priestley appelait 'air déphlogistiqué'."
                        },
                        {
                            "question": "Quelle théorie Lavoisier a-t-il réfutée ?",
                            "options": ["Théorie atomique", "Théorie du phlogistique", "Théorie des humeurs", "Théorie des miasmes"],
                            "answer": 1,
                            "explanation": "Lavoisier a réfuté la théorie du phlogistique en expliquant la combustion par l'oxygène."
                        },
                        {
                            "question": "Comment Lavoisier est-il mort ?",
                            "options": ["Maladie", "Accident", "Guillotiné", "Empoisonnement"],
                            "answer": 2,
                            "explanation": "Lavoisier a été guillotiné en 1794 pendant la Terreur révolutionnaire."
                        },
                        {
                            "question": "Avec qui Lavoisier a-t-il travaillé pour décomposer l'eau ?",
                            "options": ["Priestley", "Cavendish", "Laplace", "Berthollet"],
                            "answer": 2,
                            "explanation": "Lavoisier a travaillé avec Laplace pour démontrer que l'eau est composée d'hydrogène et d'oxygène."
                        }
                    ],
                    "exam": {
                        "title": "Conservation de la masse dans les réactions chimiques",
                        "problem": "Dans la combustion complète du méthane (CH₄), on obtient du dioxyde de carbone et de l'eau selon l'équation : CH₄ + 2O₂ → CO₂ + 2H₂O. Si on brûle 16 g de méthane avec 64 g d'oxygène, calculez les masses de produits formés en appliquant la loi de Lavoisier.",
                        "solution": "Masses molaires : CH₄ = 16 g/mol, O₂ = 32 g/mol, CO₂ = 44 g/mol, H₂O = 18 g/mol\\nQuantités : 1 mol CH₄ + 2 mol O₂ → 1 mol CO₂ + 2 mol H₂O\\nMasse totale réactifs = 16 + 64 = 80 g\\nMasses produits : CO₂ = 44 g, H₂O = 2 × 18 = 36 g\\nMasse totale produits = 44 + 36 = 80 g\\nLa loi de conservation est vérifiée."
                    },
                    "experiment": {
                        "videoUrl": "https://www.youtube.com/embed/zhKdVKjKyfw",
                        "title": "La combustion selon Lavoisier",
                        "description": "Cette vidéo montre comment Lavoisier a expliqué la combustion par l'oxygène.",
                        "context": "Lavoisier a révolutionné la compréhension de la combustion en montrant qu'elle implique une combinaison avec l'oxygène, et non la perte de phlogistique.",
                        "keyPoints": [
                            "Observer l'augmentation de masse lors de la combustion",
                            "Comprendre le rôle de l'oxygène",
                            "Noter l'importance de la mesure précise"
                        ]
                    }
                },
                {
                    "name": "Galilée",
                    "field": "Astronomie et Physique",
                    "category": "astronomie",
                    "years": "1564-1642",
                    "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Justus_Sustermans_-_Portrait_of_Galileo_Galilei%2C_1636.jpg/220px-Justus_Sustermans_-_Portrait_of_Galileo_Galilei%2C_1636.jpg",
                    "description": "Astronome, physicien et ingénieur italien, figure centrale de la révolution scientifique. Il a perfectionné le télescope et défendu l'héliocentrisme.",
                    "discoveries": [
                        "Amélioration du télescope astronomique",
                        "Découverte des lunes de Jupiter",
                        "Observation des phases de Vénus",
                        "Loi de la chute des corps"
                    ],
                    "quiz": [
                        {
                            "question": "Combien de lunes de Jupiter Galilée a-t-il découvertes ?",
                            "options": ["Deux", "Trois", "Quatre", "Cinq"],
                            "answer": 2,
                            "explanation": "Galilée a découvert les quatre plus grandes lunes de Jupiter : Io, Europe, Ganymède et Callisto."
                        },
                        {
                            "question": "Quelle théorie Galilée a-t-il défendue ?",
                            "options": ["Géocentrisme", "Héliocentrisme", "Théorie des cordes", "Théorie atomique"],
                            "answer": 1,
                            "explanation": "Galilée a défendu l'héliocentrisme de Copernic contre le géocentrisme ptolémaïque."
                        },
                        {
                            "question": "De quelle tour Galilée aurait-il fait tomber des objets ?",
                            "options": ["Tour Eiffel", "Tour de Pise", "Tour de Londres", "Tour de Babel"],
                            "answer": 1,
                            "explanation": "Selon la légende, Galilée aurait fait ses expériences sur la chute des corps depuis la tour de Pise."
                        },
                        {
                            "question": "Quel tribunal a condamné Galilée ?",
                            "options": ["Tribunal civil", "Inquisition", "Parlement", "Université"],
                            "answer": 1,
                            "explanation": "L'Inquisition romaine a condamné Galilée en 1633 pour avoir défendu l'héliocentrisme."
                        },
                        {
                            "question": "Qu'a observé Galilée à la surface de la Lune ?",
                            "options": ["Des cratères", "De l'eau", "De la végétation", "Des constructions"],
                            "answer": 0,
                            "explanation": "Galilée a observé que la Lune n'était pas parfaitement lisse mais couverte de cratères et de montagnes."
                        }
                    ],
                    "exam": {
                        "title": "Mouvement uniformément accéléré",
                        "problem": "Galilée a établi que dans le vide, tous les corps tombent avec la même accélération g = 9,8 m/s². Une pierre est lâchée du haut d'une tour de 45 m de hauteur. Calculez le temps de chute et la vitesse d'impact au sol.",
                        "solution": "Équation du mouvement : h = ½gt²\\n45 = ½ × 9,8 × t²\\nt² = 90/9,8 = 9,18 s²\\nt = 3,03 s\\nVitesse finale : v = gt = 9,8 × 3,03 = 29,7 m/s"
                    },
                    "experiment": {
                        "videoUrl": "https://www.youtube.com/embed/E43-CfukEgs",
                        "title": "Les observations de Galilée au télescope",
                        "description": "Cette vidéo montre les découvertes astronomiques révolutionnaires de Galilée.",
                        "context": "Galilée a été le premier à utiliser systématiquement le télescope pour l'astronomie, révolutionnant notre vision du cosmos.",
                        "keyPoints": [
                            "Observer les cratères lunaires",
                            "Comprendre l'importance des lunes de Jupiter",
                            "Noter les phases de Vénus comme preuve de l'héliocentrisme"
                        ]
                    }
                },
                {
                    "name": "Archimède",
                    "field": "Mathématiques et Physique",
                    "category": "mathematiques",
                    "years": "287-212 av. J.-C.",
                    "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e7/Archimedes_Thoughtful_by_Fetti_%281620%29.jpg/220px-Archimedes_Thoughtful_by_Fetti_%281620%29.jpg",
                    "description": "Mathématicien, physicien et ingénieur grec de l'Antiquité. Il a établi les fondements de l'hydrostatique et fait des découvertes importantes en géométrie.",
                    "discoveries": [
                        "Principe d'Archimède (poussée hydrostatique)",
                        "Calcul de π avec une précision remarquable",
                        "Loi du levier",
                        "Vis d'Archimède"
                    ],
                    "quiz": [
                        {
                            "question": "Qu'énonce le principe d'Archimède ?",
                            "options": ["Tout corps plongé dans un fluide subit une poussée", "Les corps tombent à la même vitesse", "L'énergie se conserve", "La matière est composée d'atomes"],
                            "answer": 0,
                            "explanation": "Le principe d'Archimède énonce qu'un corps plongé dans un fluide subit une poussée égale au poids du fluide déplacé."
                        },
                        {
                            "question": "Comment Archimède aurait-il découvert son principe ?",
                            "options": ["En observant les étoiles", "En prenant un bain", "En étudiant les leviers", "En calculant π"],
                            "answer": 1,
                            "explanation": "Selon la légende, Archimède a découvert son principe en observant l'eau déborder de sa baignoire."
                        },
                        {
                            "question": "Quelle phrase célèbre Archimède aurait-il prononcée ?",
                            "options": ["Eurêka !", "E pur si muove", "Cogito ergo sum", "Alea jacta est"],
                            "answer": 0,
                            "explanation": "Archimède aurait crié 'Eurêka !' (J'ai trouvé !) en découvrant son principe."
                        },
                        {
                            "question": "Quelle valeur approximative d'π Archimède a-t-il calculée ?",
                            "options": ["3", "3,14", "3,141", "3,1416"],
                            "answer": 2,
                            "explanation": "Archimède a encadré π entre 3,1408 et 3,1429, une précision remarquable pour l'époque."
                        },
                        {
                            "question": "Comment Archimède est-il mort ?",
                            "options": ["De maladie", "Tué par un soldat romain", "Dans un accident", "De vieillesse"],
                            "answer": 1,
                            "explanation": "Archimède a été tué par un soldat romain lors du siège de Syracuse en 212 av. J.-C."
                        }
                    ],
                    "exam": {
                        "title": "Application du principe d'Archimède",
                        "problem": "Un bloc de bois de volume 0,2 m³ et de densité 0,6 flotte sur l'eau (densité 1000 kg/m³). Calculez la fraction du volume immergée et la poussée d'Archimède exercée par l'eau.",
                        "solution": "Masse du bloc = 0,6 × 1000 × 0,2 = 120 kg\\nPoids du bloc = 120 × 9,8 = 1176 N\\nÀ l'équilibre : Poussée = Poids\\nPoussée = ρ_eau × g × V_immergé\\n1176 = 1000 × 9,8 × V_immergé\\nV_immergé = 1176/(1000 × 9,8) = 0,12 m³\\nFraction immergée = 0,12/0,2 = 0,6 = 60%"
                    },
                    "experiment": {
                        "videoUrl": "https://www.youtube.com/embed/fDTFpMGOeKc",
                        "title": "Démonstration du principe d'Archimède",
                        "description": "Cette vidéo illustre le principe d'Archimède avec des expériences simples.",
                        "context": "Le principe d'Archimède explique pourquoi les objets flottent ou coulent, et est fondamental en hydrostatique.",
                        "keyPoints": [
                            "Observer la poussée exercée par le fluide",
                            "Comprendre la relation avec le volume déplacé",
                            "Noter les applications pratiques (bateaux, ballons)"
                        ]
                    }
                },
                {
                    "name": "Léonard de Vinci",
                    "field": "Inventeur et Artiste",
                    "category": "physique",
                    "years": "1452-1519",
                    "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/ba/Leonardo_self.jpg/220px-Leonardo_self.jpg",
                    "description": "Polymathe italien de la Renaissance, à la fois artiste, inventeur, ingénieur, scientifique et anatomiste. Il a conçu de nombreuses machines en avance sur son temps.",
                    "discoveries": [
                        "Études anatomiques détaillées",
                        "Conception d'machines volantes",
                        "Études sur l'hydraulique",
                        "Observations sur la lumière et l'optique"
                    ],
                    "quiz": [
                        {
                            "question": "Quelle machine volante Léonard de Vinci a-t-il conçue ?",
                            "options": ["Avion", "Hélicoptère", "Ornithoptère", "Planeur"],
                            "answer": 2,
                            "explanation": "Léonard a conçu l'ornithoptère, une machine volante imitant le battement des ailes d'oiseaux."
                        },
                        {
                            "question": "Dans quel domaine Léonard a-t-il fait des dissections ?",
                            "options": ["Botanique", "Anatomie humaine", "Zoologie", "Géologie"],
                            "answer": 1,
                            "explanation": "Léonard a pratiqué des dissections humaines pour comprendre l'anatomie, malgré les interdictions religieuses."
                        },
                        {
                            "question": "Quel tableau célèbre Léonard a-t-il peint ?",
                            "options": ["La Naissance de Vénus", "La Joconde", "La Cène", "Les deux"],
                            "answer": 3,
                            "explanation": "Léonard a peint à la fois La Joconde et La Cène, deux chefs-d'œuvre de la Renaissance."
                        },
                        {
                            "question": "Comment Léonard écrivait-il ses notes ?",
                            "options": ["En latin", "En miroir", "En code", "En grec"],
                            "answer": 1,
                            "explanation": "Léonard écrivait en miroir, de droite à gauche, peut-être pour protéger ses idées ou par habitude de gaucher."
                        },
                        {
                            "question": "Quelle machine de guerre Léonard a-t-il conçue ?",
                            "options": ["Canon", "Tank", "Catapulte", "Arbalète"],
                            "answer": 1,
                            "explanation": "Léonard a conçu un char d'assaut blindé, ancêtre du tank moderne."
                        }
                    ],
                    "exam": {
                        "title": "Mécanique des fluides selon Léonard",
                        "problem": "Léonard de Vinci a étudié l'écoulement de l'eau. Il a observé qu'un fluide s'écoulant dans un tube de section variable conserve son débit. Si l'eau s'écoule à 2 m/s dans une section de 0,1 m², quelle sera sa vitesse dans une section de 0,05 m² ?",
                        "solution": "Principe de continuité : Q = S₁v₁ = S₂v₂\\nDébit Q = 0,1 × 2 = 0,2 m³/s\\nVitesse dans la section réduite : v₂ = Q/S₂ = 0,2/0,05 = 4 m/s\\nLa vitesse double quand la section est divisée par deux."
                    },
                    "experiment": {
                        "videoUrl": "https://www.youtube.com/embed/QRt12jzGlfw",
                        "title": "Les inventions de Léonard de Vinci",
                        "description": "Cette vidéo présente les machines et inventions révolutionnaires de Léonard.",
                        "context": "Léonard de Vinci était en avance de plusieurs siècles sur son époque, concevant des machines qui ne seront réalisées qu'à l'ère moderne.",
                        "keyPoints": [
                            "Observer la complexité des mécanismes",
                            "Comprendre l'approche multidisciplinaire",
                            "Noter l'influence de l'observation de la nature"
                        ]
                    }
                },
                {
                    "name": "Louis Pasteur",
                    "field": "Microbiologie",
                    "category": "biologie",
                    "years": "1822-1895",
                    "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e2/Louis_Pasteur%2C_foto_av_F%C3%A9lix_Nadar.jpg/220px-Louis_Pasteur%2C_foto_av_F%C3%A9lix_Nadar.jpg",
                    "description": "Chimiste et microbiologiste français, pionnier de la microbiologie. Il a développé la pasteurisation et créé les premiers vaccins contre la rage et l'anthrax.",
                    "discoveries": [
                        "Pasteurisation",
                        "Théorie microbienne des maladies",
                        "Vaccin contre la rage",
                        "Réfutation de la génération spontanée"
                    ],
                    "quiz": [
                        {
                            "question": "Qu'est-ce que la pasteurisation ?",
                            "options": ["Stérilisation complète", "Chauffage contrôlé", "Congélation", "Irradiation"],
                            "answer": 1,
                            "explanation": "La pasteurisation est un chauffage contrôlé qui détruit les microbes pathogènes sans altérer le produit."
                        },
                        {
                            "question": "Quelle théorie Pasteur a-t-il réfutée ?",
                            "options": ["Évolution", "Génération spontanée", "Atomisme", "Héliocentrisme"],
                            "answer": 1,
                            "explanation": "Pasteur a démontré que les microbes ne naissent pas spontanément mais proviennent d'autres microbes."
                        },
                        {
                            "question": "Contre quelle maladie Pasteur a-t-il créé le premier vaccin ?",
                            "options": ["Variole", "Rage", "Tuberculose", "Choléra"],
                            "answer": 1,
                            "explanation": "Pasteur a développé le premier vaccin contre la rage en 1885."
                        },
                        {
                            "question": "Quel phénomène Pasteur a-t-il découvert en chimie ?",
                            "options": ["Radioactivité", "Chiralité", "Catalyse", "Électrolyse"],
                            "answer": 1,
                            "explanation": "Pasteur a découvert la chiralité moléculaire en étudiant les cristaux d'acide tartrique."
                        },
                        {
                            "question": "Quelle expérience célèbre Pasteur a-t-il réalisée ?",
                            "options": ["Col de cygne", "Goutte d'huile", "Prisme", "Pendule"],
                            "answer": 0,
                            "explanation": "L'expérience du col de cygne a démontré que l'air contient des microbes responsables de la fermentation."
                        }
                    ],
                    "exam": {
                        "title": "Cinétique de destruction microbienne",
                        "problem": "La pasteurisation suit une cinétique de premier ordre. Si 90% des microbes sont détruits en 1 minute à 72°C, combien de temps faut-il pour détruire 99,9% des microbes ? Utilisez la loi N(t) = N₀e^(-kt).",
                        "solution": "Pour 90% de destruction : N/N₀ = 0,1\\n0,1 = e^(-k×1)\\nk = -ln(0,1) = 2,303 min⁻¹\\nPour 99,9% de destruction : N/N₀ = 0,001\\n0,001 = e^(-2,303×t)\\nt = -ln(0,001)/2,303 = 6,908/2,303 = 3 minutes"
                    },
                    "experiment": {
                        "videoUrl": "https://www.youtube.com/embed/XjAcT4xeKZE",
                        "title": "L'expérience du col de cygne de Pasteur",
                        "description": "Cette vidéo reconstitue l'expérience historique qui a réfuté la génération spontanée.",
                        "context": "L'expérience de Pasteur a définitivement prouvé que les microbes ne naissent pas spontanément mais proviennent de l'environnement.",
                        "keyPoints": [
                            "Observer l'importance du contrôle expérimental",
                            "Comprendre le rôle de l'air dans la contamination",
                            "Noter l'impact sur l'hygiène médicale"
                        ]
                    }
                },
                {
                    "name": "Michael Faraday",
                    "field": "Physique et Électricité",
                    "category": "physique",
                    "years": "1791-1867",
                    "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/88/M_Faraday_Th_Phillips_oil_1841-1842.jpg/220px-M_Faraday_Th_Phillips_oil_1841-1842.jpg",
                    "description": "Physicien et chimiste britannique, pionnier de l'électromagnétisme. Il a découvert l'induction électromagnétique et établi les lois de l'électrolyse.",
                    "discoveries": [
                        "Induction électromagnétique",
                        "Lois de l'électrolyse",
                        "Cage de Faraday",
                        "Concept de champ électromagnétique"
                    ],
                    "quiz": [
                        {
                            "question": "Qu'est-ce que l'induction électromagnétique ?",
                            "options": ["Production d'électricité par magnétisme", "Attraction magnétique", "Résistance électrique", "Conduction thermique"],
                            "answer": 0,
                            "explanation": "L'induction électromagnétique est la production d'un courant électrique par variation d'un champ magnétique."
                        },
                        {
                            "question": "Combien de lois de l'électrolyse Faraday a-t-il établies ?",
                            "options": ["Une", "Deux", "Trois", "Quatre"],
                            "answer": 1,
                            "explanation": "Faraday a établi deux lois de l'électrolyse reliant la quantité de matière décomposée au courant électrique."
                        },
                        {
                            "question": "Qu'est-ce qu'une cage de Faraday ?",
                            "options": ["Une prison", "Un blindage électromagnétique", "Un générateur", "Un condensateur"],
                            "answer": 1,
                            "explanation": "Une cage de Faraday est une enceinte conductrice qui protège de l'influence des champs électriques extérieurs."
                        },
                        {
                            "question": "Quelle unité porte le nom de Faraday ?",
                            "options": ["Le farad", "Le faraday", "Le maxwell", "Le tesla"],
                            "answer": 0,
                            "explanation": "Le farad (F) est l'unité de capacité électrique nommée en l'honneur de Faraday."
                        },
                        {
                            "question": "Quel phénomène Faraday a-t-il découvert avec un aimant et une bobine ?",
                            "options": ["Résistance", "Induction", "Résonance", "Diffraction"],
                            "answer": 1,
                            "explanation": "Faraday a découvert qu'un aimant en mouvement dans une bobine induit un courant électrique."
                        }
                    ],
                    "exam": {
                        "title": "Loi de Faraday et induction",
                        "problem": "Une bobine de 100 spires a une surface de 0,01 m². Elle est placée dans un champ magnétique uniforme qui varie de 0,2 T à 0,8 T en 0,1 seconde. Calculez la force électromotrice induite selon la loi de Faraday.",
                        "solution": "Loi de Faraday : ε = -N × dΦ/dt\\nFlux magnétique : Φ = B × S\\nVariation de flux : dΦ = (0,8 - 0,2) × 0,01 = 0,006 Wb\\nVariation de temps : dt = 0,1 s\\nFEM induite : ε = -100 × 0,006/0,1 = -6 V\\nLa valeur absolue est 6 V."
                    },
                    "experiment": {
                        "videoUrl": "https://www.youtube.com/embed/NHpZ8ZWGgmw",
                        "title": "Démonstration de l'induction électromagnétique",
                        "description": "Cette vidéo montre les expériences de Faraday sur l'induction électromagnétique.",
                        "context": "Les découvertes de Faraday ont permis le développement des générateurs électriques et des transformateurs.",
                        "keyPoints": [
                            "Observer la production de courant par mouvement magnétique",
                            "Comprendre la relation entre électricité et magnétisme",
                            "Noter les applications pratiques (générateurs, moteurs)"
                        ]
                    }
                },
                {
                    "name": "Nikola Tesla",
                    "field": "Génie Électrique",
                    "category": "physique",
                    "years": "1856-1943",
                    "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/79/Tesla_circa_1890.jpeg/220px-Tesla_circa_1890.jpeg",
                    "description": "Inventeur et ingénieur serbo-américain, pionnier de l'électricité moderne. Il a développé le système de courant alternatif et de nombreuses inventions révolutionnaires.",
                    "discoveries": [
                        "Système de courant alternatif polyphasé",
                        "Moteur à induction",
                        "Bobine Tesla",
                        "Transmission d'énergie sans fil"
                    ],
                    "quiz": [
                        {
                            "question": "Quel type de courant Tesla a-t-il développé ?",
                            "options": ["Courant continu", "Courant alternatif", "Courant pulsé", "Courant variable"],
                            "answer": 1,
                            "explanation": "Tesla a développé le système de courant alternatif polyphasé, plus efficace que le courant continu."
                        },
                        {
                            "question": "Avec qui Tesla a-t-il eu la 'guerre des courants' ?",
                            "options": ["Einstein", "Edison", "Marconi", "Bell"],
                            "answer": 1,
                            "explanation": "Tesla (courant alternatif) s'est opposé à Edison (courant continu) dans la 'guerre des courants'."
                        },
                        {
                            "question": "Qu'est-ce qu'une bobine Tesla ?",
                            "options": ["Un moteur", "Un transformateur haute tension", "Une batterie", "Un générateur"],
                            "answer": 1,
                            "explanation": "La bobine Tesla est un transformateur qui produit de très hautes tensions et des arcs électriques spectaculaires."
                        },
                        {
                            "question": "Quelle unité magnétique porte le nom de Tesla ?",
                            "options": ["L'induction magnétique", "Le flux magnétique", "La perméabilité", "La reluctance"],
                            "answer": 0,
                            "explanation": "Le tesla (T) est l'unité d'induction magnétique dans le système international."
                        },
                        {
                            "question": "Quel projet futuriste Tesla a-t-il imaginé ?",
                            "options": ["Internet", "Transmission d'énergie sans fil", "Téléphone portable", "Télévision"],
                            "answer": 1,
                            "explanation": "Tesla a imaginé la transmission d'énergie électrique sans fil à travers la Terre."
                        }
                    ],
                    "exam": {
                        "title": "Courant alternatif triphasé",
                        "problem": "Un système triphasé de Tesla fournit une tension efficace de 400 V par phase. Les trois phases sont déphasées de 120°. Calculez la tension entre phases (tension composée) et expliquez l'avantage du système triphasé.",
                        "solution": "Tension entre phases : U = √3 × V = √3 × 400 = 692 V\\nAvantages du triphasé :\\n- Puissance constante (pas de pulsation)\\n- Meilleur rendement des moteurs\\n- Économie de cuivre (3 fils au lieu de 6)\\n- Équilibrage des charges"
                    },
                    "experiment": {
                        "videoUrl": "https://www.youtube.com/embed/VydPQuLyEns",
                        "title": "Démonstration de la bobine Tesla",
                        "description": "Cette vidéo montre le fonctionnement spectaculaire d'une bobine Tesla.",
                        "context": "La bobine Tesla illustre les principes de résonance électrique et de transformation haute tension développés par Tesla.",
                        "keyPoints": [
                            "Observer la production de hautes tensions",
                            "Comprendre la résonance électrique",
                            "Noter les applications en radio et télécommunications"
                        ]
                    }
                },
                {
                    "name": "Alan Turing",
                    "field": "Informatique et Mathématiques",
                    "category": "mathematiques",
                    "years": "1912-1954",
                    "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a1/Alan_Turing_Aged_16.jpg/220px-Alan_Turing_Aged_16.jpg",
                    "description": "Mathématicien et informaticien britannique, père de l'informatique théorique. Il a conçu la machine de Turing et contribué au décryptage d'Enigma.",
                    "discoveries": [
                        "Machine de Turing (modèle de calcul)",
                        "Test de Turing (intelligence artificielle)",
                        "Contribution au décryptage d'Enigma",
                        "Morphogenèse mathématique"
                    ],
                    "quiz": [
                        {
                            "question": "Qu'est-ce qu'une machine de Turing ?",
                            "options": ["Un ordinateur", "Un modèle théorique de calcul", "Une machine à écrire", "Un robot"],
                            "answer": 1,
                            "explanation": "La machine de Turing est un modèle mathématique abstrait qui définit ce qu'est un calcul."
                        },
                        {
                            "question": "Quel code Turing a-t-il aidé à décrypter ?",
                            "options": ["Morse", "Enigma", "César", "Vigenère"],
                            "answer": 1,
                            "explanation": "Turing a contribué au décryptage du code Enigma utilisé par les Allemands pendant la Seconde Guerre mondiale."
                        },
                        {
                            "question": "Qu'est-ce que le test de Turing ?",
                            "options": ["Un test de QI", "Un test d'intelligence artificielle", "Un test de programmation", "Un test de logique"],
                            "answer": 1,
                            "explanation": "Le test de Turing évalue si une machine peut exhiber un comportement intelligent indiscernable de celui d'un humain."
                        },
                        {
                            "question": "Dans quel domaine Turing a-t-il aussi travaillé ?",
                            "options": ["Biologie", "Chimie", "Géologie", "Astronomie"],
                            "answer": 0,
                            "explanation": "Turing a travaillé sur la morphogenèse, étudiant comment les formes biologiques se développent."
                        },
                        {
                            "question": "Comment Turing est-il mort ?",
                            "options": ["Accident", "Maladie", "Empoisonnement", "Guerre"],
                            "answer": 2,
                            "explanation": "Turing est mort en 1954 d'un empoisonnement au cyanure, probablement un suicide."
                        }
                    ],
                    "exam": {
                        "title": "Complexité algorithmique",
                        "problem": "Turing a établi les bases de la théorie de la complexité. Soit un algorithme de tri qui compare n éléments. Dans le pire cas, combien de comparaisons sont nécessaires pour un tri par insertion ? Exprimez la complexité en notation O(n).",
                        "solution": "Tri par insertion dans le pire cas :\\nPour chaque élément i (de 1 à n-1), on fait au maximum i comparaisons\\nNombre total : 1 + 2 + 3 + ... + (n-1) = n(n-1)/2\\nComplexité : O(n²)\\nCeci illustre l'importance de l'analyse algorithmique initiée par Turing."
                    },
                    "experiment": {
                        "videoUrl": "https://www.youtube.com/embed/dNRDvLACg5Q",
                        "title": "La machine de Turing expliquée",
                        "description": "Cette vidéo explique le concept révolutionnaire de la machine de Turing.",
                        "context": "La machine de Turing a défini les fondements théoriques de l'informatique moderne et de l'intelligence artificielle.",
                        "keyPoints": [
                            "Comprendre le modèle abstrait de calcul",
                            "Observer la simplicité du concept",
                            "Noter l'impact sur l'informatique moderne"
                        ]
                    }
                },
                {
                    "name": "James Clerk Maxwell",
                    "field": "Physique Électromagnétique",
                    "category": "physique",
                    "years": "1831-1879",
                    "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/57/James_Clerk_Maxwell.png/220px-James_Clerk_Maxwell.png",
                    "description": "Physicien écossais qui a unifié l'électricité, le magnétisme et la lumière dans la théorie électromagnétique. Ses équations sont fondamentales en physique.",
                    "discoveries": [
                        "Équations de Maxwell (électromagnétisme)",
                        "Théorie cinétique des gaz",
                        "Première photographie couleur",
                        "Distribution de Maxwell-Boltzmann"
                    ],
                    "quiz": [
                        {
                            "question": "Combien d'équations Maxwell a-t-il formulées ?",
                            "options": ["Deux", "Trois", "Quatre", "Cinq"],
                            "answer": 2,
                            "explanation": "Maxwell a formulé quatre équations fondamentales de l'électromagnétisme."
                        },
                        {
                            "question": "Qu'a unifié Maxwell dans sa théorie ?",
                            "options": ["Électricité et magnétisme", "Électricité, magnétisme et lumière", "Forces et énergie", "Matière et énergie"],
                            "answer": 1,
                            "explanation": "Maxwell a montré que l'électricité, le magnétisme et la lumière sont des aspects du même phénomène électromagnétique."
                        },
                        {
                            "question": "Quelle vitesse Maxwell a-t-il calculée ?",
                            "options": ["Vitesse du son", "Vitesse de la lumière", "Vitesse de l'électricité", "Vitesse des ondes"],
                            "answer": 1,
                            "explanation": "Maxwell a calculé que la vitesse de la lumière égale c = 1/√(μ₀ε₀), reliant optique et électromagnétisme."
                        },
                        {
                            "question": "Dans quel domaine Maxwell a-t-il aussi contribué ?",
                            "options": ["Thermodynamique", "Mécanique quantique", "Relativité", "Chimie"],
                            "answer": 0,
                            "explanation": "Maxwell a développé la théorie cinétique des gaz et la distribution statistique des vitesses."
                        },
                        {
                            "question": "Qu'est-ce qu'un 'démon de Maxwell' ?",
                            "options": ["Une particule", "Une expérience de pensée", "Un instrument", "Une équation"],
                            "answer": 1,
                            "explanation": "Le démon de Maxwell est une expérience de pensée sur la thermodynamique et l'entropie."
                        }
                    ],
                    "exam": {
                        "title": "Ondes électromagnétiques",
                        "problem": "Les équations de Maxwell prédisent l'existence d'ondes électromagnétiques. Une onde radio a une fréquence de 100 MHz. Calculez sa longueur d'onde dans le vide et expliquez pourquoi cette onde peut se propager sans support matériel.",
                        "solution": "Relation onde : c = λf\\nλ = c/f = 3×10⁸/(100×10⁶) = 3 m\\nLes ondes électromagnétiques se propagent sans support car elles consistent en champs électrique et magnétique qui se régénèrent mutuellement selon les équations de Maxwell."
                    },
                    "experiment": {
                        "videoUrl": "https://www.youtube.com/embed/FWCN_uI5ygY",
                        "title": "Les équations de Maxwell visualisées",
                        "description": "Cette vidéo visualise les équations de Maxwell et leurs implications.",
                        "context": "Les équations de Maxwell ont révolutionné la physique en unifiant des phénomènes apparemment distincts et en prédisant l'existence des ondes électromagnétiques.",
                        "keyPoints": [
                            "Observer l'interaction entre champs électrique et magnétique",
                            "Comprendre la propagation des ondes",
                            "Noter l'impact sur les télécommunications modernes"
                        ]
                    }
                },
                {
                    "name": "Aristote",
                    "field": "Philosophie Naturelle",
                    "category": "biologie",
                    "years": "384-322 av. J.-C.",
                    "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ae/Aristotle_Altemps_Inv8575.jpg/220px-Aristotle_Altemps_Inv8575.jpg",
                    "description": "Philosophe grec de l'Antiquité, fondateur de la logique et précurseur de nombreuses sciences. Il a établi les premières classifications systématiques du vivant.",
                    "discoveries": [
                        "Classification des êtres vivants",
                        "Logique formelle (syllogisme)",
                        "Théorie des quatre causes",
                        "Observations anatomiques"
                    ],
                    "quiz": [
                        {
                            "question": "Qu'est-ce qu'Aristote a créé en logique ?",
                            "options": ["L'algèbre", "Le syllogisme", "Les probabilités", "La géométrie"],
                            "answer": 1,
                            "explanation": "Aristote a créé le syllogisme, une forme de raisonnement logique déductif."
                        },
                        {
                            "question": "Comment Aristote classait-il les animaux ?",
                            "options": ["Par couleur", "Par taille", "Par sang/sans sang", "Par habitat"],
                            "answer": 2,
                            "explanation": "Aristote distinguait les animaux à sang (vertébrés) des animaux sans sang (invertébrés)."
                        },
                        {
                            "question": "Combien de causes Aristote distinguait-il ?",
                            "options": ["Deux", "Trois", "Quatre", "Cinq"],
                            "answer": 2,
                            "explanation": "Aristote distinguait quatre causes : matérielle, formelle, efficiente et finale."
                        },
                        {
                            "question": "Qui était le maître d'Aristote ?",
                            "options": ["Socrate", "Platon", "Pythagore", "Thalès"],
                            "answer": 1,
                            "explanation": "Aristote a été l'élève de Platon à l'Académie d'Athènes."
                        },
                        {
                            "question": "Qui Aristote a-t-il enseigné ?",
                            "options": ["César", "Alexandre le Grand", "Cicéron", "Ptolémée"],
                            "answer": 1,
                            "explanation": "Aristote a été le précepteur d'Alexandre le Grand, futur conquérant macédonien."
                        }
                    ],
                    "exam": {
                        "title": "Classification aristotélicienne",
                        "problem": "Aristote a établi une hiérarchie du vivant. Classez les organismes suivants selon sa méthode : homme, cheval, poisson, insecte, plante. Expliquez les critères utilisés et comparez avec la classification moderne.",
                        "solution": "Classification d'Aristote (du plus 'parfait' au moins 'parfait') :\\n1. Homme (animal rationnel, sang chaud, vivipare)\\n2. Cheval (animal à sang, quadrupède, vivipare)\\n3. Poisson (animal à sang, ovipare, aquatique)\\n4. Insecte (animal sans sang, métamorphose)\\n5. Plante (âme végétative seulement)\\nCritères : présence de sang, mode de reproduction, habitat, complexité de l'âme."
                    },
                    "experiment": {
                        "videoUrl": "https://www.youtube.com/embed/leX541Dr2rU",
                        "title": "La méthode scientifique d'Aristote",
                        "description": "Cette vidéo explore l'approche scientifique d'Aristote et son influence.",
                        "context": "Aristote a établi les bases de la méthode scientifique par l'observation systématique et la classification rationnelle.",
                        "keyPoints": [
                            "Observer l'importance de la classification",
                            "Comprendre la méthode déductive",
                            "Noter l'influence sur la science médiévale"
                        ]
                    }
                },
                {
                    "name": "Johannes Kepler",
                    "field": "Astronomie",
                    "category": "astronomie",
                    "years": "1571-1630",
                    "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Johannes_Kepler_1610.jpg/220px-Johannes_Kepler_1610.jpg",
                    "description": "Astronome allemand qui a découvert les lois du mouvement planétaire. Ses travaux ont confirmé l'héliocentrisme et préparé la mécanique céleste de Newton.",
                    "discoveries": [
                        "Trois lois du mouvement planétaire",
                        "Orbites elliptiques des planètes",
                        "Relation période-distance (3e loi)",
                        "Télescope de Kepler"
                    ],
                    "quiz": [
                        {
                            "question": "Quelle forme Kepler a-t-il découverte pour les orbites planétaires ?",
                            "options": ["Circulaires", "Elliptiques", "Paraboliques", "Hyperboliques"],
                            "answer": 1,
                            "explanation": "Kepler a découvert que les planètes suivent des orbites elliptiques, et non circulaires."
                        },
                        {
                            "question": "Combien de lois Kepler a-t-il formulées ?",
                            "options": ["Deux", "Trois", "Quatre", "Cinq"],
                            "answer": 1,
                            "explanation": "Kepler a formulé trois lois fondamentales du mouvement planétaire."
                        },
                        {
                            "question": "Où se trouve le Soleil dans l'orbite elliptique selon Kepler ?",
                            "options": ["Au centre", "À un foyer", "À l'extrémité", "Variable"],
                            "answer": 1,
                            "explanation": "Selon la première loi de Kepler, le Soleil occupe l'un des foyers de l'ellipse orbitale."
                        },
                        {
                            "question": "Que relie la troisième loi de Kepler ?",
                            "options": ["Vitesse et distance", "Période et distance", "Masse et vitesse", "Température et distance"],
                            "answer": 1,
                            "explanation": "La troisième loi relie le carré de la période au cube de la distance moyenne au Soleil."
                        },
                        {
                            "question": "De qui Kepler a-t-il utilisé les observations ?",
                            "options": ["Galilée", "Copernic", "Tycho Brahe", "Ptolémée"],
                            "answer": 2,
                            "explanation": "Kepler a utilisé les observations précises de Tycho Brahe pour établir ses lois."
                        }
                    ],
                    "exam": {
                        "title": "Application des lois de Kepler",
                        "problem": "Mars a une période orbitale de 687 jours terrestres. En utilisant la troisième loi de Kepler (T² ∝ a³), calculez la distance moyenne de Mars au Soleil en unités astronomiques (UA), sachant que la Terre est à 1 UA du Soleil.",
                        "solution": "Troisième loi de Kepler : T²/a³ = constante\\nPour la Terre : T₁ = 365 jours, a₁ = 1 UA\\nPour Mars : T₂ = 687 jours, a₂ = ?\\n(T₂/T₁)² = (a₂/a₁)³\\n(687/365)² = a₂³\\n3,54 = a₂³\\na₂ = ∛3,54 = 1,52 UA"
                    },
                    "experiment": {
                        "videoUrl": "https://www.youtube.com/embed/8Vkz1-tJkSI",
                        "title": "Les lois de Kepler visualisées",
                        "description": "Cette vidéo illustre les trois lois de Kepler sur le mouvement planétaire.",
                        "context": "Les lois de Kepler ont révolutionné l'astronomie en décrivant mathématiquement le mouvement des planètes.",
                        "keyPoints": [
                            "Observer les orbites elliptiques",
                            "Comprendre la variation de vitesse orbitale",
                            "Noter la relation période-distance"
                        ]
                    }
                },
                {
                    "name": "Dmitri Mendeleïev",
                    "field": "Chimie",
                    "category": "chimie",
                    "years": "1834-1907",
                    "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/ce/DIMendeleev.jpg/220px-DIMendeleev.jpg",
                    "description": "Chimiste russe qui a créé le tableau périodique des éléments. Sa classification a permis de prédire l'existence d'éléments non encore découverts.",
                    "discoveries": [
                        "Tableau périodique des éléments",
                        "Loi périodique",
                        "Prédiction d'éléments inconnus",
                        "Propriétés périodiques"
                    ],
                    "quiz": [
                        {
                            "question": "Sur quoi Mendeleïev a-t-il basé sa classification ?",
                            "options": ["Masse atomique", "Numéro atomique", "Électronégativité", "Rayon atomique"],
                            "answer": 0,
                            "explanation": "Mendeleïev a classé les éléments par masse atomique croissante, observant la périodicité des propriétés."
                        },
                        {
                            "question": "Combien d'éléments Mendeleïev a-t-il prédits ?",
                            "options": ["Deux", "Trois", "Quatre", "Cinq"],
                            "answer": 1,
                            "explanation": "Mendeleïev a prédit trois éléments : eka-bore (scandium), eka-aluminium (gallium), eka-silicium (germanium)."
                        },
                        {
                            "question": "Qu'est-ce que la loi périodique ?",
                            "options": ["Les propriétés se répètent périodiquement", "Les masses augmentent", "Les éléments se transforment", "Les atomes se divisent"],
                            "answer": 0,
                            "explanation": "La loi périodique énonce que les propriétés des éléments sont des fonctions périodiques de leur masse atomique."
                        },
                        {
                            "question": "Quel élément Mendeleïev a-t-il appelé 'eka-aluminium' ?",
                            "options": ["Scandium", "Gallium", "Germanium", "Indium"],
                            "answer": 1,
                            "explanation": "L'eka-aluminium prédit par Mendeleïev correspond au gallium découvert en 1875."
                        },
                        {
                            "question": "Quelle anomalie Mendeleïev a-t-il acceptée dans son tableau ?",
                            "options": ["Inversion de masse", "Éléments manquants", "Propriétés différentes", "Toutes les réponses"],
                            "answer": 3,
                            "explanation": "Mendeleïev a accepté des inversions de masse et laissé des cases vides pour maintenir la périodicité des propriétés."
                        }
                    ],
                    "exam": {
                        "title": "Prédictions de Mendeleïev",
                        "problem": "Mendeleïev a prédit les propriétés de l'eka-silicium (germanium). Il a prédit une masse atomique de 72 et une densité de 5,5 g/cm³. Les valeurs réelles sont 72,6 et 5,32 g/cm³. Calculez l'erreur relative de ses prédictions et commentez leur précision.",
                        "solution": "Erreur relative masse = |72,6-72|/72,6 × 100% = 0,83%\\nErreur relative densité = |5,32-5,5|/5,32 × 100% = 3,38%\\nCes prédictions remarquablement précises ont validé la loi périodique et démontré la puissance prédictive du tableau de Mendeleïev."
                    },
                    "experiment": {
                        "videoUrl": "https://www.youtube.com/embed/fPnwBITSmgU",
                        "title": "Construction du tableau périodique",
                        "description": "Cette vidéo montre comment Mendeleïev a construit son tableau périodique.",
                        "context": "Le tableau périodique de Mendeleïev a organisé la chimie et permis de comprendre la structure atomique.",
                        "keyPoints": [
                            "Observer la périodicité des propriétés",
                            "Comprendre l'importance des prédictions",
                            "Noter l'évolution vers le tableau moderne"
                        ]
                    }
                },
                {
                    "name": "Rosalind Franklin",
                    "field": "Biologie Moléculaire",
                    "category": "biologie",
                    "years": "1920-1958",
                    "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e4/Rosalind_Franklin_%281920-1958%29.jpg/220px-Rosalind_Franklin_%281920-1958%29.jpg",
                    "description": "Chimiste britannique spécialisée en cristallographie aux rayons X. Ses travaux ont été cruciaux pour la découverte de la structure de l'ADN.",
                    "discoveries": [
                        "Structure hélicoïdale de l'ADN (Photo 51)",
                        "Structure de l'ARN",
                        "Cristallographie des virus",
                        "Structure du charbon et du graphite"
                    ],
                    "quiz": [
                        {
                            "question": "Quelle technique Franklin utilisait-elle pour étudier l'ADN ?",
                            "options": ["Microscopie", "Cristallographie aux rayons X", "Spectroscopie", "Électrophorèse"],
                            "answer": 1,
                            "explanation": "Franklin utilisait la cristallographie aux rayons X pour déterminer la structure de l'ADN."
                        },
                        {
                            "question": "Comment s'appelle la célèbre photo de l'ADN prise par Franklin ?",
                            "options": ["Photo 50", "Photo 51", "Photo 52", "Photo X"],
                            "answer": 1,
                            "explanation": "La Photo 51 de Franklin a révélé la structure hélicoïdale de l'ADN."
                        },
                        {
                            "question": "Quelle forme Franklin a-t-elle identifiée pour l'ADN ?",
                            "options": ["Linéaire", "Circulaire", "Hélicoïdale", "Ramifiée"],
                            "answer": 2,
                            "explanation": "Franklin a identifié la structure hélicoïdale de l'ADN grâce à ses clichés de diffraction."
                        },
                        {
                            "question": "Sur quoi d'autre Franklin a-t-elle travaillé ?",
                            "options": ["Protéines", "Virus", "Lipides", "Glucides"],
                            "answer": 1,
                            "explanation": "Franklin a aussi étudié la structure des virus, notamment le virus de la mosaïque du tabac."
                        },
                        {
                            "question": "Pourquoi Franklin n'a-t-elle pas reçu le prix Nobel pour l'ADN ?",
                            "options": ["Travail incomplet", "Décédée avant", "Discrimination", "Refus"],
                            "answer": 1,
                            "explanation": "Franklin est décédée en 1958, avant l'attribution du prix Nobel pour la structure de l'ADN en 1962."
                        }
                    ],
                    "exam": {
                        "title": "Cristallographie et structure de l'ADN",
                        "problem": "La Photo 51 de Franklin montre un motif de diffraction avec une périodicité de 3,4 Å le long de l'axe de l'hélice. Sachant que l'ADN fait un tour complet tous les 10 paires de bases, calculez le pas de l'hélice et l'angle de rotation par base.",
                        "solution": "Distance entre bases = 3,4 Å\\nPas de l'hélice (tour complet) = 10 × 3,4 = 34 Å\\nAngle par base = 360°/10 = 36°\\nCes mesures précises de Franklin ont été essentielles pour établir le modèle de Watson et Crick."
                    },
                    "experiment": {
                        "videoUrl": "https://www.youtube.com/embed/BIP0lYrdirI",
                        "title": "La cristallographie aux rayons X de Franklin",
                        "description": "Cette vidéo explique comment Franklin a utilisé les rayons X pour étudier l'ADN.",
                        "context": "Les techniques de cristallographie de Franklin ont révélé des détails cruciaux sur la structure de l'ADN.",
                        "keyPoints": [
                            "Comprendre la diffraction des rayons X",
                            "Observer les motifs de la Photo 51",
                            "Noter la précision des mesures"
                        ]
                    }
                }
            ]

            # Insérer les données dans la collection
            scientists_collection.insert_many(scientists_data)
            print("Base de données initialisée avec 20 scientifiques et leurs quiz.")
            return True
        else:
            print("Base de données déjà initialisée.")
            return False

