import pandas as pd
import numpy as np

# Upload data

data = 'File_name.csv'

df = pd.read_csv(data)

# Calculate velcoity and acceleration
metrics = {}
for id in range(33):  # 33 landmarks
    metrics[f'lm_{id}_vx'] = df[f'lm_{id}_x'].diff() / df['time'].diff()
    metrics[f'lm_{id}_vy'] = df[f'lm_{id}_y'].diff() / df['time'].diff()
    metrics[f'lm_{id}_ax'] = metrics[f'lm_{id}_vx'].diff() / df['time'].diff()
    metrics[f'lm_{id}_ay'] = metrics[f'lm_{id}_vy'].diff() / df['time'].diff()

# calculate distance
for id in range(33):
    metrics[f'lm_{id}_dist'] = np.sqrt(df[f'lm_{id}_x'].diff()**2 + df[f'lm_{id}_y'].diff()**2)

# calculate the metrics for 15 and 16 landmarks
metrics['speed_15'] = np.sqrt(metrics['lm_15_vx']**2 + metrics['lm_15_vy']**2)
metrics['speed_16'] = np.sqrt(metrics['lm_16_vx']**2 + metrics['lm_16_vy']**2)
metrics['acc_15'] = np.sqrt(metrics['lm_15_ax']**2 + metrics['lm_15_ay']**2)
metrics['acc_16'] = np.sqrt(metrics['lm_16_ax']**2 + metrics['lm_16_ay']**2)

metrics['mean_speed_15'] = metrics['speed_15'].expanding().mean()
metrics['max_speed_15'] = metrics['speed_15'].expanding().max()
metrics['mean_speed_16'] = metrics['speed_16'].expanding().mean()
metrics['max_speed_16'] = metrics['speed_16'].expanding().max()

metrics['mean_acc_15'] = metrics['acc_15'].expanding().mean()
metrics['max_acc_15'] = metrics['acc_15'].expanding().max()
metrics['mean_acc_16'] = metrics['acc_16'].expanding().mean()
metrics['max_acc_16'] = metrics['acc_16'].expanding().max()

metrics['disp_15_frame'] = metrics['lm_15_dist']
metrics['total_disp_15'] = metrics['lm_15_dist'].expanding().sum()
metrics['disp_16_frame'] = metrics['lm_16_dist']
metrics['total_disp_16'] = metrics['lm_16_dist'].expanding().sum()

weight = 70  # default weight
metrics['power_15'] = weight * metrics['speed_15']
metrics['mean_power_15'] = metrics['power_15'].expanding().mean()
metrics['max_power_15'] = metrics['power_15'].expanding().max()
metrics['power_16'] = weight * metrics['speed_16']
metrics['mean_power_16'] = metrics['power_16'].expanding().mean()
metrics['max_power_16'] = metrics['power_16'].expanding().max()

# new dataframe with metrics
metrics_df = pd.DataFrame(metrics)

# join old and new dataframe
result_df = pd.concat([df, metrics_df], axis=1)

# save dataframe in a new CSV
result_df.to_csv(f'{data}_with_metrics.csv', index=False)



        # connections = [
        #     (11, 12), (12, 14), (14, 16), (11, 13), (13, 15),  # Upper body
        #     (12, 24), (24, 26), (26, 28), (28, 32), (11, 23), (23, 25), (25, 27), (27, 31),  # Lower body
        #     (23, 24),  # Hip
        #     (8, 0 ,7), # Head
        #     (15, 16) # barbell
        # ]

