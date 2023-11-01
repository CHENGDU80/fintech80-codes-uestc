import pandas as pd
import openai
import time
import re

# 改成自己的key
openai.api_key = "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"

filename= '6.csv'
df = pd.read_csv(filename)
# 新建number_list,长度等于df的长度
number_list = [0] * len(df)

# 如果有category列,保留
if 'category' in df.columns:
  df = df[['title', 'content', 'comment', 'date', 'category']]
else:
  df = df[['title', 'content', 'comment', 'date']]

for i, text in enumerate(df['content']):
    if 'category' in df.columns and df['category'][i] != 0:
      print('skipping row', i)
      number_list[i]=df['category'][i]
      continue
    print('getting category for row', i)
    # 在这里编写你的问题
    question = "You will receive a piece of text. Please classify the text into one of the following six topics and respond with a number from 1 to 8 representing the categories: 1. supply and demand, 2. geopolitical events, 3. economic growth, 4. OPEC, 5. crude oil production/inventory, 6. energy policies, 7.other energy development, 8.others. Your response should follow the format: category:1."
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system",
             "content": question},
            {"role": "user", "content": text}]
    )
    res = completion.choices[0].message["content"]
    # 打印中文文本
    print(res)

    # 提取第一个数字
    category_number = re.findall(r'\d+', res)[0]
    print(category_number)
    # 转数字
    category_number = int(category_number)

    # 存number_list
    number_list[i]=category_number

    # 存到df里
    df['category'] = number_list
    print(df['category'][i])
    df.to_csv('6.csv')
    print('sleeping...')
    time.sleep(21)
