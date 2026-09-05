import os
import re

# Your list of search texts
search_texts = [
("Adjusted Forecast", []),
("Short Term Driver Based Forecast", ["ST Driver Based Fcst"]),
("Long Term Driver Based Forecast", ["MT Driver Based Fcst"]),
("LY Sales", []),
("Forecast Multiplication Factor", ["Fcst Multiplication Factor"]),
("LLY Sales", []),
("Actual", []),
("JDA Forecast", ["Test Fcst"]),
("LLLY Sales", []),
("Adjusted History", []),
("Adjusted Fcst LC", ["Adjusted ST Fcst LC"]),
("LY Adjusted History", []),
("LLY Adjusted History", []),
("LLLY Adjusted History", []),
("Final Long Term Driver Based Forecast", ["Final Long Term Driver Based Fcst"]),
("Final Multiplying Factor", ["Seasonality & Mean Value Adj"]),
("Adjusted Forecast NR", ["Adjusted Fcst NR"]),
("Adjusted Forecast MT LC", ["Adjusted MT Fcst LC"]),
("External fcst for constrained", ["Stuructural Constraints"]),
("Unconstrained Adjusted Forecast", ["Unconstrained Forecast"]),
("PW Supply Commit", ["Supply Commit"]),
("AOP Mosaic Partial Week at DFU", ["AOP Mosaic Partial Week"]),
("Short Term Multiplying Factor", []),
("Final Short Term Driver Based Forecast", ["Final Short Term Driver Based Fcst"]),
("Long Term Multiplying Factor", []),
("Fcst LY", []),
("Fcst LLY", []),
("Short Term Driver Based Forecast LC", ["ST Driver Based Fcst LC"]),
("PW Supply Commit LC", ["Supply Commit LC"]),
("MT Driver Based Forecast LC", ["MT Driver Based Fcst LC"]),
("Mid Term Driver Based Forecast", ["MT Driver Based Fcst"]),
("Promo Driver", ["Promo", "Promo Driver ST"]),
("Holidays Driver", ["Holidays Driver ST"]),
("Media Driver", ["Media", "A&M Driver ST"]),
("Weather Driver", ["Weather Driver ST"]),
("SNOP Target", ["S&OP Plan"]),
("XYZ", ["FE XYZ Segmentation"]),
("ABC", ["FE ABC Segmentation"]),
("Channel Trend", ["Channel Trend Adj"]),
("External Forecast", ["External Fcst"]),
("External forecast Adj", ["External Fcst Adj"]),
("Promotions Investment", ["Trade Promotions/ Investment in promotions (discounts, samples, offers)", "Promo Adj"]),
("Product Line expansion existing cust", ["Distribution Adj"]),
("Cannibalization", ["Cannibalization/ Halo", "Cannibalization Adj"]),
("Portfolio Evolution", ["Portfolio Evolution (NPI, Phase In / Phase Out)", "Portfolio Adj"]),
("Adjusted Forecast in Kg/Lts", []),
("Adjusted Forecast in Cases", []),
("DFU", [])
]

final_search_texts = []
# Normalize search texts
for m, t in search_texts:
    final_search_texts.append(m.strip().lower())
    for tr in t:
        final_search_texts.append(tr.strip().lower())

print(final_search_texts)

# Folder containing your .txt/.docx files
folder_path = r"C:\Users\sahil.garg\Downloads\Functional Specifications"

def read_file(file_path):
    if file_path.endswith(".txt"):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read().lower()
        except UnicodeDecodeError:
            with open(file_path, "r", encoding="latin-1") as f:
                return f.read().lower()

    elif file_path.endswith(".docx"):
        from docx import Document
        doc = Document(file_path)
        return "\n".join(p.text for p in doc.paragraphs).lower()

    else:
        return ""

# Store results
results = {}

for file_name in os.listdir(folder_path):
    file_path = os.path.join(folder_path, file_name)


    content = read_file(file_path)

    # Count matches
    total_matches = 0

    for term in final_search_texts:
        pattern = r'\b' + re.escape(term) + r'\b'
        total_matches += len(re.findall(pattern, content))

    results[file_name] = total_matches

# Print results
for doc, counts in results.items():
    print(f"{doc}: {counts}")