from langchain_tavily import TavilySearch
from config import get_settings

# ==========================================
# SECTION 1: TAVILY SEARCH TOOL
# ==========================================
settings = get_settings()
_web_search = None

def web_search_tool():
    global _web_search
    if _web_search is None:
        if not settings.tavily_api_key:
            raise RuntimeError("TAVILY_API_KEY is missing")
        _web_search = TavilySearch(
            tavily_api_key=settings.tavily_api_key,
            max_results=5,
            topic="general",
            include_answer=True,
            include_raw_content=False,
        )
    return _web_search
