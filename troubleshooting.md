# Troubleshooting Guide

## Common Issues

### Dependency Management Issues
- **Dependency errors:**
  - Ensure all dependencies are installed using `poetry install` (not pip).
  - If migrating from pip to Poetry, remove `requirements.txt` and use `pyproject.toml`.
  - Run `poetry lock` to generate/update `poetry.lock` file.

- **Poetry not found:**
  - Install Poetry: `curl -sSL https://install.python-poetry.org | python3 -`
  - Add Poetry to PATH: `export PATH="/root/.local/bin:$PATH"` (for Docker) or `export PATH="$HOME/.local/bin:$PATH"` (for local)

- **flak8 and Python version compatibility:**
  - If you see an error like:
    ```
    flake8 requires Python >=3.8.1, so it will not be installable for Python >=3.8,<3.8.1
    So, because flake8 (6.1.0) requires Python >=3.8.1 and my-project depends on flake8 (^6.0.0), version solving failed.
    ```
  - This is because your `pyproject.toml` allows Python 3.8.0, but flake8 requires at least 3.8.1.
  - **Solution:** Update your `pyproject.toml` to:
    ```toml
    python = ">=3.8.1,<4.0"
    ```
  - Then rebuild your Docker image or re-run `poetry install`.

### Environment Variables Issues
- **Environment variables not set:**
  - Copy `.env.example` to `.env` and update values as needed.
  - Ensure `.env` file is not in `.gitignore` if you need it tracked.
  - Check that required variables like `OPENAI_API_KEY` are properly set.

- **Environment file creation blocked:**
  - If file creation is blocked by global ignore settings, use terminal commands:
    ```bash
    echo "OPENAI_API_KEY=your_key_here" > .env
    ```
  - Or manually create the file in your IDE/editor.

### Docker Issues
- **Docker build fails with pip/requirements.txt:**
  - Ensure Dockerfile uses Poetry instead of pip.
  - Remove references to `requirements.txt` in Dockerfile.
  - Use `pyproject.toml` and `poetry.lock` for dependency management.

- **Docker Poetry installation issues:**
  - Ensure curl is installed in Docker image: `apt-get install -y curl`
  - Add Poetry to PATH in Dockerfile: `ENV PATH="/root/.local/bin:$PATH"`
  - Use `poetry config virtualenvs.create false` for Docker containers.

### File Structure Issues
- **Empty directories not tracked by git:**
  - Add `.gitkeep` files to empty directories to ensure they're tracked.
  - Common directories: `data/`, `src/`, `tests/`, `configs/`, `scripts/`, `docs/`

- **Missing project files:**
  - Ensure all scaffolding files are created: `README.md`, `pyproject.toml`, `Dockerfile`, etc.
  - Check that file creation wasn't blocked by ignore patterns.

### Diagnostics Script Issues
- **Missing dependencies for diagnostics:**
  - Install required packages: `poetry add requests psutil`
  - Ensure all imports are available in `pyproject.toml`

- **Permission errors:**
  - Ensure proper file permissions for scripts.
  - Use `chmod +x` for executable scripts if needed.

## Migration from pip to Poetry

### Step-by-step Migration
1. **Remove old files:**
   ```bash
   rm requirements.txt
   ```

2. **Create pyproject.toml:**
   - Define project metadata
   - List dependencies and dev dependencies
   - Configure build system

3. **Update Dockerfile:**
   - Install Poetry in container
   - Use `poetry install` instead of `pip install`
   - Copy `pyproject.toml` instead of `requirements.txt`

4. **Update Makefile:**
   - Replace `pip` commands with `poetry run`
   - Add Poetry-specific commands

5. **Update documentation:**
   - Update README with Poetry setup instructions
   - Update troubleshooting guide

## Getting Help
- Check the documentation in the `docs/` folder.
- Search for similar issues online or in the project's issue tracker.
- Run `poetry run python diagnostics.py` to check system health.
- Review the diagnostic report for specific error details.

## Prevention Tips
- Always test Poetry setup in a clean environment.
- Use `.env.example` as a template for environment variables.
- Keep Dockerfile and pyproject.toml in sync.
- Run diagnostics script after major changes to catch issues early. 