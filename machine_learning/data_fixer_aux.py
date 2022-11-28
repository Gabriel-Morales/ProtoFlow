#!/usr/bin/env python3
import pandas as pd

csv_name = input("File path: ") #"unswiotan18_labelled_classified.csv"
df = pd.read_csv(csv_name, low_memory=False)

# metric_obj.total_duration_ms = (last_seen_time_ms - first_seen_time_ms)

nfstream_cols_to_drop = ['id', 'expiration_id', 'src_ip', 'src_port', 'dst_ip', 
						'dst_port', 'protocol', 'ip_version', 'vlan_id', 'bidirectional_min_piat_ms',
						'bidirectional_mean_piat_ms', 'bidirectional_stddev_piat_ms', 'bidirectional_max_piat_ms', 
						'src2dst_min_piat_ms', 'src2dst_mean_piat_ms', 'src2dst_stddev_piat_ms', 'src2dst_max_piat_ms', 
						'dst2src_min_piat_ms', 'dst2src_mean_piat_ms', 'dst2src_stddev_piat_ms', 'dst2src_max_piat_ms', 
						'bidirectional_syn_packets', 'bidirectional_cwr_packets', 'bidirectional_ece_packets', 
						'bidirectional_urg_packets', 'bidirectional_ack_packets', 'bidirectional_psh_packets', 
						'bidirectional_rst_packets', 'bidirectional_fin_packets', 'src2dst_syn_packets',
						 'src2dst_cwr_packets', 'src2dst_ece_packets', 'src2dst_urg_packets', 'src2dst_ack_packets', 
						 'src2dst_psh_packets', 'src2dst_rst_packets', 'src2dst_fin_packets', 'dst2src_syn_packets', 
						 'dst2src_cwr_packets', 'dst2src_ece_packets', 'dst2src_urg_packets', 'dst2src_ack_packets', 
						 'dst2src_psh_packets', 'dst2src_rst_packets', 'dst2src_fin_packets', 'application_name', 
						 'application_category_name', 'application_is_guessed', 'application_confidence', 
						 'requested_server_name', 'client_fingerprint', 'server_fingerprint', 'user_agent', 
						 'content_type']#, 'dst2src_first_seen_time_ms', 'dst2src_last_seen_time_ms', 'src2dst_first_seen_time_ms','src2dst_last_seen_time_ms']

rename_cols = {'bidirectional_duration_ms':'bidirectional_total_duration_ms', 
				'bidirectional_packets':'bidirectional_total_packets',
				'bidirectional_bytes':'bidirectional_total_bytes', 
				'src2dst_duration_ms':'src2dst_total_duration_ms', 
				'src2dst_packets':'src2dst_total_packets',
				'src2dst_bytes':'src2dst_total_bytes',
				'dst2src_duration_ms':'dst2src_total_duration_ms', 
				'dst2src_packets':'dst2src_total_packets', 
				'dst2src_bytes':'dst2src_total_bytes', 
				'bidirectional_stddev_ps':'bidirectional_stdev_ps',
				'src2dst_stddev_ps':'src2dst_stdev_ps',
				'dst2src_stddev_ps':'dst2src_stdev_ps',
				'bidirectional_last_seen_ms' : 'bidirectional_last_seen_time_ms',
				'bidirectional_first_seen_ms': 'bidirectional_first_seen_time_ms',
				'src2dst_last_seen_ms': 'src2dst_last_seen_time_ms',
				'src2dst_first_seen_ms' : 'src2dst_first_seen_time_ms', 
				'dst2src_first_seen_ms' : 'dst2src_first_seen_time_ms',
				'dst2src_last_seen_ms' : 'dst2src_last_seen_time_ms'} 

df['protocol'] = 'w'
df.rename(columns = rename_cols, inplace = True)

df['bidirectional_total_duration_ms'].mask(df['bidirectional_total_duration_ms'] == 0, 0.00000001, inplace=True)
df['src2dst_total_duration_ms'].mask(df['src2dst_total_duration_ms'] == 0, 0.00000001, inplace=True)
df['dst2src_total_duration_ms'].mask(df['dst2src_total_duration_ms'] == 0, 0.00000001, inplace=True)
df['src2dst_total_duration_ms'].mask(df['src2dst_total_duration_ms'] == 0, 0.00000001, inplace=True)
df['bidirectional_total_duration_ms'].mask(df['bidirectional_total_duration_ms'] == 0, 0.00000001, inplace=True)

df['bidirectional_transmission_rate_ms'] = (df['bidirectional_total_packets'] / df['bidirectional_total_duration_ms']) #if df['bidirectional_total_packets'] != 0 else df['bidirectional_total_packets']  
df['src2dst_transmission_rate_bytes_ms'] = (df['src2dst_total_bytes'] / df['src2dst_total_duration_ms']) #if df['src2dst_total_bytes'] != 0 else df['src2dst_total_bytes']
df['dst2src_transmission_rate_ms'] = (df['dst2src_total_duration_ms'] / df['dst2src_total_duration_ms']) #if df['dst2src_total_duration_ms'] != 0 else df['dst2src_total_duration_ms']
df['src2dst_transmission_rate_ms'] = (df['src2dst_total_duration_ms'] / df['src2dst_total_duration_ms']) #if df['src2dst_total_duration_ms'] != 0 else df['src2dst_total_duration_ms']
df['bidirectional_transmission_rate_byte_ms'] = (df['bidirectional_total_bytes'] / df['bidirectional_total_duration_ms'])# if df['bidirectional_total_bytes'] != 0 else df['bidirectional_total_bytes']

df.drop(columns=nfstream_cols_to_drop, axis=1, inplace=True)


df.to_csv("test_out",index=False)

