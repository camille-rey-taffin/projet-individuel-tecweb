# script d'installation de l'environnement virtuel, dépendances et variables
# pour pouvoir lancer l'application web et les scripts d'extraction

# création et installation des dépendances de l'environnement virtuel
pipenv install

# pseudo Ntealan
read -p "Saisissez le chemin de votre driver Chrome: " driverpath
# pseudo Ntealan
read -p "Saisissez votre pseudo NTeALan: " username
# mot de passe Ntealan
read -p "Saisissez votre mot de passe NTeALan: " password

echo "DRIVER_PATH = $driverpath\nUSERNAME = $username\nPASSWORD = $password" > ./scripts_extraction/.env
