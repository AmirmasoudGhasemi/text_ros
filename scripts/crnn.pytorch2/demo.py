#!/usr/bin/env python
import rospy

import torch
from torch.autograd import Variable
import utils
import dataset
from sensor_msgs.msg import Image as Image_msg
from PIL import Image
import models.crnn as crnn

from text_ros.srv import *
from std_msgs.msg import String

model_path = './data/crnn.pth'
img_path = './data/demo.png'
alphabet = '0123456789abcdefghijklmnopqrstuvwxyz'

model = crnn.CRNN(32, 1, 37, 256)
if torch.cuda.is_available():
    model = model.cuda()
print('loading pretrained model from %s' % model_path)
model.load_state_dict(torch.load(model_path))
converter = utils.strLabelConverter(alphabet)
transformer = dataset.resizeNormalize((100, 32))

def handle_text_read(req):

	image = Image.open(img_path).convert('L')
	image = transformer(image)
	if torch.cuda.is_available():
	    image = image.cuda()
	image = image.view(1, *image.size())
	image = Variable(image)

	model.eval()
	preds = model(image)

	_, preds = preds.max(2)
	preds = preds.transpose(1, 0).contiguous().view(-1)

	preds_size = Variable(torch.IntTensor([preds.size(0)]))
	raw_pred = converter.decode(preds.data, preds_size.data, raw=True)
	sim_pred = converter.decode(preds.data, preds_size.data, raw=False)
	print('%-20s => %-20s' % (raw_pred, sim_pred))
	text_str = '%-20s => %-20s' % (raw_pred, sim_pred)
	return(text_str)

def text_read_server():
	rospy.init_node('text_read_server', anonymous=True)
	rospy.Service('text_read', TextRead, handle_text_read)
	rospy.spin()	


if __name__ == '__main__':
    try:
        text_read_server()
    except rospy.ROSInterruptException:
        pass
