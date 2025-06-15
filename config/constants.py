# IAB Tier 1 Categories
IAB_TIER1_CATEGORIES = [
    "Arts & Entertainment",
    "Automotive", 
    "Business",
    "Careers",
    "Education",
    "Family & Parenting",
    "Health & Fitness",
    "Food & Drink",
    "Hobbies & Interests",
    "Home & Garden",
    "Law, Government & Politics",
    "News",
    "Personal Finance",
    "Society",
    "Science",
    "Pets",
    "Sports",
    "Style & Fashion",
    "Technology & Computing",
    "Travel",
    "Real Estate",
    "Shopping",
    "Religion & Spirituality",
    "Non-Standard Content"
]

# Intent scoring weights
INTENT_WEIGHTS = {
    'transactional': 95,
    'commercial': 75,
    'navigational': 45,
    'informational': 15
}

# Confidence multipliers
CONFIDENCE_MULTIPLIERS = {
    'high': 1.0,
    'medium': 0.85,
    'low': 0.7
}