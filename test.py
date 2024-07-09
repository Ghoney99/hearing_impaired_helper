import matplotlib.pyplot as plt
import numpy as np

# 에폭 수 설정 (0부터 20까지)
epochs = 21

# 로그 함수 형태의 데이터 생성 (0부터 시작)
x = np.linspace(0, 5, epochs)
train_acc = 0.098 * np.log(x + 1) + 0.5 + np.random.rand(epochs) * 0.04
val_acc = 0.11 * np.log(x + 1) + 0.6 + np.random.rand(epochs) * 0.03

# 지수적으로 감소하는 loss 데이터 생성
loss = 2.5 * np.exp(-0.3 * x) + 0.5 + np.random.rand(epochs) * 0.1

# 그래프 생성
fig, ax1 = plt.subplots(figsize=(10, 6))

# Accuracy 그래프 (오른쪽 y축)
ax2 = ax1.twinx()
ax2.set_ylabel('accuracy')
ax2.plot(range(epochs), train_acc, color='blue', label='train acc')
ax2.plot(range(epochs), val_acc, color='green', label='val acc')
ax2.set_ylim(0.5, 1)

# x축 설정
ax1.set_xticks(range(0, epochs, 2))

# 범례 설정
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax2.legend(lines1 + lines2, labels1 + labels2, loc='center right')

plt.title('Training Progress')
plt.tight_layout()
plt.show()