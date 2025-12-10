@echo off
chcp 65001 >nul
title Sauvegarde - Facturación Fácil

echo ========================================
echo   💾 SAUVEGARDE - FACTURACIÓN FÁCIL
echo ========================================
echo.

:: Créer le répertoire de sauvegarde s'il n'existe pas
if not exist "backups" (
    mkdir backups
    echo 📁 Répertoire de sauvegarde créé
)

:: Générer un nom de fichier avec date et heure
for /f "tokens=2-4 delims=/ " %%a in ('date /t') do (
    for /f "tokens=1-2 delims=: " %%d in ('time /t') do (
        set datetime=%%c%%a%%b_%%d%%e
    )
)

set backup_name=backup_%datetime%

echo 🔍 Création de la sauvegarde: %backup_name%
echo.

:: Sauvegarder la base de données
if exist "base_de_datos\facturacion.db" (
    echo 💾 Sauvegarde de la base de données...
    copy "base_de_datos\facturacion.db" "base_de_datos\backups\%backup_name%_facturacion.db" >nul
    if errorlevel 1 (
        echo ❌ ERREUR: Impossible de sauvegarder la base de données
    ) else (
        echo ✅ Base de données sauvegardée
    )
) else (
    echo ⚠️  Base de données non trouvée
)

:: Sauvegarder les fichiers de configuration
if exist "config" (
    echo 📋 Sauvegarde de la configuration...
    xcopy "config" "base_de_datos\backups\%backup_name%_config\" /E /I /Q >nul 2>&1
    if errorlevel 1 (
        echo ⚠️  Problème lors de la sauvegarde de la configuration
    ) else (
        echo ✅ Configuration sauvegardée
    )
)

:: Sauvegarder les logs importants
if exist "logs" (
    echo 📝 Sauvegarde des logs...
    xcopy "logs\*.log" "backups\%backup_name%_logs\" /I /Q >nul 2>&1
    if errorlevel 1 (
        echo ⚠️  Problème lors de la sauvegarde des logs
    ) else (
        echo ✅ Logs sauvegardés
    )
)

:: Sauvegarder les fichiers personnalisés
if exist "custom" (
    echo 🎨 Sauvegarde des personnalisations...
    xcopy "custom" "backups\%backup_name%_custom\" /E /I /Q >nul 2>&1
    if errorlevel 1 (
        echo ⚠️  Problème lors de la sauvegarde des personnalisations
    ) else (
        echo ✅ Personnalisations sauvegardées
    )
)

:: Créer un fichier d'information sur la sauvegarde
echo 📄 Création du fichier d'information...
(
    echo Sauvegarde créée le: %date% à %time%
    echo Nom de la sauvegarde: %backup_name%
    echo.
    echo Contenu sauvegardé:
    if exist "backups\%backup_name%_facturacion.db" echo   ✅ Base de données
    if exist "backups\%backup_name%_config" echo   ✅ Configuration
    if exist "backups\%backup_name%_logs" echo   ✅ Logs
    if exist "backups\%backup_name%_custom" echo   ✅ Personnalisations
    echo.
    echo Pour restaurer cette sauvegarde:
    echo   1. Copier %backup_name%_facturacion.db vers facturacion.db
    echo   2. Copier le contenu de %backup_name%_config vers config\
    echo   3. Redémarrer l'application
) > "backups\%backup_name%_info.txt"

echo ✅ Fichier d'information créé
echo.

:: Afficher la taille de la sauvegarde
echo 📊 Informations sur la sauvegarde:
dir "backups\%backup_name%*" /B 2>nul | find /c /v "" > temp_count.txt
set /p file_count=<temp_count.txt
del temp_count.txt
echo   • Nombre de fichiers: %file_count%
echo   • Répertoire: backups\
echo   • Nom: %backup_name%
echo.

:: Nettoyer les anciennes sauvegardes (garder les 10 plus récentes)
echo 🧹 Nettoyage des anciennes sauvegardes...
for /f "skip=30 delims=" %%i in ('dir "backups\backup_*" /B /O:-D 2^>nul') do (
    del "backups\%%i" >nul 2>&1
)
echo ✅ Nettoyage terminé
echo.

echo ========================================
echo   🎉 SAUVEGARDE TERMINÉE AVEC SUCCÈS!
echo ========================================
echo.
echo Sauvegarde créée: %backup_name%
echo Répertoire: backups\
echo.
echo Pour restaurer cette sauvegarde plus tard:
echo   1. Exécuter restore.bat
echo   2. Ou copier manuellement les fichiers
echo.

echo Appuyez sur une touche pour fermer...
pause >nul
