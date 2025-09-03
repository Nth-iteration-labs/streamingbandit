"""Shared pytest fixtures for the StreamingBandit project."""

import os
import tempfile
import shutil
import pytest
from unittest.mock import Mock, MagicMock
import redis
import pymongo
import yaml


@pytest.fixture
def temp_dir():
    """Create a temporary directory for testing."""
    temp_path = tempfile.mkdtemp()
    yield temp_path
    shutil.rmtree(temp_path, ignore_errors=True)


@pytest.fixture
def temp_file():
    """Create a temporary file for testing."""
    fd, path = tempfile.mkstemp()
    os.close(fd)
    yield path
    if os.path.exists(path):
        os.unlink(path)


@pytest.fixture
def mock_redis():
    """Mock Redis client for testing."""
    mock_client = Mock(spec=redis.Redis)
    mock_client.get.return_value = None
    mock_client.set.return_value = True
    mock_client.delete.return_value = 1
    mock_client.exists.return_value = False
    mock_client.flushdb.return_value = True
    return mock_client


@pytest.fixture
def mock_mongo():
    """Mock MongoDB client for testing."""
    mock_client = MagicMock(spec=pymongo.MongoClient)
    mock_db = MagicMock()
    mock_collection = MagicMock()
    
    mock_client.__getitem__.return_value = mock_db
    mock_db.__getitem__.return_value = mock_collection
    
    # Common collection methods
    mock_collection.find.return_value = []
    mock_collection.find_one.return_value = None
    mock_collection.insert_one.return_value = Mock(inserted_id="test_id")
    mock_collection.update_one.return_value = Mock(modified_count=1)
    mock_collection.delete_one.return_value = Mock(deleted_count=1)
    mock_collection.count_documents.return_value = 0
    
    return mock_client


@pytest.fixture
def mock_config():
    """Mock configuration for testing."""
    return {
        'redis_host': 'localhost',
        'redis_port': 6379,
        'redis_db': 0,
        'mongo_host': 'localhost',
        'mongo_port': 27017,
        'mongo_db': 'test_streamingbandit',
        'debug': True,
        'log_level': 'INFO'
    }


@pytest.fixture
def sample_config_yaml():
    """Sample YAML configuration content."""
    config = {
        'redis': {
            'host': 'localhost',
            'port': 6379,
            'db': 0
        },
        'mongodb': {
            'host': 'localhost',
            'port': 27017,
            'database': 'streamingbandit'
        },
        'logging': {
            'level': 'INFO'
        }
    }
    return yaml.dump(config)


@pytest.fixture
def mock_experiment():
    """Mock experiment object for testing."""
    experiment = Mock()
    experiment.exp_id = "test_exp_123"
    experiment.name = "Test Experiment"
    experiment.actions = ["action1", "action2", "action3"]
    experiment.contexts = ["context1", "context2"]
    experiment.is_active = True
    return experiment


@pytest.fixture
def mock_bandit_algorithm():
    """Mock bandit algorithm for testing."""
    algorithm = Mock()
    algorithm.get_action.return_value = {"action": "action1", "prob": 0.5}
    algorithm.set_reward.return_value = True
    algorithm.get_context.return_value = {"context1": 1.0, "context2": 0.5}
    return algorithm


@pytest.fixture
def sample_action_data():
    """Sample action data structure."""
    return {
        "exp_id": "test_exp_123",
        "action": "action1",
        "context": {"feature1": 1.0, "feature2": 0.5},
        "timestamp": "2024-01-01T12:00:00Z",
        "user_id": "user123"
    }


@pytest.fixture
def sample_reward_data():
    """Sample reward data structure."""
    return {
        "exp_id": "test_exp_123",
        "action": "action1",
        "reward": 1.0,
        "timestamp": "2024-01-01T12:05:00Z",
        "user_id": "user123"
    }


@pytest.fixture
def mock_tornado_application():
    """Mock Tornado application for testing handlers."""
    from unittest.mock import AsyncMock
    
    app = Mock()
    app.settings = {
        'debug': True,
        'redis': Mock(),
        'mongodb': Mock()
    }
    return app


@pytest.fixture
def mock_request_handler():
    """Mock Tornado RequestHandler for testing."""
    handler = Mock()
    handler.get_argument.return_value = "test_value"
    handler.get_arguments.return_value = ["test_value"]
    handler.request = Mock()
    handler.request.body = b'{"test": "data"}'
    handler.request.headers = {}
    handler.write = Mock()
    handler.set_status = Mock()
    handler.finish = Mock()
    return handler


@pytest.fixture(autouse=True)
def reset_environment():
    """Reset environment variables before each test."""
    original_env = dict(os.environ)
    yield
    # Restore original environment
    os.environ.clear()
    os.environ.update(original_env)


@pytest.fixture
def numpy_random_state():
    """Provide a consistent numpy random state for testing."""
    import numpy as np
    return np.random.RandomState(42)


@pytest.fixture
def sample_numpy_array():
    """Sample numpy array for testing."""
    import numpy as np
    return np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])


@pytest.fixture
def mock_scikit_model():
    """Mock scikit-learn model for testing."""
    model = Mock()
    model.fit.return_value = model
    model.predict.return_value = [0.5, 0.8, 0.3]
    model.predict_proba.return_value = [[0.3, 0.7], [0.2, 0.8], [0.6, 0.4]]
    model.score.return_value = 0.85
    return model