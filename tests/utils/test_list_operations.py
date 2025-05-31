import pytest
from typing import List
from src.utils.list_operations import (
    batch_generator,
    filter_products_by_criteria,
    group_products_by_status,
    get_product_summary_generator,
    find_products_by_name_pattern
)
from src.domain.Product_Entity import _Product

class TestBatchGenerator:
    """Test cases for batch_generator function."""
    
    def test_batch_generator_normal_case(self):
        """Test batch generator with normal input."""
        items = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        batches = list(batch_generator(items, 3))
        
        expected = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10]]
        assert batches == expected
    
    def test_batch_generator_exact_division(self):
        """Test batch generator when items divide evenly."""
        items = [1, 2, 3, 4, 5, 6]
        batches = list(batch_generator(items, 2))
        
        expected = [[1, 2], [3, 4], [5, 6]]
        assert batches == expected
    
    def test_batch_generator_empty_list(self):
        """Test batch generator with empty list."""
        items = []
        batches = list(batch_generator(items, 3))
        
        assert batches == []
    
    def test_batch_generator_single_item(self):
        """Test batch generator with single item."""
        items = [42]
        batches = list(batch_generator(items, 3))
        
        expected = [[42]]
        assert batches == expected
    
    def test_batch_generator_batch_size_larger_than_list(self):
        """Test batch generator when batch size is larger than list."""
        items = [1, 2, 3]
        batches = list(batch_generator(items, 10))
        
        expected = [[1, 2, 3]]
        assert batches == expected


class TestFilterProductsByCriteria:
    """Test cases for filter_products_by_criteria function."""
    
    @pytest.fixture
    def sample_products(self):
        """Create sample products for testing."""
        return [
            _Product(name="Apple", quantity=5, purchased=True),
            _Product(name="Banana", quantity=3, purchased=False),
            _Product(name="Orange", quantity=10, purchased=True),
            _Product(name="Milk", quantity=1, purchased=False),
            _Product(name="Bread", quantity=2, purchased=True)
        ]
    
    def test_filter_products_single_criterion(self, sample_products):
        """Test filtering with single criterion."""
        # Filter only purchased products
        criteria = [lambda p: p.purchased]
        result = filter_products_by_criteria(sample_products, criteria)
        
        assert len(result) == 3
        assert all(p.purchased for p in result)
        assert {p.name for p in result} == {"Apple", "Orange", "Bread"}
    
    def test_filter_products_multiple_criteria(self, sample_products):
        """Test filtering with multiple criteria."""
        # Filter purchased products with quantity > 2
        criteria = [
            lambda p: p.purchased,
            lambda p: p.quantity > 2
        ]
        result = filter_products_by_criteria(sample_products, criteria)
        
        assert len(result) == 2
        assert all(p.purchased and p.quantity > 2 for p in result)
        assert {p.name for p in result} == {"Apple", "Orange"}
    
    def test_filter_products_no_criteria(self, sample_products):
        """Test filtering with no criteria."""
        criteria = []
        result = filter_products_by_criteria(sample_products, criteria)
        
        assert result == sample_products
    
    def test_filter_products_no_matches(self, sample_products):
        """Test filtering with criteria that match nothing."""
        # Filter products with quantity > 100
        criteria = [lambda p: p.quantity > 100]
        result = filter_products_by_criteria(sample_products, criteria)
        
        assert result == []
    
    def test_filter_products_empty_list(self):
        """Test filtering empty product list."""
        criteria = [lambda p: p.purchased]
        result = filter_products_by_criteria([], criteria)
        
        assert result == []


class TestGroupProductsByStatus:
    """Test cases for group_products_by_status function."""
    
    @pytest.fixture
    def sample_products(self):
        """Create sample products for testing."""
        return [
            _Product(name="Apple", quantity=5, purchased=True),
            _Product(name="Banana", quantity=3, purchased=False),
            _Product(name="Orange", quantity=10, purchased=True),
            _Product(name="Milk", quantity=1, purchased=False),
            _Product(name="Bread", quantity=2, purchased=True)
        ]
    
    def test_group_products_by_status_mixed(self, sample_products):
        """Test grouping products with mixed purchase status."""
        result = group_products_by_status(sample_products)
        
        assert "purchased" in result
        assert "not_purchased" in result
        
        purchased_names = {p.name for p in result["purchased"]}
        not_purchased_names = {p.name for p in result["not_purchased"]}
        
        assert purchased_names == {"Apple", "Orange", "Bread"}
        assert not_purchased_names == {"Banana", "Milk"}
        assert len(result["purchased"]) == 3
        assert len(result["not_purchased"]) == 2
    
    def test_group_products_all_purchased(self):
        """Test grouping when all products are purchased."""
        products = [
            _Product(name="Apple", quantity=5, purchased=True),
            _Product(name="Orange", quantity=10, purchased=True)
        ]
        result = group_products_by_status(products)
        
        assert len(result["purchased"]) == 2
        assert len(result["not_purchased"]) == 0
        assert {p.name for p in result["purchased"]} == {"Apple", "Orange"}
    
    def test_group_products_none_purchased(self):
        """Test grouping when no products are purchased."""
        products = [
            _Product(name="Banana", quantity=3, purchased=False),
            _Product(name="Milk", quantity=1, purchased=False)
        ]
        result = group_products_by_status(products)
        
        assert len(result["purchased"]) == 0
        assert len(result["not_purchased"]) == 2
        assert {p.name for p in result["not_purchased"]} == {"Banana", "Milk"}
    
    def test_group_products_empty_list(self):
        """Test grouping empty product list."""
        result = group_products_by_status([])
        
        assert result["purchased"] == []
        assert result["not_purchased"] == []


