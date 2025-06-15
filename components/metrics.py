def calculate_intent_accuracy(result):
    """Calculate intent accuracy based on confidence and intentionality"""
    intention = result.get('intention', {})
    confidence = intention.get('confidence', 'low')
    confidence_accuracy = {'high': 85, 'medium': 70, 'low': 50}
    accuracy = confidence_accuracy.get(confidence, 85)
    
    intentionality = result.get('intentionality_breakdown', {})
    if intentionality and any(val > 0 for val in intentionality.values()):
        accuracy += 10
    
    return min(accuracy, 99)

def calculate_intentionality_score(result):
    """Calculate weighted intentionality score"""
    intentionality = result.get('intentionality_breakdown', {})
    intention = result.get('intention', {})
    confidence = intention.get('confidence', 'medium')
    
    if not intentionality:
        return 0
    
    intent_weights = {
        'transactional': 95,
        'commercial': 75,
        'navigational': 45,
        'informational': 15
    }
    
    weighted_score = 0
    for intent_type, percentage in intentionality.items():
        weight = intent_weights.get(intent_type.lower(), 0)
        weighted_score += (percentage / 100) * weight
    
    confidence_multipliers = {
        'high': 1.0,
        'medium': 0.85,
        'low': 0.7
    }
    
    confidence_multiplier = confidence_multipliers.get(confidence, 0.85)
    final_score = weighted_score * confidence_multiplier
    
    return min(round(final_score), 100)

def get_intentionality_grade(score):
    """Get letter grade and description for intentionality score"""
    if score >= 85:
        return "A+", "Very High Action Intent"
    elif score >= 75:
        return "A", "High Action Intent"
    elif score >= 65:
        return "B+", "Good Action Intent"
    elif score >= 55:
        return "B", "Moderate Action Intent"
    elif score >= 45:
        return "C+", "Some Action Intent"
    elif score >= 35:
        return "C", "Low Action Intent"
    elif score >= 25:
        return "D", "Very Low Action Intent"
    else:
        return "F", "Minimal Action Intent"

def calculate_content_score(result):
    """Calculate overall content score"""
    score = 0
    confidence = result.get('intention', {}).get('confidence', 'Low')
    confidence_scores = {'High': 40, 'Medium': 30, 'Low': 20}
    score += confidence_scores.get(confidence, 20)
    
    primary_kw = len(result.get('primary_keywords', []))
    secondary_kw = len(result.get('secondary_keywords', []))
    keyword_score = min((primary_kw * 3 + secondary_kw * 2), 20)
    score += keyword_score
    
    tier2_categories = result.get('tier2_categories', [])
    category_score = min(len(tier2_categories) * 5, 15)
    score += category_score
    
    audience_types = result.get('audience_profile', {}).get('type', [])
    interest_groups = result.get('audience_profile', {}).get('interest_groups', [])
    audience_score = min((len(audience_types) * 3 + len(interest_groups) * 2), 15)
    score += audience_score
    
    return min(score, 100)

def calculate_final_intention_score(result, campaign_relevancy=None):
    """
    Calculate the final intention score based on:
    - 80% Campaign Fit Score (if available)
    - 20% Action Intent Score
    
    If campaign analysis is disabled, returns only the Action Intent Score
    """
    # Get the action intent score (intentionality score)
    action_intent_score = calculate_intentionality_score(result)
    
    # If no campaign data, return just the action intent score
    if not campaign_relevancy:
        return action_intent_score, "action_only"
    
    # Get campaign fit score
    campaign_fit_score = campaign_relevancy.get('overall_relevancy_score', 0)
    
    # Calculate weighted final score: 80% campaign fit + 20% action intent
    final_score = (campaign_fit_score * 0.8) + (action_intent_score * 0.2)
    
    return round(final_score), "combined"

def get_final_intention_grade(score, score_type="combined"):
    """
    Get grade and description for the final intention score
    """
    if score_type == "action_only":
        prefix = "Action Intent: "
    else:
        prefix = "Overall Intent: "
    
    if score >= 90:
        return "A+", f"{prefix}Exceptional"
    elif score >= 80:
        return "A", f"{prefix}Excellent"
    elif score >= 70:
        return "B+", f"{prefix}Very Good"
    elif score >= 60:
        return "B", f"{prefix}Good"
    elif score >= 50:
        return "C+", f"{prefix}Fair"
    elif score >= 40:
        return "C", f"{prefix}Below Average"
    elif score >= 30:
        return "D", f"{prefix}Poor"
    else:
        return "F", f"{prefix}Very Poor"
