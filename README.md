# Tkinter ShopList Todo

## Opis projektu

Celem projektu jest stworzenie aplikacji do zarządzania listą zakupów z wykorzystaniem biblioteki Tkinter. Aplikacja pozwala na dodawanie, edytowanie oraz usuwanie produktów z listy. Użytkownik może także zaznaczać produkty jako kupione lub odznaczać je.

Zakres projektu obejmuje:
- Tworzenie listy zakupów
- Edytowanie produktów na liście
- Usuwanie produktów z listy
- Zaznaczanie i odznaczanie produktów jako kupione

Oczekiwane rezultaty to funkcjonalna aplikacja, która ułatwi zarządzanie listą zakupów.

## Technologie

- Python
- Tkinter
- CustomTkinter
- Pydantic
- Mypy

## Architektura

Projekt został zaprojektowany z wykorzystaniem architektury warstwowej, co pozwala na lepsze zarządzanie kodem i jego skalowalność. Architektura składa się z następujących warstw:

- **src/application**: Logika biznesowa aplikacji. Zawiera przypadki użycia i interfejsy repozytoriów.
- **src/domain**: Warstwa domenowa, która zawiera encje i logikę domenową.
- **src/infrastructure**: Implementacje repozytoriów i inne usługi zewnętrzne.
- **src/presentation**: Warstwa prezentacji, która zawiera kontrolery, widoki i widgety.

### Struktura plików/folderów całego projektu
```
Tkinter_ShopList_Todo/
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
├── tests/
│   ├── application/
│   │   ├── test_AddProduct_usecase.py
│   │   ├── test_GetAllProduct_usecase.py
│   │   ├── test_GetProductById_usecase.py
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
│   │   ├── test_HandleExceptions.py
│   │   └── test_purchaseStatus.py
│   └── __init__.py
├── .gitignore
├── LICENSE
├── README.md
├── requirements.txt
└── mypy.ini
```

### Dlaczego taka architektura?

Architektura Clean Architecture została wybrana, aby oddzielić logikę biznesową od warstwy prezentacji i dostępu do danych. Dzięki temu kod jest bardziej czytelny, łatwiejszy do testowania oraz utrzymania.

## Instalacja

### Tworzenie wirtualnego środowiska

Aby stworzyć wirtualne środowisko, uruchom poniższe polecenie:

```bash
py -m venv venv
```
lub
```bash
python3 -m venv venv
```

### Instalacja zależności

Aby zainstalować wymagane zależności, uruchom poniższe polecenie:

```bash
pip install -r requirements.txt
```

## Uruchamianie testów

Aby uruchomić testy, wykonaj poniższe polecenie:

```bash
pytest
```

## Uruchamianie programu

Aby uruchomić program, wykonaj poniższe polecenie w katalogu głównym projektu:

```bash
py src/presentation/views/main.py
```
lub
```bash
python3 src/presentation/views/main.py
```

## Jak korzystać z programu

1. **Dodawanie produktu**:
   - Uzupełnij pola tekstowe wymaganymi informacjami. Pamiętaj, że ilość (`quantity`) musi być liczbą całkowitą dodatnią, a żadne pole tekstowe nie może być puste.
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

> [!NOTE] 
> Pamiętaj o spełnieniu wymagań dotyczących dodawania oraz aktualizacji produktów.
