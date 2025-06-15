#!/bin/bash
# Atualizar GeoIP DB Wazuh
# Victor Oliveira

ACCOUNT_ID="<YOUR-ACCOUNT-ID>"
LICENCE_KEY="<YOUR-LICENCE-KEY>"
DEST_DIR="/usr/share/wazuh-indexer/modules/ingest-geoip"
TMP_DIR="/tmp/geoip_update"

mkdir -p "$TMP_DIR"
cd "$TMP_DIR" || exit 1

declare -A DATABASES
DATABASES["GeoLite2-ASN"]="https://download.maxmind.com/geoip/databases/GeoLite2-ASN/download?suffix=tar.gz"
DATABASES["GeoLite2-City"]="https://download.maxmind.com/geoip/databases/GeoLite2-City/download?suffix=tar.gz"
DATABASES["GeoLite2-Country"]="https://download.maxmind.com/geoip/databases/GeoLite2-Country/download?suffix=tar.gz"

for DB in "${!DATABASES[@]}"; do
    URL="${DATABASES[$DB]}"
    FILE="${DB}.tar.gz"

    echo "Baixando $DB..."
    wget -q --content-disposition --user="$ACCOUNT_ID" --password="$LICENCE_KEY" -O "$FILE" "$URL"

    if [ ! -f "$FILE" ]; then
        echo "Erro: Falha no download de $DB"
        exit 1
    fi

    echo "Extraindo $FILE..."
    tar -xzf "$FILE"

    MMDB_PATH=$(find . -type f -name "$DB.mmdb" | head -n 1)

    if [ -z "$MMDB_PATH" ]; then
        echo "Erro: Arquivo $DB.mmdb não encontrado após extração."
        exit 1
    fi

    echo "Copiando $DB.mmdb para $DEST_DIR"
    cp "$MMDB_PATH" "$DEST_DIR/"
done

chown -R wazuh-indexer:wazuh-indexer "$DEST_DIR"
rm -rf "$TMP_DIR"
echo "Atualização concluída com sucesso!"
