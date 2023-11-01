import pandas as pd
import numpy as np
import os
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from keras.layers import Dropout, BatchNormalization
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv1D, Flatten, MaxPooling1D
import matplotlib.pyplot as plt
from tensorflow.keras.optimizers import Adam

# 数据整理函数
def create_dataset(X, y, time_steps=7):
    Xs, ys = [], []
    for i in range(len(X) - time_steps):
        v = X[i:(i + time_steps)]
        Xs.append(v)
        ys.append(y[i + time_steps])
    return np.array(Xs), np.array(ys)

# 读取数据
dataset = pd.read_csv('TCN_train.csv')
X = dataset.iloc[:, 1:-1].values
y = dataset.iloc[:, -1].values

# 数据缩放
scaler_X = MinMaxScaler()
X = scaler_X.fit_transform(X)

scaler_y = MinMaxScaler()
y = y.reshape(-1, 1)
y = scaler_y.fit_transform(y)

# 根据7天的数据来预测第8天
time_steps = 7
X_seq, y_seq = create_dataset(X, y, time_steps)

# 分割数据
X_train, X_val, y_train, y_val = train_test_split(X_seq, y_seq, test_size=0.3, random_state=0)

# 创建CNN模型
model = Sequential()
model.add(Conv1D(filters=64, kernel_size=3, activation='relu', input_shape=(time_steps, X_train.shape[2])))
model.add(MaxPooling1D(pool_size=2))
model.add(Flatten())
model.add(Dense(50, activation='relu'))
model.add(Dense(1))
optimizer = Adam(learning_rate=0.0008)
model.compile(optimizer=optimizer, loss='mse')

# 训练模型
history = model.fit(X_train, y_train, validation_data=(X_val, y_val), epochs=100, verbose=1)

# 绘制训练和验证损失
plt.figure(figsize=(15, 8))
plt.plot(history.history['loss'], label='Training Loss', color='green', linewidth=2.5)
plt.plot(history.history['val_loss'], label='Validation Loss', color='red', linewidth=2.5)
plt.title('Model Loss During Training', fontsize=25)
plt.xlabel('Epoch', fontsize=20)
plt.ylabel('Loss', fontsize=20)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.legend(fontsize=14)
plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()

# 使用模型进行预测
y_val_pred = model.predict(X_val)

# 计算R^2值
r2 = r2_score(y_val, y_val_pred)
print(f"R^2 Score: {r2}")

# 绘制模型训练时测试与真实的匹配图
plt.figure(figsize=(15, 8))
plt.plot(scaler_y.inverse_transform(y_val), label='Actual Values', color='black', linewidth=3)
plt.plot(scaler_y.inverse_transform(y_val_pred), linestyle='--', label='Predicted Values', color='red', linewidth=3)
plt.title('Actual vs Predicted Values During Training', fontsize=25)
plt.xlabel('Samples', fontsize=20)
plt.ylabel('Value', fontsize=20)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.legend(fontsize=14)
plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()

import pandas as pd

# 预测新数据
# 1. 导入数据
dataset_7days = pd.read_csv('TCN_test.csv')

# 2. 使用除第一列和最后一列之外的所有列作为特征
X_7days_raw = dataset_7days.iloc[:, 1:-1].values
num_features = X_7days_raw.shape[1]

# 对数据进行标准化处理
X_7days_transformed = scaler_X.transform(X_7days_raw)

# 使用最后7天的数据预测第8天
X_last_7days = X_7days_transformed[-7:].reshape(1, 7, num_features)  # 注意这里的num_features
y_pred_8th_day = model.predict(X_last_7days)
y_pred_original_8th_day = scaler_y.inverse_transform(y_pred_8th_day)

price_seven_days = dataset_7days.iloc[-1, -1]
price_eight_days = y_pred_original_8th_day[0][0]

# 计算变化率
change_rate = (price_eight_days - price_seven_days) / price_seven_days * 100

# 对变化率进行分类
A = 1
B = 3
if -A <= change_rate <= A:
    result = "Stable"
elif A < change_rate <= B:
    result = "Minor Increase"
elif change_rate > B:
    result = "Major Increase"
elif -B <= change_rate < -A:
    result = "Minor Decrease"
else:
    result = "Major Decrease"

