from io import BytesIO

import matplotlib

matplotlib.use("Agg")  # phải đứng trước khi import pyplot
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns


def distribution_png(df):
    fig, ax = plt.subplots(figsize=(8, 4.5))
    if df.empty:
        ax.text(0.5, 0.5, "Không có dữ liệu",
                ha="center", va="center", fontsize=16)
        ax.set_axis_off()
    else:
        sns.histplot(data=df, x="total_score", bins=10,
                     kde=True, color="#2563eb", ax=ax)
        ax.set(title="Phân phối điểm tổng kết",
               xlabel="Điểm tổng kết", ylabel="Số sinh viên")
    fig.tight_layout()

    buffer = BytesIO()
    fig.savefig(buffer, format="png", dpi=140)
    plt.close(fig)
    buffer.seek(0)
    return buffer


def classification_chart_html(df):
    counts = (
        df["classification"].astype(str)
        .value_counts()
        .rename_axis("classification")
        .reset_index(name="count")
    )
    fig = px.bar(
        counts, x="classification", y="count",
        color="classification",
        title="Số sinh viên theo xếp loại",
    )
    fig.update_layout(showlegend=False, height=420)
    return fig.to_html(full_html=False, include_plotlyjs="cdn")