# Contributing to Eating Detection

Thank you for your interest in contributing to the Eating Detection project! This document provides guidelines for contributing to the project.

## Development Setup

### Prerequisites

- Python 3.8 or higher
- Git
- A webcam or USB camera for testing

### Setting Up the Development Environment

1. **Fork and Clone the Repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/eating-detection.git
   cd eating-detection
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify Installation**
   ```bash
   python -m pytest tests/ -v
   ```

## Development Workflow

### Making Changes

1. **Create a Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make Your Changes**
   - Follow the existing code style and conventions
   - Add docstrings for new functions and classes
   - Include type hints where appropriate

3. **Write Tests**
   - Add tests for new functionality in the `tests/` directory
   - Ensure existing tests still pass
   - Aim for good test coverage

4. **Test Your Changes**
   ```bash
   # Run all tests
   python -m pytest tests/ -v
   
   # Test specific functionality
   python main.py
   ```

### Code Style Guidelines

- **Python Style**: Follow PEP 8 conventions
- **Docstrings**: Use Google-style docstrings for all functions and classes
- **Type Hints**: Include type hints for function parameters and return values
- **Error Handling**: Use appropriate exception handling and meaningful error messages

### Example Code Style

```python
def detect_objects(self, frame: np.ndarray) -> List[str]:
    """
    Perform object detection on a given frame.
    
    Args:
        frame: Input image frame for object detection.
        
    Returns:
        List of detected object names that meet the threshold.
        
    Raises:
        RuntimeError: If detection fails due to model issues.
    """
```

## Testing

### Running Tests

```bash
# Run all tests with verbose output
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_FoodDetectionSystem.py -v

# Run tests with coverage
python -m pytest tests/ --cov=src --cov-report=html
```

### Writing Tests

- Place test files in the `tests/` directory
- Name test files with the pattern `test_*.py`
- Use descriptive test function names that explain what is being tested
- Use pytest fixtures for setup and teardown
- Mock external dependencies (camera, YOLO model) in tests

### Test Structure Example

```python
import pytest
from unittest.mock import Mock, patch
from src.your_module import YourClass

@pytest.fixture
def mock_settings():
    return {
        'objects_to_detect': ['bottle'],
        'threshold': 0.5,
        'camera_settings': {
            'resolution': [640, 480],
            'frame_check_interval': 1
        }
    }

def test_your_function(mock_settings):
    # Test implementation
    pass
```

## Pull Request Process

1. **Ensure Your Branch is Up to Date**
   ```bash
   git checkout main
   git pull origin main
   git checkout feature/your-feature-name
   git rebase main
   ```

2. **Run Final Tests**
   ```bash
   python -m pytest tests/ -v
   ```

3. **Commit Your Changes**
   ```bash
   git add .
   git commit -m "Add descriptive commit message"
   ```

4. **Push to Your Fork**
   ```bash
   git push origin feature/your-feature-name
   ```

5. **Create Pull Request**
   - Provide a clear description of your changes
   - Reference any related issues
   - Include screenshots or demos if applicable

### Pull Request Checklist

- [ ] Tests pass locally
- [ ] New functionality includes tests
- [ ] Documentation is updated if needed
- [ ] Code follows project style guidelines
- [ ] Commit messages are descriptive
- [ ] No unnecessary files are included

## Types of Contributions

### Bug Fixes
- Report bugs using GitHub issues
- Include steps to reproduce the issue
- Provide system information (OS, Python version, etc.)

### New Features
- Discuss major features in issues before implementing
- Keep features focused and atomic
- Include comprehensive tests and documentation

### Documentation Improvements
- Fix typos, improve clarity, add examples
- Update README.md for new features
- Add inline code documentation

### Performance Improvements
- Profile code to identify bottlenecks
- Include benchmarks in your PR description
- Ensure improvements don't break existing functionality

## Architecture Guidelines

### Project Structure
```
eating-detection/
├── main.py                    # Application entry point
├── notification_client.py     # Notification client
├── src/                      # Core application code
│   ├── cmd_app.py           # Command-line interface
│   ├── food_detection_system.py  # Main detection logic
│   ├── notification_system.py    # Notification handling
│   └── yolo.py              # YOLO model wrapper
├── tests/                   # Unit tests
└── docs/                    # Documentation (if added)
```

### Key Design Principles
- **Separation of Concerns**: Each module has a single responsibility
- **Testability**: Code should be easily testable with mocked dependencies
- **Configuration**: Use settings.json for all configurable parameters
- **Error Handling**: Graceful degradation and meaningful error messages

## Getting Help

- **Documentation**: Check the README.md and inline docstrings
- **Issues**: Search existing issues before creating new ones
- **Discussions**: Use GitHub Discussions for questions and ideas

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Help newcomers get started
- Follow project guidelines and conventions

Thank you for contributing to Eating Detection!