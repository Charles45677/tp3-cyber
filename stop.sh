#!/bin/bash
# --rmi local supprime les images maison (build) mais JAMAIS les images de base
# frgagnon/ctf3-srv et frgagnon/ctf3-bot.
docker compose down --rmi local
