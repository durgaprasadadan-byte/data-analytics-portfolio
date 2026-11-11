"""Single source of truth for every portfolio project.

The home page, category pages and statistics all read from here, so a project
is added or promoted by editing one entry. Statistics are derived from
`Project.status`; nothing counts as published until it is marked COMPLETED.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Status(str, Enum):
    PLANNED = "Planned"
    IN_PROGRESS = "In progress"
    COMPLETED = "Completed"


@dataclass(frozen=True)
class Category:
    key: str
    label: str
    icon: str  # Material icon shorthand
    page_path: str
    summary: str
    phase: int  # build phase in which the category's content ships
    is_technology: bool = True


@dataclass(frozen=True)
class Project:
    id: str
    title: str
    category: str
    domain: str
    difficulty: str
    description: str
    tools: tuple[str, ...]
    status: Status = Status.PLANNED
    featured: bool = False
    dataset_name: str | None = None  # set only once a real dataset is chosen


@dataclass(frozen=True)
class Tool:
    key: str  # matches entries in Project.tools
    label: str
    blurb: str


@dataclass(frozen=True)
class PortfolioStats:
    total: int
    live: int
    categories: int
    datasets_live: int
    ml_total: int
    ml_live: int


CATEGORIES: dict[str, Category] = {
    c.key: c
    for c in (
        Category("tableau", "Tableau", ":material/bar_chart:", "pages/02_Tableau.py",
                 "Interactive dashboards and visual storytelling for sales, HR, healthcare and marketing.", 6),
        Category("power_bi", "Power BI", ":material/dashboard:", "pages/03_Power_BI.py",
                 "Data models, DAX measures and reports for finance, e-commerce, supply chain and banking.", 6),
        Category("excel", "Excel", ":material/table_chart:", "pages/04_Excel.py",
                 "PivotTables, lookup formulas, Power Query and dashboards for everyday business reporting.", 6),
        Category("python_analytics", "Python Analytics", ":material/code:", "pages/05_Python_Analytics.py",
                 "Data cleaning, exploratory analysis and interactive charts with Pandas, NumPy and Plotly.", 4),
        Category("machine_learning", "Machine Learning", ":material/model_training:", "pages/06_Machine_Learning.py",
                 "Supervised learning workflows with Scikit-learn, from preprocessing to explainable predictions.", 5),
        Category("end_to_end", "End-to-End Projects", ":material/hub:", "pages/07_End_to_End.py",
                 "Full pipelines that combine data preparation, analytics, modelling and reporting.", 7,
                 is_technology=False),
    )
}

TOOLS: tuple[Tool, ...] = (
    Tool("Tableau", "Tableau", "Dashboards and visual storytelling"),
    Tool("Power BI", "Power BI", "Data models, DAX and published reports"),
    Tool("Excel", "Microsoft Excel", "PivotTables, formulas and reporting workbooks"),
    Tool("Python", "Python", "Scripting and analysis workflows"),
    Tool("Pandas", "Pandas", "Data cleaning and transformation"),
    Tool("NumPy", "NumPy", "Numerical computing and statistics"),
    Tool("Scikit-learn", "Scikit-learn", "Predictive modelling and evaluation"),
    Tool("SQL", "SQL", "Querying and shaping relational data"),
    Tool("Streamlit", "Streamlit", "Interactive data applications"),
)

_PY = ("Python", "Pandas", "NumPy", "Plotly", "Streamlit")
_ML = ("Python", "Pandas", "NumPy", "Scikit-learn", "Streamlit")

PROJECTS: tuple[Project, ...] = (
    # Tableau
    Project("tableau-sales", "Global Sales Performance & Revenue Analytics", "tableau", "Sales & Revenue",
            "Intermediate", "Revenue, margin and regional performance dashboard for sales leadership.",
            ("Tableau",), featured=True),
    Project("tableau-hr", "HR Analytics & Employee Attrition", "tableau", "Human Resources",
            "Intermediate", "Headcount, turnover and attrition drivers for HR teams.", ("Tableau",)),
    Project("tableau-healthcare", "Healthcare Operations & Patient Analytics", "tableau", "Healthcare",
            "Intermediate", "Patient flow, length of stay and operational load across care units.", ("Tableau",)),
    Project("tableau-marketing", "Digital Marketing & Campaign Performance", "tableau", "Marketing",
            "Intermediate", "Channel spend, conversion and return on campaign investment.", ("Tableau",)),
    # Power BI
    Project("powerbi-finance", "Financial Performance & Profitability Dashboard", "power_bi", "Finance",
            "Advanced", "Star-schema model with DAX measures for profit, margin and period comparison.",
            ("Power BI",), featured=True),
    Project("powerbi-ecommerce", "E-commerce Customer & Sales Intelligence", "power_bi", "E-commerce",
            "Intermediate", "Customer segments, basket behaviour and sales trends in one report.", ("Power BI",)),
    Project("powerbi-supply-chain", "Supply Chain & Inventory Management", "power_bi", "Supply Chain",
            "Intermediate", "Stock levels, supplier delivery and fulfilment performance.", ("Power BI",)),
    Project("powerbi-banking", "Banking Transactions & Fraud Monitoring", "power_bi", "Banking",
            "Advanced", "Transaction monitoring with time intelligence and anomaly flags.", ("Power BI",)),
    # Excel
    Project("excel-sales", "Sales Analysis & Executive Reporting", "excel", "Sales & Revenue",
            "Beginner", "PivotTable-driven executive summary with lookup formulas and conditional formatting.",
            ("Excel",), featured=True),
    Project("excel-personal-finance", "Personal Finance & Expense Management", "excel", "Personal Finance",
            "Beginner", "Budget and expense tracker built with SUMIFS, validation and charts.", ("Excel",)),
    Project("excel-payroll", "Employee Payroll & Workforce Analytics", "excel", "Human Resources",
            "Intermediate", "Payroll calculations and workforce summaries using nested formulas.", ("Excel",)),
    Project("excel-inventory", "Inventory & Stock Management System", "excel", "Supply Chain",
            "Intermediate", "Stock tracking with reorder alerts and Power Query refresh.", ("Excel",)),
    # Python analytics
    Project("py-ecommerce", "E-commerce Data Analysis & Customer Behavior", "python_analytics", "E-commerce",
            "Intermediate", "Cleaning, profiling and exploring order data to understand customer behaviour.",
            _PY, featured=True),
    Project("py-healthcare", "Healthcare Data Analysis & Patient Outcomes", "python_analytics", "Healthcare",
            "Intermediate", "Statistical exploration of patient records and outcome drivers.", _PY),
    Project("py-web-analytics", "Web Analytics & Digital Marketing Performance", "python_analytics", "Marketing",
            "Intermediate", "Traffic, engagement and conversion analysis with interactive filters.", _PY),
    Project("py-banking", "Banking Transaction Analysis & Fraud EDA", "python_analytics", "Banking",
            "Advanced", "Exploratory analysis of transaction patterns and fraud indicators.", _PY),
    # Machine learning
    Project("ml-fraud", "Credit Card Fraud Detection", "machine_learning", "Banking",
            "Advanced", "Imbalanced-class classification evaluated with precision, recall and ROC-AUC.", _ML),
    Project("ml-churn", "Customer Churn Prediction", "machine_learning", "Telecom & Subscriptions",
            "Intermediate", "Classification model with a prediction form and feature importance.", _ML,
            featured=True),
    Project("ml-house-price", "Real Estate Price Prediction", "machine_learning", "Real Estate",
            "Intermediate", "Regression workflow comparing linear and tree-based models.", _ML),
    Project("ml-attrition", "Employee Attrition Prediction", "machine_learning", "Human Resources",
            "Intermediate", "Classification of attrition risk with explainable drivers.", _ML),
    # End to end
    Project("e2e-ecommerce", "E-commerce Analytics Platform", "end_to_end", "E-commerce",
            "Advanced", "Pipeline from raw orders to cleaned data, dashboards and churn scoring.",
            _ML + ("Plotly",), featured=True),
    Project("e2e-banking", "Banking Analytics Platform", "end_to_end", "Banking",
            "Advanced", "Pipeline from raw transactions to monitoring views and fraud scoring.",
            _ML + ("Plotly",)),
)


def _validate() -> None:
    ids = [p.id for p in PROJECTS]
    if len(ids) != len(set(ids)):
        raise ValueError("Duplicate project ids in registry")
    for p in PROJECTS:
        if p.category not in CATEGORIES:
            raise ValueError(f"{p.id}: unknown category {p.category!r}")
    known_tools = {t.key for t in TOOLS}
    for p in PROJECTS:
        # Plotly is a supporting library, not a headline tool card.
        unknown = set(p.tools) - known_tools - {"Plotly"}
        if unknown:
            raise ValueError(f"{p.id}: unknown tools {sorted(unknown)}")


_validate()


def projects_by_category(category_key: str) -> list[Project]:
    return [p for p in PROJECTS if p.category == category_key]


def featured_projects() -> list[Project]:
    return [p for p in PROJECTS if p.featured]


def portfolio_stats() -> PortfolioStats:
    live = [p for p in PROJECTS if p.status is Status.COMPLETED]
    ml = projects_by_category("machine_learning")
    return PortfolioStats(
        total=len(PROJECTS),
        live=len(live),
        categories=len({p.category for p in PROJECTS if CATEGORIES[p.category].is_technology}),
        datasets_live=len({p.dataset_name for p in live if p.dataset_name}),
        ml_total=len(ml),
        ml_live=sum(1 for p in ml if p.status is Status.COMPLETED),
    )


def tool_usage(tool_key: str) -> tuple[int, int]:
    """Return (projects using the tool, of which completed)."""
    using = [p for p in PROJECTS if tool_key in p.tools]
    return len(using), sum(1 for p in using if p.status is Status.COMPLETED)
