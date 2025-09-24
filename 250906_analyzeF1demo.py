from matplotlib import pyplot as plt
import fastf1
import fastf1.plotting

fastf1.plotting.setup_mpl(color_scheme='fastf1')

session = fastf1.get_session(2024, 'Monza','Q')

session.load()
fast_tsunoda = session.laps.pick_drivers('TSU').pick_fastest()

tsu_car_data = fast_tsunoda.get_car_data()

t = tsu_car_data['Time']

vCar = tsu_car_data['Speed']

fig, ax = plt.subplots()
ax.plot(t, vCar, label='Fast')
ax.set_xlabel('Time')
ax.set_ylabel('Speed [km/h]')
ax.set_title('Tsunoda is')
ax.legend()
plt.show()