# Justfile for mecab-ko-dic-admin

set shell := ["bash", "-c"]

# List available commands
default:
    @just --list

# --- Setup & Dependencies ---
install:
    uv sync

# --- Django Commands ---
run:
    uv run python manage.py runserver

migrate:
    uv run python manage.py migrate

makemigrations:
    uv run python manage.py makemigrations

shell:
    uv run python manage.py shell

superuser:
    uv run python manage.py createsuperuser

# --- Docker Infrastructure ---
up:
    docker-compose -f env/docker-compose.yaml up -d

down:
    docker-compose -f env/docker-compose.yaml down

build:
    docker-compose -f env/docker-compose.yaml up -d --build

logs:
    docker-compose -f env/docker-compose.yaml logs -f

ps:
    docker-compose -f env/docker-compose.yaml ps

# --- QA & Testing ---
test:
    uv run pytest

lint:
    uv run ruff check .

format:
    uv run ruff format .

# --- MeCab Build & Source Management ---
# 1. Update MeCab sources and required config scripts (Host side)
download-mecab:
    @echo "Updating MeCab-ko sources..."
    mkdir -p env/data/ubuntu/sources
    cd env/data/ubuntu/sources && \
    (git clone https://bitbucket.org/eunjeon/mecab-ko.git || (cd mecab-ko && git pull)) && \
    (git clone https://bitbucket.org/eunjeon/mecab-ko-lucene-analyzer.git || (cd mecab-ko-lucene-analyzer && git pull))
    @echo "Downloading mecab-ko-dic-2.1.1-20180720.tar.gz..."
    curl -L -o env/data/ubuntu/sources/mecab-ko-dic-2.1.1-20180720.tar.gz 'https://bitbucket.org/eunjeon/mecab-ko-dic/downloads/mecab-ko-dic-2.1.1-20180720.tar.gz'
    @echo "Updating architecture support scripts from GitHub mirror..."
    curl -L -o env/data/ubuntu/sources/mecab-ko/config.guess 'https://raw.githubusercontent.com/gcc-mirror/gcc/master/config.guess'
    curl -L -o env/data/ubuntu/sources/mecab-ko/config.sub 'https://raw.githubusercontent.com/gcc-mirror/gcc/master/config.sub'
    @echo "--------------------------------------------------------"
    @echo "MeCab sources and dictionary have been downloaded."
    @echo "--------------------------------------------------------"

# 2. Build MeCab inside the Ubuntu container (No network required)
build-mecab:
    @echo "Building MeCab inside existing Ubuntu container..."
    docker-compose -f env/docker-compose.yaml exec mecab_ko_dic_builder bash -c "\
        set -e; \
        echo '--- 1. Building mecab-ko (Engine) ---'; \
        cd sources/mecab-ko; \
        ./configure && make && sudo make install && sudo ldconfig; \
        \
        echo '--- 2. Building mecab-ko-dic (Dictionary) ---'; \
        cd ../mecab-ko-dic; \
        if [ -f ../mecab-ko-dic-2.1.1-20180720.tar.gz ]; then \
            echo 'Found manual tarball. Extracting and building...'; \
            tar zxf ../mecab-ko-dic-2.1.1-20180720.tar.gz --strip-components=1; \
            cp ../mecab-ko/config.guess . && cp ../mecab-ko/config.sub .; \
            ./autogen.sh; \
            ./configure --with-mecab-config=/usr/local/bin/mecab-config; \
            make && sudo make install; \
        else \
            echo 'ERROR: mecab-ko-dic-2.1.1-20180720.tar.gz not found in sources!'; \
            echo 'Please run: just download-mecab'; \
            exit 1; \
        fi; \
        \
        echo '--- 3. Final Test ---'; \
        mecab -v && echo '안녕하세요' | mecab"

# Access the builder container's shell for manual work
mecab-shell:
    docker-compose -f env/docker-compose.yaml exec mecab_ko_dic_builder bash

# --- Data Management ---
# Import all MeCab system dictionary CSV files
import-all:
    #!/usr/bin/env bash
    for csv_file in env/data/ubuntu/sources/mecab-ko-dic-2.1.1-20180720/*.csv; do
        echo "Importing system dic: $csv_file..."
        uv run python manage.py import_mecab_csv "$csv_file" --type SYSTEM
    done

# Import all MeCab user dictionary CSV files
import-user:
    #!/usr/bin/env bash
    for csv_file in env/data/ubuntu/sources/mecab-ko-dic-2.1.1-20180720/user-dic/*.csv; do
        echo "Importing user dic: $csv_file..."
        uv run python manage.py import_mecab_csv "$csv_file" --type USER
    done

# Export user-defined place names to CSV
export-user-places:
    uv run python manage.py export_mecab_csv "user-place-names.csv" --type USER --category "지명"
