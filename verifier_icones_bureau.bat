@echo off
chcp 65001 >nul
title Vérification Icônes Bureau - Facturación Fácil

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                🔍 VÉRIFICATION ICÔNES BUREAU                ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

set "BUREAU=%USERPROFILE%\Desktop"
set "ICONE_LANCEMENT=%BUREAU%\🚀 Facturación Fácil.lnk"
set "ICONE_UPDATE=%BUREAU%\🔄 Mise à Jour Facturación Fácil.lnk"

echo 🖥️  Bureau utilisateur: %BUREAU%
echo.

echo 🔍 Vérification des icônes sur le bureau...
echo.

:: Vérifier icône de lancement
if exist "%ICONE_LANCEMENT%" (
    echo ✅ Icône de lancement trouvée: 🚀 Facturación Fácil.lnk
    
    :: Vérifier que le raccourci pointe vers le bon endroit
    powershell -Command "
    try {
        $WshShell = New-Object -comObject WScript.Shell
        $Shortcut = $WshShell.CreateShortcut('%ICONE_LANCEMENT%')
        $Target = $Shortcut.TargetPath
        Write-Host '   📁 Pointe vers: ' -NoNewline -ForegroundColor Gray
        Write-Host $Target -ForegroundColor White
        if (Test-Path $Target) {
            Write-Host '   ✅ Fichier cible existe' -ForegroundColor Green
        } else {
            Write-Host '   ❌ Fichier cible manquant' -ForegroundColor Red
        }
    } catch {
        Write-Host '   ❌ Erreur lecture raccourci' -ForegroundColor Red
    }"
) else (
    echo ❌ Icône de lancement MANQUANTE: 🚀 Facturación Fácil.lnk
)

echo.

:: Vérifier icône de mise à jour
if exist "%ICONE_UPDATE%" (
    echo ✅ Icône de mise à jour trouvée: 🔄 Mise à Jour Facturación Fácil.lnk
    
    :: Vérifier que le raccourci pointe vers le bon endroit
    powershell -Command "
    try {
        $WshShell = New-Object -comObject WScript.Shell
        $Shortcut = $WshShell.CreateShortcut('%ICONE_UPDATE%')
        $Target = $Shortcut.TargetPath
        Write-Host '   📁 Pointe vers: ' -NoNewline -ForegroundColor Gray
        Write-Host $Target -ForegroundColor White
        if (Test-Path $Target) {
            Write-Host '   ✅ Fichier cible existe' -ForegroundColor Green
        } else {
            Write-Host '   ❌ Fichier cible manquant' -ForegroundColor Red
        }
    } catch {
        Write-Host '   ❌ Erreur lecture raccourci' -ForegroundColor Red
    }"
) else (
    echo ❌ Icône de mise à jour MANQUANTE: 🔄 Mise à Jour Facturación Fácil.lnk
)

echo.

:: Résumé
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                        📋 RÉSUMÉ                            ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

set ICONES_OK=0

if exist "%ICONE_LANCEMENT%" (
    set /a ICONES_OK+=1
    echo ✅ Icône de lancement: PRÉSENTE sur le bureau
) else (
    echo ❌ Icône de lancement: ABSENTE du bureau
)

if exist "%ICONE_UPDATE%" (
    set /a ICONES_OK+=1
    echo ✅ Icône de mise à jour: PRÉSENTE sur le bureau
) else (
    echo ❌ Icône de mise à jour: ABSENTE du bureau
)

echo.

if %ICONES_OK%==2 (
    echo 🎉 PARFAIT! Les 2 icônes sont sur le bureau
    echo.
    echo 💡 L'utilisateur peut maintenant:
    echo    • Double-cliquer sur 🚀 pour lancer l'application
    echo    • Double-cliquer sur 🔄 pour mettre à jour
    echo.
    echo 🎯 Mission accomplie!
) else if %ICONES_OK%==1 (
    echo ⚠️  PARTIEL: 1 icône sur 2 présente
    echo.
    echo 💡 Actions suggérées:
    echo    • Relancer creer_icones_bureau.bat
    echo    • Vérifier les permissions du bureau
) else (
    echo ❌ PROBLÈME: Aucune icône trouvée sur le bureau
    echo.
    echo 💡 Actions suggérées:
    echo    • Exécuter creer_icones_bureau.bat
    echo    • Vérifier les permissions
    echo    • Vérifier l'antivirus (peut bloquer la création)
)

echo.

:: Proposer des actions
if %ICONES_OK% LSS 2 (
    echo 🔧 Voulez-vous créer/recréer les icônes maintenant? (O/N)
    set /p recreer=
    if /i "%recreer%"=="O" if /i "%recreer%"=="o" (
        echo.
        echo 🔄 Lancement de la création des icônes...
        if exist "creer_icones_bureau.bat" (
            call creer_icones_bureau.bat
        ) else if exist "setup_icons.bat" (
            call setup_icons.bat
        ) else (
            echo ❌ Script de création non trouvé
            echo Assurez-vous d'être dans le bon dossier
        )
    )
)

echo.

:: Afficher le contenu du bureau (fichiers .lnk seulement)
echo 📂 Fichiers .lnk actuellement sur le bureau:
echo.
dir "%BUREAU%\*.lnk" /b 2>nul | findstr /i "factur" && (
    echo.
    echo ✅ Raccourcis Facturación trouvés ci-dessus
) || (
    echo ❌ Aucun raccourci Facturación trouvé
)

echo.
echo 🖥️  Pour voir les icônes, regardez directement sur votre bureau Windows
echo.

pause
