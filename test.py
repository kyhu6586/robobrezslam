from runSLAM import RunBreezySlam
from data_utils import *

# we expect 1+24+667=692

# Format the CSV into a .dat file
comma_to_space("lidar_readings.csv","lidar_data")
remove_empty_line("lidar_data.dat","lidar_data")
# Run BreezySLAM
little_shit = RunBreezySlam("lidar_data",1,9999)

plt.imshow(little_shit)
plt.savefig('little_shit.png')

visualize_output("no_trajectory.npy")

visualize_output("with_trajectory.npy")

# convolve_map("no_trajectory_convolved","no_trajectory.npy",16)
# visualize_output("no_trajectory_convolved.npy")
# convolve_map("with_trajectory_convolved","with_trajectory.npy",16)
# visualize_output("with_trajectory_convolved.npy")