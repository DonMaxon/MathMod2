import numpy as np
import plotly.graph_objects as go
import random


def count_common(n_0: np.ndarray, a: np.ndarray, m: np.ndarray, prob: float, epid: int, prolongation: int, c: float, t: int, step: float) -> tuple:
	"""
	Функция выполняет расчет путем решения системы дифференциальных уравнений
	:param n_0: начальная численность популяции
	:param a: коэффициенты прироста популяций
	:param m: матрица взаимодействия популяций
	:param prob: вероятность наступления эпидемии
	:param epid: номер популяции, для которой может возникнуть эпидемия
	:param prolongation: длительность эпидемии
	:param c: коэффициент затухания при эпидемии
	:param t: время моделирования
	:param step: временной шаг
	:return: массив времени и численности популяций
	"""
	step_count = int(t / step)
	pop_number = n_0.shape[0]
	res = np.zeros((pop_number, step_count), dtype=float)
	res[:, 0] = np.copy(n_0)
	time = np.arange(start=0, stop=t, step=step, dtype=float)
	is_epid = False
	till_end = prolongation
	for i in range(1, step_count):
		p = random.random()
		if till_end == 0:
			is_epid = False
			till_end = prolongation
			a[epid-1] += c
		if not is_epid and p < prob:
			a[epid-1] -= c
			is_epid = True
		if is_epid:
			till_end -= 1
		print(a[epid-1])
		k1 = a * res[:, i-1] + m@res[:, i-1]*res[:, i-1]
		k2 = a * (res[:, i-1]+k1*step/2) + m@(res[:, i-1]+k1*step/2)*(res[:, i-1]+k1*step/2)
		k3 = a * (res[:, i-1]+k2*step/2) + m@(res[:, i-1]+k2*step/2)*(res[:, i-1]+k2*step/2)
		k4 = a * (res[:, i-1]+k3*step) + m@(res[:, i-1]+k3*step)*(res[:, i-1]+k3*step)
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
