# Django CI/CD — GitHub Actions et Vercel

Application Django à page unique. Le fond bleu passe le contrôle CI ; un fond orange provoque volontairement l'échec du test et bloque la fusion vers `main` lorsque la règle de protection est activée.

## Exécution locale

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py runserver
```

Tests :

```powershell
python -m unittest tests.test_background_color -v
python manage.py test
```

## Branches et publication

1. Créer un dépôt GitHub **public** avec `main` comme branche de production.
2. Créer `test`, puis configurer localement `test` comme branche de travail par défaut :

   ```powershell
   git init
   git add .
   git commit -m "Initialiser l'application Django et le pipeline CI/CD"
   git branch -M test
   git remote add origin https://github.com/UTILISATEUR/DEPOT.git
   git push -u origin test
   git push origin test:main
   ```

3. Dans **Settings → Branches → Add branch protection rule**, cibler `main`, activer **Require a pull request before merging** et **Require status checks to pass before merging**, puis sélectionner `Tests obligatoires`.
4. Dans Vercel, importer le dépôt, choisir la branche de production `main` et laisser Vercel utiliser `vercel.json`.
5. Travailler uniquement sur `test`, pousser, puis ouvrir une pull request `test` → `main`.

> Un workflow déclenché uniquement sur `push` vers `main` ne peut pas bloquer un merge déjà effectué. Le workflow couvre donc les `pull_request` vers `main` et les `push` sur `main`.

## Démonstration de l'échec

Remplacer temporairement `background-color: #0d6efd;` par `background-color: orange;`, pousser sur `test` et ouvrir/mettre à jour la pull request. Le job `Tests obligatoires` échoue avec « Déploiement bloqué ». Ne pas fusionner cette version ; remettre ensuite le bleu pour restaurer une CI verte.

## Livrables

- Application Django : `config/`, `home/`, `manage.py`
- Test de couleur : `tests/test_background_color.py`
- Workflow : `.github/workflows/ci.yml`
- Configuration Vercel : `api/index.py`, `vercel.json`
- Rapport : `rapport/Rapport_CICD_Django.pdf`
