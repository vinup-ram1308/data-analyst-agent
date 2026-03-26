import json
import pandas as pd
from io import StringIO


def analyze_csv(csv_text: str) -> dict:
    """
    Performs a complete analysis of a CSV dataset in one step.

    This tool does everything internally:
    - Data quality check (nulls, types, duplicates)
    - Statistical summary (mean, median, std, min, max)
    - Markdown report generation

    Args:
        csv_text: Raw CSV content as a plain string.

    Returns:
        A dictionary with a 'report' key containing the full Markdown report.
    """
    try:
        df = pd.read_csv(StringIO(csv_text))

        total_rows, total_cols = df.shape
        duplicate_count = int(df.duplicated().sum())
        missing = {col: int(df[col].isna().sum()) for col in df.columns}
        missing_pct = {
            col: round((count / total_rows) * 100, 1)
            for col, count in missing.items()
        }
        col_types = {col: str(dtype) for col, dtype in df.dtypes.items()}

        numeric_cols   = df.select_dtypes(include="number").columns.tolist()
        categorical_cols = df.select_dtypes(
            include=["object", "category", "bool"]
        ).columns.tolist()

        numeric_stats = {}
        for col in numeric_cols:
            series = df[col].dropna()
            numeric_stats[col] = {
                "count":  int(series.count()),
                "mean":   round(float(series.mean()), 2),
                "median": round(float(series.median()), 2),
                "std":    round(float(series.std()), 2),
                "min":    round(float(series.min()), 2),
                "max":    round(float(series.max()), 2),
                "q25":    round(float(series.quantile(0.25)), 2),
                "q75":    round(float(series.quantile(0.75)), 2),
            }

        categorical_stats = {}
        for col in categorical_cols:
            series = df[col].dropna()
            top5 = series.value_counts().head(5).to_dict()
            categorical_stats[col] = {
                "unique": int(series.nunique()),
                "top5":   {str(k): int(v) for k, v in top5.items()},
            }

        # ── Helper: format numbers with commas ───────────────────────────
        def fmt(val):
            if isinstance(val, float) and val == int(val):
                return f"{int(val):,}"
            if isinstance(val, float):
                return f"{val:,.2f}"
            if isinstance(val, int):
                return f"{val:,}"
            return str(val)

        # ── Issues summary ────────────────────────────────────────────────
        issues = []
        cols_with_missing = [c for c, v in missing.items() if v > 0]
        if duplicate_count > 0:
            issues.append(f"{duplicate_count} duplicate row(s) detected")
        if cols_with_missing:
            issues.append(
                f"missing values in: {', '.join(cols_with_missing)}"
            )

        # ── Build Markdown report ─────────────────────────────────────────
        lines = []

        # ── Header ───────────────────────────────────────────────────────
        lines += [
            "# CSV Dataset Analysis Report",
            "",
            "> **Agent:** CSV Analyst · **Model:** Gemini · **Platform:** Google Cloud",
            "",
            "---",
            "",
        ]

        # ── Issues callout ────────────────────────────────────────────────
        if issues:
            lines += [
                f"> ⚠️ **Issues found:** {' · '.join(issues)}",
                "",
            ]
        else:
            lines += [
                "> ✅ **No data quality issues found.**",
                "",
            ]

        # ── Section 1: Overview ───────────────────────────────────────────
        lines += [
            "## 1. Dataset Overview",
            "",
            f"| Metric | Value |",
            f"|:-------|------:|",
            f"| Total rows | {fmt(total_rows)} |",
            f"| Total columns | {fmt(total_cols)} |",
            f"| Duplicate rows | {fmt(duplicate_count)} |",
            f"| Numeric columns | {fmt(len(numeric_cols))} |",
            f"| Categorical columns | {fmt(len(categorical_cols))} |",
            f"| Columns with missing values | {fmt(len(cols_with_missing))} |",
            "",
            "---",
            "",
        ]

        # ── Section 2: Data Quality ───────────────────────────────────────
        lines += [
            "## 2. Data Quality Check",
            "",
            "| Column | Type | Missing | Missing % | Status |",
            "|:-------|:-----|--------:|----------:|:-------|",
        ]
        for col in df.columns:
            m   = missing[col]
            p   = missing_pct[col]
            status = "⚠️  Missing"  if m > 0 else "✅  Complete"
            lines.append(
                f"| `{col}` | {col_types[col]} | {fmt(m)} | {p}% | {status} |"
            )

        dup_msg = (
            f"\n> ⚠️ **{duplicate_count} duplicate row(s)** found — "
            "consider deduplication before further analysis."
            if duplicate_count > 0
            else "\n> ✅ No duplicate rows detected."
        )
        lines += [dup_msg, "", "---", ""]

        # ── Section 3: Statistical Summary ───────────────────────────────
        if numeric_stats:
            lines += [
                "## 3. Statistical Summary",
                "",
                "| Column | Count | Mean | Median | Std Dev | Min | Max | 25th % | 75th % |",
                "|:-------|------:|-----:|-------:|--------:|----:|----:|-------:|-------:|",
            ]
            for col, s in numeric_stats.items():
                lines.append(
                    f"| `{col}` "
                    f"| {fmt(s['count'])} "
                    f"| {fmt(s['mean'])} "
                    f"| {fmt(s['median'])} "
                    f"| {fmt(s['std'])} "
                    f"| {fmt(s['min'])} "
                    f"| {fmt(s['max'])} "
                    f"| {fmt(s['q25'])} "
                    f"| {fmt(s['q75'])} |"
                )
            lines += ["", "---", ""]

        # ── Section 4: Categorical Summary ───────────────────────────────
        if categorical_stats:
            lines += [
                "## 4. Categorical Column Summary",
                "",
            ]
            for col, s in categorical_stats.items():
                lines += [
                    f"### `{col}` — {s['unique']} unique value(s)",
                    "",
                    "| Value | Count | Share |",
                    "|:------|------:|------:|",
                ]
                total_cat = sum(s["top5"].values())
                for val, count in s["top5"].items():
                    share = round((count / total_rows) * 100, 1)
                    lines.append(f"| {val} | {fmt(count)} | {share}% |")
                lines.append("")
            lines += ["---", ""]

        # ── Footer ────────────────────────────────────────────────────────
        lines += [
            "*Report generated by the CSV Analyst Agent · "
            "Powered by Gemini on Google Cloud*",
        ]

        return {
            "status": "success",
            "report": "\n".join(lines),
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}
        