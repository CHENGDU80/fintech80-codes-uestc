import pandas as pd
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import os
import re


def analysisOneFile(rawDir, filename, processedDir1, processedDir2):
    # 读新闻文本
    df = pd.read_csv(os.path.join(rawDir, filename))

    # 通过vader分析情感
    sid = SentimentIntensityAnalyzer()
    vader_score = [
        sid.polarity_scores(text)['compound'] for text in df['content']
    ]
    df['vader_score'] = vader_score

    # 通过字典统计词频
    dict = pd.read_csv('MasterDictionary.csv')
    dict_score = []
    for text in df['content']:
        positive = 0
        negative = 0
        for word in text.split():
            # 转大写
            word = word.upper()
            if word in dict['word'].values:
                if dict[dict['word'] == word]['positive'].values == 1:
                    positive += 1
                elif dict[dict['word'] == word]['negative'].values == 1:
                    negative += 1
        # positive_count.append(positive)
        # negative_count.append(negative)
        score = (positive - negative) / ((positive + negative) + 0.000001)
        dict_score.append(score)
    df['dict_score'] = dict_score

    # 保存结果
    df.to_csv(os.path.join(processedDir1, filename))

    # 只保留date,vader_score和dict_score
    df = df[['date', 'vader_score', 'dict_score']]
    # 裁切date,只要前10位
    df['date'] = df['date'].str.slice(0, 10)
    # 按照date分组，计算每组的的平均值
    df = df.groupby('date').mean()
    df = df.reset_index()

    # 保存结果
    df.to_csv(os.path.join(processedDir2, filename))


def dataCleaning(rawDir, filename, cleanDir):
    df = pd.read_csv(os.path.join(rawDir, filename), header=None)
    # 添加列名
    df.columns = ['title', 'content', 'comment', 'date']
    # 裁切date,只要前10位
    df['date'] = df['date'].str.slice(0, 10)
    # 如果content为空，删除该行
    df = df.dropna(subset=['content'])
    # 如果content的单词数小于20，删除该行
    df = df[df['content'].str.split().str.len() > 20]
    # 如果content包含乱码，删除该行
    df = df[df['content'].str.contains('�') == False]
    # 去掉content中的所有符号
    df['content'] = df['content'].apply(lambda x: re.sub(r'[^\w\s]+', '', x))

    # 保存结果
    df.to_csv(os.path.join(cleanDir, filename), index=False)


if __name__ == '__main__':
    rawDir = 'raw_data'
    cleanDir = 'clean_data'
    processedDir1 = 'processed_data/news_with_score'
    processedDir2 = 'processed_data/with_compound_score'
    # for filename in os.listdir(rawDir):
    #     if filename.endswith('.csv'):
    #         print('processing ' + filename)
    #         # dataCleaning(rawDir, filename, cleanDir)
    #         analysisOneFile(cleanDir, filename, processedDir1, processedDir2)
    analysisOneFile('', '6.csv', processedDir1, processedDir2)
