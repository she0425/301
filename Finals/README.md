# Contactly — Contact Management System

**Contactly** is a contact management web application built with HTML5, CSS3, Vanilla JavaScript, and a **Node.js + Express + SQLite** backend. It provides authentication screens, dashboard statistics, a searchable and filterable contact directory, favorites, categories, account settings, and contact photo uploads.

---

## Project Team & Academic Information

Developed and submitted as a **Final Major Course Output (MCO)** by **BSCS-3C** students:

* **Odeza Len A. Verzosa**
* **Sheraica Mae P. Nobela**
* **Joycel D. Basita**

---

## Features

* **Authentication Screens:** Login (`index.html`), account registration (`register.html`), and local password recovery (`forgot-password.html`) with password visibility toggles and form status feedback.
* **Dashboard (`dashboard.html`):** Displays summary cards for total contacts, favorites, and contacts added this week alongside a recently added connections list.
* **Contacts Directory (`contacts.html`):** Create, view, edit, favorite, and delete contacts with live search, category filtering, sorting (`Newest first`, `Oldest first`, `Name A–Z`, `Name Z–A`), and a `?recent=1` view.
* **Contact Photo Uploads:** Upload image files (with live preview and file-size validation) or enter a photo URL when adding or editing contacts.
* **Categories (`categories.html`):** Add, view, and organize custom categories for grouping contacts.
* **Favorites (`favorites.html`):** View and manage starred contacts in a dedicated shortlist view.
* **Account Settings (`settings.html`):** Update profile information, change account passwords, and access account deletion controls.
* **SQLite Database & File Uploads (`server/`):** Uses `sqlite3` to store data in `server/contactly.db` (`users`, `categories`, and `contacts` tables) and saves uploaded photos to `server/uploads/`.


Tech Stack
Frontend: HTML5, CSS3, Vanilla JavaScript
Backend: Node.js, Express, Multer, CORS
Database: SQLite (sqlite3 with server/contactly.db)

Running Locally
Navigate to the project directory:

PowerShell
cd "C:\Users\DELL\Documents\CS 3RD YEAR\contact-management-system"

Install server dependencies and start the Express server:
PowerShell
cd server
npx expo install react-dom
Open http://localhost:3000/contacts.html (or http://localhost:3000/index.html) in your web browser.
npm install
node server.js
npx expo start
Open http://localhost:3000/contacts.html (or http://localhost:3000/index.html) in your web browser.
