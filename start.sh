#!/bin/sh
set -x
echo "hello from the Body Heat Service"
whoami
cd /home/paulo/body-heat
.venv/bin/python main.py
