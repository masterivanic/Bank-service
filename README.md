![CI Tests](https://github.com/masterivanic/Bank-service/actions/workflows/python.yml/badge.svg)
![Coverage](https://img.shields.io/badge/dynamic/json?url=https://gist.githubusercontent.com/masterivanic/080dc9fbb8e45d7cfa7d596572e9bf62/raw/coverage.json&query=message&label=Coverage&color=blue)

# 💰 **Bank Account Kata** 💰

### 🧩 Feature 1 : Le compte bancaire

Un **compte bancaire** doit permettre les opérations de base suivantes :

* Posséder un **numéro de compte unique** (format libre)
* Gérer un **solde**
* Permettre le **dépôt d’argent**
* Permettre le **retrait d’argent**

**Règle métier :**
Un retrait ne peut pas être effectué s’il excède le solde disponible du compte.

---

### 💳 Feature 2 : Le découvert autorisé

Certains comptes bancaires peuvent bénéficier d’un **découvert autorisé**.

**Règle métier :**

* Si un compte dispose d’une autorisation de découvert, un retrait supérieur au solde du compte est autorisé **uniquement si** le solde final ne dépasse pas le montant de découvert autorisé.

---

### 💰 Feature 3 : Le livret d’épargne

Un **livret d’épargne** est un type particulier de compte bancaire avec des contraintes spécifiques :

* Il dispose d’un **plafond de dépôt** : on ne peut déposer d’argent que dans la limite de ce plafond (exemple : 22 950 € pour un livret A)
* Il **ne peut pas avoir de découvert autorisé**

---

### 📄 Feature 4 : Le relevé de compte

Un **relevé mensuel** doit pouvoir être généré pour chaque compte.
Ce relevé présente les informations suivantes :

* Le **type de compte** (Compte Courant ou Livret)
* Le **solde du compte** à la date d’émission du relevé
* La **liste des opérations** effectuées sur le mois, **triées par date décroissante**

---

## 🧱 Architecture cible

L’application doit suivre les principes de l’**architecture hexagonale** :

* Le **domaine** contient les règles métier pures
* Les **ports** définissent les interfaces pour interagir avec le domaine
* Les **adapteurs** implémentent ces interfaces (API REST, persistance, etc.)

---

![Architecture hexagonale](./assets/hexa-schema.png)
