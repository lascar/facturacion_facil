@echo off
chcp 65001 >nul
title Diagnostic Bureau - Facturación Fácil

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                    🔍 DIAGNOSTIC BUREAU                     ║
echo ║                  Pourquoi les icônes n'apparaissent pas?    ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

echo 🔍 Analyse du système pour trouver pourquoi les icônes n'apparaissent pas...
echo.

:: 1. DÉTECTER LES CHEMINS DU BUREAU
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                    1. CHEMINS DU BUREAU                     ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

set "BUREAU_TROUVE=NON"

echo 📁 Test des chemins possibles du bureau:
echo.

:: Chemin standard anglais
if exist "%USERPROFILE%\Desktop" (
    echo ✅ %USERPROFILE%\Desktop - EXISTE
    set "BUREAU_PRINCIPAL=%USERPROFILE%\Desktop"
    set "BUREAU_TROUVE=OUI"
) else (
    echo ❌ %USERPROFILE%\Desktop - N'EXISTE PAS
)

:: Chemin espagnol
if exist "%USERPROFILE%\Escritorio" (
    echo ✅ %USERPROFILE%\Escritorio - EXISTE
    set "BUREAU_PRINCIPAL=%USERPROFILE%\Escritorio"
    set "BUREAU_TROUVE=OUI"
) else (
    echo ❌ %USERPROFILE%\Escritorio - N'EXISTE PAS
)

:: Chemin public
if exist "%PUBLIC%\Desktop" (
    echo ✅ %PUBLIC%\Desktop - EXISTE (bureau public)
) else (
    echo ❌ %PUBLIC%\Desktop - N'EXISTE PAS
)

:: Autres chemins
if exist "%HOMEDRIVE%%HOMEPATH%\Desktop" (
    echo ✅ %HOMEDRIVE%%HOMEPATH%\Desktop - EXISTE
) else (
    echo ❌ %HOMEDRIVE%%HOMEPATH%\Desktop - N'EXISTE PAS
)

echo.

if "%BUREAU_TROUVE%"=="NON" (
    echo ❌ PROBLÈME: Aucun bureau trouvé!
    echo.
    echo 💡 Solutions:
    echo    • Vérifiez la langue de votre Windows
    echo    • Le bureau peut avoir un nom différent
    echo.
    pause
    exit /b 1
) else (
    echo ✅ Bureau principal détecté: %BUREAU_PRINCIPAL%
)

echo.

:: 2. TESTER LES PERMISSIONS
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                    2. TEST DES PERMISSIONS                  ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

echo 🔐 Test d'écriture sur le bureau...

:: Créer un fichier de test
echo Test > "%BUREAU_PRINCIPAL%\test_facturacion.txt" 2>nul

if exist "%BUREAU_PRINCIPAL%\test_facturacion.txt" (
    echo ✅ PERMISSIONS OK - Peut écrire sur le bureau
    del "%BUREAU_PRINCIPAL%\test_facturacion.txt" >nul 2>&1
) else (
    echo ❌ PERMISSIONS INSUFFISANTES - Ne peut pas écrire sur le bureau
    echo.
    echo 💡 Solutions:
    echo    • Exécuter ce script en tant qu'administrateur
    echo    • Clic droit → "Exécuter en tant qu'administrateur"
    echo    • Vérifier les paramètres de sécurité Windows
)

echo.

:: 3. DÉTECTER L'ANTIVIRUS
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                    3. DÉTECTION ANTIVIRUS                   ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

echo 🛡️  Recherche d'antivirus actifs...

:: Vérifier Windows Defender
sc query WinDefend >nul 2>&1
if %errorlevel%==0 (
    echo ✅ Windows Defender détecté
    echo    💡 Peut bloquer la création de fichiers .bat/.lnk
)

:: Vérifier d'autres antivirus courants
tasklist /FI "IMAGENAME eq avp.exe" 2>nul | find /I "avp.exe" >nul && echo ✅ Kaspersky détecté
tasklist /FI "IMAGENAME eq avgui.exe" 2>nul | find /I "avgui.exe" >nul && echo ✅ AVG détecté
tasklist /FI "IMAGENAME eq avguard.exe" 2>nul | find /I "avguard.exe" >nul && echo ✅ Avira détecté
tasklist /FI "IMAGENAME eq mcshield.exe" 2>nul | find /I "mcshield.exe" >nul && echo ✅ McAfee détecté

echo.
echo 💡 Si un antivirus est détecté:
echo    • Ajouter le dossier de l'application aux exceptions
echo    • Désactiver temporairement la protection en temps réel
echo    • Autoriser la création de fichiers .bat et .lnk

echo.

