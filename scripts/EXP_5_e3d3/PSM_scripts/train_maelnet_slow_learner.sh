export CUDA_VISIBLE_DEVICES=0

python -u run_anomaly.py \
  --is_training 1 \
  --root_path ./dataset/PSM/ \
  --model_id MaelNetS2_AnomalyTransformer_DCDetector_RL_TA\
  --model MaelNetS2 \
  --is_slow_learner true \
  --data PSM \
  --e_layers 3 \
  --d_layers 3 \
  --anomaly_ratio 0.85 \
  --d_ff 512 \
  --dropout 0.0 \
  --factor 5 \
  --enc_in 25 \
  --dec_in 25 \
  --c_out 25 \
  --d_model 512 \
  --moving_avg 100 \
  --win_size 100 \
  --gpu 0 \
  --des 'TA' \
  --p_hidden_dims 128 128 \
  --p_hidden_layers 2 \
  --result_dir ./results/ \
  --itr 1
