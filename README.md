# PROJET_FLASK

Ce travail s'inscrit dans le processus d'apprentissage des pensionnaires de la promo4 SA, senegal.

Alors pour executer ce projet, veuillez suivre les étapes suivantes:

1. Cloner le projet dans votre machine et positionner vous dans ce dossier
2. Mettre en palce un environnement virtuel

   1. Création: `  python3 -m venv nom_environnement_virtual`
   2. Activation:   `source nom_environnement_virtuel/bin/activate`
3. Installer les requirements(dépendances)
   Il y'a dans le projet un fichier requirements.txt. Ce dernier contient toutes les installations nécessaires pour ce projet
   executer la commande ` python -m pip install -r requirements.txt`
4. Mettre en place la base de donnée
   Vous devez absoluement avoir déjà installé postgres.
   un dump de la base de donnée est présent dans le projet sous le nom projetflask.sql.
5. 1. connectez vous dans votre terminal postgres
      en tant que user postgres ou un autre avec:

      `sudo -u -i nom_de_votre_user`
   2. créer une base de donné: `createdb projetflask`
   3. Faire un backup de la base de donnée:

      `psql projetflask < chemin_du_fichier/projetflask.sql`

      pour plus d'infos sur postgres, reporterz vous à `https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-22-04`
   4. connection à mla base de donnée

      Ouvrez le fichier `app.py`

      A la ligne 26, remplacer `groupe4` par `votre_user_linux` et `test123` par `le password de votre user linux`
6. Lancement du projet
   Dans votre terminal, assurez vous de bien vous positionner dans le dossier du projet. Executer les commande ci-dessous

   `export FLASK_APP=app`

   `flask run`

Vous de vez à présent apercevoir dans votre terminal le lien `127.0.0.1:5000`, copiez le et collez le dans votre navigateur. 

ET BOUMMM! LE TOUR EST JOUÉ,
