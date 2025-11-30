@echo off
chcp 65001 >nul
title Test des Icônes Bureau - Facturación Fácil

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                    🧪 TEST DES ICÔNES                       ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

set "BUREAU=%USERPROFILE%\Desktop"

echo 🖥️  Bureau utilisateur: %BUREAU%
echo.

echo 🔍 Recherche des icônes Facturación Fácil sur le bureau...
echo.

:: Compter les icônes trouvées
set ICONES_TROUVEES=0

:: Vérifier les différents types de fichiers possibles
echo 📋 Fichiers trouvés sur le bureau:
echo.

:: Fichiers .bat avec émojis
if exist "%BUREAU%\🚀 Lancer Facturacion Facil.bat" (
    echo ✅ 🚀 Lancer Facturacion Facil.bat
    set /a ICONES_TROUVEES+=1
)

if exist "%BUREAU%\🔄 Mettre a Jour Facturacion Facil.bat" (
    echo ✅ 🔄 Mettre a Jour Facturacion Facil.bat
    set /a ICONES_TROUVEES+=1
)

:: Fichiers .lnk
if exist "%BUREAU%\Facturacion Facil.lnk" (
    echo ✅ Facturacion Facil.lnk
    set /a ICONES_TROUVEES+=1
)

if exist "%BUREAU%\Mise a Jour Facturacion Facil.lnk" (
    echo ✅ Mise a Jour Facturacion Facil.lnk
    set /a ICONES_TROUVEES+=1
)

:: Autres variantes possibles
if exist "%BUREAU%\Facturación Fácil.lnk" (
    echo ✅ Facturación Fácil.lnk
    set /a ICONES_TROUVEES+=1
)

if exist "%BUREAU%\🚀 Facturación Fácil.lnk" (
    echo ✅ 🚀 Facturación Fácil.lnk
    set /a ICONES_TROUVEES+=1
)

if exist "%BUREAU%\🔄 Mise à Jour Facturación Fácil.lnk" (
    echo ✅ 🔄 Mise à Jour Facturación Fácil.lnk
    set /a ICONES_TROUVEES+=1
)

echo.

:: Résumé
if %ICONES_TROUVEES%==0 (
    echo ❌ AUCUNE ICÔNE TROUVÉE sur le bureau
    echo.
    echo 💡 Solutions:
    echo    1. Exécuter creer_icones_simple.bat
    echo    2. Exécuter creer_icones_natif.bat
    echo    3. Vérifier les permissions du bureau
    echo.
    
) else (
    echo ✅ %ICONES_TROUVEES% icône(s) trouvée(s) sur le bureau
    echo.
    echo 🎉 SUCCÈS! L'utilisateur a des icônes pour utiliser l'application
)

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                    🔧 ACTIONS DISPONIBLES                   ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

echo Que voulez-vous faire?
echo.
echo   1. 🔄 Recréer les icônes (méthode simple)
echo   2. 🔧 Recréer les icônes (méthode native)
echo   3. 🖥️  Ouvrir le bureau pour voir les icônes
echo   4. 📋 Lister tous les fichiers .lnk et .bat du bureau
echo   5. 🧹 Nettoyer les anciennes icônes
echo   6. ❌ Quitter
echo.

set /p choix="Votre choix (1-6): "

if "%choix%"=="1" (
    echo.
    echo 🔄 Lancement de la création simple...
    if exist "creer_icones_simple.bat" (
        call creer_icones_simple.bat
    ) else (
        echo ❌ creer_icones_simple.bat non trouvé
    )
    
) else if "%choix%"=="2" (
    echo.
    echo 🔧 Lancement de la création native...
    if exist "creer_icones_natif.bat" (
        call creer_icones_natif.bat
    ) else (
        echo ❌ creer_icones_natif.bat non trouvé
    )
    
) else if "%choix%"=="3" (
    echo.
    echo 🖥️  Ouverture du bureau...
    explorer "%BUREAU%"
    
) else if "%choix%"=="4" (
    echo.
    echo 📋 Tous les fichiers .lnk sur le bureau:
    dir "%BUREAU%\*.lnk" /b 2>nul | findstr /v "^$" || echo Aucun fichier .lnk trouvé
    echo.
    echo 📋 Tous les fichiers .bat sur le bureau:
    dir "%BUREAU%\*.bat" /b 2>nul | findstr /v "^$" || echo Aucun fichier .bat trouvé
    
) else if "%choix%"=="5" (
    echo.
    echo 🧹 Nettoyage des anciennes icônes...
    
    :: Supprimer les anciennes icônes
    del "%BUREAU%\🚀 Lancer Facturacion Facil.bat" >nul 2>&1
    del "%BUREAU%\🔄 Mettre a Jour Facturacion Facil.bat" >nul 2>&1
    del "%BUREAU%\Facturacion Facil.lnk" >nul 2>&1
    del "%BUREAU%\Mise a Jour Facturacion Facil.lnk" >nul 2>&1
    del "%BUREAU%\Facturación Fácil.lnk" >nul 2>&1
    del "%BUREAU%\🚀 Facturación Fácil.lnk" >nul 2>&1
    del "%BUREAU%\🔄 Mise à Jour Facturación Fácil.lnk" >nul 2>&1
    
    echo ✅ Nettoyage terminé
    echo 💡 Vous pouvez maintenant recréer les icônes proprement
    
) else if "%choix%"=="6" (
    echo Sortie...
    timeout /t 1 /nobreak >nul
    exit /b 0
    
) else (
    echo ❌ Choix invalide
)

echo.
echo 🔄 Nouvelle vérification...
echo.

:: Revérifier après l'action
set ICONES_FINALES=0

if exist "%BUREAU%\🚀 Lancer Facturacion Facil.bat" set /a ICONES_FINALES+=1
if exist "%BUREAU%\🔄 Mettre a Jour Facturacion Facil.bat" set /a ICONES_FINALES+=1
if exist "%BUREAU%\Facturacion Facil.lnk" set /a ICONES_FINALES+=1
if exist "%BUREAU%\Mise a Jour Facturacion Facil.lnk" set /a ICONES_FINALES+=1
if exist "%BUREAU%\Facturación Fácil.lnk" set /a ICONES_FINALES+=1
if exist "%BUREAU%\🚀 Facturación Fácil.lnk" set /a ICONES_FINALES+=1
if exist "%BUREAU%\🔄 Mise à Jour Facturación Fácil.lnk" set /a ICONES_FINALES+=1

if %ICONES_FINALES% GTR 0 (
    echo ✅ %ICONES_FINALES% icône(s) maintenant présente(s) sur le bureau
    echo.
    echo 🎯 MISSION ACCOMPLIE!
    echo    L'utilisateur peut maintenant double-cliquer sur les icônes
    echo    de son bureau pour utiliser l'application!
) else (
    echo ❌ Aucune icône trouvée après l'action
    echo.
    echo 💡 Essayez une autre méthode ou vérifiez les permissions
)

echo.
pause
