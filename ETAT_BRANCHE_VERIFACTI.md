# État de la branche `verifacti`

> **Date :** 2026-10-25
> **Branche :** `verifacti`
> **Branche principale de comparaison :** `master` (pas de branche `main` locale)

---

## Position par rapport à `master`

Les branches ont **divergé**.

**Commits sur `verifacti` (absents de `master`) :**

| Commit | Description |
|---|---|
| `3338789` | verifactu 1 |
| `4efe746` | Retirer les `__pycache__` / `*.pyc` du suivi git |
| `7895140` | feat(verifactu) : inclure le QR Verifacti dans le PDF |

**Commits sur `master` (absents de `verifacti`) :**

| Commit | Description |
|---|---|
| `b2ad8f9` | stock négatif |
| `ff9c4d6` | Retirer les `__pycache__` / `*.pyc` du suivi |

⚠️ La branche ne contient donc **pas** le correctif « stock négatif » de `master`.

## Contenu de la branche (~5 144 lignes ajoutées vs `master`)

Fonctionnalité **Verifacti** (délégation à l'API tiers verifacti.com, pas
d'implémentation directe du protocole AEAT) :

- `services/verifacti_service.py` (+381) — client HTTP (`requests`), envoi/statut/santé
- `ui/verifacti_config_dialog.py` (+235) — dialogue de configuration
- `ui/verifacti_factura_handler.py` (+362) — gestion envoi/renvoi, archivage
- `ui/facturas_pyqt5.py` (+97) — bouton envoi dans le détail facture
- `ui/organizacion_pyqt5.py` (+47) — entrée configuration
- `utils/pdf_generator.py` (~90 lignes) — affichage du QR dans le PDF
- `requirements.txt` (+1 dépendance : `requests`)
- `database/migration_manager.py` — colonnes `estado_verifacti`, `qr_verifacti`, `uuid_verifacti`, `fecha_envio_verifacti`

## État fonctionnel

**Partiellement fonctionnel — jamais testé contre l'API réelle.**

Fonctionne (en tant que code) :

- Câblage UI complet (boutons, dialogue, détail facture)
- Client HTTP réel (pas une simulation)
- Logique d'archivage `verifacti/{enviadas,pendientes,errores}`
- Migration BDD + affichage QR dans le PDF

Manque / bloquant :

1. **URL de l'API non vérifiée** — `https://api.verifacti.com` hardcodé
   (`services/verifacti_service.py:25`), contrat deviné
2. **Aucune configuration** — clé `verifacti` absente de `config/config.json`,
   fonctionnalité désactivée (`habilitado=False`)
3. **Zéro envoi réel** — dossiers `verifacti/` vides, aucune trace dans les logs
4. **Zéro test automatisé** — rien dans `test/`
5. **BDD de production non migrée** — colonnes absentes de
   `base_de_datos/facturacion.db` (migrations exécutées uniquement sur BDD de test)
6. **Protocole AEAT non implémenté localement** — pas de chaînage de hachage,
   pas de `QRCodeUID`, pas de déclaration du sistema informático
7. Code mort : `consultar_estado_factura` importé mais jamais appelé ;
   NIF émetteur collecté dans le dialogue jamais envoyé

## Tâches avant fusion vers `master`

1. Tester avec une vraie clé API (tâche n°1 de `VERIFACTI_STATUS.md`)
2. Vérifier l'URL/les endpoints de l'API
3. Appliquer la migration sur la BDD de production
4. Écrire des tests
5. Rebaser/merger `master` (récupérer « stock négatif »)
6. Trancher le sort de `docs/verifactu/` (supprimé de l'index dans cette branche,
   alors que la branche l'ajoute par rapport à `master`)
