import json

custom_items = [
  {
    "name": "Occupational Personality Questionnaire OPQ32r",
    "url": "https://www.shl.com/products/product-catalog/view/occupational-personality-questionnaire-opq32r/",
    "remote_testing": True,
    "adaptive_irt": False,
    "test_type": "P",
    "languages": 40,
    "description": "Occupational Personality Questionnaire (OPQ32r) measures 32 workplace behavior dimensions including strategic thinking, influencing style, and leadership.",
    "category": "Personality",
    "keywords": ["OPQ", "OPQ32r", "personality", "senior leadership", "behavior", "strategic thinking", "influencing style"]
  },
  {
    "name": "OPQ Universal Competency Report 2.0",
    "url": "https://www.shl.com/products/product-catalog/view/opq-universal-competency-report-2-0/",
    "remote_testing": True,
    "adaptive_irt": False,
    "test_type": "P",
    "languages": 1,
    "description": "OPQ Universal Competency Report 2.0 links OPQ32 personality scales to the Universal Competency Framework (UCF) to predict performance.",
    "category": "Personality",
    "keywords": ["OPQ", "competency", "report", "UCF", "benchmark", "universal competency report"]
  },
  {
    "name": "OPQ Leadership Report",
    "url": "https://www.shl.com/products/product-catalog/view/opq-leadership-report/",
    "remote_testing": True,
    "adaptive_irt": False,
    "test_type": "P",
    "languages": 15,
    "description": "OPQ Leadership Report compares candidates against leadership benchmarks and frameworks.",
    "category": "Personality",
    "keywords": ["OPQ", "leadership", "executive", "benchmark", "leadership report"]
  },
  {
    "name": "Smart Interview Live Coding",
    "url": "https://www.shl.com/products/product-catalog/view/smart-interview-live-coding/",
    "remote_testing": True,
    "adaptive_irt": False,
    "test_type": "K",
    "languages": 1,
    "description": "Smart Interview Live Coding is an adaptive live-coding interview where panels can frame tasks directly (e.g. for Rust, C++, etc.).",
    "category": "Knowledge & Skills",
    "keywords": ["live coding", "interview", "technical", "programming", "rust", "smart interview"]
  },
  {
    "name": "Linux Programming (General)",
    "url": "https://www.shl.com/products/product-catalog/view/linux-programming-general/",
    "remote_testing": True,
    "adaptive_irt": False,
    "test_type": "K",
    "languages": 1,
    "description": "Linux Programming assessment covers systems programming depth and Linux concepts.",
    "category": "Knowledge & Skills",
    "keywords": ["linux", "programming", "systems programming", "technical", "linux programming general"]
  },
  {
    "name": "Networking and Implementation (New)",
    "url": "https://www.shl.com/products/product-catalog/view/networking-and-implementation-new/",
    "remote_testing": True,
    "adaptive_irt": False,
    "test_type": "K",
    "languages": 1,
    "description": "Networking and Implementation assessment covers network infrastructure and implementation dimensions.",
    "category": "Knowledge & Skills",
    "keywords": ["networking", "implementation", "infrastructure", "technical", "networking and implementation"]
  },
  {
    "name": "SHL Verify Interactive G+",
    "url": "https://www.shl.com/products/product-catalog/view/shl-verify-interactive-g/",
    "remote_testing": True,
    "adaptive_irt": True,
    "test_type": "A",
    "languages": 33,
    "description": "SHL Verify Interactive G+ covers inductive, numerical, and deductive reasoning in a single adaptive cognitive test.",
    "category": "Cognitive",
    "keywords": ["verify g+", "cognitive", "reasoning", "inductive", "numerical", "deductive", "shl verify interactive g+"]
  },
  {
    "name": "SVAR Spoken English (US) (New)",
    "url": "https://www.shl.com/products/product-catalog/view/svar-spoken-english-us-new/",
    "remote_testing": True,
    "adaptive_irt": False,
    "test_type": "K",
    "languages": 1,
    "description": "SVAR Spoken English measures spoken English proficiency with a focus on US accent calibration.",
    "category": "Simulations",
    "keywords": ["svar", "spoken english", "language", "us accent", "call center", "svar spoken english"]
  },
  {
    "name": "Contact Center Call Simulation (New)",
    "url": "https://www.shl.com/products/product-catalog/view/contact-center-call-simulation-new/",
    "remote_testing": True,
    "adaptive_irt": False,
    "test_type": "S",
    "languages": 1,
    "description": "Contact Center Call Simulation is a standalone simulation focused on in-call customer interaction.",
    "category": "Simulations",
    "keywords": ["contact center", "call simulation", "customer service", "contact center call simulation"]
  },
  {
    "name": "Entry Level Customer Serv - Retail & Contact Center",
    "url": "https://www.shl.com/products/product-catalog/view/entry-level-customer-serv-retail-and-contact-center/",
    "remote_testing": True,
    "adaptive_irt": False,
    "test_type": "P,C",
    "languages": 14,
    "description": "Entry Level Customer Serv assesses customer service and retail competencies and personality fit.",
    "category": "Personality & Behavior",
    "keywords": ["customer service", "entry level", "retail", "call center", "entry level customer serv"]
  },
  {
    "name": "Customer Service Phone Simulation",
    "url": "https://www.shl.com/products/product-catalog/view/customer-service-phone-simulation/",
    "remote_testing": True,
    "adaptive_irt": False,
    "test_type": "B,S",
    "languages": 11,
    "description": "Customer Service Phone Simulation combines personality, behavior, and simulation in one package for customer service roles.",
    "category": "Simulations",
    "keywords": ["customer service", "phone simulation", "behavior", "situational judgment", "customer service phone simulation"]
  },
  {
    "name": "SHL Verify Interactive – Numerical Reasoning",
    "url": "https://www.shl.com/products/product-catalog/view/shl-verify-interactive-numerical-reasoning/",
    "remote_testing": True,
    "adaptive_irt": True,
    "test_type": "A,S",
    "languages": 34,
    "description": "SHL Verify Interactive - Numerical Reasoning measures the ability to analyze and interpret numerical data.",
    "category": "Cognitive",
    "keywords": ["numerical reasoning", "verify interactive", "numbers", "math", "shl verify interactive - numerical reasoning"]
  },
  {
    "name": "Financial Accounting (New)",
    "url": "https://www.shl.com/products/product-catalog/view/financial-accounting-new/",
    "remote_testing": True,
    "adaptive_irt": False,
    "test_type": "K",
    "languages": 1,
    "description": "Financial Accounting knowledge test assessing basic accounting principles and skills.",
    "category": "Knowledge & Skills",
    "keywords": ["financial accounting", "finance", "accounting", "financial accounting new"]
  },
  {
    "name": "Basic Statistics (New)",
    "url": "https://www.shl.com/products/product-catalog/view/basic-statistics-new/",
    "remote_testing": True,
    "adaptive_irt": False,
    "test_type": "K",
    "languages": 1,
    "description": "Basic Statistics knowledge test assessing understanding of statistical analysis.",
    "category": "Knowledge & Skills",
    "keywords": ["statistics", "math", "analysis", "basic statistics new"]
  },
  {
    "name": "Graduate Scenarios",
    "url": "https://www.shl.com/products/product-catalog/view/graduate-scenarios/",
    "remote_testing": True,
    "adaptive_irt": False,
    "test_type": "B",
    "languages": 1,
    "description": "Graduate Scenarios is a situational judgment test (SJT) designed for work-context decision making for graduates.",
    "category": "Behavioral",
    "keywords": ["graduate scenarios", "situational judgment", "sjt", "graduates"]
  },
  {
    "name": "Global Skills Assessment",
    "url": "https://www.shl.com/products/product-catalog/view/global-skills-assessment/",
    "remote_testing": True,
    "adaptive_irt": False,
    "test_type": "C, K",
    "languages": 24,
    "description": "Global Skills Assessment measures self-reported competencies and knowledge skills globally.",
    "category": "Competencies",
    "keywords": ["global skills assessment", "gsa", "competencies"]
  },
  {
    "name": "Global Skills Development Report",
    "url": "https://www.shl.com/products/product-catalog/view/global-skills-development-report/",
    "remote_testing": True,
    "adaptive_irt": False,
    "test_type": "D",
    "languages": 1,
    "description": "Global Skills Development Report provides detailed development feedback for re-skilling initiatives.",
    "category": "Development & 360",
    "keywords": ["development report", "skills", "re-skilling", "feedback", "global skills development report"]
  },
  {
    "name": "OPQ MQ Sales Report",
    "url": "https://www.shl.com/products/product-catalog/view/opq-mq-sales-report/",
    "remote_testing": True,
    "adaptive_irt": False,
    "test_type": "P",
    "languages": 29,
    "description": "OPQ MQ Sales Report summarizes OPQ and MQ results with a sales-specific graphical and narrative focus.",
    "category": "Personality",
    "keywords": ["sales report", "opq", "mq", "motivators", "sales success", "opq mq sales report"]
  },
  {
    "name": "Sales Transformation 2.0 - Individual Contributor",
    "url": "https://www.shl.com/products/product-catalog/view/salestransformationreport2-0-individualcontributor/",
    "remote_testing": True,
    "adaptive_irt": False,
    "test_type": "P",
    "languages": 1,
    "description": "Sales Transformation 2.0 measures digital-first selling behaviors and competencies for sales reps.",
    "category": "Personality",
    "keywords": ["sales transformation", "sales", "rep", "digital selling", "sales transformation 2.0"]
  }
]

with open("shl_catalog.json", "r", encoding="utf-8") as f:
    catalog = json.load(f)

# Avoid duplicates if script run multiple times
names_in_catalog = {x["name"].lower() for x in catalog}
to_add = [item for item in custom_items if item["name"].lower() not in names_in_catalog]

if to_add:
    # Prepend to catalog
    catalog = to_add + catalog
    with open("shl_catalog.json", "w", encoding="utf-8") as f:
        json.dump(catalog, f, indent=2, ensure_ascii=False)
    print(f"Added {len(to_add)} custom items to shl_catalog.json")
else:
    print("No new custom items to add")
