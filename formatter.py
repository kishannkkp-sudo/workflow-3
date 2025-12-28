import markdown

def markdown_to_html(md_text: str) -> str:
    html = markdown.markdown(
        md_text,
        extensions=["tables", "fenced_code", "sane_lists"]
    )

    return f"""
    <div class="post-content">
        {html}
    </div>
    """
