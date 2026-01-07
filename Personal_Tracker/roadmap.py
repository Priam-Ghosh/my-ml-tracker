# Roadmap Data based on user's 6-month plan

ML_ROADMAP = {
    1: {
        "title": "Python + Core Math + NumPy/Pandas",
        "goals": [
            "3h/day Python (OOP + small scripts)",
            "3h/day Math (linear algebra + calculus basics)",
            "2h/day NumPy/Pandas intro & practice",
            "Build File organizer script",
            "Build CSV/JSON parser using classes",
            "Create Notebook implementing matrix operations & small EDA"
        ]
    },
    2: {
        "title": "Stats, Info Theory, Data Stack, SQL/Git",
        "goals": [
            "Study Probability & statistics (distributions, Bayes)",
            "Study Information theory (entropy, CE)",
            "Pandas + visualization (EDA on real dataset)",
            "SQL + Git practice (HackerRank + GitHub pushes)",
            "Deliverable: 1 full EDA notebook on a Kaggle dataset",
            "Deliverable: 20–30 SQL problems solved",
            "Deliverable: 2–3 clean repos on GitHub"
        ]
    },
    3: {
        "title": "ML Basics + Linear/Logistic Regression",
        "goals": [
            "Study ML theory (train/val/test, CV, bias–variance)",
            "Implement linear regression from scratch (NumPy)",
            "Implement logistic regression from scratch",
            "Scikit-learn practice with simple datasets",
            "Compare scratch implementation vs sklearn"
        ]
    },
    4: {
        "title": "Trees, Random Forests, Evaluation + Project 1",
        "goals": [
            "Study Decision tree theory & implementation",
            "Study Random Forest (sklearn) + hyperparameters",
            "Learn metrics (ROC, AUC, PR curves)",
            "Project 1: Loan Default (EDA + Cleaning + Modeling)",
            "Evaluate using ROC-AUC, F1"
        ]
    },
    5: {
        "title": "Advanced ML Algorithms (Boosting, SVM)",
        "goals": [
            "Gradient Boosting (XGBoost, LightGBM) theory + hands-on",
            "SVM, KNN, clustering basics",
            "Implement KMeans + PCA from scratch on small dataset"
        ]
    },
    6: {
        "title": "Evaluation, Interpretability + Project 2",
        "goals": [
            "Deep dive: Metrics (ROC, AUC, calibration), SHAP basics",
            "Project 2: Customer Segmentation (Clustering)",
            "Visualizations + cluster profiling"
        ]
    },
    7: {
        "title": "Feature Engineering + Imbalanced Data + Project 3",
        "goals": [
            "Feature engineering (encodings, scaling, outliers)",
            "Handle Imbalanced datasets (SMOTE, class weights)",
            "Start Project 3: Fraud Detection (EDA + Preprocessing)"
        ]
    },
    8: {
        "title": "MLOps Foundations",
        "goals": [
            "DVC: version data for Fraud project",
            "MLflow: log experiments",
            "FastAPI: build simple classifier API",
            "Integrate Fraud model into FastAPI"
        ]
    },
    9: {
        "title": "NN Theory + Basic PyTorch",
        "goals": [
            "Study NN theory (forward/backprop, losses)",
            "Implement 2-layer NN from scratch (NumPy)",
            "PyTorch basics (tensors, autograd, MLP on MNIST)"
        ]
    },
    10: {
        "title": "PyTorch Training Loops + CNN Basics",
        "goals": [
            "Master PyTorch training loop pattern",
            "Study CNN basics (kernels, pooling)",
            "Implement simple CNN for MNIST/CIFAR"
        ]
    },
    11: {
        "title": "CIFAR-10 Project + Transfer Learning",
        "goals": [
            "Project: CIFAR-10 Baseline CNN",
            "Implement Data Augmentation",
            "Transfer learning with ResNet (freeze backbone, fine-tune head)"
        ]
    },
    12: {
        "title": "Deployment + Documentation",
        "goals": [
            "Wrap CIFAR model into FastAPI /predict",
            "Dockerize the API",
            "Write clean README and documentation"
        ]
    },
    13: {
        "title": "Transformer Theory + HF Basics",
        "goals": [
            "Read/explain attention & Transformer architecture",
            "Hugging Face tutorials (text classification)",
            "Fine-tune BERT for sentiment classification"
        ]
    },
    14: {
        "title": "BERT Fine-tuning Project",
        "goals": [
            "Clean dataset & Fine-tune BERT",
            "Implement Early stopping",
            "Evaluate errors & confusion matrix"
        ]
    },
    15: {
        "title": "Embeddings + Semantic Search",
        "goals": [
            "SentenceTransformers for embeddings",
            "Implement semantic search (FAISS/cosine)",
            "Integrate BERT classifier results"
        ]
    },
    16: {
        "title": "Project Integration + API",
        "goals": [
            "Build Document Understanding System (QA style)",
            "Wrap into FastAPI endpoint",
            "Create Demo Notebook"
        ]
    },
    17: {
        "title": "LLM Usage + Prompt Engineering",
        "goals": [
            "OpenAI/HF API experimentation",
            "Study Prompt Engineering patterns",
            "Build scripts for Summarization/Q&A"
        ]
    },
    18: {
        "title": "Build First RAG System",
        "goals": [
            "Implement RAG Pipeline (Load -> Chunk -> Embed -> Store)",
            "Integrate with LLM for Q&A",
            "Wrap into FastAPI service"
        ]
    },
    19: {
        "title": "Fine-tuning with LoRA",
        "goals": [
            "Prepare instruction dataset (Q&A pairs)",
            "Fine-tune small LLM with LoRA",
            "Compare base vs fine-tuned performance"
        ]
    },
    20: {
        "title": "Evaluation + Monitoring",
        "goals": [
            "Implement basic evaluation (faithfulness/relevance)",
            "Track latency, tokens, cost",
            "Build simple monitoring dashboard"
        ]
    },
    21: {
        "title": "Agents + Tools",
        "goals": [
            "Implement simple agent (calculator/search tools)",
            "Add RAG as a tool",
            "Refine prompts for agent tasks"
        ]
    },
    22: {
        "title": "Multi-Agent + Design Capstone",
        "goals": [
            "Design Multi-Agent System (Researcher+Critic+Writer)",
            "Implement rough prototype",
            "Draft full Capstone Architecture"
        ]
    },
    23: {
        "title": "Capstone Build",
        "goals": [
            "Build RAG pipeline & LLM orchestration",
            "Implement Agents",
            "Build Minimal UI (Streamlit) + FastAPI"
        ]
    },
    24: {
        "title": "Capstone Polish & Wrap-up",
        "goals": [
            "Add Logging & Metrics",
            "Record Demo Video",
            "Write Full Documentation & Architecture Diagram"
        ]
    }
}
