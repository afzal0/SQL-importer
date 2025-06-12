# Contributing to Universal Database Importer

First off, thank you for considering contributing to Universal Database Importer! It's people like you that make this tool better for everyone.

## Code of Conduct

By participating in this project, you are expected to uphold our Code of Conduct:

- Use welcoming and inclusive language
- Be respectful of differing viewpoints and experiences
- Gracefully accept constructive criticism
- Focus on what is best for the community
- Show empathy towards other community members

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues as you might find out that you don't need to create one. When you are creating a bug report, please include as many details as possible:

- **Use a clear and descriptive title**
- **Describe the exact steps to reproduce the problem**
- **Provide specific examples**
- **Describe the behavior you observed and expected**
- **Include screenshots if possible**
- **Include your environment details** (OS, Python version, database type)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

- **Use a clear and descriptive title**
- **Provide a detailed description of the proposed enhancement**
- **Explain why this enhancement would be useful**
- **List any alternatives you've considered**

### Your First Code Contribution

Unsure where to begin? You can start by looking through these issues:

- Issues labeled `good first issue` - should only require a few lines of code
- Issues labeled `help wanted` - more involved but accessible

### Pull Requests

1. **Fork the repository** and create your branch from `main`
2. **Make your changes** following our coding standards
3. **Add tests** if you've added code that should be tested
4. **Ensure the test suite passes** (if available)
5. **Update documentation** as needed
6. **Submit your pull request**

## Development Setup

1. **Fork and clone the repository**
   ```bash
   git clone https://github.com/your-username/universal-database-importer.git
   cd universal-database-importer
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install development dependencies**
   ```bash
   pip install -r requirements.txt
   pip install pytest pytest-cov flake8  # Development tools
   ```

4. **Create a new branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Coding Standards

### Python Style Guide

We follow PEP 8 with some modifications:

- Line length: 100 characters (not 79)
- Use meaningful variable names
- Add docstrings to all functions and classes
- Use type hints where appropriate

### Example Code Style

```python
def import_csv_data(
    self,
    file_path: str,
    table_name: str,
    columns: List[str] = None
) -> bool:
    """
    Import CSV data into the specified database table.
    
    Args:
        file_path: Path to the CSV file
        table_name: Name of the target database table
        columns: List of columns to import (default: all)
        
    Returns:
        bool: True if import successful, False otherwise
    """
    # Implementation here
    pass
```

### Commit Messages

- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters or less
- Reference issues and pull requests liberally after the first line

### Documentation

- Update the README.md if you change functionality
- Add docstrings to new functions
- Comment complex logic
- Update the changelog if applicable

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=.

# Run specific test file
pytest tests/test_database_manager.py
```

### Writing Tests

- Place tests in the `tests/` directory
- Name test files as `test_*.py`
- Use descriptive test names
- Test edge cases and error conditions

Example test:

```python
def test_database_connection_mysql():
    """Test MySQL database connection."""
    config = {
        'db_type': 'MySQL',
        'host': 'localhost',
        'port': '3306',
        'username': 'test',
        'password': 'test',
        'database': 'test_db'
    }
    
    db_manager = DatabaseManager()
    assert db_manager.test_connection(config) is True
```

## Project Structure Guidelines

When adding new features:

- **GUI components**: Add to `main.py` or create separate module if large
- **Database logic**: Add to `database_manager.py`
- **Utilities**: Create new module in project root
- **Documentation**: Update README.md and add inline documentation

## Review Process

1. **Automated checks** run on all PRs
2. **Code review** by maintainers
3. **Testing** on different platforms
4. **Documentation** review
5. **Merge** when approved

## Release Process

1. Update version in relevant files
2. Update CHANGELOG.md
3. Create release PR
4. Tag release after merge
5. Build and publish if applicable

## Questions?

Feel free to:
- Open an issue for questions
- Join our discussions
- Contact maintainers

## Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Given credit in the project

Thank you for contributing!