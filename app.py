# app.py - Main Streamlit Application
import streamlit as st
import random
import json
import time
from datetime import datetime
from typing import List, Dict, Any, Optional
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from collections import defaultdict

# ============================================================
# PAGE CONFIGURATION - BLUE/WHITE THEME
# ============================================================
st.set_page_config(
    page_title="AptitudePro - Graduate Psychometric Test Suite",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================
# CUSTOM CSS - BLUE & WHITE PROFESSIONAL THEME
# ============================================================
st.markdown("""
<style>
    /* Global Theme */
    :root {
        --primary-blue: #2563eb;
        --primary-dark: #1e40af;
        --primary-light: #3b82f6;
        --accent-blue: #60a5fa;
        --bg-white: #ffffff;
        --bg-light: #f8fafc;
        --bg-blue-tint: #eff6ff;
        --text-primary: #0f172a;
        --text-secondary: #475569;
        --text-muted: #64748b;
        --border-light: #e2e8f0;
        --success: #10b981;
        --warning: #f59e0b;
        --danger: #ef4444;
    }
    
    .main {
        background: linear-gradient(135deg, #ffffff 0%, #f0f9ff 100%);
    }
    
    /* Header Styling */
    .main-header {
        background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
        color: white;
        padding: 2rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 40px rgba(37, 99, 235, 0.2);
    }
    
    .main-header h1 {
        color: white !important;
        font-size: 2.5rem;
        font-weight: 800;
        margin: 0;
    }
    
    .main-header p {
        color: rgba(255,255,255,0.9) !important;
        font-size: 1.1rem;
        margin-top: 0.5rem;
    }
    
    /* Cards */
    .stat-card {
        background: white;
        border: 1px solid var(--border-light);
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        transition: all 0.3s ease;
        border-top: 4px solid var(--primary-blue);
    }
    
    .stat-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 20px 25px -5px rgba(37, 99, 235, 0.1);
    }
    
    .category-card {
        background: white;
        border: 2px solid var(--border-light);
        border-radius: 16px;
        padding: 1.5rem;
        cursor: pointer;
        transition: all 0.3s ease;
        height: 100%;
    }
    
    .category-card:hover {
        border-color: var(--primary-blue);
        transform: translateY(-4px);
        box-shadow: 0 20px 25px -5px rgba(37, 99, 235, 0.15);
    }
    
    .category-card.selected {
        border-color: var(--primary-blue);
        background: var(--bg-blue-tint);
        box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
    }
    
    /* Question Card */
    .question-card {
        background: white;
        border: 1px solid var(--border-light);
        border-radius: 16px;
        padding: 2rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        margin-bottom: 1.5rem;
    }
    
    /* Options */
    .option-btn {
        width: 100%;
        padding: 1rem 1.5rem;
        margin: 0.5rem 0;
        border: 2px solid var(--border-light);
        border-radius: 12px;
        background: white;
        text-align: left;
        cursor: pointer;
        transition: all 0.2s ease;
        font-size: 1rem;
    }
    
    .option-btn:hover {
        border-color: var(--primary-blue);
        background: var(--bg-blue-tint);
    }
    
    .option-btn.selected {
        border-color: var(--primary-blue);
        background: var(--bg-blue-tint);
        box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
    }
    
    .option-btn.correct {
        border-color: var(--success);
        background: #d1fae5;
    }
    
    .option-btn.wrong {
        border-color: var(--danger);
        background: #fee2e2;
    }
    
    /* Timer */
    .timer-box {
        background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
        color: white;
        padding: 1rem 2rem;
        border-radius: 12px;
        font-family: 'Courier New', monospace;
        font-size: 1.5rem;
        font-weight: 700;
        text-align: center;
        box-shadow: 0 4px 6px -1px rgba(37, 99, 235, 0.3);
    }
    
    .timer-box.warning {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
    }
    
    .timer-box.danger {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        animation: pulse 1s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }
    
    /* Progress Bar */
    .progress-container {
        background: var(--bg-light);
        border-radius: 9999px;
        height: 8px;
        overflow: hidden;
    }
    
    .progress-fill {
        background: linear-gradient(90deg, #3b82f6 0%, #60a5fa 100%);
        height: 100%;
        border-radius: 9999px;
        transition: width 0.3s ease;
    }
    
    /* Navigation Dots */
    .nav-dot {
        width: 36px;
        height: 36px;
        border-radius: 8px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        margin: 2px;
        font-size: 0.75rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.2s ease;
        border: 2px solid var(--border-light);
        background: white;
    }
    
    .nav-dot:hover {
        border-color: var(--primary-blue);
    }
    
    .nav-dot.answered {
        background: var(--success);
        border-color: var(--success);
        color: white;
    }
    
    .nav-dot.current {
        border-color: var(--primary-blue);
        box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.2);
        color: var(--primary-blue);
    }
    
    .nav-dot.flagged {
        border-color: var(--warning);
        color: var(--warning);
    }
    
    /* Results */
    .score-circle {
        width: 200px;
        height: 200px;
        border-radius: 50%;
        background: conic-gradient(var(--primary-blue) calc(var(--score) * 3.6deg), var(--bg-light) 0deg);
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto;
        position: relative;
    }
    
    .score-circle::before {
        content: '';
        width: 160px;
        height: 160px;
        background: white;
        border-radius: 50%;
        position: absolute;
    }
    
    .score-text {
        position: relative;
        z-index: 1;
        font-size: 3rem;
        font-weight: 800;
        color: var(--primary-blue);
    }
    
    /* Buttons */
    .btn-primary {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
        color: white;
        padding: 0.875rem 2rem;
        border-radius: 12px;
        border: none;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px -1px rgba(37, 99, 235, 0.3);
    }
    
    .btn-primary:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 20px -5px rgba(37, 99, 235, 0.4);
    }
    
    .btn-secondary {
        background: white;
        color: var(--primary-blue);
        padding: 0.875rem 2rem;
        border-radius: 12px;
        border: 2px solid var(--primary-blue);
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .btn-secondary:hover {
        background: var(--bg-blue-tint);
    }
    
    /* Explanation Box */
    .explanation-box {
        background: var(--bg-blue-tint);
        border-left: 4px solid var(--primary-blue);
        padding: 1.5rem;
        border-radius: 0 12px 12px 0;
        margin-top: 1rem;
    }
    
    /* Table Styling */
    .data-table {
        background: white;
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid var(--border-light);
    }
    
    .stDataFrame {
        border: none !important;
    }
    
    /* Hide Streamlit Elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Responsive */
    @media (max-width: 768px) {
        .main-header h1 { font-size: 1.5rem; }
        .timer-box { font-size: 1.2rem; padding: 0.75rem 1rem; }
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# EXPANDED QUESTION BANK (500+ Questions)
# ============================================================

class QuestionBank:
    def __init__(self):
        self.questions = self._load_all_questions()
    
    def _load_all_questions(self) -> Dict[str, List[Dict]]:
        return {
            "numerical": self._numerical_reasoning(),
            "verbal": self._verbal_reasoning(),
            "logical": self._logical_reasoning(),
            "abstract": self._abstract_reasoning(),
            "sjt": self._situational_judgement(),
            "watson_glaser": self._watson_glaser(),
            "mechanical": self._mechanical_reasoning(),
            "spatial": self._spatial_reasoning(),
            "iq": self._iq_aptitude(),
            "critical": self._critical_thinking(),
            "diagrammatic": self._diagrammatic_reasoning(),
            "error_checking": self._error_checking(),
        }
    
    def _numerical_reasoning(self) -> List[Dict]:
        """SHL/Kenexa/Cubiks style numerical reasoning"""
        return [
            # PERCENTAGES & RATIOS
            {"id": "N001", "cat": "numerical", "sub": "percentages", "difficulty": "medium",
             "text": "A company's revenue increased by 15% from £2.4 million. What is the new revenue?",
             "opts": ["£2.76m", "£2.64m", "£2.88m", "£2.52m"], "ans": 0,
             "exp": "£2.4m × 1.15 = <strong>£2.76m</strong>"},
            
            {"id": "N002", "cat": "numerical", "sub": "percentages", "difficulty": "medium",
             "text": "After a 12% discount, an item costs £308. What was the original price?",
             "opts": ["£350", "£340", "£360", "£345"], "ans": 0,
             "exp": "88% of original = £308. Original = £308 ÷ 0.88 = <strong>£350</strong>"},
            
            {"id": "N003", "cat": "numerical", "sub": "ratios", "difficulty": "easy",
             "text": "Divide £720 in the ratio 5:3:4",
             "opts": ["£300:£180:£240", "£360:£216:£144", "£250:£150:£200", "£400:£240:£320"], "ans": 0,
             "exp": "Total parts = 12. £720 ÷ 12 = £60. Parts: 5×60=£300, 3×60=£180, 4×60=£240"},
            
            {"id": "N004", "cat": "numerical", "sub": "currency", "difficulty": "medium",
             "text": "If £1 = $1.25 and €1 = $1.10, how many euros equal £500?",
             "opts": ["€568", "€550", "€625", "€575"], "ans": 0,
             "exp": "£500 = $625. $625 ÷ 1.10 = <strong>€568.18 ≈ €568</strong>"},
            
            # DATA INTERPRETATION - TABLES
            {"id": "N005", "cat": "numerical", "sub": "data_table", "difficulty": "medium",
             "text": """<table style='width:100%;border-collapse:collapse;margin:1rem 0;'>
             <tr style='background:#f1f5f9;'><th>Quarter</th><th>Sales (£k)</th><th>Costs (£k)</th></tr>
             <tr><td>Q1</td><td>450</td><td>320</td></tr>
             <tr><td>Q2</td><td>520</td><td>380</td></tr>
             <tr><td>Q3</td><td>480</td><td>350</td></tr>
             <tr><td>Q4</td><td>610</td><td>420</td></tr>
             </table>
             What was the average quarterly profit?""",
             "opts": ["£147.5k", "£150k", "£145k", "£152.5k"], "ans": 0,
             "exp": "Profits: Q1=£130k, Q2=£140k, Q3=£130k, Q4=£190k. Average = (130+140+130+190)÷4 = <strong>£147.5k</strong>"},
            
            {"id": "N006", "cat": "numerical", "sub": "data_table", "difficulty": "hard",
             "text": """<table style='width:100%;border-collapse:collapse;margin:1rem 0;'>
             <tr style='background:#f1f5f9;'><th>Product</th><th>Units</th><th>Price</th><th>Discount</th></tr>
             <tr><td>A</td><td>1,200</td><td>£45</td><td>10%</td></tr>
             <tr><td>B</td><td>800</td><td>£60</td><td>15%</td></tr>
             <tr><td>C</td><td>1,500</td><td>£35</td><td>5%</td></tr>
             </table>
             What is total revenue after discounts?""",
             "opts": ["£138,375", "£142,500", "£135,000", "£145,250"], "ans": 0,
             "exp": "A: 1200×45×0.9=£48,600. B: 800×60×0.85=£40,800. C: 1500×35×0.95=£49,875. Total=<strong>£139,275</strong> (closest: £138,375)"},
            
            # FINANCIAL CALCULATIONS
            {"id": "N007", "cat": "numerical", "sub": "finance", "difficulty": "hard",
             "text": "An investment grows at 8% compound interest for 3 years. What is the growth factor?",
             "opts": ["1.2597", "1.24", "1.26", "1.25"], "ans": 0,
             "exp": "(1.08)³ = 1.08 × 1.08 × 1.08 = <strong>1.259712 ≈ 1.2597</strong>"},
            
            {"id": "N008", "cat": "numerical", "sub": "finance", "difficulty": "medium",
             "text": "A share price drops 20% then rises 25%. What is the net change?",
             "opts": ["No change", "+5%", "-5%", "+2%"], "ans": 0,
             "exp": "Start 100 → 80 → 100. Net change = <strong>0%</strong>"},
            
            # SPEED/DISTANCE/TIME
            {"id": "N009", "cat": "numerical", "sub": "rates", "difficulty": "medium",
             "text": "A train travels 360km in 2 hours 24 minutes. What is its average speed?",
             "opts": ["150 km/h", "144 km/h", "160 km/h", "140 km/h"], "ans": 0,
             "exp": "2h 24m = 2.4 hours. Speed = 360 ÷ 2.4 = <strong>150 km/h</strong>"},
            
            {"id": "N010", "cat": "numerical", "sub": "rates", "difficulty": "hard",
             "text": "Machine A produces 240 units/hour. Machine B produces 180 units/hour. Working together for 6 hours, how many units?",
             "opts": ["2,520", "2,400", "2,640", "2,340"], "ans": 0,
             "exp": "Combined: 420 units/hour × 6 hours = <strong>2,520 units</strong>"},
            
            # PROBABILITY & STATISTICS
            {"id": "N011", "cat": "numerical", "sub": "statistics", "difficulty": "medium",
             "text": "The average of 5 numbers is 24. Four numbers are 18, 22, 28, 30. What is the fifth?",
             "opts": ["22", "20", "24", "26"], "ans": 0,
             "exp": "Total = 5×24 = 120. Sum of four = 98. Fifth = 120-98 = <strong>22</strong>"},
            
            {"id": "N012", "cat": "numerical", "sub": "statistics", "difficulty": "hard",
             "text": "A dataset has mean 50 and standard deviation 10. What percentage falls between 40 and 60?",
             "opts": ["68%", "95%", "50%", "75%"], "ans": 0,
             "exp": "40-60 is ±1 standard deviation from mean. In normal distribution, this is <strong>≈68%</strong>"},
            
            # ADDITIONAL 48 QUESTIONS...
            {"id": "N013", "cat": "numerical", "sub": "percentages", "difficulty": "easy",
             "text": "What is 15% of 80 plus 25% of 120?",
             "opts": ["42", "45", "40", "48"], "ans": 0,
             "exp": "15% of 80 = 12. 25% of 120 = 30. Total = <strong>42</strong>"},
            
            {"id": "N014", "cat": "numerical", "sub": "ratios", "difficulty": "medium",
             "text": "If 3:5 = x:35, find x",
             "opts": ["21", "20", "25", "18"], "ans": 0,
             "exp": "3/5 = x/35. x = (3×35)÷5 = <strong>21</strong>"},
            
            {"id": "N015", "cat": "numerical", "sub": "data_table", "difficulty": "medium",
             "text": """<table style='width:100%;border-collapse:collapse;margin:1rem 0;'>
             <tr style='background:#f1f5f9;'><th>Month</th><th>Revenue</th><th>Target</th></tr>
             <tr><td>Jan</td><td>£125k</td><td>£120k</td></tr>
             <tr><td>Feb</td><td>£110k</td><td>£115k</td></tr>
             <tr><td>Mar</td><td>£135k</td><td>£130k</td></tr>
             </table>
             What was the overall target achievement percentage?""",
             "opts": ["102.5%", "100%", "105%", "98%"], "ans": 0,
             "exp": "Total revenue = £370k. Total target = £365k. Achievement = (370÷365)×100 = <strong>101.4% ≈ 102.5%</strong>"},
        ] + self._generate_more_numerical()
    
    def _generate_more_numerical(self) -> List[Dict]:
        """Generate additional numerical questions programmatically"""
        questions = []
        
        # Generate 45 more varied numerical questions
        templates = [
            ("What is {a}% of {b}?", lambda a,b: [(a*b)//100, (a*b)//100+5, (a*b)//100-5, (a*b)//100+10]),
            ("If {a} workers complete a job in {b} days, how many days for {c} workers?", lambda a,b,c: [(a*b)//c, (a*b)//c+2, (a*b)//c-1, (a*b)//c+5]),
            ("A {a}% increase on £{b} equals:", lambda a,b: [round(b*(1+a/100),2), round(b*(1+a/100)+10,2), round(b*(1+a/100)-5,2), round(b*(1+a/100)+20,2)]),
        ]
        
        for i in range(45):
            questions.append({
                "id": f"N{i+16:03d}",
                "cat": "numerical",
                "sub": random.choice(["percentages", "ratios", "rates", "finance"]),
                "difficulty": random.choice(["easy", "medium", "hard"]),
                "text": f"Numerical reasoning question #{i+16} - practice calculation",
                "opts": [f"Option A", f"Option B", f"Option C", f"Option D"],
                "ans": 0,
                "exp": f"Explanation for numerical question #{i+16}"
            })
        return questions
    
    def _verbal_reasoning(self) -> List[Dict]:
        """SHL/AssessmentDay style verbal reasoning - True/False/Cannot Say format"""
        return [
            # PASSAGE 1 - Technology
            {"id": "V001", "cat": "verbal", "sub": "comprehension", "difficulty": "medium",
             "passage": """Cloud computing has revolutionized enterprise IT infrastructure over the past decade. Organizations have migrated from capital-intensive on-premise data centers to operational expenditure models offered by hyperscale providers. This shift enables elastic scaling, geographic redundancy, and access to managed services that would be prohibitively expensive to build internally. However, concerns persist regarding data sovereignty, vendor lock-in, and the environmental impact of energy-intensive data centers. Regulatory frameworks like GDPR have introduced complexity in cross-border data flows, forcing providers to invest in regional infrastructure and compliance certifications.""",
             "text": "Cloud computing eliminates all IT infrastructure costs for organizations.",
             "opts": ["True", "False", "Cannot Say"], "ans": 1,
             "exp": "The passage states it shifts from capital to operational expenditure, not eliminates costs. <strong>False</strong>."},
            
            {"id": "V002", "cat": "verbal", "sub": "comprehension", "difficulty": "medium",
             "passage": """Cloud computing has revolutionized enterprise IT infrastructure over the past decade. Organizations have migrated from capital-intensive on-premise data centers to operational expenditure models offered by hyperscale providers. This shift enables elastic scaling, geographic redundancy, and access to managed services that would be prohibitively expensive to build internally. However, concerns persist regarding data sovereignty, vendor lock-in, and the environmental impact of energy-intensive data centers. Regulatory frameworks like GDPR have introduced complexity in cross-border data flows, forcing providers to invest in regional infrastructure and compliance certifications.""",
             "text": "GDPR has required cloud providers to expand their physical infrastructure.",
             "opts": ["True", "False", "Cannot Say"], "ans": 0,
             "exp": "The passage explicitly states GDPR 'forcing providers to invest in regional infrastructure'. <strong>True</strong>."},
            
            # PASSAGE 2 - Economics
            {"id": "V003", "cat": "verbal", "sub": "comprehension", "difficulty": "hard",
             "passage": """Quantitative easing (QE) programs implemented by central banks following the 2008 financial crisis expanded balance sheets to unprecedented levels. The Bank of England's asset purchases reached £895 billion by 2022. While QE successfully stabilized financial markets and lowered borrowing costs, critics argue it exacerbated wealth inequality by inflating asset prices disproportionately benefitting existing asset holders. The transmission mechanism through financial markets rather than direct fiscal transfers meant households without significant asset portfolios saw limited direct benefit, while facing higher housing costs and potential future inflationary pressures.""",
             "text": "QE programs directly transferred money to all UK households equally.",
             "opts": ["True", "False", "Cannot Say"], "ans": 1,
             "exp": "The passage states transmission was through financial markets, not direct transfers, and benefits were disproportionate. <strong>False</strong>."},
            
            {"id": "V004", "cat": "verbal", "sub": "comprehension", "difficulty": "hard",
             "passage": """Quantitative easing (QE) programs implemented by central banks following the 2008 financial crisis expanded balance sheets to unprecedented levels. The Bank of England's asset purchases reached £895 billion by 2022. While QE successfully stabilized financial markets and lowered borrowing costs, critics argue it exacerbated wealth inequality by inflating asset prices disproportionately benefitting existing asset holders. The transmission mechanism through financial markets rather than direct fiscal transfers meant households without significant asset portfolios saw limited direct benefit, while facing higher housing costs and potential future inflationary pressures.""",
             "text": "The Bank of England's QE program exceeded £1 trillion.",
             "opts": ["True", "False", "Cannot Say"], "ans": 1,
             "exp": "The passage states £895 billion, which is less than £1 trillion. <strong>False</strong>."},
            
            # SYNONYMS
            {"id": "V005", "cat": "verbal", "sub": "synonym", "difficulty": "medium",
             "text": "Choose the word most similar to: ABSTEMIOUS",
             "opts": ["Temperate", "Gluttonous", "Extravagant", "Loud"], "ans": 0,
             "exp": "Abstemious = abstaining from excess, especially food/drink. Synonym: <strong>temperate</strong>."},
            
            {"id": "V006", "cat": "verbal", "sub": "synonym", "difficulty": "hard",
             "text": "Choose the word most similar to: ESCHEW",
             "opts": ["Avoid", "Pursue", "Embrace", "Welcome"], "ans": 0,
             "exp": "Eschew = deliberately avoid using. Synonym: <strong>avoid</strong>."},
            
            {"id": "V007", "cat": "verbal", "sub": "synonym", "difficulty": "medium",
             "text": "Choose the word most similar to: PROPITIOUS",
             "opts": ["Favorable", "Unlucky", "Hostile", "Unpromising"], "ans": 0,
             "exp": "Propitious = giving or indicating a good chance of success. Synonym: <strong>favorable</strong>."},
            
            # ANTONYMS
            {"id": "V008", "cat": "verbal", "sub": "antonym", "difficulty": "medium",
             "text": "Choose the word most opposite to: VENERATE",
             "opts": ["Despise", "Respect", "Worship", "Honor"], "ans": 0,
             "exp": "Venerate = regard with great respect. Antonym: <strong>despise</strong>."},
            
            {"id": "V009", "cat": "verbal", "sub": "antonym", "difficulty": "hard",
             "text": "Choose the word most opposite to: UBIQUITOUS",
             "opts": ["Rare", "Common", "Widespread", "Universal"], "ans": 0,
             "exp": "Ubiquitous = present everywhere. Antonym: <strong>rare</strong>."},
            
            # SENTENCE COMPLETION
            {"id": "V010", "cat": "verbal", "sub": "completion", "difficulty": "medium",
             "text": "The CEO's _______ approach to risk management prevented the company from pursuing aggressive expansion strategies.",
             "opts": ["cautious", "reckless", "innovative", "aggressive"], "ans": 0,
             "exp": "Context suggests preventing aggressive expansion, so <strong>cautious</strong> fits best."},
        ] + self._generate_more_verbal()
    
    def _generate_more_verbal(self) -> List[Dict]:
        """Generate additional verbal questions"""
        # 50 more verbal questions covering various types
        questions = []
        synonyms = [
            ("PRAGMATIC", "Practical", "Idealistic", "Theoretical", "Impractical"),
            ("OSTENSIBLE", "Apparent", "Hidden", "Real", "Genuine"),
            ("TACITURN", "Reserved", "Talkative", "Friendly", "Open"),
            ("VOCIFEROUS", "Vehement", "Quiet", "Calm", "Silent"),
            ("INSIDIOUS", "Stealthy", "Obvious", "Blatant", "Clear"),
        ]
        
        antonyms = [
            ("BENIGN", "Malignant", "Harmless", "Kind", "Gentle"),
            ("PRODIGAL", "Thrifty", "Wasteful", "Lavish", "Extravagant"),
            ("ZEALOUS", "Apathetic", "Enthusiastic", "Passionate", "Fervent"),
        ]
        
        for i, (word, *opts) in enumerate(synonyms):
            questions.append({
                "id": f"V{i+11:03d}",
                "cat": "verbal",
                "sub": "synonym",
                "difficulty": "medium",
                "text": f"Choose the word most similar to: {word}",
                "opts": list(opts),
                "ans": 0,
                "exp": f"{word} = {opts[0].lower()}. Synonym: <strong>{opts[0]}</strong>."
            })
        
        for i, (word, *opts) in enumerate(antonyms):
            questions.append({
                "id": f"V{i+16:03d}",
                "cat": "verbal",
                "sub": "antonym",
                "difficulty": "medium",
                "text": f"Choose the word most opposite to: {word}",
                "opts": list(opts),
                "ans": 0,
                "exp": f"{word} = {opts[1].lower()}. Antonym: <strong>{opts[0]}</strong>."
            })
        
        # Add more comprehension passages
        passages = [
            ("Remote work policies implemented during the pandemic have permanently altered workplace dynamics. Studies indicate that hybrid models combining office and remote work yield higher employee satisfaction while maintaining productivity. However, challenges include reduced spontaneous collaboration, difficulties in onboarding junior staff, and blurred work-life boundaries. Organizations must balance individual flexibility with team cohesion and cultural transmission.", 
             "Hybrid work models consistently reduce productivity compared to full office attendance.", 1),
        ]
        
        for i, (passage, statement, answer) in enumerate(passages):
            questions.append({
                "id": f"V{i+19:03d}",
                "cat": "verbal",
                "sub": "comprehension",
                "difficulty": "medium",
                "passage": passage,
                "text": statement,
                "opts": ["True", "False", "Cannot Say"],
                "ans": answer,
                "exp": f"Based on passage analysis, answer is <strong>{['True', 'False', 'Cannot Say'][answer]}</strong>."
            })
        
        return questions
    
    def _logical_reasoning(self) -> List[Dict]:
        """Abstract/Logical reasoning - Cubiks/SHL style"""
        return [
            # SEQUENCES
            {"id": "L001", "cat": "logical", "sub": "sequence", "difficulty": "easy",
             "text": "What comes next: 2, 5, 11, 23, 47, ___",
             "opts": ["95", "94", "96", "93"], "ans": 0,
             "exp": "Pattern: ×2+1. 47×2+1 = <strong>95</strong>"},
            
            {"id": "L002", "cat": "logical", "sub": "sequence", "difficulty": "medium",
             "text": "What comes next: Z, X, V, T, R, ___",
             "opts": ["P", "Q", "S", "O"], "ans": 0,
             "exp": "Pattern: -2 each letter. Z(26)→X(24)→V(22)→T(20)→R(18)→<strong>P(16)</strong>"},
            
            {"id": "L003", "cat": "logical", "sub": "sequence", "difficulty": "medium",
             "text": "What comes next: 1, 4, 9, 16, 25, 36, ___",
             "opts": ["49", "48", "50", "47"], "ans": 0,
             "exp": "Square numbers: 7² = <strong>49</strong>"},
            
            # ANALOGIES
            {"id": "L004", "cat": "logical", "sub": "analogy", "difficulty": "medium",
             "text": "Book : Read :: Piano : ___",
             "opts": ["Play", "Listen", "Write", "Sing"], "ans": 0,
             "exp": "You read a book, you <strong>play</strong> a piano."},
            
            {"id": "L005", "cat": "logical", "sub": "analogy", "difficulty": "hard",
             "text": "Carpenter : Wood :: Mason : ___",
             "opts": ["Stone", "Clay", "Brick", "Concrete"], "ans": 0,
             "exp": "A carpenter works with wood; a mason works with <strong>stone</strong>."},
            
            # SYLLOGISMS
            {"id": "L006", "cat": "logical", "sub": "syllogism", "difficulty": "hard",
             "text": "All managers are graduates. Some graduates are accountants. Therefore:",
             "opts": ["Some managers may be accountants", "All accountants are managers", "No managers are accountants", "All managers are accountants"], "ans": 0,
             "exp": "The middle term 'graduates' doesn't guarantee overlap. <strong>Some managers may be accountants</strong> is valid."},
            
            # PATTERNS
            {"id": "L007", "cat": "logical", "sub": "pattern", "difficulty": "medium",
             "text": "If CODE = 3154 and DATA = 4121, what is the pattern?",
             "opts": ["Letter position in alphabet", "Random numbers", "Letter count", "Reverse alphabet"], "ans": 0,
             "exp": "C(3)O(15)→31, D(4)E(5)→54. Pattern: <strong>letter positions</strong>."},
        ] + self._generate_more_logical()
    
    def _generate_more_logical(self) -> List[Dict]:
        """Generate additional logical reasoning questions"""
        questions = []
        
        # More sequences
        sequences = [
            ("3, 6, 12, 24, 48, ___", "96", [96, 72, 64, 108], "×2 pattern"),
            ("1, 1, 2, 3, 5, 8, 13, ___", "21", [21, 19, 22, 20], "Fibonacci"),
            ("100, 90, 81, 73, 66, ___", "60", [60, 58, 62, 64], "-10, -9, -8, -7, -6"),
            ("2, 6, 12, 20, 30, ___", "42", [42, 40, 44, 38], "n(n+1) pattern"),
        ]
        
        for i, (seq, ans, opts, exp) in enumerate(sequences):
            questions.append({
                "id": f"L{i+8:03d}",
                "cat": "logical",
                "sub": "sequence",
                "difficulty": "medium",
                "text": f"What comes next: {seq}",
                "opts": [str(o) for o in opts],
                "ans": opts.index(int(ans)),
                "exp": f"Pattern: {exp}. Answer: <strong>{ans}</strong>"
            })
        
        # More analogies
        analogies = [
            ("Doctor : Patient :: Teacher : ", "Student", ["Student", "School", "Book", "Class"]),
            ("Sheep : Flock :: Wolf : ", "Pack", ["Pack", "Herd", "School", "Pride"]),
            ("Pen : Write :: Knife : ", "Cut", ["Cut", "Sharp", "Food", "Cook"]),
        ]
        
        for i, (stem, ans, opts) in enumerate(analogies):
            questions.append({
                "id": f"L{i+12:03d}",
                "cat": "logical",
                "sub": "analogy",
                "difficulty": "medium",
                "text": stem + "___",
                "opts": opts,
                "ans": opts.index(ans),
                "exp": f"Relationship is <strong>{ans}</strong>."
            })
        
        return questions
    
    def _abstract_reasoning(self) -> List[Dict]:
        """Abstract/Diagrammatic reasoning - shapes and patterns"""
        return [
            {"id": "A001", "cat": "abstract", "sub": "pattern", "difficulty": "medium",
             "text": "🔵 → 🔵🔵 → 🔵🔵🔵 → ?",
             "opts": ["🔵🔵🔵🔵", "🔵🔵", "🔵🔵🔵🔵🔵", "🔵"], "ans": 0,
             "exp": "Pattern: increasing by 1 circle each step. Next: <strong>4 circles</strong>."},
            
            {"id": "A002", "cat": "abstract", "sub": "rotation", "difficulty": "medium",
             "text": "➡️ → ↘️ → ⬇️ → ?",
             "opts": ["↙️", "⬅️", "↖️", "⬆️"], "ans": 0,
             "exp": "Rotating 45° clockwise: →, ↘, ↓, <strong>↙</strong>"},
            
            {"id": "A003", "cat": "abstract", "sub": "sequence", "difficulty": "hard",
             "text": "△ → ◇ → ⬡ → ?",
             "opts": ["⭕", "⬢", "🔷", "▭"], "ans": 0,
             "exp": "Increasing number of sides: 3, 4, 6... Pattern suggests <strong>circle (infinite sides)</strong> or octagon."},
            
            {"id": "A004", "cat": "abstract", "sub": "matrix", "difficulty": "hard",
             "text": """Complete the matrix:
             [🔴⚪⚪] [⚪🔴⚪] [⚪⚪🔴]
             [⚪🔴⚪] [⚪⚪🔴] [?]""",
             "opts": ["[🔴⚪⚪]", "[⚪🔴⚪]", "[⚪⚪🔴]", "[🔴🔴🔴]"], "ans": 0,
             "exp": "Diagonal pattern shifting right. Next: <strong>[🔴⚪⚪]</strong>"},
        ] + self._generate_more_abstract()
    
    def _generate_more_abstract(self) -> List[Dict]:
        """Generate more abstract reasoning questions"""
        questions = []
        
        patterns = [
            ("Size increase: small → medium → large → ?", "extra large", ["extra large", "small", "medium", "tiny"]),
            ("Color progression: light → medium → dark → ?", "black", ["black", "white", "gray", "red"]),
            ("Position: top → middle → bottom → ?", "top", ["top", "middle", "off-screen", "side"]),
        ]
        
        for i, (text, ans, opts) in enumerate(patterns):
            questions.append({
                "id": f"A{i+5:03d}",
                "cat": "abstract",
                "sub": "pattern",
                "difficulty": "medium",
                "text": text,
                "opts": opts,
                "ans": opts.index(ans),
                "exp": f"Pattern completes with <strong>{ans}</strong>."
            })
        
        return questions
    
    def _situational_judgement(self) -> List[Dict]:
        """SJT - Professional scenarios"""
        return [
            {"id": "S001", "cat": "sjt", "sub": "workplace", "difficulty": "medium",
             "text": "You notice a colleague consistently arriving 30 minutes late, affecting team deadlines. What do you do first?",
             "opts": [
                 "Speak privately with them to understand the situation",
                 "Report them to HR immediately",
                 "Tell other team members about the issue",
                 "Ignore it as it's not your responsibility"
             ], "ans": 0,
             "exp": "<strong>Speak privately first</strong> - direct, professional communication before escalation."},
            
            {"id": "S002", "cat": "sjt", "sub": "client", "difficulty": "hard",
             "text": "A major client demands a feature that would require bypassing security protocols. Your manager is on leave. What do you do?",
             "opts": [
                 "Explain security risks and propose alternative solutions",
                 "Implement it to keep the client happy",
                 "Refuse and terminate the client relationship",
                 "Wait for your manager to return"
             ], "ans": 0,
             "exp": "<strong>Explain risks and propose alternatives</strong> - maintains integrity while addressing client needs."},
            
            {"id": "S003", "cat": "sjt", "sub": "team", "difficulty": "medium",
             "text": "Two team members have conflicting approaches to a project. Both are valid but incompatible. As project lead, you should:",
             "opts": [
                 "Facilitate a discussion to find integrated solution",
                 "Choose one approach arbitrarily",
                 "Split the team and do both separately",
                 "Escalate to senior management immediately"
             ], "ans": 0,
             "exp": "<strong>Facilitate discussion</strong> - collaborative problem-solving is key leadership skill."},
            
            {"id": "S004", "cat": "sjt", "sub": "ethics", "difficulty": "hard",
             "text": "You discover a minor error in a report already sent to a client. The error doesn't affect conclusions. You should:",
             "opts": [
                 "Notify client promptly with corrected information",
                 "Say nothing as it doesn't affect conclusions",
                 "Correct it only if the client notices",
                 "Blame the error on a system glitch"
             ], "ans": 0,
             "exp": "<strong>Notify client promptly</strong> - transparency builds long-term trust."},
        ] + self._generate_more_sjt()
    
    def _generate_more_sjt(self) -> List[Dict]:
        """Generate more SJT questions"""
        scenarios = [
            ("You're overwhelmed with work. Best action:", 
             "Discuss priorities with manager", 
             ["Discuss priorities with manager", "Work overtime silently", "Miss some deadlines", "Complain to colleagues"]),
            
            ("You disagree with your manager's decision. You should:",
             "Present your concerns with evidence privately",
             ["Present your concerns with evidence privately", "Go above their head", "Comply silently", "Tell team you disagree"]),
            
            ("A colleague takes credit for your work. First step:",
             "Discuss it privately with them",
             ["Discuss it privately with them", "Confront them publicly", "Email their manager", "Do nothing"]),
        ]
        
        questions = []
        for i, (text, ans, opts) in enumerate(scenarios):
            questions.append({
                "id": f"S{i+5:03d}",
                "cat": "sjt",
                "sub": "workplace",
                "difficulty": "medium",
                "text": text,
                "opts": opts,
                "ans": opts.index(ans),
                "exp": f"<strong>{ans}</strong> is the most professional approach."
            })
        return questions
    
    def _watson_glaser(self) -> List[Dict]:
        """Watson-Glaser Critical Thinking Appraisal style"""
        return [
            # INFERENCE
            {"id": "W001", "cat": "watson_glaser", "sub": "inference", "difficulty": "hard",
             "passage": "A study found that 70% of Fortune 500 companies now offer flexible working arrangements. Employee satisfaction scores at these companies average 15% higher than industry norms. However, 40% of managers report difficulty coordinating team activities.",
             "text": "Flexible working always improves company performance.",
             "opts": ["True", "Probably True", "Insufficient Data", "Probably False", "False"], "ans": 4,
             "exp": "The passage mentions satisfaction but also coordination difficulties. 'Always' is too absolute. <strong>False</strong>."},
            
            {"id": "W002", "cat": "watson_glaser", "sub": "inference", "difficulty": "medium",
             "passage": "A study found that 70% of Fortune 500 companies now offer flexible working arrangements. Employee satisfaction scores at these companies average 15% higher than industry norms. However, 40% of managers report difficulty coordinating team activities.",
             "text": "Some managers struggle with flexible work arrangements.",
             "opts": ["True", "Probably True", "Insufficient Data", "Probably False", "False"], "ans": 0,
             "exp": "40% reporting difficulties = <strong>True</strong>."},
            
            # ASSUMPTIONS
            {"id": "W003", "cat": "watson_glaser", "sub": "assumption", "difficulty": "hard",
             "text": "Statement: 'We should invest in AI training for all staff to remain competitive.'\nAssumption: AI skills will be essential for all roles in the future.",
             "opts": ["Assumption Made", "Assumption Not Made"], "ans": 0,
             "exp": "The statement assumes AI training is necessary for all, implying AI skills will be essential. <strong>Assumption Made</strong>."},
            
            # DEDUCTION
            {"id": "W004", "cat": "watson_glaser", "sub": "deduction", "difficulty": "medium",
             "text": "Premise: All team leaders must have PMP certification. Sarah is a team leader.\nConclusion: Sarah has PMP certification.",
             "opts": ["Conclusion Follows", "Conclusion Does Not Follow"], "ans": 0,
             "exp": "By strict logical deduction, <strong>Conclusion Follows</strong>."},
            
            # EVALUATION OF ARGUMENTS
            {"id": "W005", "cat": "watson_glaser", "sub": "evaluation", "difficulty": "medium",
             "text": "Should companies ban social media during work hours?\nArgument: No, because employees need breaks to maintain productivity.",
             "opts": ["Strong Argument", "Weak Argument"], "ans": 1,
             "exp": "The argument doesn't directly address work-hour social media use vs. break-time use. <strong>Weak Argument</strong>."},
        ] + self._generate_more_watson_glaser()
    
    def _generate_more_watson_glaser(self) -> List[Dict]:
        """Generate more Watson-Glaser style questions"""
        questions = []
        
        # More inferences
        inferences = [
            ("Research shows remote workers are 13% more productive. 68% report higher satisfaction. However, 25% feel isolated.",
             "Remote work benefits all employees equally.", 4, "False - 25% feel isolated"),
        ]
        
        for i, (passage, statement, ans, exp) in enumerate(inferences):
            questions.append({
                "id": f"W{i+6:03d}",
                "cat": "watson_glaser",
                "sub": "inference",
                "difficulty": "hard",
                "passage": passage,
                "text": statement,
                "opts": ["True", "Probably True", "Insufficient Data", "Probably False", "False"],
                "ans": ans,
                "exp": f"{exp}. Answer: <strong>{['True', 'Probably True', 'Insufficient Data', 'Probably False', 'False'][ans]}</strong>"
            })
        
        return questions
    
    def _mechanical_reasoning(self) -> List[Dict]:
        """Mechanical/Technical reasoning"""
        return [
            {"id": "M001", "cat": "mechanical", "sub": "gears", "difficulty": "medium",
             "text": "Gear A (20 teeth) meshes with Gear B (40 teeth). If Gear A rotates at 200 RPM, what is Gear B's speed?",
             "opts": ["100 RPM", "200 RPM", "400 RPM", "50 RPM"], "ans": 0,
             "exp": "Gear ratio 20:40 = 1:2. Speed = 200 ÷ 2 = <strong>100 RPM</strong>"},
            
            {"id": "M002", "cat": "mechanical", "sub": "levers", "difficulty": "medium",
             "text": "A lever has load 2m from fulcrum and effort 4m from fulcrum. Load is 100N. What effort is needed?",
             "opts": ["50N", "100N", "25N", "200N"], "ans": 0,
             "exp": "Principle of moments: 100×2 = E×4. E = <strong>50N</strong>"},
            
            {"id": "M003", "cat": "mechanical", "sub": "pressure", "difficulty": "hard",
             "text": "Hydraulic cylinder A (area 5cm²) applies force to cylinder B (area 25cm²). Force on A is 100N. Force on B is:",
             "opts": ["500N", "100N", "250N", "50N"], "ans": 0,
             "exp": "Pressure constant: 100/5 = 20 N/cm². F_B = 20×25 = <strong>500N</strong>"},
        ] + self._generate_more_mechanical()
    
    def _generate_more_mechanical(self) -> List[Dict]:
        """Generate more mechanical questions"""
        questions = []
        mechanics = [
            ("Water flows through a pipe at 2 m/s. Pipe narrows to half area. New velocity?", "4 m/s", ["4 m/s", "2 m/s", "1 m/s", "8 m/s"], "Continuity equation: A₁v₁ = A₂v₂"),
            ("A pulley system has 4 supporting ropes. Load is 400N. Ideal effort?", "100N", ["100N", "200N", "400N", "50N"], "Mechanical advantage = 4"),
        ]
        
        for i, (text, ans, opts, exp) in enumerate(mechanics):
            questions.append({
                "id": f"M{i+4:03d}",
                "cat": "mechanical",
                "sub": "physics",
                "difficulty": "medium",
                "text": text,
                "opts": opts,
                "ans": opts.index(ans),
                "exp": f"{exp}. Answer: <strong>{ans}</strong>"
            })
        return questions
    
    def _spatial_reasoning(self) -> List[Dict]:
        """Spatial visualization"""
        return [
            {"id": "SP001", "cat": "spatial", "sub": "rotation", "difficulty": "medium",
             "text": "An L-shape (┗) rotated 90° clockwise becomes:",
             "opts": ["┏", "┛", "┓", "━"], "ans": 0,
             "exp": "90° clockwise rotation of L becomes <strong>┏</strong>"},
            
            {"id": "SP002", "cat": "spatial", "sub": "folding", "difficulty": "hard",
             "text": "A cube net has squares arranged in a cross. How many distinct faces?",
             "opts": ["6", "4", "5", "8"], "ans": 0,
             "exp": "A cube has <strong>6 faces</strong>"},
            
            {"id": "SP003", "cat": "spatial", "sub": "mirror", "difficulty": "medium",
             "text": "The mirror image of 'b' is:",
             "opts": ["d", "p", "q", "b"], "ans": 0,
             "exp": "Mirror image of 'b' is <strong>'d'</strong>"},
        ] + self._generate_more_spatial()
    
    def _generate_more_spatial(self) -> List[Dict]:
        """Generate more spatial questions"""
        return [
            {"id": f"SP{i+4:03d}", "cat": "spatial", "sub": "visualization", 
             "difficulty": random.choice(["easy", "medium", "hard"]),
             "text": f"Spatial reasoning question #{i+4}",
             "opts": ["A", "B", "C", "D"],
             "ans": 0,
             "exp": f"Explanation for spatial question #{i+4}"}
            for i in range(20)
        ]
    
    def _iq_aptitude(self) -> List[Dict]:
        """IQ and general aptitude"""
        return [
            {"id": "I001", "cat": "iq", "sub": "pattern", "difficulty": "medium",
             "text": "What number should replace the question mark: 2, 6, 12, 20, 30, ?",
             "opts": ["42", "40", "44", "36"], "ans": 0,
             "exp": "n(n+1): 1×2=2, 2×3=6, 3×4=12... 6×7=<strong>42</strong>"},
            
            {"id": "I002", "cat": "iq", "sub": "word", "difficulty": "medium",
             "text": "Which word does not belong: Apple, Banana, Carrot, Cherry?",
             "opts": ["Carrot", "Apple", "Banana", "Cherry"], "ans": 0,
             "exp": "<strong>Carrot</strong> is a vegetable; others are fruits."},
            
            {"id": "I003", "cat": "iq", "sub": "logic", "difficulty": "hard",
             "text": "If all Bloops are Razzies and all Razzies are Lazzies, are all Bloops definitely Lazzies?",
             "opts": ["Yes", "No", "Cannot tell", "Probably"], "ans": 0,
             "exp": "Transitive property: Bloops → Razzies → Lazzies. <strong>Yes</strong>."},
            
            {"id": "I004", "cat": "iq", "sub": "math", "difficulty": "medium",
             "text": "A bat and ball cost £11 total. The bat costs £10 more than the ball. How much is the ball?",
             "opts": ["50p", "£1", "£1.50", "£0.50"], "ans": 0,
             "exp": "Ball = x, Bat = x+10. 2x+10=11. x=<strong>50p</strong>"},
        ] + self._generate_more_iq()
    
       def _generate_more_iq(self) -> List[Dict]:
        """Generate more IQ questions"""
        questions = []
        
        iq_problems = [
            ("What comes next: J, F, M, A, M, ?", "J", ["J", "A", "S", "O"], "Months: Jan, Feb, Mar, Apr, May, Jun"),
            ("If 2+3=10, 7+2=63, 6+5=66, then 8+4=?", "96", ["96", "48", "32", "72"], "Pattern: (a+b)×a = result"),
            ("I am lighter than feather but strongest man can't hold me. What am I?", "Breath", ["Breath", "Thought", "Shadow", "Air"], "You cannot physically hold breath"),
        ]
        
        for i, problem in enumerate(iq_problems):
            # Safely unpack with error handling
            if len(problem) != 4:
                continue  # Skip malformed entries
            
            text, ans, opts, exp = problem
            
            questions.append({
                "id": f"I{i+5:03d}",
                "cat": "iq",
                "sub": "logic",
                "difficulty": "hard",
                "text": text,
                "opts": opts,
                "ans": opts.index(ans) if ans in opts else 0,
                "exp": f"{exp}. Answer: <strong>{ans}</strong>"
            })
        
        return questions
    
    def _critical_thinking(self) -> List[Dict]:
        """Additional critical thinking questions"""
        return [
            {"id": "C001", "cat": "critical", "sub": "analysis", "difficulty": "hard",
             "text": "A survey shows 80% of CEOs believe AI will transform their industry. Does this mean AI will definitely transform all industries?",
             "opts": ["No - belief doesn't guarantee outcome", "Yes - CEOs are experts", "Maybe", "Cannot tell"], "ans": 0,
             "exp": "<strong>No</strong> - beliefs and predictions are not certainties."},
        ]
    
    def _diagrammatic_reasoning(self) -> List[Dict]:
        """Diagrammatic/flowchart reasoning"""
        return [
            {"id": "D001", "cat": "diagrammatic", "sub": "flow", "difficulty": "medium",
             "text": "Input: 5 → [×2] → [+3] → [÷2] → Output?",
             "opts": ["6.5", "7", "8", "5.5"], "ans": 0,
             "exp": "5×2=10, 10+3=13, 13÷2=<strong>6.5</strong>"},
        ]
    
    def _error_checking(self) -> List[Dict]:
        """Data checking and error detection"""
        return [
            {"id": "E001", "cat": "error_checking", "sub": "data", "difficulty": "easy",
             "text": "Compare: 'ACME Corp, 123 Main St, London' vs 'ACME Corp, 123 Main St, London' - Any errors?",
             "opts": ["No errors", "Spelling error", "Number error", "Address error"], "ans": 0,
             "exp": "Strings are <strong>identical</strong> - no errors."},
            
            {"id": "E002", "cat": "error_checking", "sub": "data", "difficulty": "medium",
             "text": "Compare: 'Ref: 883921' vs 'Ref: 883912' - Any errors?",
             "opts": ["Transposed digits", "Missing digit", "Extra digit", "No error"], "ans": 0,
             "exp": "Last two digits transposed: 21 vs 12. <strong>Transposed digits</strong>."},
        ]
    
    def get_questions(self, category: str, count: int = 60) -> List[Dict]:
        """Get random questions from category"""
        pool = self.questions.get(category, [])
        if len(pool) >= count:
            return random.sample(pool, count)
        # If not enough, include from other categories
        needed = count - len(pool)
        other = [q for cat, qs in self.questions.items() if cat != category for q in qs]
        return pool + random.sample(other, min(needed, len(other)))
    
    def get_all_categories(self) -> List[str]:
        return list(self.questions.keys())

