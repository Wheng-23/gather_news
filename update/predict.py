import numpy as np
from sklearn.linear_model import LinearRegression
from config.mysqlop import Mysqlop


def predict_heat(id):
    a = Mysqlop()
    # 0,0,0,0,0,0,1
    # 1, 1, 0, 1, 0, 0, 2
    # 7,2,2,1,0,1,8
    # for i in range(97):
    for i in range(id, a.get_row_count() + 1):
    # for i in range(id, 2048):
        X = np.array([[1], [2], [3], [4], [5], [6], [7]]).reshape(-1, 1)  # 特征
        heat6 = str(a.getData(i - 1, 1, "6天前"))
        heat5 = str(a.getData(i - 1, 1, "5天前"))
        heat4 = str(a.getData(i - 1, 1, "4天前"))
        heat3 = str(a.getData(i - 1, 1, "3天前"))
        heat2 = str(a.getData(i - 1, 1, "2天前"))
        heat1 = str(a.getData(i - 1, 1, "1天前"))
        heat = str(a.getData(i - 1, 1, "0天前"))
        y = np.array([heat6, heat5, heat4, heat3, heat2, heat1, heat])  # 目标值

        model = LinearRegression()
        model.fit(X, y)
        # 预测下一天的数据
        next_day_data = np.array([[8]])  # 使用下一天的索引作为特征
        prediction = model.predict(next_day_data)

        print(round(prediction[0]))
        predicted_heat = round(prediction[0])
        if predicted_heat < 0:
            predicted_heat = 0

        a.updateHeat('下一天', predicted_heat, i)




if __name__ == '__main__':
    predict_heat(2252)