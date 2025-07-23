# 🗺️ Διαδραστικός Χάρτης Έργων Ύδρευσης

Interactive dashboard for analyzing water infrastructure projects across Greece.

## Features
- Interactive map visualization by prefecture
- Detailed project analysis
- Budget and timeline tracking
- Export capabilities

## Usage
1. Upload your Excel file with project data
2. Explore the interactive map and charts
3. Filter by region, prefecture, or project type
4. Export results for further analysis

## Data Format
Upload an Excel file with columns including project details, budgets, locations, and timelines.

## Local Development

1. Clone the repository:
```bash
git clone https://github.com/your-username/greece-water-projects-map.git
cd greece-water-projects-map
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the Streamlit app:
```bash
streamlit run map_projects.py
```

## Deployment
This app is ready to be deployed on Streamlit Cloud. Just connect your GitHub repository to Streamlit Cloud and select `map_projects.py` as the main file.

## License
[Add your license here]