print(price_seven_days)
print(price_eight_days)
print('86.35')
print(f"Predicted category for the next day based on the last 7 days: {result}")

# 前七天的真实值和第八天的预测值
true_values = dataset_7days.iloc[-7:-1, -1].values  # 去掉最后一个数据点
predicted_values = np.append(true_values, price_eight_days)  # 将预测值添加到前七天的真实值中

# print("true_values shape:", true_values.shape)
# print("predicted_values shape:", predicted_values.shape)
# print("true_values:", true_values)
# print("predicted_values:", predicted_values)

# 绘制折线图
plt.figure(figsize=(15, 8))

# 扩展 predicted_values 的长度，将第八天的预测值添加到末尾
predicted_values_extended = np.append(predicted_values, price_eight_days)

# 扩展 true_values 到包含第八天的数据
true_values_extended = np.append(true_values, price_eight_days)

# 绘制折线图
plt.figure(figsize=(15, 8))
plt.plot(range(1, 8), true_values_extended, marker='o', label='True Values', color='blue', linewidth=2)
plt.plot([8], [price_eight_days], marker='x', label='Predicted Value', markersize=10, color='red', linestyle='--', linewidth=2)
plt.title('True vs Predicted Values for the Next 8 Days', fontsize=25)
plt.xlabel('Day', fontsize=20)
plt.ylabel('Price', fontsize=20)
plt.xticks(range(1, 9), fontsize=16)
plt.yticks(fontsize=16)
plt.grid(True, linestyle='--', linewidth=0.5)
plt.legend(fontsize=14)
plt.show()


# 创建Result目录，如果不存在的话
if not os.path.exists('Result'):
    os.mkdir('Result')

# 获取所有的testX目录
test_dirs = [d for d in os.listdir('Result') if d.startswith('test')]
if not test_dirs:
    new_test_dir = 'test1'
else:
    max_index = max([int(dir.split('test')[-1]) for dir in test_dirs])
    new_test_dir = f'test{max_index + 1}'

# 在Result目录下创建新的testX目录
new_test_path = os.path.join('Result', new_test_dir)
os.mkdir(new_test_path)

# 保存第一张图片
plt.figure(figsize=(15, 8))
plt.plot(history.history['loss'], label='Training Loss', color='green', linewidth=2.5)
plt.plot(history.history['val_loss'], label='Validation Loss', color='red', linewidth=2.5)
plt.title('Model Loss During Training', fontsize=25)
plt.xlabel('Epoch', fontsize=20)
plt.ylabel('Loss', fontsize=20)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.legend(fontsize=14)
plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.savefig(os.path.join(new_test_path, 'Model_Loss_During_Training.png'))  # 保存为图片
plt.close()  # 移除 plt.close()，以便保存成功

# 保存第二张图片
plt.figure(figsize=(15, 8))
plt.plot(scaler_y.inverse_transform(y_val), label='Actual Values', color='black', linewidth=3)
plt.plot(scaler_y.inverse_transform(y_val_pred), linestyle='--', label='Predicted Values', color='red', linewidth=3)
plt.title('Actual vs Predicted Values During Training', fontsize=25)
plt.xlabel('Samples', fontsize=20)
plt.ylabel('Value', fontsize=20)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.legend(fontsize=14)
plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.savefig(os.path.join(new_test_path, 'Actual_vs_Predicted_Values_During_Training.png'))  # 保存为图片
plt.close()  # 移除 plt.close()，以便保存成功

# 保存第三张图片
plt.figure(figsize=(15, 8))
plt.plot(range(1, 8), true_values_extended, marker='o', label='True Values', color='blue', linewidth=2)
plt.plot([8], [price_eight_days], marker='x', label='Predicted Value', markersize=10, color='red', linestyle='--', linewidth=2)
plt.title('True vs Predicted Values for the Next 8 Days', fontsize=25)
plt.xlabel('Day', fontsize=20)
plt.ylabel('Price', fontsize=20)
plt.xticks(range(1, 9), fontsize=16)
plt.yticks(fontsize=16)
plt.grid(True, linestyle='--', linewidth=0.5)
plt.legend(fontsize=14)
plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.savefig(os.path.join(new_test_path, 'True_vs_Predicted_Values_for_the_Next_8_Days.png'))  # 保存为图片
plt.close()  # 移除 plt.close()，以便保存成功
