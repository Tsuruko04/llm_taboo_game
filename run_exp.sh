CUDA_VISIBLE_DEVICES=4 python run.py -n 50 -w data/selected_words.txt -s settings/settings.yaml -l log_no_exp &
CUDA_VISIBLE_DEVICES=5 python run.py -n 50 -w data/selected_words.txt -s settings/settings_exp.yaml -l log_exp_5 &
CUDA_VISIBLE_DEVICES=6 python run.py -n 50 -w data/selected_words.txt -s settings/settings_dc.yaml -l log_dc &
