from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Settings

from django.conf import settings

import ktrain
from ktrain import vision as vis
import re
from django.conf import settings
from pathlib import Path
# Create your views here.

class SettingsView(APIView):
    
    def get(self, request, format=None):
        settings_dict = {}
        try:
            settings_object = Settings.objects.all()
        
            for settings in settings_object:
             settings_dict[settings.name] = settings.value
        except:
            Response(status=404)

        return Response(settings_dict, status=200)

    def post(self, request, format=None):
        settings = request.data['settings']
        bad_settings = []
        for setting in settings:
            try:
                new_settings = Settings(name=setting['NAME'], value=setting['VALUE'])
                new_settings.save()
            except:
                bad_settings.append(setting)
        
            if len(bad_settings) > 0:
                return Response({"Invalid data": bad_settings}, status=200)

            else:
                return Response(status=200)
        

def model(fname):
    pattern=r'([^/Images\\]+)_\d+_\d+_\d+ .jpg$'
    p=re.compile(pattern)
    r=p.search('11_0_0_20170117190914091 .jpg')
    filepath = settings.MEDIA_ROOT
    print(filepath)
    print (r.group(1))
    
    (train_data, test_data, preproc) = vis.images_from_fname(filepath, pattern=pattern, is_regression = True, target_size=(200, 200),color_mode='rgb', random_state = 42)

    vis.print_image_regression_models()
    model = vis.image_regression_model('pretrained_resnet50', train_data=train_data,
                                val_data =test_data, metrics=['mae'],
                                optimizer_name= 'adam')
    learner=ktrain.get_learner(model=model, train_data=train_data,
                        val_data=test_data, batch_size=64)
                        
    learner.lr_find(max_epochs=2)
    learner.lr_plot()
    learner.fit_onecycle(1e-4, 5)

    learner.plot('loss')

    learner.freeze(15)
    learner.fit_onecycle(1e-4, 5)
    learner.plot('loss')

    learner.freeze(15)
    learner.fit_onecycle(1e-4, 5)
    learner.plot('loss')

    learner.evaluate()

    model.summary()

    predictor= ktrain.get_predictor(learner.model, preproc)
    test_data.filenames[10:20]

    # def show_prediction(fname):
    fname= filepath  + '/' + fname
    pred = round(predictor.predict_filename(fname)[0])
    actual = int(p.search(fname).group(1))
    vis.show_image(fname)
    print('Estimated age: %s | Actual Age: %s' % (pred, actual))

    


def homepage(request):
    model('54_0_0_20170113184055047 .jpg')
    return render(request, 'home.html')