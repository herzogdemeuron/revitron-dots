import revitron
import os
from pyrevit import forms, script

config = revitron.DocumentConfigStorage().get('revitron.dots', dict())
configFile = config.get('file', '')

msg = 'No configuration is selected.'

if configFile:
	msg = 'Selected configuration:\n{}'.format(configFile)

optionSelect = 'Select Configuration File'
optionOpenLocation = 'Open Configuration File Location'
optionCancel = 'Cancel'

res = None

if configFile:
	res = forms.alert(msg, options=[optionSelect, optionOpenLocation, optionCancel])
else:
	res = forms.alert(msg, options=[optionSelect, optionCancel])

if res == optionOpenLocation:
	script.show_folder_in_explorer(os.path.dirname(configFile))

if res == optionSelect:

	jsonFile = forms.save_file(
	    file_ext='json',
	    default_name='{}-dots-config.json'.format(revitron.DOC.Title),
	    unc_paths=False,
	    title='Select Configuration File'
	)

	if jsonFile:
		revitron.DocumentConfigStorage().set('revitron.dots', {'file': jsonFile})
