import argparse
from exp.exp_main_anomaly_SL import Exp_Anomaly_Detection_SL
import torch

def get_args():
    parser = argparse.ArgumentParser(description='Train MaelNet on MSL dataset')

    # basic config
    parser.add_argument('--is_training', type=int, default=1, help='status')
    parser.add_argument('--model_id', type=str, default='MaelNetS1_AnomalyTransformer_DCDetector_RL_Coba', help='model id')    
    parser.add_argument('--model', type=str, default='MaelNet', help='model name, options: [MaelNet]')

    ### Add folder result
    parser.add_argument('--result_dir', type=str, default='results', help='directory for the result files')

    # # # data loader
    parser.add_argument('--data', type=str, default='MSL', help='dataset type')
    parser.add_argument('--root_path', type=str, default='./dataset/MSL/', help='root path of the data file')
    parser.add_argument('--win_size', type=int, default=100, help='window size')
    parser.add_argument('--chunk_size', type=str, default='0', help='Chunk size. Example: 2048, 4096, 8192')

    parser.add_argument('--features', type=str, default='M',
                        help='forecasting task, options:[M, S, MS]; M:multivariate predict multivariate, S:univariate predict univariate, MS:multivariate predict univariate')
    parser.add_argument('--target', type=str, default='OT', help='target feature in S or MS task')
    parser.add_argument('--checkpoints', type=str, default='checkpoints', help='location of model checkpoints')
    parser.add_argument('--freq', type=str, default='h',
                            help='freq for time features encoding, options:[s:secondly, t:minutely, h:hourly, d:daily, b:business days, w:weekly, m:monthly], you can also use more detailed freq like 15min or 3h')

    # anomaly task
    parser.add_argument('--anomaly_ratio', type=float, default=0.85, help="Anomaly ratio for threshold")

    #KBJNet & DCDetector
    parser.add_argument('--n_windows', type=int, default=100, help="Sliding Windows KBJNet")

    #DCDetector
    parser.add_argument('--channel', type=int, default=25, help="Channel DCDetector")
    parser.add_argument('--patch_size', type=list, default=[5], help="Sliding Windows KBJNet")

    #AnomalyTransformer
    parser.add_argument('--k', type=int, default=3, help="reconstruction loss")

    # FEDFormer task
    parser.add_argument('--seq_len', type=int, default=96, help='input sequence length')
    parser.add_argument('--label_len', type=int, default=48, help='start token length')
    parser.add_argument('--pred_len', type=int, default=96, help='prediction sequence length')
    parser.add_argument('--cross_activation', type=str, default='tanh')
    parser.add_argument('--version', type=str, default='Wavelets',help='for FEDformer, there are two versions to choose, options: [Fourier, Wavelets]')
    parser.add_argument('--mode_select', type=str, default='random',help='for FEDformer, there are two mode selection method, options: [random, low]')
    parser.add_argument('--modes', type=int, default=32, help='modes to be selected random 32')
    parser.add_argument('--L', type=int, default=3, help='ignore level')
    parser.add_argument('--base', type=str, default='legendre', help='mwt base')

    # Reinforcement Learning
    parser.add_argument('--use_weight',   action='store_true', default=False)
    parser.add_argument('--use_td',       action='store_false', default=True)
    parser.add_argument('--use_extra',    action='store_false', default=True)
    parser.add_argument('--use_pretrain', action='store_false', default=True)
    parser.add_argument('--epsilon', default=0.5, type=float)
    parser.add_argument('--exp_name', default='rlmc', type=str)

    # TimesNet
    parser.add_argument('--top_k', type=int, default=5)

    # MANTRA
    parser.add_argument('--n_learner', type=int, default=3)
    parser.add_argument('--slow_model', type=str, default='MaelNetS2', help='model name, options: [MaelNet]')
    parser.add_argument('--is_slow_learner', type=bool, default=False)

    # lOSS TYPE
    parser.add_argument('--loss_type', type=str, default="neg_corr", help='loss type')
    parser.add_argument('--correlation_penalty', type=float, default=0.5, help='correlation penalty')

    # model define    
    parser.add_argument('--enc_in', type=int, default=25, help='encoder input size')
    parser.add_argument('--dec_in', type=int, default=25, help='decoder input size')
    parser.add_argument('--c_out', type=int, default=25, help='output size')
    parser.add_argument('--d_model', type=int, default=512, help='dimension of model')
    parser.add_argument('--n_heads', type=int, default=8, help='num of heads attention')
    parser.add_argument('--e_layers', type=int, default=3, help='num of encoder layers')
    parser.add_argument('--d_layers', type=int, default=1, help='num of decoder layers')
    parser.add_argument('--d_ff', type=int, default=2048, help='dimension of fcn')
    parser.add_argument('--moving_avg', type=int, default=100, help='window size of moving average')
    parser.add_argument('--factor', type=int, default=5, help='attn factor')
    parser.add_argument('--distil', action='store_false',
                        help='whether to use distilling in encoder, using this argument means not using distilling',
                        default=True)
    parser.add_argument('--dropout', type=float, default=0.05, help='dropout')
    parser.add_argument('--embed', type=str, default='timeF',
                        help='time features encoding, options:[timeF, fixed, learned]')
    parser.add_argument('--activation', type=str, default='gelu', help='activation')
    # parser.add_argument('--output_attention', action='store_true', help='whether to output attention in encoder')
    parser.add_argument('--output_attention', default=True, action='store_true', help='whether to output attention in encoder')
    parser.add_argument('--do_predict', action='store_true', help='whether to predict unseen future data')

    # optimization
    parser.add_argument('--num_workers', type=int, default=10, help='data loader num workers')
    parser.add_argument('--itr', type=int, default=1, help='experiments times')
    parser.add_argument('--train_epochs', type=int, default=10, help='train epochs')
    parser.add_argument('--batch_size', type=int, default=32, help='batch size of train input data')
    parser.add_argument('--patience', type=int, default=3, help='early stopping patience') # Apabila Counter >= patience, akan dilakukan early stop
    parser.add_argument('--learning_rate', type=float, default=0.0001, help='optimizer learning rate')
    parser.add_argument('--des', type=str, default='test', help='exp description')
    parser.add_argument('--loss', type=str, default='mse', help='loss function')
    parser.add_argument('--lradj', type=str, default='type1', help='adjust learning rate')
    parser.add_argument('--use_amp', action='store_true', help='use automatic mixed precision training', default=False)

    # GPU
    parser.add_argument('--use_gpu', type=bool, default=True, help='use gpu')
    parser.add_argument('--gpu', type=int, default=0, help='gpu')
    parser.add_argument('--use_multi_gpu', action='store_true', help='use multiple gpus', default=False)
    parser.add_argument('--devices', type=str, default='0,1,2,3', help='device ids of multile gpus')
    parser.add_argument('--seed', type=int, default=2021, help='random seed')

    # de-stationary projector params
    parser.add_argument('--p_hidden_dims', type=int, nargs='+', default=[128, 128], help='hidden layer dimensions of projector (List)')
    parser.add_argument('--p_hidden_layers', type=int, default=2, help='number of hidden layers in projector')

