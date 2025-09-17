# molalchemy Project Roadmap

This document outlines the development roadmap for molalchemy, a SQLAlchemy extension for working with chemical cartridges in PostgreSQL. The roadmap is organized by development phases and includes specific opportunities for contributors.

## 🎯 Project Vision

molalchemy aims to be the **definitive Python library** for chemical database operations, providing:
- Integration between Python and chemical databases
- Support for all major chemical cartridges (Bingo, RDKit)
- Type-safe, modern SQLAlchemy 2.0+ API with full IDE support (type hints, autocompletion)
- Production-ready Docker containers for easy deployment
- Comprehensive documentation and examples

## 📊 Current Status

- **Bingo PostgreSQL Integration**
  - ✅ All data types (`BingoMol`, `BingoBinaryMol`, `BingoReaction`, `BingoBinaryReaction`)
  - ✅ Chemical indices (`BingoMolIndex`, etc.)
  - ❌ Function library (`mol`, `rxn`), some conversion and export functions missing
  - ❌ Full documentation with examples

- **RDKit PostgreSQL Integration**
  - ✅ Core data types (`RdkitMol`, fingerprint types)
  - ✅ Basic function library
  - ❌ Missing: Complete function set, tests, documentation

- **Infrastructure**
  - ✅ Modern development setup (uv, ruff, pytest, pre-commit)
  - 🚧 Docker containers for Bingo and RDKit
  - ✅ CI/CD pipeline setup
  - 🚧 Documentation framework (MkDocs + mkdocstrings)


### 🚧 **In Progress**
- Documentation enhancements
- RDKit module completion
- Docker image optimization

### ❌ **Not Started**
- ChemAxon cartridge integration (closed source, requires license)
- NextMove Author integration (closed source, requires license)
- SQLite RDKit support (including custom builds or custom event listeners)
- Performance benchmarking
- Advanced chemical operations

---

## To be discussed

### How to handle functions

Currently both Bingo and Rdkit functions under the hood just use SQLAlchemy's `func` to call the underlying SQL functions.
Wrapping them in Python functions allows for type hints and better IDE support. However, this approach is not the prefered SQLAlchemy way, it expects the functions to be registedred using `sqlalchemy.sql.functions.Function`, which allows to e.g define the expected return type and provides some internal validation(i guess?)

Also, for now, I splitted the functions module into the separte namespace modules based on the function's input type (e.g `mol`, `rxn`, `fp`), which makes it easier to find the functions, but clutters the top-level namespace. Maybe it would be better to have a flat structure with all functions in one module?

### Multi-dialect support

Currently the library is tightly coupled to PostgreSQL, as RDkit extension is only available for PostgreSQL. But technically for Bingo and some other closed source cartridges (e.g ChemAxon) it would be possible to support other databases (e.g MySQL, Oracle).

---

## 🐳 Docker Container Strategy

### **Current Docker Infrastructure**

We maintain Docker containers for each supported cartridge to ensure easy deployment and consistent environments.

#### **Existing Containers**
- PostgreSQL with Bingo cartridge
- PostgreSQL with RDKit cartridge



#### **Documentation**
- Container usage guides
- Environment variable reference
- Volume mounting best practices
- Production deployment guides

---

## 🔧 Development Environment

### **For Contributors**

```bash
# Clone and setup
git clone https://github.com/asiomchen/molalchemy.git
cd molalchemy
uv sync

# Start development database
docker-compose up bingo  # or rdkit

# Run tests
make test

# Start documentation server
uv run mkdocs serve
```

### **Development Guidelines**

#### **Code Quality**
- Type hints for all public APIs
- 100% test coverage for new features
- Documentation for all public functions
- Follow existing code patterns

#### **Testing Requirements**
- Unit tests for all functions
- Integration tests for complex workflows
- Performance tests for critical paths
- Docker-based testing for CI/CD

#### **Documentation Standards**
- NumPy-style docstrings
- Working code examples
- API reference completeness
- User guide updates

---

## 🤝 How to Contribute

### **Getting Started**
1. Check the [issues page](https://github.com/asiomchen/molalchemy/issues) for good first issues
2. Read the [Contributing Guide](contributing.md)
3. Join discussions in GitHub Discussions
4. Set up your development environment

### **Contribution Process**
1. Fork the repository
2. Create a feature branch
3. Implement your changes
4. Add tests and documentation
5. Submit a pull request

### **Support**
- GitHub Discussions for questions
- GitHub Issues for bugs and features
- Direct contact: anton.siomchen+molalchemy@gmail.com

---

**molalchemy** - Making chemical databases as easy as regular databases! 🧪✨

*Last updated: September 2025*