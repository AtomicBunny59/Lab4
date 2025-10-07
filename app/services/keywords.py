MAJOR_TO_KEYWORDS = {
    "computer science": ["computer science", "software engineer", "backend developer", "full stack engineer"],
    "data science": ["data science", "data scientist", "machine learning engineer", "data analyst"],
    "information systems": ["information systems", "business analyst", "systems analyst", "it support specialist"],
    "marketing": ["marketing", "marketing specialist", "digital marketing manager", "seo specialist"],
    "business": ["business", "business analyst", "operations analyst", "project coordinator"],
    "accounting": ["accounting", "accountant", "audit associate", "tax associate"],
    "finance": ["finance", "financial", "finance manager", "financial analyst", "credit analyst", "investment analyst", "financial advisor", "financial planner"],
    "nursing": ["nursing", "registered nurse", "clinical nurse", "staff nurse"],
    "not listed": ["warehouse associate", "retail associate", "customer service"],
}

def get_keywords(major):
    return MAJOR_TO_KEYWORDS.get((major or "").strip().lower(), [])