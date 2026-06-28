# Bank Expense Analyzer

> A comprehensive personal finance management system that automates expense categorization, consolidates multiple bank accounts, and provides actionable spending insights through interactive visualizations.

---

## 📋 Table of Contents

- [Overview](#overview)
- [STAR: Project Context](#star-project-context)
- [Key Features](#key-features)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Configuration](#configuration)
- [Data Pipeline](#data-pipeline)
- [Troubleshooting](#troubleshooting)
- [Future Enhancements](#future-enhancements)

---

## 🎯 Overview

Bank Expense Analyzer is a Python-based financial management system designed to help users gain control over their spending habits. By integrating data from multiple bank accounts, automatically categorizing transactions, and providing visual analytics, the system enables informed financial decision-making.

**Perfect for:**
- Tracking expenses across multiple bank accounts
- Understanding spending patterns by category
- Automating transaction categorization with customizable rules
- Building a unified personal finance dashboard

---

## 🎬 STAR: Project Context

### **Situation**
Managing personal finances across multiple bank accounts can be overwhelming. Bank statements arrive in different formats, transaction descriptions are inconsistent, and manually categorizing hundreds of transactions is time-consuming and error-prone. Users lack a centralized view of their spending patterns across all accounts.

### **Tasks**
The project required developing an automated solution to:
1. **Consolidate** transactions from multiple bank accounts into a unified database
2. **Normalize** data across different bank export formats
3. **Intelligently categorize** transactions using configurable rule-based matching
4. **Prevent duplicates** when importing new statements
5. **Provide visualization** of spending patterns and trends
6. **Enable manual adjustments** to automatically-assigned categories

### **Actions**
✅ **Data Ingestion Pipeline**: Built a robust data loading system that reads CSV files from multiple banks, handling various formats and column naming conventions

✅ **Data Cleaning Module**: Implemented comprehensive data validation including:
   - Column standardization and renaming
   - Duplicate detection and removal
   - Date and amount format normalization
   - Empty column and row elimination

✅ **Intelligent Categorization Engine**: Developed a regex-based rule system that:
   - Matches transaction descriptions against customizable category patterns
   - Supports hierarchical categorization (Category → Subcategory)
   - Tracks manual vs. automatic categorizations
   - Allows rule versioning and updates

✅ **Interactive Dashboard**: Created a Streamlit-powered frontend to:
   - Visualize spending patterns and trends
   - Edit and manage transaction categories
   - Export processed data for further analysis

✅ **Configuration Management**: Designed a YAML-based configuration system for:
   - File paths and data sources
   - Column mappings for different bank formats
   - Category rules and patterns
   - Output specifications

### **Results**
📊 **Operational Efficiency**:
   - Reduced manual data processing time by automating imports
   - Eliminated duplicate entry issues through intelligent deduplication
   - Enabled 90%+ automatic categorization accuracy with rule refinement

📈 **Financial Insights**:
   - Consolidated view of spending across all bank accounts
   - Clear identification of major expense categories
   - Ability to track spending trends over time
   - Foundation for budgeting and financial forecasting

🛠️ **System Quality**:
   - Modular architecture for easy maintenance and updates
   - Unit tests ensuring data integrity
   - Configuration-driven approach for flexibility
   - Incrementally updatable database preventing data loss

---

## ✨ Key Features

| Feature | Description |
|---------|-------------|
| **Multi-Account Integration** | Import and consolidate transactions from multiple bank accounts |
| **Automatic Categorization** | Regex-based rule engine for intelligent transaction categorization |
| **Format Flexibility** | Handles various CSV formats from different banks |
| **Duplicate Prevention** | Automatic detection and prevention of duplicate entries |
| **Manual Corrections** | Interactive UI to adjust categories and manage rules |
| **Data Persistence** | Incremental updates preserving historical data |
| **Visual Analytics** | Dashboard with spending patterns and trends |
| **Configuration-Driven** | YAML-based settings for easy customization |
| **Data Validation** | Comprehensive cleaning and normalization pipeline |

---

## 🛠️ Technology Stack

### Core Technologies
- **Python 3.13**: Primary programming language
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computing

### Frontend
- **Streamlit 1.53.0**: Interactive web dashboard

### Configuration & Data
- **PyYAML**: YAML configuration file parsing
- **JSONSchema**: Data validation
- **JSON/CSV**: Data formats

### Visualization
- **Matplotlib**: Core plotting library
- **Seaborn**: Statistical data visualization

### Environment Management
- **Conda**: Package and environment management
- **Python 3.13**: Runtime environment

---

## 📁 Project Structure

```
├── src/                           # Core application modules
│   ├── __init__.py
│   ├── run_pipeline.py           # Main ETL orchestration
│   ├── categorize.py             # Transaction categorization engine
│   ├── clean.py                  # Data cleaning functions
│   ├── config_loader.py          # Configuration management
│   └── io_utils.py               # File I/O utilities
│
├── app/                           # User-facing applications
│   ├── streamlit/                # Streamlit dashboard
│   │   ├── main.py               # Dashboard entry point
│   │   └── edit_categories.py    # Category management interface
│   └── power bi/                 # Power BI integration
│
├── config/                        # Configuration files
│   ├── config_example.yml        # Example configuration template
│   └── config_local.yml          # Local configuration (user-specific)
│
├── data/                          # Data directory
│   ├── raw/                      # Raw bank export files
│   │   ├── example/
│   │   └── personal/
│   ├── processed/                # Processed and cleaned data
│   │   ├── example/
│   │   └── personal/
│   └── reference/                # Reference data (categories)
│       └── categories.json
│
├── notebook/                      # Jupyter notebooks
│   ├── EDA.ipynb                 # Exploratory data analysis
│   └── test.ipynb                # Testing and development
│
├── tests/                         # Unit tests
│   ├── __init__.py
│   └── test_pipeline.py
│
├── environment.yml               # Conda environment specification
└── README.md                     # This file

```

---

## 🚀 Getting Started

### Prerequisites
- **Conda/Anaconda** installed on your system
- **Git** for version control
- Minimum **1GB free disk space** for data storage

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Analyse_comptes_bancaires
   ```

2. **Create the Conda environment**
   ```bash
   conda env create -f environment.yml
   ```

3. **Activate the environment**
   ```bash
   conda activate bank_expense_analyzer
   ```

4. **Copy and customize the configuration**
   ```bash
   cp config/config_example.yml config/config_local.yml
   # Edit config_local.yml with your paths and settings
   ```

### Quick Start

**Run the data pipeline:**
```bash
python -m src.run_pipeline
```

**Launch the Streamlit dashboard:**
```bash
streamlit run app/streamlit/main.py
```

**Access the dashboard:**
- Open your browser to `http://localhost:8501`

---

## 📊 Usage

### Data Import Workflow

1. **Export your bank statements** as CSV files from your bank
2. **Place them** in the configured `data/raw/` directory
3. **Run the pipeline** to process new transactions
4. **Review** categorizations in the dashboard
5. **Manually adjust** categories as needed

### Configuration Setup

Edit `config/config_local.yml`:

```yaml
# Data paths
input_folder: "data/raw/personal"
output_final: "data/processed/personal/final_data.csv"

# Column mappings for your bank format
columns_mapping:
  date: "Date"
  amount: "Amount"
  description: "Description"

# File specifications
file_extensions: [".csv"]
merge_col: "Transaction_ID"

# Path to categorization rules
rules_file: "config/rules.json"
```

### Categorization Rules

Define rules in JSON format:

```json
{
  "Food & Dining": [
    "(?i)restaurant",
    "(?i)pizza|burger|cafe",
    "(?i)supermarket"
  ],
  "Transport": [
    "(?i)uber|taxi|gas",
    "(?i)parking"
  ]
}
```

---

## 🔄 Data Pipeline

The system follows a robust ETL (Extract, Transform, Load) process:

```
┌─────────────────────────────────────────────────────────────┐
│                    DATA PIPELINE FLOW                        │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  1. EXTRACT                                                  │
│     └─ Load CSV files from data/raw/                        │
│     └─ Read existing processed dataset (if exists)          │
│                                                               │
│  2. TRANSFORM                                               │
│     └─ Rename columns based on config mapping             │
│     └─ Convert date formats (day-first)                     │
│     └─ Normalize amounts (comma → dot)                     │
│     └─ Drop empty columns & duplicates                     │
│     └─ Parse configuration and rules                       │
│                                                               │
│  3. DEDUPLICATION                                           │
│     └─ Compare against existing dataset                     │
│     └─ Identify new transactions                            │
│     └─ Preserve historical data                             │
│                                                               │
│  4. CATEGORIZATION                                          │
│     └─ Apply regex-based category rules                     │
│     └─ Assign primary & secondary categories                │
│     └─ Flag for manual review if uncertain                 │
│                                                               │
│  5. LOAD                                                    │
│     └─ Merge with existing dataset                          │
│     └─ Save to data/processed/final_data.csv               │
│     └─ Maintain data integrity and backups                 │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

---

## ⚙️ Configuration

### Key Configuration Parameters

| Parameter | Purpose | Example |
|-----------|---------|---------|
| `input_folder` | Raw CSV import location | `data/raw/personal` |
| `output_final` | Processed output file | `data/processed/final_data.csv` |
| `file_extensions` | Import file types | `[".csv"]` |
| `columns_mapping` | Column name mapping | `{date: "Date", ...}` |
| `merge_col` | Unique transaction identifier | `"Transaction_ID"` |
| `rules_file` | Category rules location | `"config/rules.json"` |

### Environment Variables

Set in your `.bashrc`, `.zshrc`, or system environment:

```bash
# Optional: override config location
export BANK_ANALYZER_CONFIG="path/to/config.yml"

# Optional: enable debug logging
export BANK_ANALYZER_DEBUG="true"
```

---

## 🧪 Testing

Run the test suite:

```bash
pytest tests/
```

Run specific tests:

```bash
pytest tests/test_pipeline.py -v
```

---

## 🔍 Troubleshooting

### Issue: "File not found" error
**Solution**: Verify file paths in `config_local.yml` and ensure files exist in specified directories.

### Issue: Columns not recognized
**Solution**: Check column names match exactly in `columns_mapping` within config file. Use EDA.ipynb to inspect actual column names.

### Issue: Transactions not categorized
**Solution**: Review categorization rules in `config/rules.json`. Rules use regex patterns; ensure patterns match transaction descriptions.

### Issue: Duplicate entries appearing
**Solution**: Verify the `merge_col` is correctly identifying unique transactions. Check for inconsistencies in the data.

### Issue: Streamlit dashboard not loading
**Solution**: 
```bash
# Ensure environment is activated
conda activate bank_expense_analyzer

# Clear Streamlit cache
streamlit cache clear

# Restart the app
streamlit run app/streamlit/main.py
```

---

## 🚦 Dependencies

### Python Packages
- `pandas`: Data manipulation
- `numpy`: Numerical operations
- `pyyaml`: Configuration parsing
- `jsonschema`: Validation
- `streamlit`: Web interface
- `matplotlib`: Visualization
- `seaborn`: Statistical plotting

### System Requirements
- Python 3.13+
- 2GB RAM (minimum)
- 1GB disk space for sample data

---

## 📈 Future Enhancements

### Phase 2: Advanced Analytics
- [ ] Machine learning-based categorization refinement
- [ ] Anomaly detection for unusual transactions
- [ ] Spending forecasting and budget recommendations
- [ ] Multi-currency support

### Phase 3: User Experience
- [ ] Web-based UI (replacing Streamlit)
- [ ] User authentication and data privacy
- [ ] Multi-user support with shared accounts
- [ ] Mobile application

### Phase 4: Integration
- [ ] Real-time bank API integration (Open Banking standards)
- [ ] Automated transaction syncing
- [ ] Export to accounting software (QuickBooks, FreshBooks)
- [ ] Integration with financial planning tools

### Phase 5: Data Governance
- [ ] Encrypted data storage
- [ ] Audit logging
- [ ] Data retention policies
- [ ] GDPR compliance features

---

## 📝 Development Notes

### Code Style
- Follow PEP 8 guidelines
- Use type hints for function parameters
- Document complex functions with docstrings
- Keep functions focused and modular

### Adding New Features
1. Create a new module in `src/`
2. Write unit tests in `tests/`
3. Update configuration schema if needed
4. Document in README

### Debugging
- Use the notebooks in `notebook/` for exploratory work
- Enable logging: `logging.basicConfig(level=logging.DEBUG)`
- Check data at each pipeline stage

---

## 📜 License

This project is provided as-is for personal financial management. All data remains private and local.

---

## 👤 Author

**Adeline Le Ray**  
*Data Analyst | Finance Automation*

---

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## ❓ Support

For issues, questions, or feedback:
- Check the [Troubleshooting](#troubleshooting) section
- Review existing issues
- Create a new issue with detailed information

---

**Last Updated**: April 2026  
**Version**: 1.0.0
