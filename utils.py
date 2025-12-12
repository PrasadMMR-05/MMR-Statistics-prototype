def build_text(stat, chart):
    title = stat.get("title", "")
    region = stat.get("region", "")
    time_period = stat.get("timePeriod", "")
    desc = stat.get("description", "")

    chart_type = chart.get("chartType") if chart else None
    x_label = chart.get("xLabel") if chart else None
    y_label = chart.get("yLabel") if chart else None
    series = chart.get("series") if chart else []

    series_names = ",".join([s.get("name","") for s in series]) if series else ""

    text = f"""
{title} | {region} | {time_period}
{desc}
CHART: type={chart_type}, series={series_names}, x={x_label}, y={y_label}
    """.strip()

    return text
