from typing import Iterator, List, TypeVar, Callable
from src.domain.Product_Entity import _Product

T = TypeVar("T")


def batch_generator(items: List[T], batch_size: int) -> Iterator[List[T]]:
    """
    Generator that yields items in batches.

    :param items: List of items to batch.
    :param batch_size: Size of each batch.
    :yield: Batches of items.
    """
    for i in range(0, len(items), batch_size):
        yield items[i : i + batch_size]


def filter_products_by_criteria(
    products: List[_Product], criteria: List[Callable]
) -> List[_Product]:
    """
    Filter products by multiple criteria using list comprehension.

    :param products: List of products to filter.
    :param criteria: List of filter functions.
    :return: Filtered list of products.
    """
    result = products
    for criterion in criteria:
        result = [product for product in result if criterion(product)]
    return result


def group_products_by_status(products: List[_Product]) -> dict:
    """
    Group products by purchase status using dictionary comprehension.

    :param products: List of products to group.
    :return: Dictionary with purchase status as keys and product lists as values.
    """
    return {
        "purchased": [p for p in products if p.purchased],
        "not_purchased": [p for p in products if not p.purchased],
    }


def get_product_summary_generator(products: List[_Product]) -> Iterator[str]:
    """
    Generator that yields product summaries.

    :param products: List of products.
    :yield: Product summary strings.
    """
    for product in products:
        status = "✓" if product.purchased else "✗"
        yield f"{product.name} (Qty: {product.quantity}) [{status}]"


def find_products_by_name_pattern(
    products: List[_Product], pattern: str
) -> List[_Product]:
    """
    Find products matching name pattern using list comprehension.

    :param products: List of products to search.
    :param pattern: Pattern to match in product names.
    :return: List of matching products.
    """
    return [product for product in products if pattern.lower() in product.name.lower()]
