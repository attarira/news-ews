from pyabsa import ATEPCCheckpointManager

def analyze_aspect_sentiment(text, target_entity=None):
    """
    Perform aspect-based sentiment analysis on text
    
    Args:
        text (str): Input text to analyze
        target_entity (str, optional): Specific entity to focus on (e.g., "Tesla")
    
    Returns:
        dict: Analysis results with aspects, sentiments, and confidence scores
    """
    
    # Load ABSA model
    aspect_extractor = ATEPCCheckpointManager.get_aspect_extractor(
        checkpoint="english",
        auto_device=True
    )
    
    results = {}
    
    # Method 1: Automatic aspect extraction
    print("🔍 Analyzing all aspects in the text...")
    auto_result = aspect_extractor.predict([text], print_result=False, save_result=False)
    results['automatic'] = auto_result[0]
    
    print(f"Found aspects: {results['automatic']['aspect']}")
    print(f"Sentiments: {results['automatic']['sentiment']}")
    print(f"Confidence scores: {[f'{conf:.3f}' for conf in results['automatic']['confidence']]}")
    
    # Method 2: Entity-focused analysis (if target_entity provided)
    if target_entity:
        print(f"\n🎯 Focusing on '{target_entity}'...")
        marked_text = text.replace(target_entity, f"$T$ {target_entity} $T$")
        focused_result = aspect_extractor.predict([marked_text], print_result=False, save_result=False)
        results['focused'] = focused_result[0]
        
        print(f"Focused aspects: {results['focused']['aspect']}")
        print(f"Focused sentiments: {results['focused']['sentiment']}")
        print(f"Focused confidence: {[f'{conf:.3f}' for conf in results['focused']['confidence']]}")
    
    return results

# Example usage
text = "00:00 Speaker A\n\nI think Musk's uh America party isn't likely to uh amount too much for. And I'll give you I'll give you a five test and he only meets one of them. First is money. Uh, I think he's got enough. So check on that. Secondly, the brand. I mean, he's torched his brand with both the most engaged people on the left and the most engaged people on the right. That's hard to do, but this is an unusual guy. So I think the brand is probably not in good shape. Thirdly, uh does he have trust? I mean, you know, the brand's in the toilet. So I I would say not not any trust to move things forward. Uh, fourthly, does he have a plan? Uh, not so far except to provide people more freedom and uh and cut spending. So good luck with that cuz he couldn't do it when he was actually sitting next to the president. And fifthly, are there results uh available? Uh he couldn't achieve what he wanted to achieve uh the few months he was in there. So why would anybody think he could do it now? Plus, existing politicians find him radioactive. So uh on both the left and the right. So I think he's uh I I think this isn't going to amount to much, frankly."

# Analyze with focus on Tesla
results = analyze_aspect_sentiment(text, target_entity="Tesla")

# Pretty print results
print("\n" + "="*60)
print("📊 ASPECT-BASED SENTIMENT ANALYSIS RESULTS")
print("="*60)

# Automatic analysis
auto = results['automatic']
print(f"\n🤖 AUTOMATIC ANALYSIS:")
print(f"Text: {auto['sentence']}")
for i, (aspect, sentiment, conf) in enumerate(zip(auto['aspect'], auto['sentiment'], auto['confidence'])):
    print(f"  • Aspect: '{aspect}' → Sentiment: {sentiment} (Confidence: {conf:.1%})")

# Focused analysis
if 'focused' in results:
    focused = results['focused']
    print(f"\n🎯 TESLA-FOCUSED ANALYSIS:")
    print(f"Text: {focused['sentence']}")
    for i, (aspect, sentiment, conf) in enumerate(zip(focused['aspect'], focused['sentiment'], focused['confidence'])):
        print(f"  • Aspect: '{aspect}' → Sentiment: {sentiment} (Confidence: {conf:.1%})")

# Extract sentiment probabilities for detailed analysis
print(f"\n📈 DETAILED PROBABILITIES (Negative, Neutral, Positive):")
auto_probs = auto['probs'][0]
print(f"Automatic: [{auto_probs[0]:.3f}, {auto_probs[1]:.3f}, {auto_probs[2]:.3f}]")
if 'focused' in results:
    focused_probs = results['focused']['probs'][0]
    print(f"Focused:   [{focused_probs[0]:.3f}, {focused_probs[1]:.3f}, {focused_probs[2]:.3f}]")