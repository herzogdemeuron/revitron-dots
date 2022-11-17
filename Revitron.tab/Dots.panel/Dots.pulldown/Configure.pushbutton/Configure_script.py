import revitron
from pyrevit import forms

config = revitron.DocumentConfigStorage().get('revitron.dots', dict())
configFile = config.get('file', '')

msg = 'No configuration is selected.'

if configFile:
	msg = 'Selected configuration:\n{}'.format(configFile)

optionSelect = 'Select Configuration'
optionCancel = 'Close'

if forms.alert(msg, options=[optionSelect, optionCancel]) == optionSelect:

	jsonFile = forms.save_file(
	    file_ext='json',
	    default_name='{}-dots-config.json'.format(revitron.DOC.Title),
	    unc_paths=False,
	    title='Select Configuration File'
	)

	if jsonFile:
		revitron.DocumentConfigStorage().set('revitron.dots', {'file': jsonFile})
