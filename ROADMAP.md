# molalchemy Project Roadmap

This document outlines the development roadmap for molalchemy, a SQLAlchemy extension for working with chemical cartridges in PostgreSQL. The roadmap is organized by development phases and includes specific opportunities for contributors.

## 🎯 Project Vision

molalchemy aims to be the **definitive Python library** for chemical database operations, providing:
- Seamless integration between Python and chemical databases
- Support for all major chemical cartridges (Bingo, RDKit, ChemAxon, etc.)
- Type-safe, modern SQLAlchemy 2.0+ API with full IDE support (type hints, autocompletion)
- Production-ready Docker containers for easy deployment
- Comprehensive documentation and examples

## 📊 Current Status

- **Bingo PostgreSQL Integration** (95% complete)
  - ✅ All data types (`BingoMol`, `BingoBinaryMol`, `BingoReaction`, `BingoBinaryReaction`)
  - ✅ Chemical indices (`BingoMolIndex`, etc.)
  - ✅ Function library (`mol`, `rxn`), some conversion and export functions missing
  - ❌ Full documentation with examples

- **RDKit PostgreSQL Integration** (75% complete)
  - ✅ Core data types (`RdkitMol`, fingerprint types)
  - ✅ Basic function library
  - ❌ Missing: Complete function set, tests, documentation

- **Infrastructure**
  - ✅ Modern development setup (uv, ruff, pytest, pre-commit)
  - ✅ Docker containers for Bingo and RDKit
  - ✅ CI/CD pipeline setup
  - ✅ Documentation framework (MkDocs + mkdocstrings)
  - 🚧

### 🚧 **In Progress**
- Documentation enhancements
- RDKit module completion
- Docker image optimization

### ❌ **Not Started**
- ChemAxon cartridge integration
- SQLite RDKit support (including custom builds)
- Performance benchmarking
- Advanced chemical operations

---

## 🐳 Docker Container Strategy

### **Current Docker Infrastructure**

We maintain Docker containers for each supported cartridge to ensure easy deployment and consistent environments.

#### **Existing Containers**
- `molalchemy/bingo-postgres` - PostgreSQL with Bingo cartridge
- `molalchemy/rdkit-postgres` - PostgreSQL with RDKit cartridge



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
uv run pytest tests/

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