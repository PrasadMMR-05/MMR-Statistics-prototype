def build_text(stat, chart):
    """
    Build a single readable text block for embedding
    combining statistic + chart information
    """

    title = stat.get("title", "No title")
    region = stat.get("region", "Global")
    period = stat.get("timePeriod", "N/A")
    industry = str(stat.get("industryId", ""))
    description = stat.get("description", "")

    # Chart details (safe access)
    chart_type = ""
    series_names = []
    x_label = ""
    y_label = ""

    if chart:
        chart_type = chart.get("chartType", "")

        # Extract series names if available
        series = chart.get("series", [])
        if isinstance(series, list):
            for s in series:
                name = s.get("name")
                if name:
                    series_names.append(name)

        x_label = chart.get("xAxisLabel", "")
        y_label = chart.get("yAxisLabel", "")

    text = f"""
{title}
Region: {region}
Time Period: {period}
Industry: {industry}

Description:
{description}

Chart Information:
Type: {chart_type}
Series: {", ".join(series_names)}
X-axis: {x_label}
Y-axis: {y_label}
""".strip()

    return text
