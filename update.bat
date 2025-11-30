@echo off
chcp 65001 >nul
title Mise à Jour - Facturación Fácil

echo ========================================
echo   🔄 MISE À JOUR - FACTURACIÓN FÁCIL
echo ========================================
echo.

:: Vérifier si on est dans le bon répertoire
if not exist "main.py" (
    echo ❌ ERREUR: Fichier main.py non trouvé
    echo Assurez-vous d'être dans le répertoire de l'application
    echo.
    pause
    exit /b 1
)

:: Vérifier si Git est installé
git --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERREUR: Git n'est pas installé ou pas dans le PATH
    echo Veuillez installer Git depuis: https://git-scm.com/download/win
    echo.
    pause
    exit /b 1
)

echo 🔍 Vérification de l'état actuel...
echo.

:: Vérifier s'il y a des modifications locales
git status --porcelain >nul 2>&1
if errorlevel 1 (
    echo ⚠️  ATTENTION: Impossible de vérifier l'état Git
    echo Continuez-vous quand même? (O/N)
    set /p choice=
    if /i not "%choice%"=="O" if /i not "%choice%"=="o" (
        echo Mise à jour annulée
        pause
        exit /b 1
    )
)

:: Sauvegarder la base de données
echo 💾 Sauvegarde de la base de données...
if exist "facturacion.db" (
    for /f "tokens=2-4 delims=/ " %%a in ('date /t') do (
        for /f "tokens=1-2 delims=: " %%d in ('time /t') do (
            set datetime=%%c%%a%%b_%%d%%e
        )
    )
    copy "facturacion.db" "facturacion_backup_%datetime%.db" >nul
    if errorlevel 1 (
        echo ⚠️  Impossible de sauvegarder la base de données
    ) else (
        echo ✅ Base de données sauvegardée: facturacion_backup_%datetime%.db
    )
)
echo.

:: Fermer l'application si elle est en cours d'exécution
echo 🔒 Vérification si l'application est en cours d'exécution...
tasklist /FI "IMAGENAME eq python.exe" /FI "WINDOWTITLE eq Facturación Fácil*" >nul 2>&1
if not errorlevel 1 (
    echo ⚠️  L'application semble être en cours d'exécution
    echo Veuillez la fermer avant de continuer
    echo Appuyez sur une touche quand c'est fait...
    pause >nul
)
echo.

:: Récupérer les mises à jour
echo 🌐 Téléchargement des mises à jour...
git fetch origin
if errorlevel 1 (
    echo ❌ ERREUR: Impossible de récupérer les mises à jour
    echo Vérifiez votre connexion Internet
    echo.
    pause
    exit /b 1
)

:: Vérifier s'il y a des mises à jour disponibles
git log HEAD..origin/main --oneline >nul 2>&1
if errorlevel 1 (
    echo ℹ️  Aucune mise à jour disponible
    echo Votre application est déjà à jour!
    echo.
    pause
    exit /b 0
)

echo 📋 Mises à jour disponibles:
git log HEAD..origin/main --oneline --format="  • %%s"
echo.

echo Voulez-vous appliquer ces mises à jour? (O/N)
set /p choice=
if /i not "%choice%"=="O" if /i not "%choice%"=="o" (
    echo Mise à jour annulée
    pause
    exit /b 0
)

:: Appliquer les mises à jour
echo 🔄 Application des mises à jour...
git pull origin main
if errorlevel 1 (
    echo ❌ ERREUR: Échec de la mise à jour
    echo Essayez de résoudre les conflits manuellement
    echo.
    pause
    exit /b 1
)

echo ✅ Code mis à jour avec succès!
echo.

:: Vérifier si l'environnement virtuel existe
if not exist "env\Scripts\activate.bat" (
    echo ⚠️  Environnement virtuel non trouvé
    echo Exécution de install.bat pour le créer...
    call install.bat
    if errorlevel 1 (
        echo ❌ ERREUR: Impossible de créer l'environnement virtuel
        pause
        exit /b 1
    )
)

:: Activer l'environnement virtuel et mettre à jour les dépendances
echo 📦 Mise à jour des dépendances...
call env\Scripts\activate.bat
pip install -r requirements.txt --upgrade --quiet
if errorlevel 1 (
    echo ⚠️  Problème lors de la mise à jour des dépendances
    echo L'application peut quand même fonctionner
)

echo ✅ Dépendances mises à jour!
echo.

:: Test rapide de l'application
echo 🧪 Test de l'application...
python -c "import main; print('✅ Application testée avec succès!')" 2>nul
if errorlevel 1 (
    echo ⚠️  Problème détecté lors du test
    echo Essayez de lancer l'application manuellement
) else (
    echo ✅ Test réussi!
)

echo.
echo ========================================
echo   🎉 MISE À JOUR TERMINÉE AVEC SUCCÈS!
echo ========================================
echo.
echo Vous pouvez maintenant lancer l'application avec:
echo   • Double-clic sur start.bat
echo   • Ou: python main.py
echo.

:: Proposer de lancer l'application
echo Voulez-vous lancer l'application maintenant? (O/N)
set /p choice=
if /i "%choice%"=="O" if /i "%choice%"=="o" (
    echo 🚀 Lancement de l'application...
    start "" python main.py
)

echo.
echo Appuyez sur une touche pour fermer...
pause >nul