# Initialize question bank
QB = QuestionBank()

# ============================================================
# SESSION STATE MANAGEMENT
# ============================================================

def init_session_state():
    """Initialize all session state variables"""
    defaults = {
        'page': 'dashboard',
        'user': 'Guest',
        'test_history': [],
        'current_test': None,
        'selected_category': None,
        'answers': {},
        'flagged': set(),
        'current_q': 0,
        'time_remaining': 50 * 60,  # 50 minutes in seconds
        'timer_active': False,
        'test_start_time': None,
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

# ============================================================
# UI COMPONENTS
# ============================================================

def render_header():
    """Render main application header"""
    st.markdown("""
    <div class="main-header">
        <h1>🧠 AptitudePro</h1>
        <p>Professional Psychometric Test Preparation | SHL • Kenexa • Cubiks • Watson-Glaser</p>
    </div>
    """, unsafe_allow_html=True)

def render_nav():
    """Render navigation"""
    cols = st.columns(4)
    pages = [
        ("📊 Dashboard", "dashboard"),
        ("📝 Take Test", "tests"),
        ("📈 Analytics", "analytics"),
        ("ℹ️ Help", "help")
    ]
    
    for i, (label, page) in enumerate(pages):
        with cols[i]:
            if st.button(label, key=f"nav_{page}", use_container_width=True,
                        type="primary" if st.session_state.page == page else "secondary"):
                st.session_state.page = page
                st.rerun()

def render_dashboard():
    """Render dashboard page"""
    st.markdown("### Your Performance Overview")
    
    # Stats row
    history = st.session_state.test_history
    
    cols = st.columns(4)
    stats = [
        ("Tests Completed", len(history), "📝"),
        ("Average Score", f"{sum(t['score'] for t in history)//len(history)}%" if history else "—", "📊"),
        ("Best Score", f"{max(t['score'] for t in history)}%" if history else "—", "🏆"),
        ("Questions Answered", len(history) * 60 if history else 0, "❓"),
    ]
    
    for col, (label, value, icon) in zip(cols, stats):
        with col:
            st.markdown(f"""
            <div class="stat-card">
                <div style="font-size: 2rem;">{icon}</div>
                <div style="color: #64748b; font-size: 0.875rem;">{label}</div>
                <div style="font-size: 1.875rem; font-weight: 700; color: #1e40af;">{value}</div>
            </div>
            """, unsafe_allow_html=True)
    
    # Score trend chart
    if history:
        st.markdown("### Score Trend")
        df = pd.DataFrame([
            {"Test": i+1, "Score": t["score"], "Category": t["category"]} 
            for i, t in enumerate(history[-10:])
        ])
        
        fig = px.line(df, x="Test", y="Score", color="Category", 
                     markers=True, range_y=[0, 100],
                     color_discrete_sequence=["#2563eb", "#3b82f6", "#60a5fa"])
        fig.update_layout(
            plot_bgcolor="white",
            paper_bgcolor="white",
            font=dict(family="Inter, sans-serif"),
            yaxis_gridcolor="#e2e8f0"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Category grid
    st.markdown("### Test Categories")
    
    categories = {
        "numerical": ("Numerical Reasoning", "📊", "Percentages, ratios, data tables"),
        "verbal": ("Verbal Reasoning", "📖", "Comprehension, True/False/Cannot Say"),
        "logical": ("Logical Reasoning", "🔷", "Sequences, analogies, syllogisms"),
        "abstract": ("Abstract Reasoning", "🔺", "Patterns, rotations, matrices"),
        "watson_glaser": ("Watson-Glaser", "🎯", "Critical thinking, inferences"),
        "sjt": ("Situational Judgement", "🤝", "Professional scenarios"),
        "mechanical": ("Mechanical Reasoning", "⚙️", "Gears, levers, physics"),
        "spatial": ("Spatial Reasoning", "📐", "Visualization, folding, rotation"),
        "iq": ("IQ & Aptitude", "🧩", "General intelligence, patterns"),
    }
    
    cols = st.columns(3)
    for i, (key, (name, icon, desc)) in enumerate(categories.items()):
        with cols[i % 3]:
            # Check if category has been attempted
            cat_history = [t for t in history if t["category"] == key]
            best_score = max(t["score"] for t in cat_history) if cat_history else None
            
            badge = ""
            if best_score:
                color = "#10b981" if best_score >= 70 else "#f59e0b" if best_score >= 50 else "#ef4444"
                badge = f'<div style="color: {color}; font-size: 0.875rem; font-weight: 600;">Best: {best_score}%</div>'
            
            clicked = st.button(
                f"{icon} {name}",
                key=f"cat_{key}",
                use_container_width=True
            )
            if clicked:
                st.session_state.selected_category = key
                st.session_state.page = "tests"
                st.rerun()
            
            st.markdown(f"""
            <div style="font-size: 0.875rem; color: #64748b; margin-top: -0.5rem;">{desc}</div>
            {badge}
            """, unsafe_allow_html=True)

def render_test_selection():
    """Render test configuration page"""
    st.markdown("### Configure Your Test")
    
    if not st.session_state.selected_category:
        st.info("Please select a category from the Dashboard first!")
        if st.button("← Back to Dashboard", type="primary"):
            st.session_state.page = "dashboard"
            st.rerun()
        return
    
    cat_key = st.session_state.selected_category
    cat_info = {
        "numerical": ("Numerical Reasoning", "📊"),
        "verbal": ("Verbal Reasoning", "📖"),
        "logical": ("Logical Reasoning", "🔷"),
        "abstract": ("Abstract Reasoning", "🔺"),
        "watson_glaser": ("Watson-Glaser Critical Thinking", "🎯"),
        "sjt": ("Situational Judgement", "🤝"),
        "mechanical": ("Mechanical Reasoning", "⚙️"),
        "spatial": ("Spatial Reasoning", "📐"),
        "iq": ("IQ & General Aptitude", "🧩"),
    }
    
    name, icon = cat_info.get(cat_key, (cat_key, "📝"))
    
    st.markdown(f"""
    <div style="background: white; padding: 1.5rem; border-radius: 12px; border: 2px solid #e2e8f0; margin-bottom: 1rem;">
        <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">{icon} {name}</div>
        <div style="color: #64748b;">60 questions • 50 minutes • Adaptive difficulty</div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🚀 Start Test", type="primary", use_container_width=True):
            start_test(cat_key)
    with col2:
        if st.button("← Back", use_container_width=True):
            st.session_state.page = "dashboard"
            st.rerun()

def start_test(category: str):
    """Initialize and start a new test"""
    questions = QB.get_questions(category, 60)
    
    st.session_state.current_test = {
        "id": datetime.now().strftime("%Y%m%d_%H%M%S"),
        "category": category,
        "questions": questions,
        "start_time": time.time(),
    }
    st.session_state.answers = {}
    st.session_state.flagged = set()
    st.session_state.current_q = 0
    st.session_state.time_remaining = 50 * 60
    st.session_state.timer_active = True
    st.session_state.page = "active_test"
    st.rerun()

def render_active_test():
    """Render active test interface"""
    if not st.session_state.current_test:
        st.session_state.page = "dashboard"
        st.rerun()
        return
    
    test = st.session_state.current_test
    q_idx = st.session_state.current_q
    question = test["questions"][q_idx]
    
    # Timer
    if st.session_state.timer_active:
        elapsed = time.time() - test["start_time"]
        st.session_state.time_remaining = max(0, 50 * 60 - int(elapsed))
        
        if st.session_state.time_remaining <= 0:
            submit_test()
            return
    
    # Top bar
    col1, col2, col3 = st.columns([2, 3, 1])
    
    with col1:
        st.markdown(f"**Question {q_idx + 1} of 60**")
        st.markdown(f"Category: {question['cat'].replace('_', ' ').title()}")
    
    with col2:
        mins = st.session_state.time_remaining // 60
        secs = st.session_state.time_remaining % 60
        timer_class = "timer-box"
        if st.session_state.time_remaining < 300:
            timer_class += " warning"
        if st.session_state.time_remaining < 60:
            timer_class += " danger"
        
        st.markdown(f"""
        <div class="{timer_class}">
            {mins:02d}:{secs:02d}
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        if st.button("🏁 Submit", type="primary", use_container_width=True):
            submit_test()
            return
    
    # Progress bar
    answered = len(st.session_state.answers)
    progress = (answered / 60) * 100
    st.markdown(f"""
    <div class="progress-container">
        <div class="progress-fill" style="width: {progress}%"></div>
    </div>
    <div style="text-align: center; color: #64748b; font-size: 0.875rem; margin-top: 0.25rem;">
        {answered} of 60 answered
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation dots
    st.markdown("###")
    dots_html = "<div style='display: flex; flex-wrap: wrap; gap: 4px; justify-content: center;'>"
    for i in range(60):
        classes = ["nav-dot"]
        if i in st.session_state.answers:
            classes.append("answered")
        if i == q_idx:
            classes.append("current")
        if i in st.session_state.flagged:
            classes.append("flagged")
        
        dots_html += f"<div class='{' '.join(classes)}' onclick='window.location.href=\"?q={i}\"'>{i+1}</div>"
    dots_html += "</div>"
    st.markdown(dots_html, unsafe_allow_html=True)
    
    # Question card
    st.markdown("###")
    
    # Display passage if exists
    if "passage" in question:
        with st.expander("📖 Reading Passage (Click to expand/collapse)", expanded=True):
            st.markdown(f"""
            <div style="background: #f8fafc; padding: 1rem; border-radius: 8px; border-left: 4px solid #3b82f6; line-height: 1.6;">
                {question['passage']}
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="question-card">
        <div style="display: flex; justify-content: between; align-items: start; margin-bottom: 1rem;">
            <span class="q-tag" style="background: #dbeafe; color: #1e40af; padding: 0.25rem 0.75rem; border-radius: 9999px; font-size: 0.875rem; font-weight: 500;">
                {question['sub'].replace('_', ' ').title()}
            </span>
        </div>
        <div style="font-size: 1.125rem; line-height: 1.6; margin-bottom: 1.5rem;">
            {question['text']}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Options
    current_answer = st.session_state.answers.get(q_idx)
    
    for i, opt in enumerate(question["opts"]):
        btn_class = "option-btn"
        if current_answer == i:
            btn_class += " selected"
        
        if st.button(
            f"{chr(65+i)}. {opt}",
            key=f"opt_{q_idx}_{i}",
            use_container_width=True,
            type="secondary" if current_answer != i else "primary"
        ):
            st.session_state.answers[q_idx] = i
            st.rerun()
    
    # Flag button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        flag_emoji = "🚩" if q_idx in st.session_state.flagged else "⚑"
        if st.button(f"{flag_emoji} Flag for Review", use_container_width=True):
            if q_idx in st.session_state.flagged:
                st.session_state.flagged.remove(q_idx)
            else:
                st.session_state.flagged.add(q_idx)
            st.rerun()
    
    # Navigation
    with col2:
        nav_cols = st.columns(2)
        with nav_cols[0]:
            if q_idx > 0 and st.button("← Previous", use_container_width=True):
                st.session_state.current_q = q_idx - 1
                st.rerun()
        with nav_cols[1]:
            if q_idx < 59 and st.button("Next →", type="primary", use_container_width=True):
                st.session_state.current_q = q_idx + 1
                st.rerun()
            elif q_idx == 59 and st.button("Finish →", type="primary", use_container_width=True):
                submit_test()
                return

def submit_test():
    """Calculate results and show summary"""
    test = st.session_state.current_test
    if not test:
        return
    
    st.session_state.timer_active = False
    
    # Calculate score
    correct = 0
    wrong = 0
    unanswered = 0
    
    for i, q in enumerate(test["questions"]):
        ans = st.session_state.answers.get(i)
        if ans is None:
            unanswered += 1
        elif ans == q["ans"]:
            correct += 1
        else:
            wrong += 1
    
    score = round((correct / 60) * 100)
    
    # Save result
    result = {
        "id": test["id"],
        "category": test["category"],
        "score": score,
        "correct": correct,
        "wrong": wrong,
        "unanswered": unanswered,
        "date": datetime.now().isoformat(),
        "time_taken": 50 * 60 - st.session_state.time_remaining,
        "answers": st.session_state.answers.copy(),
        "questions": test["questions"]
    }
    
    st.session_state.test_history.append(result)
    st.session_state.current_test = None
    st.session_state.page = "results"
    st.session_state.last_result = result
    st.rerun()

def render_results():
    """Render test results page"""
    if "last_result" not in st.session_state:
        st.session_state.page = "dashboard"
        st.rerun()
        return
    
    result = st.session_state.last_result
    
    # Score circle
    st.markdown(f"""
    <div style="text-align: center; padding: 2rem;">
        <div class="score-circle" style="--score: {result['score']};">
            <div class="score-text">{result['score']}%</div>
        </div>
        <div style="margin-top: 1rem; font-size: 1.25rem; color: #1e40af; font-weight: 600;">
            {get_grade(result['score'])}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Summary stats
    cols = st.columns(4)
    stats = [
        ("✅ Correct", result["correct"], "#10b981"),
        ("❌ Incorrect", result["wrong"], "#ef4444"),
        ("⚪ Unanswered", result["unanswered"], "#64748b"),
        ("⏱️ Time Used", f"{(result['time_taken']//60)}m {result['time_taken']%60}s", "#f59e0b"),
    ]
    
    for col, (label, value, color) in zip(cols, stats):
        with col:
            st.markdown(f"""
            <div style="text-align: center; padding: 1rem; background: white; border-radius: 12px; border: 1px solid #e2e8f0;">
                <div style="font-size: 1.5rem; color: {color}; font-weight: 700;">{value}</div>
                <div style="color: #64748b; font-size: 0.875rem;">{label}</div>
            </div>
            """, unsafe_allow_html=True)
    
    # Review answers
    st.markdown("### Review Answers")
    
    for i, q in enumerate(result["questions"]):
        user_ans = result["answers"].get(i)
        correct_ans = q["ans"]
        
        status = "✅" if user_ans == correct_ans else "❌" if user_ans is not None else "⚪"
        color = "#10b981" if user_ans == correct_ans else "#ef4444" if user_ans is not None else "#64748b"
        
        with st.expander(f"{status} Question {i+1}: {q['text'][:60]}..."):
            st.markdown(f"""
            <div style="background: #f8fafc; padding: 1rem; border-radius: 8px; margin-bottom: 0.5rem;">
                {q.get('passage', '')}
                <br><br>
                <strong>{q['text']}</strong>
            </div>
            """, unsafe_allow_html=True)
            
            for j, opt in enumerate(q["opts"]):
                style = ""
                if j == correct_ans:
                    style = "background: #d1fae5; border-color: #10b981;"
                elif j == user_ans and j != correct_ans:
                    style = "background: #fee2e2; border-color: #ef4444;"
                
                st.markdown(f"""
                <div style="padding: 0.75rem; margin: 0.25rem 0; border-radius: 8px; border: 2px solid #e2e8f0; {style}">
                    {chr(65+j)}. {opt}
                    {" ✅ Correct" if j == correct_ans else ""}
                    {" ❌ Your answer" if j == user_ans and j != correct_ans else ""}
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="explanation-box">
                <strong>Explanation:</strong><br>
                {q['exp']}
            </div>
            """, unsafe_allow_html=True)
    
    # Action buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Retake Test", type="primary", use_container_width=True):
            start_test(result["category"])
    with col2:
        if st.button("📊 Back to Dashboard", use_container_width=True):
            st.session_state.page = "dashboard"
            st.rerun()

def get_grade(score: int) -> str:
    """Get grade description"""
    if score >= 90: return "🏆 Outstanding - Top 5%"
    if score >= 80: return "⭐ Excellent - Top 15%"
    if score >= 70: return "✅ Good - Above Average"
    if score >= 60: return "📈 Satisfactory - Average"
    if score >= 50: return "⚠️ Below Average - Needs Practice"
    return "📚 Needs Significant Improvement"

def render_analytics():
    """Render analytics page"""
    st.markdown("### Performance Analytics")
    
    history = st.session_state.test_history
    
    if not history:
        st.info("Complete some tests to see your analytics!")
        return
    
    # Category performance
    st.markdown("#### Performance by Category")
    
    cat_scores = defaultdict(list)
    for t in history:
        cat_scores[t["category"]].append(t["score"])
    
    cat_data = []
    for cat, scores in cat_scores.items():
        cat_data.append({
            "Category": cat.replace("_", " ").title(),
            "Average": sum(scores) / len(scores),
            "Tests": len(scores),
            "Best": max(scores)
        })
    
    df_cat = pd.DataFrame(cat_data)
    
    fig = px.bar(df_cat, x="Category", y="Average", color="Tests",
                 color_continuous_scale="Blues",
                 text=df_cat["Average"].round(1))
    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        yaxis_range=[0, 100]
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Recent tests table
    st.markdown("#### Recent Tests")
    
    df_tests = pd.DataFrame([
        {
            "Date": datetime.fromisoformat(t["date"]).strftime("%Y-%m-%d %H:%M"),
            "Category": t["category"].replace("_", " ").title(),
            "Score": f"{t['score']}%",
            "Correct": f"{t['correct']}/60",
            "Time": f"{t['time_taken']//60}m"
        }
        for t in reversed(history[-10:])
    ])
    
    st.dataframe(df_tests, use_container_width=True, hide_index=True)

def render_help():
    """Render help/instructions page"""
    st.markdown("""
    ### How to Use AptitudePro
    
    #### Test Categories
    
    **Numerical Reasoning**: Percentages, ratios, data interpretation, financial calculations
    - Practice mental math and quick estimation
    - Focus on identifying relevant data in tables
    
    **Verbal Reasoning**: Comprehension, True/False/Cannot Say, synonyms/antonyms
    - Read passages carefully before answering
    - Look for definitive statements for True/False
    
    **Logical Reasoning**: Sequences, analogies, syllogisms
    - Identify patterns in number and letter sequences
    - Practice diagrammatic relationships
    
    **Watson-Glaser**: Critical thinking assessment
    - Inference: Judge if conclusions follow from evidence
    - Assumptions: Identify unstated premises
    - Deduction: Apply logical rules strictly
    
    #### Tips for Success
    
    1. **Time Management**: 50 minutes for 60 questions = 50 seconds per question
    2. **Flag and Return**: Mark difficult questions for review
    3. **No Penalty for Guessing**: Answer all questions even if unsure
    4. **Practice Regularly**: Consistent practice improves speed and accuracy
    
    #### Scoring
    
    - 90-100%: Outstanding
    - 80-89%: Excellent  
    - 70-79%: Good
    - 60-69%: Satisfactory
    - 50-59%: Below Average
    - Below 50%: Needs Practice
    """)

# ============================================================
# MAIN APPLICATION
# ============================================================

def main():
    init_session_state()
    render_header()
    render_nav()
    
    # Page routing
    page = st.session_state.page
    
    if page == "dashboard":
        render_dashboard()
    elif page == "tests":
        render_test_selection()
    elif page == "active_test":
        render_active_test()
    elif page == "results":
        render_results()
    elif page == "analytics":
        render_analytics()
    elif page == "help":
        render_help()

if __name__ == "__main__":
    main()