:: 4. TESTER LA CRÉATION D'ICÔNES
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                    4. TEST CRÉATION ICÔNES                  ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

echo 🧪 Test de création d'icônes...

:: Test 1: Fichier .bat simple
echo @echo off > "%BUREAU_PRINCIPAL%\TEST_FACTURACION.bat"
echo echo Test Facturacion Facil >> "%BUREAU_PRINCIPAL%\TEST_FACTURACION.bat"
echo pause >> "%BUREAU_PRINCIPAL%\TEST_FACTURACION.bat"

if exist "%BUREAU_PRINCIPAL%\TEST_FACTURACION.bat" (
    echo ✅ Création fichier .bat: SUCCÈS
    del "%BUREAU_PRINCIPAL%\TEST_FACTURACION.bat" >nul 2>&1
) else (
    echo ❌ Création fichier .bat: ÉCHEC
)

:: Test 2: Raccourci .lnk avec PowerShell
powershell -ExecutionPolicy Bypass -NoProfile -Command "try { $ws = New-Object -ComObject WScript.Shell; $s = $ws.CreateShortcut('%BUREAU_PRINCIPAL%\TEST_RACCOURCI.lnk'); $s.TargetPath = 'notepad.exe'; $s.Save(); Write-Host 'OK' } catch { Write-Host 'ERREUR' }" >nul 2>&1

if exist "%BUREAU_PRINCIPAL%\TEST_RACCOURCI.lnk" (
    echo ✅ Création raccourci .lnk: SUCCÈS
    del "%BUREAU_PRINCIPAL%\TEST_RACCOURCI.lnk" >nul 2>&1
) else (
    echo ❌ Création raccourci .lnk: ÉCHEC
)

echo.

:: 5. VÉRIFIER LES PARAMÈTRES D'AFFICHAGE
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                    5. PARAMÈTRES D'AFFICHAGE                ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

echo 🖥️  Vérification des paramètres d'affichage du bureau...

:: Vérifier si les icônes du bureau sont masquées
reg query "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced" /v HideIcons >nul 2>&1
if %errorlevel%==0 (
    for /f "tokens=3" %%a in ('reg query "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced" /v HideIcons 2^>nul') do (
        if "%%a"=="0x1" (
            echo ❌ PROBLÈME: Les icônes du bureau sont MASQUÉES
            echo.
            echo 💡 Solution:
            echo    • Clic droit sur le bureau
            echo    • Affichage → Afficher les éléments du bureau
        ) else (
            echo ✅ Les icônes du bureau sont visibles
        )
    )
) else (
    echo ✅ Paramètres d'affichage normaux
)

echo.

:: 6. RÉSUMÉ ET SOLUTIONS
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                    6. RÉSUMÉ ET SOLUTIONS                   ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

echo 📋 RÉSUMÉ DU DIAGNOSTIC:
echo.
echo    🖥️  Bureau détecté: %BUREAU_PRINCIPAL%
echo    🔐 Permissions: Testées ci-dessus
echo    🛡️  Antivirus: Vérifié ci-dessus
echo    🧪 Tests création: Effectués ci-dessus
echo.

echo 💡 SOLUTIONS RECOMMANDÉES:
echo.
echo    1. 🔧 Exécuter forcer_icones_bureau.bat en tant qu'administrateur
echo    2. 🛡️  Ajouter le dossier aux exceptions de l'antivirus
echo    3. 🖥️  Vérifier que les icônes du bureau ne sont pas masquées
echo    4. 🔄 Actualiser le bureau (F5 ou clic droit → Actualiser)
echo    5. 📁 Ouvrir manuellement le dossier du bureau pour voir les fichiers
echo.

echo 🎯 ACTIONS IMMÉDIATES:
echo.
echo    A. Exécuter forcer_icones_bureau.bat
echo    B. Ouvrir le bureau pour vérifier
echo    C. Actualiser le bureau (F5)
echo.

set /p action="Voulez-vous ouvrir le bureau maintenant? (O/N): "
if /i "%action%"=="O" if /i "%action%"=="o" (
    echo 🖥️  Ouverture du bureau...
    explorer "%BUREAU_PRINCIPAL%"
)

echo.
echo 🔄 Voulez-vous exécuter forcer_icones_bureau.bat maintenant? (O/N)
set /p forcer=
if /i "%forcer%"=="O" if /i "%forcer%"=="o" (
    if exist "forcer_icones_bureau.bat" (
        echo 🚀 Lancement de forcer_icones_bureau.bat...
        call forcer_icones_bureau.bat
    ) else (
        echo ❌ forcer_icones_bureau.bat non trouvé dans ce dossier
    )
)

echo.
pause
