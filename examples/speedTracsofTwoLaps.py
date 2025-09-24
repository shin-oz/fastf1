import matplotlib.pyplot as plt # type: ignore
import fastf1.plotting # type: ignore

fastf1.Cache.offline_mode(True)

# なんでtrueにするかは不明
fastf1.plotting.setup_mpl(mpl_timedeta_support= True, color_scheme= 'fastf1')

session = fastf1.get_session(2025, 16, 'R')
session.load()

ver_laps = session.laps.pick_drivers('VER').pick_fastest()
tsu_laps = session.laps.pick_drivers('TSU').pick_fastest()

# add_distance()とは？
# sessionとは？
ver_tel = ver_laps.get_car_data().add_distance()
tsu_tel = tsu_laps.get_car_data().add_distance()

# どっちもver_lapsの値はrbrでは...
ver_color = fastf1.plotting.get_team_color(ver_laps['Team'], session=session)
tsu_color = fastf1.plotting.get_team_color(tsu_laps['Team'], session=session)

fig, ax = plt.subplots()
ax.plot(ver_tel['Distance'], ver_tel['Speed'], color=ver_color, label="VER")
ax.plot(tsu_tel['Distance'], tsu_tel['Speed'], color="RED", label="TSU")

ax.set_xlabel('Distance in m')
ax.set_ylabel('Speed in km/h')

ax.legend()
plt.suptitle(f"Fastest comparison \n"
             f"{session.event['EventName']}{session.event.year} Race")

plt.show()
