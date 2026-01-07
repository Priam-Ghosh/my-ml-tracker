import random

def generate_quiz(topic):
    """
    Generates a 15-question quiz based on the provided topic.
    Returns a list of dictionaries.
    """
    
    # In a real app, this would call an LLM. 
    # Here we use templates to create a "Self-Assessment" style quiz 
    # where the user validates their knowledge against key concepts.
    
    questions = []
    
    # --- EASY (Concepts & Definitions) ---
    easy_templates = [
        ("What is the primary definition of {topic}?", 
         ["A fundamental concept in ML", "A type of database", "A python library", "A hardware component"], "A fundamental concept in ML"),
        ("Which of the following best describes {topic}?", 
         ["Supervised Learning technique", "Unsupervised Learning technique", "Reinforcement Learning", "It depends on context"], "It depends on context"),
        ("When typically using {topic}, what is the first step?", 
         ["Data Preprocessing", "Model Training", "Deployment", "Hyperparameter Tuning"], "Data Preprocessing"),
        ("Basic syntax: How would you initialize {topic} in Python?", 
         ["import {topic}", "new {topic}()", "It varies by library", "None of the above"], "It varies by library"),
        ("True or False: {topic} is essential for deep learning.", 
         ["True", "False", "Only for CNNs", "Only for NLP"], "True")
    ]
    
    # --- MEDIUM (Application & Implementation) ---
    medium_templates = [
        ("How does {topic} handle overfitting?", 
         ["By increasing complexity", "It doesn't directly", "Through regularization", "By using more data only"], "Through regularization"),
        ("In the context of {topic}, what does the parameter 'alpha' usually control?", 
         ["Learning Rate / Regularization", "Number of trees", "Tree depth", "Batch size"], "Learning Rate / Regularization"),
        ("Which metric is most critical when evaluating {topic}?", 
         ["Accuracy", "F1 Score", "MSE", "Context dependent"], "Context dependent"),
        ("When implementing {topic}, a common pitfall is...", 
         ["Data Leakage", "Syntax Error", "Computer crashing", "Too much RAM"], "Data Leakage"),
        ("Comparing {topic} to a baseline, you should expect...", 
         ["Better performance", "Faster training", "More interpretability", "Trade-offs"], "Trade-offs")
    ]
    
    # --- HARD (Theory & Edge Cases) ---
    hard_templates = [
        ("Deriving the gradient for {topic}, what is the mathematical basis?", 
         ["Chain Rule", "Pythagoras Theorem", "Riemann Sum", "Fourier Transform"], "Chain Rule"),
        ("In a high-dimensional space, how does {topic} behave?", 
         ["Curse of Dimensionality applies", "It becomes faster", "No change", "It simplifies"], "Curse of Dimensionality applies"),
        ("What is the asymptotic complexity (Big O) of training {topic}?", 
         ["O(n log n)", "O(n^2)", "O(n^3)", "Depends on implementation"], "Depends on implementation"),
        ("If {topic} fails to converge, the most likely theoretical reason is...", 
         ["Learning rate too high", "Bad initialization", "Non-convex loss surface", "All of the above"], "All of the above"),
        ("Advanced: How would you scale {topic} to 1TB of data?", 
         ["Distributed Computing (Spark/Dask)", "Use more RAM", "Loop over files", "You can't"], "Distributed Computing (Spark/Dask)")
    ]
    
    # Generate 5 Easy
    for t in easy_templates:
        q_text = t[0].format(topic=topic)
        questions.append({
            "question": q_text,
            "options": t[1],
            "answer": t[2],
            "difficulty": "Easy"
        })
        
    # Generate 5 Medium
    for t in medium_templates:
        q_text = t[0].format(topic=topic)
        questions.append({
            "question": q_text,
            "options": t[1],
            "answer": t[2],
            "difficulty": "Medium"
        })
        
    # Generate 5 Hard
    for t in hard_templates:
        q_text = t[0].format(topic=topic)
        questions.append({
            "question": q_text,
            "options": t[1],
            "answer": t[2],
            "difficulty": "Hard"
        })
        
    return questions
