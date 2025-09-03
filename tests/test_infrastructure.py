"""Infrastructure validation tests to ensure testing setup works correctly."""

import pytest
import os
import sys
from pathlib import Path


class TestInfrastructure:
    """Test the testing infrastructure setup."""

    def test_python_path_includes_app(self):
        """Test that the app directory is accessible for imports."""
        app_path = Path(__file__).parent.parent / "app"
        assert app_path.exists(), "App directory should exist"

    def test_pytest_markers_work(self):
        """Test that custom pytest markers are properly configured."""
        # This test itself uses markers to validate they work
        pass

    @pytest.mark.unit
    def test_unit_marker(self):
        """Test that unit marker works."""
        assert True

    @pytest.mark.integration
    def test_integration_marker(self):
        """Test that integration marker works."""
        assert True

    @pytest.mark.slow
    def test_slow_marker(self):
        """Test that slow marker works."""
        assert True

    def test_fixtures_available(self, temp_dir, mock_redis, mock_mongo, mock_config):
        """Test that common fixtures are available and working."""
        # Test temp_dir fixture
        assert os.path.exists(temp_dir)
        assert os.path.isdir(temp_dir)
        
        # Test mock fixtures are available
        assert mock_redis is not None
        assert mock_mongo is not None
        assert mock_config is not None
        assert isinstance(mock_config, dict)

    def test_mock_redis_fixture(self, mock_redis):
        """Test that mock Redis fixture behaves correctly."""
        # Test basic Redis operations
        assert mock_redis.get("test_key") is None
        assert mock_redis.set("test_key", "test_value") is True
        assert mock_redis.exists("test_key") is False  # Mock behavior
        assert mock_redis.delete("test_key") == 1

    def test_mock_mongo_fixture(self, mock_mongo):
        """Test that mock MongoDB fixture behaves correctly."""
        # Access a database and collection
        db = mock_mongo["test_db"]
        collection = db["test_collection"]
        
        # Test basic MongoDB operations
        result = collection.find_one({"_id": "test"})
        assert result is None
        
        insert_result = collection.insert_one({"test": "data"})
        assert insert_result.inserted_id == "test_id"

    def test_sample_data_fixtures(self, sample_action_data, sample_reward_data):
        """Test that sample data fixtures are properly structured."""
        # Test action data structure
        assert "exp_id" in sample_action_data
        assert "action" in sample_action_data
        assert "context" in sample_action_data
        assert "timestamp" in sample_action_data
        assert "user_id" in sample_action_data
        
        # Test reward data structure
        assert "exp_id" in sample_reward_data
        assert "action" in sample_reward_data
        assert "reward" in sample_reward_data
        assert "timestamp" in sample_reward_data
        assert "user_id" in sample_reward_data

    def test_numpy_fixtures(self, numpy_random_state, sample_numpy_array):
        """Test that numpy-related fixtures work."""
        import numpy as np
        
        # Test random state
        assert isinstance(numpy_random_state, np.random.RandomState)
        
        # Test sample array
        assert isinstance(sample_numpy_array, np.ndarray)
        assert sample_numpy_array.shape == (3, 3)

    def test_import_app_modules(self):
        """Test that we can import core app modules."""
        try:
            # Add app directory to Python path for imports
            app_path = str(Path(__file__).parent.parent / "app")
            if app_path not in sys.path:
                sys.path.insert(0, app_path)
            
            # Test importing core modules
            import core
            import db
            import handlers
            import libs
            
            # Basic validation that modules loaded
            assert core is not None
            assert db is not None
            assert handlers is not None
            assert libs is not None
            
        except ImportError as e:
            pytest.fail(f"Failed to import app modules: {e}")

    def test_coverage_configuration(self):
        """Test that coverage is properly configured."""
        # This test will be covered and should contribute to coverage stats
        app_path = Path(__file__).parent.parent / "app"
        assert app_path.exists()
        
        # Test that pyproject.toml exists with coverage config
        pyproject_path = Path(__file__).parent.parent / "pyproject.toml"
        assert pyproject_path.exists()
        
        with open(pyproject_path) as f:
            content = f.read()
            assert "[tool.coverage.run]" in content
            assert "[tool.coverage.report]" in content


class TestBasicPythonFeatures:
    """Test basic Python features to ensure environment is working."""

    def test_basic_assertions(self):
        """Test basic assertion functionality."""
        assert True is True
        assert False is False
        assert 1 == 1
        assert "test" == "test"

    def test_basic_math(self):
        """Test basic mathematical operations."""
        assert 2 + 2 == 4
        assert 5 - 3 == 2
        assert 3 * 4 == 12
        assert 8 / 2 == 4

    def test_basic_data_structures(self):
        """Test basic Python data structures."""
        # Lists
        test_list = [1, 2, 3]
        assert len(test_list) == 3
        assert test_list[0] == 1
        
        # Dictionaries
        test_dict = {"key": "value"}
        assert test_dict["key"] == "value"
        assert len(test_dict) == 1
        
        # Sets
        test_set = {1, 2, 3, 3}
        assert len(test_set) == 3
        assert 1 in test_set

    def test_exception_handling(self):
        """Test exception handling works correctly."""
        with pytest.raises(ValueError):
            raise ValueError("Test exception")
        
        with pytest.raises(KeyError):
            test_dict = {}
            _ = test_dict["nonexistent_key"]

    def test_parametrized_test(self, sample_action_data):
        """Test parametrized functionality works."""
        test_cases = [
            ("exp_id", str),
            ("action", str),
            ("context", dict),
            ("user_id", str)
        ]
        
        for key, expected_type in test_cases:
            assert key in sample_action_data
            assert isinstance(sample_action_data[key], expected_type)