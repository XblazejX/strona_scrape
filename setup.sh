#!/bin/bash

# Sprawdzamy, czy środowisko wirtualne zostało utworzone.
if [ ! -d "./venv" ]; then
    echo "Nie znaleziono katalogu 'venv'. Utwórz środowisko wirtualne poleceniem:"
    echo "python -m venv venv"
    exit 1
fi

# Aktywacja środowiska wirtualnego – sprawdzamy typ systemu
if [ -f "./venv/Scripts/activate" ]; then
    # Windows (Git Bash, VS Code terminal)
    echo "Aktywacja środowiska venv (Windows)..."
    source ./venv/Scripts/activate
elif [ -f "./venv/bin/activate" ]; then
    # Linux/macOS
    echo "Aktywacja środowiska venv (Linux/macOS)..."
    source ./venv/bin/activate
else
    echo "Nie znaleziono pliku aktywacyjnego środowiska venv."
    exit 1
fi

# Instalacja instaloader
echo "Instalacja pakietu instaloader..."
pip install instaloader

echo "Instalacja zakończona! Aby uruchomić skrypt, wpisz:"
echo "python scrape.py"
