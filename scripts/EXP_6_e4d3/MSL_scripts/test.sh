export DATASET_SC="MSL"
export DIR_RES='./results/'
export FL_EXP="EXP_6_e4d3"
export FL_RES="${DIR_RES}run_${DATASET_SC}.txt"
echo "===========================> run on: `date`" >> $FL_RES
echo "Testing Model" >> $FL_RES
export CUDA_VISIBLE_DEVICES=0

python -u run_anomaly.py \
  --is_training 0 \
  --root_path ./dataset/MSL/ \
  --model_id MaelNetS2_AnomalyTransformer_DCDetector_RL_TA\
  --patch_size 5 \
  --train_epochs 3 \
  --data MSL \
  --e_layers 4 \
  --d_layers 3 \
  --anomaly_ratio 0.85 \
  --factor 5 \
  --d_ff 512 \
  --dropout 0.0 \
  --enc_in 55 \
  --dec_in 55 \
  --channel 55 \
  --c_out 55 \
  --d_model 512 \
  --moving_avg 100 \
  --win_size 100 \
  --gpu 0 \
  --des 'TA' \
  --p_hidden_dims 128 128 \
  --p_hidden_layers 2 \
  --itr 1 \
  --checkpoints ./checkpoints/ \
  --result_dir ./results/ 

echo "Testing Finished at `date`" >> $FL_RES
echo "----------------------------" >> $FL_RES