#    # Model & Data
#    parser.add_argument('--model', type=str, default='MaelNet')
#    parser.add_argument('--data', type=str, default='MSL')
#    parser.add_argument('--enc_in', type=int, default=55)   # Sesuaikan dengan fitur data MSL
#    parser.add_argument('--dec_in', type=int, default=55)
#    parser.add_argument('--c_out', type=int, default=55)
#
#    # Window dan Attention
#    parser.add_argument('--win_size', type=int, default=100)
#    parser.add_argument('--n_heads', type=int, default=8)
#    parser.add_argument('--d_model', type=int, default=512)
#    parser.add_argument('--d_ff', type=int, default=2048)
#    parser.add_argument('--e_layers', type=int, default=2)
#    parser.add_argument('--d_layers', type=int, default=1)
#    parser.add_argument('--dropout', type=float, default=0.1)
#
#    # NS Transformer Specific
#    parser.add_argument('--p_hidden_dims', nargs='+', type=int, default=[128, 128])
#    parser.add_argument('--p_hidden_layers', type=int, default=2)
#    parser.add_argument('--activation', type=str, default='gelu')
#    parser.add_argument('--moving_avg', type=int, default=25)
#    parser.add_argument('--output_attention', action='store_true')
#
#    # Training
#    parser.add_argument('--learning_rate', type=float, default=0.0001)
#    parser.add_argument('--train_epochs', type=int, default=10)
#    parser.add_argument('--patience', type=int, default=3)
#    parser.add_argument('--k', type=float, default=0.7)
#    parser.add_argument('--batch_size', type=int, default=32)
#    parser.add_argument('--num_workers', type=int, default=2)
    parser.add_argument('--kernel_size', type=int, default=3, help='kernel input size')
#
#    # Device
#    parser.add_argument('--use_gpu', type=bool, default=True)
#    parser.add_argument('--use_multi_gpu', type=bool, default=False)
    parser.add_argument('--device_ids', type=int, nargs='+', default=[0])
#
#    # Pathing
#    parser.add_argument('--checkpoints', type=str, default='./checkpoints/')
#    parser.add_argument('--result_dir', type=str, default='./results/')
#    parser.add_argument('--root_path', type=str, default='./data/MSL/')  # pastikan folder MSL ada
#    parser.add_argument('--chunk_size', type=int, default=100)
#
#    parser.add_argument('--anomaly_ratio', type=float, default=0.85)
#    parser.add_argument('--factor', type=int, default=5)
#    parser.add_argument('--gpu', type=int, default=0)
#    parser.add_argument('--des', type=str, default='TA')
#    parser.add_argument('--patch_size', type=int, default=5)
#    parser.add_argument('--channel', type=int, default=55)
#    parser.add_argument('--itr', type=int, default=1)


    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = get_args()

    if args.use_gpu and torch.cuda.is_available():
        args.device = torch.device(f'cuda:{args.device_ids[0]}')
    else:
        args.device = torch.device('cpu')

    exp = Exp_Anomaly_Detection_SL(args)
    setting = f"{args.model}_{args.data}_win{args.win_size}_run1"
    exp.train(setting)
