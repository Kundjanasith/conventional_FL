import sys, os, time, configparser, socket, logging
sys.path.insert(1, '..')       
import utils

config = configparser.ConfigParser()
config.read('../config_exp0.ini')

group = 'UFL_'
trainer_ip = sys.argv[1]
trainer_port = sys.argv[2]

aggregator_ip = config['DISTRIBUTION']['%sAGGREGATOR_IP'%group]
num_communication_rounds = int(config['TRAINING']['NUM_COMMUNICATION_ROUNDS'])
num_samples = int(config['TRAINING']['NUM_SAMPLES'])
local_batch_size = int(config['TRAINING']['LOCAL_BATCH_SIZE'])
local_epochs = int(config['TRAINING']['LOCAL_EPOCHS'])
hostname = socket.gethostname()
logging.basicConfig(filename="%s_log.txt"%hostname, level=logging.DEBUG, format="%(asctime)s - %(message)s")

for e in range(num_communication_rounds):

    logging.info("[START] RECEIVE AGGREGATED MODEL IN EP%d"%e)
    utils.receive_model('0.0.0.0',int(trainer_port))
    logging.info("[COMPLETE] RECEIVE AGGREGATED MODEL IN EP%d"%e)

    logging.info("[START] TRAIN LOCAL MODEL IN EP%d"%e)
    model = utils.model_init()
    while not os.path.exists('aggregated_models/model_ep%d.h5'%(e)):
        time.sleep(5)
    while True:
        print('aa')
        try:
            print('bb')
            model = utils.model_init()
            model.load_weights('aggregated_models/model_ep%d.h5'%(e))
            break
        except:
            print('cc')
            pass

    x_train, y_train = utils.sampling_data(num_samples)
    model.compile(optimizer='sgd', loss='categorical_crossentropy', metrics=['accuracy'])
    model.fit(x_train, y_train,epochs=local_epochs,batch_size=local_batch_size,verbose=1,validation_split=0.2)
    model.save_weights('trained_models/%s_ep%d.h5'%(trainer_ip+':'+trainer_port,e))
    logging.info("[COMPLETE] TRAIN LOCAL MODEL IN EP%d"%e)

    logging.info("[START] SEND TRAINED MODEL IN EP%d"%e)
    utils.send_model(aggregator_ip, 19191,'trained_models/%s_ep%d.h5'%(trainer_ip+':'+trainer_port,e), 'trained_models')
    logging.info("[COMPLETE] SEND TRAINED MODEL IN EP%d"%e)

