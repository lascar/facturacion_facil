#!/bin/bash
# Script para ejecutar comandos con el Python correcto (pyenv)

echo "🐍 Usando Python de pyenv..."
echo "Python version: $(~/.pyenv/shims/python --version)"
echo "Python path: $(which ~/.pyenv/shims/python)"
echo ""

# Ejecutar el comando pasado como argumentos
~/.pyenv/shims/python "$@"
