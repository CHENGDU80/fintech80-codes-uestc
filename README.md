UESTC

1. Search_News: The search.py file is used for file retrieval. It searches for files in the "news" subdirectory, naming them based on keywords.
2. News_Classified: The news.py file is for file categorization. Categorized files have a classification label added in CSV format, saved as 1.csv, 2.csv, and so on.
3. News_Rating: EMOTION.py is used to rate news articles. Processed files are saved in the "processed_data" subdirectory and grouped into three folders based on the rating criteria.
4. News_Processing: The combine.py file merges news articles by date, calculating total comments and scores for each category. Results are stored in df_new.csv. SUMMARY.csv is used to generate news summaries, with the summaries added as a new column and saved in summary.csv.
5. TNT: TNT.py is used for model training, and the directory contains the necessary training data. Training results are saved in the "result" folder, with a new test_n folder generated for each test, storing result images.
6. fintech_ui: The folder contains frontend code. Double-click 'main.exe' in 'fintech-ui/dist/main' to launch
7. User Maual_TNT.pdf: Quick-start for our product.
