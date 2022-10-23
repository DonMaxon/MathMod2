import numpy as np
import enum
import plotly.graph_objects as go


class ModelType(enum.Enum):
	MALTUS = 0
	LOGISTIC = 1
	COMMON = 2


def solve(n_0: np.ndarray, a: np.ndarray, m: np.ndarray, t: int, step: float) -> tuple:
	"""
	Функция решения задачи нахождения численности популяций
	:param n_0: начальные численности популяций
	:param a: коэффициенты прироста популяций
	:param m: матрица взаимодействия популяций
	:param t: время моделирования
	:param step: временной шаг
	:return: массив времени и численности популяций
	"""
	m_type = getModelType(m)
	if m_type == ModelType.MALTUS:
		print('maltus')
		return count_maltus(n_0, a, t, step)
	if m_type == ModelType.LOGISTIC:
		print('logistic')
		return count_logistic(n_0, a, m, t, step)
	if m_type == ModelType.COMMON:
		print('common')
		return count_common(n_0, a, m, t, step)


def getModelType(matrix: np.ndarray) -> ModelType:
	"""
	Функция по виду матрицы определяет тип модели взаимодействия популяций
	Нулевая матрица - модель Мальтуса, для которой существует точное решение
	Диагональная матрица - логистическая модель, для которой тоже существует точное решение
	Общая модель (Лотки-Вольтерра) - решение будет искаться с помощью интегрирования системы дифференциальных уравнений
	:param matrix: матрица взаимодействия популяций
	:return: тип модели взаимодействия популяций
	"""
	if len(matrix.shape) != 2:
		raise Exception("На вход подана не матрица!")
	zero_flag = True
	for i in range(matrix.shape[1]):
		indexes = np.nonzero(matrix[i, :])
		print(indexes[0])
		if zero_flag:
			if len(indexes[0]):
				zero_flag = False
		if zero_flag:
			continue
		if len(indexes[0]) == 1 and indexes[0][0] == i:
			continue
		return ModelType.COMMON
	return ModelType.MALTUS if zero_flag else ModelType.LOGISTIC


def count_maltus(n_0: np.ndarray, a: np.ndarray, t: int, step: float) -> tuple:
	"""
	Функция ведет расчет численности популяции по модели Мальтуса
	:param n_0: начальная численность каждой популяции
	:param a: коэффициенты прироста для каждой популяции
	:param t: время моделирования
	:param step: временной шаг
	:return: вектор времени и матрица изменения популяций
	"""
	step_count = int(t / step)
	pop_number = n_0.shape[0]
	res = np.zeros((pop_number, step_count), dtype=float)
	res[:, 0] = np.copy(n_0)
	time = np.arange(start=0, stop=t, step=step, dtype=float)
	for i in range(1, step_count):
		res[:, i] = n_0*np.exp(a*time[i])
	return time, res


def count_logistic(n_0: np.ndarray, a: np.ndarray, m: np.ndarray, t: int, step: float) -> tuple:
	"""
	Функция выполняет расчет численности популяций по логистической модели
	:param n_0: начальная численность популяций
	:param a: коэффициенты прироста
	:param m: матрица взаимодействия популяций
	:param t: время моделирования
	:param step: временной шаг
	:return: массив времени и матрица численности популяций
	"""
	step_count = int(t / step)
	pop_number = n_0.shape[0]
	res = np.zeros((pop_number, step_count), dtype=float)
	res[:, 0] = np.copy(n_0)
	time = np.arange(start=0, stop=t, step=step, dtype=float)
	for i in range(1, step_count):
		for j in range(pop_number):
			res[j, i] = a[j] * n_0[j] * np.exp(a[j] * time[i]) / (a[j] - m[j, j]*n_0[j]*(np.exp(a[j] * time[i])-1))
	return time, res


def count_common(n_0: np.ndarray, a: np.ndarray, m: np.ndarray, t: int, step: float) -> tuple:
	"""
	Функция выполняет расчет путем решения системы дифференциальных уравнений
	:param n_0: начальная численность популяции
	:param a: коэффициенты прироста популяций
	:param m: матрица взаимодействия популяций
	:param t: время моделирования
	:param step: временной шаг
	:return: массив времени и численности популяций
	"""
	step_count = int(t / step)
	pop_number = n_0.shape[0]
	res = np.zeros((pop_number, step_count), dtype=float)
	res[:, 0] = np.copy(n_0)
	time = np.arange(start=0, stop=t, step=step, dtype=float)
	for i in range(1, step_count):
		k1 = a * res[:, i-1] + res[:, i-1]@m*res[:, i-1]
		k2 = a * (res[:, i-1]+k1*step/2) + (res[:, i-1]+k1*step/2)@m*(res[:, i-1]+k1*step/2)
		k3 = a * (res[:, i-1]+k2*step/2) + (res[:, i-1]+k2*step/2)@m*(res[:, i-1]+k2*step/2)
		k4 = a * (res[:, i-1]+k3*step) + (res[:, i-1]+k3*step)@m*(res[:, i-1]+k3*step)
		res[:, i] = res[:, i-1] + step/6*(k1 + 2*k2 + 2*k3 + k4)
	return time, res


def draw(time: np.ndarray, res: np.ndarray, pop_number: int, step_count: int):
	"""
	Отрисовка графиков в plotly (не трожь)
	:param time: время (для оси x)
	:param res: численности популяций (для оси y)
	:param pop_number: количество популяций
	:param step_count: количество временных шагов
	:return: красивый график
	"""
	tm = - 1.5
	tM = time[-1] + 1.5
	ym = np.min(res) - 1.5
	yM = np.max(res) + 1.5
	data = []
	for i in range(pop_number):
		data.append(go.Scatter(x=time, y=res[i, :], name=str(i + 1) + ' популяция', mode="lines"))
	for i in range(pop_number):
		data.append(go.Scatter(x=time, y=res[i, :], name='Тренд ' + str(i + 1) + ' популяции', mode="lines"))
	fig = go.Figure(
		data=data,
		layout=go.Layout(
			xaxis=dict(range=[tm, tM], autorange=False, zeroline=False),
			yaxis=dict(range=[ym, yM], autorange=False, zeroline=False),
			hovermode="closest",
			updatemenus=[dict(type="buttons",
							  buttons=[
								  {
									  "args": [None, {"frame": {"duration": 5 / step_count * 1000, "redraw": False},
													  "fromcurrent": True, "transition": {"duration": 300,
																						  "easing": "quadratic-in-out"}}],
									  "label": "Play",
									  "method": "animate"
								  },
								  {
									  "args": [[None], {"frame": {"duration": 0, "redraw": False},
														"mode": "immediate",
														"transition": {"duration": 0}}],
									  "label": "Pause",
									  "method": "animate"
								  }
							  ],
							  )]),
		frames=[go.Frame(
			data=[go.Scatter(
				x=[time[k]],
				y=[res[i, k]],
				mode="markers") for i in range(pop_number)])

			for k in range(step_count)]
	)
	fig.update_layout(
		title="Графики численности популяций",
		xaxis_title="Время",
		yaxis_title="Численность популяции",
		legend_title="Легенда",
		font=dict(
			family="Courier New, monospace",
			size=18,
			color="RebeccaPurple"
		)
	)
	fig.show()