class TestGetProductSummaryGenerator:
    """Test cases for get_product_summary_generator function."""
    
    @pytest.fixture
    def sample_products(self):
        """Create sample products for testing."""
        return [
            _Product(name="Apple", quantity=5, purchased=True),
            _Product(name="Banana", quantity=3, purchased=False),
            _Product(name="Orange", quantity=10, purchased=True)
        ]
    
    def test_get_product_summary_generator_normal(self, sample_products):
        """Test product summary generator with normal input."""
        summaries = list(get_product_summary_generator(sample_products))
        
        expected = [
            "Apple (Qty: 5) [✓]",
            "Banana (Qty: 3) [✗]",
            "Orange (Qty: 10) [✓]"
        ]
        assert summaries == expected
    
    def test_get_product_summary_generator_empty_list(self):
        """Test product summary generator with empty list."""
        summaries = list(get_product_summary_generator([]))
        assert summaries == []
    
    def test_get_product_summary_generator_single_product(self):
        """Test product summary generator with single product."""
        products = [_Product(name="Test Product", quantity=1, purchased=False)]
        summaries = list(get_product_summary_generator(products))
        
        expected = ["Test Product (Qty: 1) [✗]"]
        assert summaries == expected
    
    def test_get_product_summary_generator_is_generator(self, sample_products):
        """Test that the function returns a generator object."""
        result = get_product_summary_generator(sample_products)
        
        # Check that it's a generator
        assert hasattr(result, '__iter__')
        assert hasattr(result, '__next__')
        
        # Test lazy evaluation - should not consume until iterated
        first_summary = next(result)
        assert first_summary == "Apple (Qty: 5) [✓]"


class TestFindProductsByNamePattern:
    """Test cases for find_products_by_name_pattern function."""
    
    @pytest.fixture
    def sample_products(self):
        """Create sample products for testing."""
        return [
            _Product(name="Apple Juice", quantity=5, purchased=True),
            _Product(name="Banana Split", quantity=3, purchased=False),
            _Product(name="Orange Marmalade", quantity=10, purchased=True),
            _Product(name="Milk Chocolate", quantity=1, purchased=False),
            _Product(name="Bread Crumbs", quantity=2, purchased=True)
        ]
    
    def test_find_products_by_name_pattern_single_match(self, sample_products):
        """Test finding products with pattern that matches single product."""
        result = find_products_by_name_pattern(sample_products, "Apple")
        
        assert len(result) == 1
        assert result[0].name == "Apple Juice"
    
    def test_find_products_by_name_pattern_multiple_matches(self, sample_products):
        """Test finding products with pattern that matches multiple products."""
        result = find_products_by_name_pattern(sample_products, "a")  # Common letter
        
        # Should match products containing 'a' (case insensitive)
        expected_names = {"Apple Juice", "Banana Split", "Orange Marmalade", "Milk Chocolate", "Bread Crumbs"}
        result_names = {p.name for p in result}
        assert result_names == expected_names
    
    def test_find_products_by_name_pattern_no_matches(self, sample_products):
        """Test finding products with pattern that matches nothing."""
        result = find_products_by_name_pattern(sample_products, "xyz")
        
        assert result == []
    
    def test_find_products_by_name_pattern_case_insensitive(self, sample_products):
        """Test that pattern matching is case insensitive."""
        result_lower = find_products_by_name_pattern(sample_products, "apple")
        result_upper = find_products_by_name_pattern(sample_products, "APPLE")
        result_mixed = find_products_by_name_pattern(sample_products, "ApPlE")
        
        assert len(result_lower) == 1
        assert len(result_upper) == 1
        assert len(result_mixed) == 1
        assert result_lower[0].name == "Apple Juice"
        assert result_upper[0].name == "Apple Juice"
        assert result_mixed[0].name == "Apple Juice"
    
    def test_find_products_by_name_pattern_empty_pattern(self, sample_products):
        """Test finding products with empty pattern."""
        result = find_products_by_name_pattern(sample_products, "")
        
        # Empty pattern should match all products (since "" is contained in every string)
        assert len(result) == len(sample_products)
        assert result == sample_products
    
    def test_find_products_by_name_pattern_empty_list(self):
        """Test finding products in empty list."""
        result = find_products_by_name_pattern([], "test")
        
        assert result == []
    
    def test_find_products_by_name_pattern_partial_word(self, sample_products):
        """Test finding products with partial word patterns."""
        result = find_products_by_name_pattern(sample_products, "Choc")
        
        assert len(result) == 1
        assert result[0].name == "Milk Chocolate"
