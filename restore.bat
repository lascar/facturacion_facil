@echo off
chcp 65001 >nul
title Restauration - Facturación Fácil

echo ========================================
echo   🔄 RESTAURATION - FACTURACIÓN FÁCIL
echo ========================================
echo.

:: Vérifier si le répertoire de sauvegarde existe
if not exist "backups" (
    echo ❌ ERREUR: Répertoire de sauvegarde non trouvé
    echo Aucune sauvegarde disponible
    echo.
    pause
    exit /b 1
)

:: Lister les sauvegardes disponibles
echo 📋 Sauvegardes disponibles:
echo.
set count=0
for /f "delims=" %%i in ('dir "backups\backup_*_info.txt" /B /O:-D 2^>nul') do (
    set /a count+=1
    set backup!count!=%%~ni
    echo   !count!. %%~ni
    
    :: Afficher les informations de la sauvegarde
    if exist "backups\%%i" (
        for /f "tokens=1,* delims=:" %%a in ('findstr "créée le" "backups\%%i"') do (
            echo      Date: %%b
        )
    )
    echo.
)

if %count%==0 (
    echo ❌ Aucune sauvegarde trouvée
    echo.
    pause
    exit /b 1
)

:: Demander quelle sauvegarde restaurer
echo Quelle sauvegarde voulez-vous restaurer? (1-%count% ou 0 pour annuler)
set /p choice=

if "%choice%"=="0" (
    echo Restauration annulée
    pause
    exit /b 0
)

:: Vérifier que le choix est valide
if %choice% LSS 1 goto invalid_choice
if %choice% GTR %count% goto invalid_choice

:: Obtenir le nom de la sauvegarde sélectionnée
call set selected_backup=%%backup%choice%%%

echo.
echo 📋 Sauvegarde sélectionnée: %selected_backup%
echo.

:: Afficher les détails de la sauvegarde
if exist "backups\%selected_backup%_info.txt" (
    echo 📄 Détails de la sauvegarde:
    type "backups\%selected_backup%_info.txt"
    echo.
)

:: Demander confirmation
echo ⚠️  ATTENTION: Cette opération va remplacer les données actuelles
echo Voulez-vous continuer? (O/N)
set /p confirm=
if /i not "%confirm%"=="O" if /i not "%confirm%"=="o" (
    echo Restauration annulée
    pause
    exit /b 0
)

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
echo 🔄 Restauration en cours...
echo.

:: Sauvegarder les données actuelles avant restauration
echo 💾 Sauvegarde des données actuelles...
for /f "tokens=2-4 delims=/ " %%a in ('date /t') do (
    for /f "tokens=1-2 delims=: " %%d in ('time /t') do (
        set datetime=%%c%%a%%b_%%d%%e
    )
)

if exist "facturacion.db" (
    copy "facturacion.db" "facturacion_before_restore_%datetime%.db" >nul
    echo ✅ Données actuelles sauvegardées: facturacion_before_restore_%datetime%.db
)

:: Restaurer la base de données
if exist "backups\%selected_backup%_facturacion.db" (
    echo 💾 Restauration de la base de données...
    copy "backups\%selected_backup%_facturacion.db" "facturacion.db" >nul
    if errorlevel 1 (
        echo ❌ ERREUR: Impossible de restaurer la base de données
    ) else (
        echo ✅ Base de données restaurée
    )
) else (
    echo ⚠️  Base de données de sauvegarde non trouvée
)

:: Restaurer la configuration
if exist "backups\%selected_backup%_config" (
    echo 📋 Restauration de la configuration...
    if exist "config" rmdir /S /Q "config" >nul 2>&1
    xcopy "backups\%selected_backup%_config" "config\" /E /I /Q >nul 2>&1
    if errorlevel 1 (
        echo ⚠️  Problème lors de la restauration de la configuration
    ) else (
        echo ✅ Configuration restaurée
    )
)

:: Restaurer les personnalisations
if exist "backups\%selected_backup%_custom" (
    echo 🎨 Restauration des personnalisations...
    if exist "custom" rmdir /S /Q "custom" >nul 2>&1
    xcopy "backups\%selected_backup%_custom" "custom\" /E /I /Q >nul 2>&1
    if errorlevel 1 (
        echo ⚠️  Problème lors de la restauration des personnalisations
    ) else (
        echo ✅ Personnalisations restaurées
    )
)

echo.
echo ========================================
echo   🎉 RESTAURATION TERMINÉE AVEC SUCCÈS!
echo ========================================
echo.
echo Sauvegarde restaurée: %selected_backup%
echo.
echo Données précédentes sauvegardées dans:
echo   facturacion_before_restore_%datetime%.db
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
exit /b 0

:invalid_choice
echo ❌ Choix invalide
echo.
pause
exit /b 1
