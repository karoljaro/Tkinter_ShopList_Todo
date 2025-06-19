# Tkinter ShopList Todo

![Tests](https://github.com/karoljaro/Tkinter_ShopList_Todo/workflows/Tests/badge.svg)
![Code Quality](https://github.com/karoljaro/Tkinter_ShopList_Todo/workflows/Code%20Quality/badge.svg)

## Opis projektu

Celem projektu jest stworzenie aplikacji do zarządzania listą zakupów z wykorzystaniem biblioteki Tkinter. Aplikacja pozwala na dodawanie, edytowanie oraz usuwanie produktów z listy. Użytkownik ma również możliwość zaznaczania produktów jako kupione.

### ✨ Funkcjonalności AI

Aplikacja zawiera inteligentny system normalizacji nazw produktów:
- **Automatyczne poprawki nazw** - AI sprawdza i poprawia polskie błędy ortograficzne
- **Uczenie się od użytkownika** - AI zapamiętuje preferencje i poprawki użytkownika  
- **Inteligentne sugestie** - przy dodawaniu produktów AI proponuje lepsze nazwy
- **Słownik uczący się** - możliwość ręcznego dodawania własnych poprawek

Zakres projektu obejmuje:
- Tworzenie listy zakupów
- Edytowanie produktów na liście
- Usuwanie produktów z listy
- Zaznaczanie i odznaczanie produktów jako kupione
- **🤖 AI-powered normalizacja nazw produktów**
- **📚 Uczenie się systemu od użytkownika**

Oczekiwane rezultaty to funkcjonalna aplikacja, która ułatwi zarządzanie listą zakupów.

## Technologie

- **Python** (język programowania)
- **Tkinter** (standardowa biblioteka GUI)
- **CustomTkinter** (nowoczesne widgety GUI)
- **Pydantic** (walidacja danych i modele)
- **Mypy** (sprawdzanie typów statycznych)
- **Black** (formatowanie kodu)
- **Flake8** (linting)
- **AI Services** (normalizacja nazw produktów)

## Architektura

Projekt został zaprojektowany z wykorzystaniem architektury warstwowej, co pozwala na lepsze zarządzanie kodem i jego skalowalność. Architektura składa się z następujących warstw:

- **src/application**: Logika biznesowa aplikacji. Zawiera przypadki użycia i interfejsy repozytoriów.
- **src/domain**: Warstwa domenowa, która zawiera encje i logikę domenową.
- **src/infrastructure**: Implementacje repozytoriów, serwisy AI oraz inne usługi zewnętrzne.
- **src/presentation**: Warstwa prezentacji, która zawiera kontrolery, widoki i widgety.

### Struktura plików/folderów całego projektu
```
Tkinter_ShopList_Todo/
├── assets/
│   └── icon.ico
├── src/
│   ├── application/
│   │   ├── dto/
│   │   │   └── ProductDTO.py
│   │   ├── repositories/
│   │   │   └── IProductRepository.py
│   │   ├── usecases/
│   │   │   ├── AddProduct.py
│   │   │   ├── GetAllProducts.py
│   │   │   ├── GetProductById.py
│   │   │   ├── RemoveProduct.py
│   │   │   └── UpdateProduct.py
│   │   └── __init__.py
│   ├── domain/
│   │   ├── Product_Entity.py
│   │   └── __init__.py
│   ├── infrastructure/
│   │   ├── data/
│   │   │   └── products.json
│   │   ├── services/
│   │   │   └── ProductNameNormalizationService.py
│   │   ├── InMemoryProductRepository.py
│   │   ├── JsonProductRepository.py
│   │   └── __init__.py
│   ├── presentation/
│   │   ├── controllers/
│   │   │   └── ProductController.py
│   │   ├── views/
│   │   │   └── main.py
│   │   ├── widgets/
│   │   │   ├── ctk_listbox.py
│   │   │   └── tkinter_app_widgets.py
│   │   └── __init__.py
│   ├── utils/
│   │   ├── errorHandlerDecorator.py
│   │   ├── purchaseStatus.py
│   │   └── __init__.py
│   └── __init__.py
├── tests/
│   ├── application/
│   │   ├── test_AddProduct_usecase.py
│   │   ├── test_GetAllProduct_usecase.py
│   │   ├── test_GetProductById_usecase.py
│   │   ├── test_HandleExceptions_util.py
│   │   ├── test_ProductDTO_dto.py
│   │   ├── test_RemoveProduct_usecase.py
│   │   ├── test_UpdateProduct_usecase.py
│   ├── domain/
│   │   └── test_product_entity.py
│   ├── infrastructure/
│   │   ├── test_InMemoryProductRepository.py
│   │   └── test_JsonProductRepository.py
│   ├── presentation/
│   │   └── test_ProductController.py
│   ├── utils/
│   │   ├── test_purchaseStatus.py
│   │   └── __init__.py
│   └── __init__.py
├── .gitignore
├── LICENSE
├── README.md
├── requirements.txt
├── mypy.ini
├── pyproject.toml
├── setup.cfg
└── data/
    └── learned_typos.json
```

### Dlaczego taka architektura?

Architektura Clean Architecture została wybrana, aby oddzielić logikę biznesową od warstwy prezentacji i dostępu do danych. Dzięki temu kod jest bardziej czytelny, łatwiejszy do testowania oraz utrzymania.

## 🤖 Funkcjonalności AI

Aplikacja zawiera zaawansowany system normalizacji nazw produktów oparty na uczeniu maszynowym:

### Automatyczne poprawki
- **Polskie błędy ortograficzne**: `mlko` → `mleko`, `chlb` → `chleb`
- **Standaryzacja marek**: `coca cola` → `Coca-Cola`
- **Proper capitalization**: automatyczna kapitalizacja nazw

### Inteligentne sugestie
- **Fuzzy matching**: AI znajduje podobne słowa z bazy danych
- **Confidence scoring**: system pewności dla każdej sugestii (0-100%)
- **Multiple suggestions**: pokazuje kilka opcji do wyboru

### Uczenie się od użytkownika
- **Słownik uczący się**: zapisuje poprawki do `data/learned_typos.json`
- **Automatyczne uczenie**: AI uczy się z wyborów użytkownika
- **Ręczne dodawanie**: przycisk "🧠 Add to Dictionary"

### Interfejs użytkownika
- **✨ Fix Name**: przycisk do poprawy aktualnej nazwy
- **🧠 Add to Dictionary**: ręczne dodawanie poprawek
- **Smart dialogs**: okna wyboru z wieloma sugestiami
- **Auto-suggest**: automatyczne sugestie przy dodawaniu produktów

## Instalacja

### Pobieranie i wypakowywanie projektu

Po pobraniu i wypakowaniu projektu, przejdź do folderu z projektem:

```bash
cd Tkinter_ShopList_Todo
```

### Sprawdzenie wersji Pythona

> [!IMPORTANT] 
> Przed instalacją upewnij się, że masz zainstalowanego Pythona w wersji 3.13 lub wyższej.

Wersje pythona możesz sprawdzić, uruchamiając poniższe polecenie:

```bash
# Windows/macOS/Linux
py --version

# lub

python3 --version
```

### Wymagania dla bazy danych (opcjonalnie)

> [!NOTE]
> Jeśli chcesz używać PostgreSQL zamiast plików JSON, potrzebujesz:
> - **Docker** i **Docker Compose** (zalecane)
> - LUB lokalnie zainstalowany **PostgreSQL**

### Tworzenie wirtualnego środowiska

Aby stworzyć wirtualne środowisko, uruchom poniższe polecenie:

```bash
# Windows/macOS/Linux
py -m venv venv

# lub

python3 -m venv venv
```

### Aktywacja wirtualnego środowiska

Po utworzeniu wirtualnego środowiska, aktywuj je:


#### Windows:
> [!IMPORTANT] 
> Upewnij się, że w **Windows** aktywujesz wirtualne środowko za pomocą `cmd`, a nie `PowerShell`, aby uniknąć błędów dotyczących polityki uruchamiania skryptów w PowerShell
```bash
venv\Scripts\activate
```

#### macOS/Linux:
```bash
source venv/bin/activate
```

### Instalacja dependencies

Aby zainstalować wymagane dependencies, uruchom poniższe polecenie:

```bash
pip install -r requirements.txt
```

## 🐳 Konfiguracja bazy danych PostgreSQL (Docker)

Aplikacja obsługuje różne typy repozytoriów: **InMemory**, **JSON** oraz **PostgreSQL**. Dla pełnej funkcjonalności zalecane jest użycie PostgreSQL.

### Krok 1: Uruchomienie PostgreSQL w Docker

Projekt zawiera gotowy `docker-compose.yml` z konfiguracją PostgreSQL.

```bash
# Uruchom PostgreSQL w tle
docker-compose up -d

# Sprawdź status kontenerów
docker-compose ps

# Zatrzymaj kontenery
docker-compose down
```

### Krok 2: Konfiguracja zmiennych środowiskowych

1. **Skopiuj plik przykładowy**:
```bash
# Windows
copy .env.example .env

# macOS/Linux
cp .env.example .env
```

2. **Edytuj plik `.env`** (opcjonalnie):
```bash
# Repository Configuration
REPOSITORY_TYPE=postgresql

# PostgreSQL Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=shoplist
DB_USER=shoplist_user
DB_PASSWORD=shoplist_pass

# Optional: Enable debug logging
DEBUG=true
```

### Tryby repozytoriów

Możesz zmienić typ repozytorium w pliku `.env`:

- `REPOSITORY_TYPE=postgresql` - baza danych PostgreSQL (zalecane)
- `REPOSITORY_TYPE=json` - plik JSON (domyślne, offline)
- `REPOSITORY_TYPE=in_memory` - pamięć RAM (do testów)

## Uruchamianie testów

### Szybkie testy (tryb offline)
Aby uruchomić testy w trybie offline (bez bazy danych), wykonaj:

```bash
pytest
```

> [!NOTE]
> **Testy offline** używają InMemoryRepository i mogą potrwać trochę dłużej niż testy z bazą danych, ponieważ wszystkie operacje są wykonywane w pamięci.

### Pełne testy (z PostgreSQL)
Aby uruchomić wszystkie testy z bazą danych PostgreSQL:

1. **Uruchom PostgreSQL w Docker** (patrz sekcja poniżej)
2. **Skonfiguruj zmienne środowiskowe** (patrz sekcja poniżej)
3. **Uruchom testy**:
```bash
pytest
```

### Testy dla konkretnych modułów
```bash
# Tylko testy aplikacji
pytest tests/application/

# Tylko testy infrastruktury
pytest tests/infrastructure/

# Tylko testy prezentacji
pytest tests/presentation/
```

## Narzędzia deweloperskie

Projekt zawiera skonfigurowane narzędzia do formatowania i sprawdzania jakości kodu:

### Formatowanie kodu (Black)
```bash
# Sprawdź formatowanie
black --check src/

# Zastosuj formatowanie
black src/
```

### Sprawdzanie stylu kodu (Flake8)
```bash
# Sprawdź styl kodu
flake8 src/
```

### Sprawdzanie typów (Mypy)
```bash
# Sprawdź typy
mypy src/
```

### Konfiguracja
- **pyproject.toml**: konfiguracja Black
- **setup.cfg**: konfiguracja Flake8
- **mypy.ini**: konfiguracja Mypy

## Uruchamianie programu

### Tryb podstawowy (JSON)
Aby uruchomić program z domyślnym repozytorium JSON, wykonaj:

```bash
# Windows/macOS/Linux
py src/presentation/views/main.py

# lub

python3 src/presentation/views/main.py
```

### Tryb z PostgreSQL
1. **Uruchom PostgreSQL** (patrz sekcja Docker powyżej)
2. **Skonfiguruj .env** z `REPOSITORY_TYPE=postgresql`
3. **Uruchom aplikację**:

```bash
py src/presentation/views/main.py
```

### Tryb testowy (InMemory)
Aby uruchomić w trybie testowym bez persystencji danych:

1. **Ustaw w .env**: `REPOSITORY_TYPE=in_memory`
2. **Uruchom aplikację**

> [!NOTE]
> W trybie InMemory wszystkie dane są przechowywane tylko w pamięci i giną po zamknięciu aplikacji.

## Jak korzystać z programu

### Podstawowe funkcje

1. **Dodawanie produktu**:
   - Uzupełnij pola tekstowe wymaganymi informacjami. Pamiętaj, że ilość (`quantity`) musi być liczbą całkowitą dodatnią, a żadne pole tekstowe nie może być puste.
   - **🤖 AI automatycznie sprawdzi nazwę** i zaproponuje poprawki jeśli znajdzie błędy
   - Kliknij przycisk "Add Product".

2. **Edytowanie produktu**:
   - Wybierz produkt z listy, klikając na niego.
   - Aktualne dane produktu pojawią się w polach tekstowych oraz checkboxie.
   - Zmień dane według potrzeb. Pamiętaj, że ilość (`quantity`) musi być liczbą całkowitą dodatnią, a żadne pole tekstowe nie może być puste.
   - Kliknij przycisk "Update Product".

3. **Usuwanie produktu**:
   - Wybierz produkt z listy, klikając na niego.
   - Kliknij przycisk "Remove Product".

4. **Zaznaczanie/Odznaczanie produktu**:
   - Kliknij na produkt na liście, aby go zaznaczyć.
   - Kliknij ponownie na ten sam produkt, aby go odznaczyć.

### 🤖 Funkcje AI

5. **Poprawa nazwy produktu (✨ Fix Name)**:
   - Wpisz nazwę produktu w pole tekstowe
   - Kliknij przycisk "✨ Fix Name"
   - AI zaproponuje poprawki jeśli znajdzie błędy
   - Wybierz najlepszą opcję z listy sugestii

6. **Dodawanie do słownika AI (🧠 Add to Dictionary)**:
   - Kliknij przycisk "🧠 Add to Dictionary"
   - Wpisz błędne słowo i jego poprawną wersję
   - AI zapamięta tę poprawkę na przyszłość

7. **Automatyczne sugestie**:
   - Przy dodawaniu produktu AI może automatycznie zasugerować poprawki
   - Pojawi się okno z opcjami do wyboru
   - Wybierz najlepszą opcję lub zostaw oryginalną nazwę
   - AI uczy się z Twojego wyboru

### Filtry i wyszukiwanie

8. **Wyszukiwanie produktów**:
   - Użyj pola "Search products..." aby znaleźć konkretne produkty
   - Wyszukiwanie działa w czasie rzeczywistym

9. **Filtrowanie według statusu**:
   - Wybierz "All", "Purchased" lub "Not Purchased" z menu rozwijalnego

10. **Filtrowanie według ilości**:
    - Ustaw minimum i maksimum w polach "Min Qty" i "Max Qty"
    - Kliknij "Show Low Stock" aby zobaczyć produkty o niskich stanach

> [!NOTE]
> Pamiętaj o spełnieniu wymagań dotyczących dodawania oraz aktualizacji produktów.

## 🔧 Troubleshooting

### Problem z Docker
```bash
# Sprawdź czy Docker działa
docker --version
docker-compose --version

# Restart kontenerów
docker-compose down && docker-compose up -d

# Sprawdź logi
docker-compose logs postgres
```

### Problem z bazą danych
```bash
# Sprawdź połączenie z bazą
python -c "from src.infrastructure.database.DatabaseService import DatabaseService; DatabaseService().test_connection()"

# Sprawdź czy plik .env istnieje
ls -la .env  # Linux/macOS
dir .env     # Windows
```

### Problem z AI
```bash
# Sprawdź czy plik słownika AI istnieje
ls -la data/learned_typos.json  # Linux/macOS
dir data\learned_typos.json     # Windows

# Resetuj słownik AI (usuń plik)
rm data/learned_typos.json      # Linux/macOS
del data\learned_typos.json     # Windows
```

### Testy nie przechodzą
```bash
# Sprawdź konfigurację testów
pytest --collect-only

# Uruchom testy verbose
pytest -v

# Uruchom konkretny test
pytest tests/application/test_AddProduct_usecase.py -v
```
